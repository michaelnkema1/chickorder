#!/usr/bin/env python3
"""
Test script for SMS notifications
Run this to test SMS notifications when order is ready
"""

import asyncio
import sys
from database import SessionLocal
from models import Order, OrderStatus
from services.notification_service import NotificationService

async def test_sms_notification():
    """Test SMS notification for order ready status"""
    db = SessionLocal()
    
    try:
        # Find an order to test with
        order = db.query(Order).filter(
            Order.status.in_([OrderStatus.PENDING, OrderStatus.CONFIRMED])
        ).first()
        
        if not order:
            print("❌ No suitable order found. Please create an order first.")
            return
        
        print(f"✅ Testing SMS notification")
        print(f"   Order: #{order.order_number}")
        print(f"   Customer: {order.customer_name}")
        print(f"   Phone: {order.customer_phone}")
        print(f"   Current Status: {order.status.value}")
        print()
        
        # Update order to READY status
        old_status = order.status
        order.status = OrderStatus.READY
        db.commit()
        db.refresh(order)
        
        print(f"✅ Order status updated: {old_status.value} → {order.status.value}")
        print()
        
        # Send SMS notification
        notification_service = NotificationService()
        print("📱 Sending SMS notification...")
        print()
        
        result = await notification_service.send_status_update(order)
        
        if result:
            print("✅ SMS notification sent successfully!")
            print()
            print("📋 Message sent:")
            print("─" * 50)
            message = (
                f"Order Update 🐔\n\n"
                f"Order #: {order.order_number}\n"
                f"🎉 Your chickens are ready! Order #{order.order_number} has been killed, dressed, and is ready for pickup!"
            )
            print(message)
            print("─" * 50)
        else:
            print("❌ Failed to send SMS notification")
        
        # Reset order status for testing
        order.status = old_status
        db.commit()
        print()
        print(f"✅ Order status reset to: {old_status.value}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_sms_notification())

