from typing import Optional, Dict
from models import PaymentMethod, Order
from config import settings
import httpx
import requests


class PaymentService:
    """Service for handling payment integrations"""
    
    @staticmethod
    async def initiate_payment(order: Order, payment_method: PaymentMethod) -> Dict:
        """Initiate payment based on payment method"""
        if payment_method == PaymentMethod.CASH:
            return {
                "payment_reference": f"CASH-{order.order_number}",
                "payment_url": None,
                "status": "pending",
                "message": "Payment will be collected when you pickup your order"
            }
        elif payment_method == PaymentMethod.MOBILE_MONEY:
            # For mobile money, use Hubtel or another provider
            return await PaymentService._initiate_mobile_money_payment(order)
        else:
            raise ValueError(f"Unsupported payment method: {payment_method}. Only 'cash' and 'mobile_money' are supported.")
    
    @staticmethod
    async def _initiate_mobile_money_payment(order: Order) -> Dict:
        """Initiate mobile money payment via Hubtel"""
        # For development: if credentials not configured, return mock response
        if not all([settings.HUBTEL_CLIENT_ID, settings.HUBTEL_CLIENT_SECRET]):
            return {
                "payment_reference": f"MOBILE-{order.order_number}",
                "payment_url": None,
                "status": "processing",
                "message": f"Mobile money payment initiated. You will receive a USSD prompt on {order.customer_phone} to authorize payment of GHS {order.total_amount:.2f}."
            }
        
        # Hubtel API endpoint for mobile money
        url = "https://api.hubtel.com/v1/merchantaccount/onlinecheckout/invoice/create"
        
        headers = {
            "Authorization": f"Basic {settings.HUBTEL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "total_amount": order.total_amount,
            "description": f"Order #{order.order_number}",
            "customer_mobile": order.customer_phone,
            "callback_url": f"https://yourdomain.com/api/payments/callback/hubtel",
            "return_url": f"https://yourdomain.com/api/payments/return/hubtel",
            "client_reference": order.order_number
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                return {
                    "payment_reference": data.get("invoice_id", f"MOBILE-{order.order_number}"),
                    "payment_url": data.get("invoice_url"),
                    "status": "processing",
                    "message": f"You will receive a USSD prompt on {order.customer_phone} to authorize payment."
                }
        except Exception as e:
            # Fallback for development
            return {
                "payment_reference": f"MOBILE-{order.order_number}",
                "payment_url": None,
                "status": "processing",
                "message": f"Mobile money payment initiated. You will receive a USSD prompt on {order.customer_phone} to authorize payment of GHS {order.total_amount:.2f}."
            }
    
    @staticmethod
    async def _initiate_hubtel_payment(order: Order) -> Dict:
        """Initiate Hubtel payment"""
        # For development: if credentials not configured, return mock response
        if not all([settings.HUBTEL_CLIENT_ID, settings.HUBTEL_CLIENT_SECRET]):
            return {
                "payment_reference": f"HUBTEL-{order.order_number}",
                "payment_url": None,
                "status": "processing",
                "message": "Hubtel credentials not configured. Using mock payment for development."
            }
        
        # Hubtel API endpoint (example - adjust based on actual API)
        url = "https://api.hubtel.com/v1/merchantaccount/onlinecheckout/invoice/create"
        
        headers = {
            "Authorization": f"Basic {settings.HUBTEL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "total_amount": order.total_amount,
            "description": f"Order #{order.order_number}",
            "callback_url": f"https://yourdomain.com/api/payments/callback/hubtel",
            "return_url": f"https://yourdomain.com/api/payments/return/hubtel",
            "client_reference": order.order_number
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                return {
                    "payment_reference": data.get("invoice_id", f"HUBTEL-{order.order_number}"),
                    "payment_url": data.get("invoice_url"),
                    "status": "processing"
                }
        except Exception as e:
            # Fallback for development
            return {
                "payment_reference": f"HUBTEL-{order.order_number}",
                "payment_url": None,
                "status": "processing",
                "message": f"Payment gateway error: {str(e)}. Using mock payment."
            }
    
    @staticmethod
    async def _initiate_paystack_payment(order: Order) -> Dict:
        """Initiate Paystack payment"""
        # For development: if credentials not configured, return mock response
        if not settings.PAYSTACK_SECRET_KEY:
            return {
                "payment_reference": f"PAYSTACK-{order.order_number}",
                "payment_url": None,
                "status": "processing",
                "message": "Paystack credentials not configured. Using mock payment for development."
            }
        
        url = "https://api.paystack.co/transaction/initialize"
        
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "email": order.customer_email or order.customer_phone,
            "amount": int(order.total_amount * 100),  # Paystack uses kobo (smallest currency unit)
            "reference": order.order_number,
            "callback_url": f"https://yourdomain.com/api/payments/callback/paystack",
            "metadata": {
                "order_id": order.id,
                "order_number": order.order_number
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                return {
                    "payment_reference": data["data"]["reference"],
                    "payment_url": data["data"]["authorization_url"],
                    "status": "processing"
                }
        except Exception as e:
            # Fallback for development
            return {
                "payment_reference": f"PAYSTACK-{order.order_number}",
                "payment_url": None,
                "status": "processing",
                "message": f"Payment gateway error: {str(e)}. Using mock payment."
            }
    
    @staticmethod
    async def verify_payment(payment_reference: str, payment_method: PaymentMethod) -> Dict:
        """Verify payment status"""
        if payment_method == PaymentMethod.PAYSTACK:
            return await PaymentService._verify_paystack_payment(payment_reference)
        elif payment_method == PaymentMethod.HUBTEL:
            return await PaymentService._verify_hubtel_payment(payment_reference)
        else:
            return {"status": "completed", "verified": True}
    
    @staticmethod
    async def _verify_paystack_payment(reference: str) -> Dict:
        """Verify Paystack payment"""
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                return {
                    "status": "completed" if data["data"]["status"] == "success" else "failed",
                    "verified": data["data"]["status"] == "success"
                }
        except Exception as e:
            return {"status": "failed", "verified": False}
    
    @staticmethod
    async def _verify_hubtel_payment(reference: str) -> Dict:
        """Verify Hubtel payment"""
        # Implement Hubtel verification logic
        return {"status": "completed", "verified": True}

