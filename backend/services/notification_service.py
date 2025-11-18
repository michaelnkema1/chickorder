from typing import Optional
from models import Order, OrderStatus
from config import settings
from twilio.rest import Client as TwilioClient
import httpx


class NotificationService:
    """Service for sending SMS and WhatsApp notifications"""
    
    def __init__(self):
        self.twilio_client = None
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.twilio_client = TwilioClient(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )
    
    async def send_order_confirmation(self, order: Order) -> bool:
        """Send order confirmation SMS"""
        message = (
            f"Order Confirmed! 🐔\n\n"
            f"Order #: {order.order_number}\n"
            f"Total: GHS {order.total_amount:.2f}\n"
            f"We are preparing your live chickens. We'll notify you when they are killed, dressed, and ready for pickup.\n\n"
            f"Thank you for your order!"
        )
        return await self.send_sms(order.customer_phone, message)
    
    async def send_status_update(self, order: Order) -> bool:
        """Send order status update SMS"""
        status_messages = {
            OrderStatus.CONFIRMED: "Your order has been confirmed. We're preparing to kill and dress your chickens.",
            OrderStatus.PREPARING: "Your chickens are being killed and dressed. Almost ready!",
            OrderStatus.READY: f"🎉 Your chickens are ready! Order #{order.order_number} has been killed, dressed, and is ready for pickup!",
            OrderStatus.COMPLETED: "Thank you! Your order has been completed.",
            OrderStatus.CANCELLED: f"Your order #{order.order_number} has been cancelled."
        }
        
        message = (
            f"Order Update 🐔\n\n"
            f"Order #: {order.order_number}\n"
            f"{status_messages.get(order.status, 'Your order status has been updated.')}\n"
        )
        return await self.send_sms(order.customer_phone, message)
    
    async def send_sms(self, phone: str, message: str) -> bool:
        """Send SMS via Twilio"""
        if not self.twilio_client:
            print(f"[SMS] Would send to {phone}: {message}")
            return True  # Return True in development mode
        
        try:
            message = self.twilio_client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone
            )
            return message.sid is not None
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False
    
    async def send_whatsapp(self, phone: str, message: str) -> bool:
        """Send WhatsApp message via WhatsApp Cloud API"""
        if not all([settings.WHATSAPP_BUSINESS_ID, settings.WHATSAPP_ACCESS_TOKEN]):
            print(f"[WhatsApp] Would send to {phone}: {message}")
            return True  # Return True in development mode
        
        url = f"https://graph.facebook.com/v18.0/{settings.WHATSAPP_BUSINESS_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=10.0)
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"Error sending WhatsApp: {e}")
            return False

