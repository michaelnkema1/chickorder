#!/usr/bin/env python3
"""
Test script for payment functionality
Run this to test different payment methods
"""

import asyncio
import sys
from database import SessionLocal
from models import Order, Product, OrderItem, OrderStatus, PaymentStatus, PaymentMethod
from services.payment_service import PaymentService

async def test_payment_methods():
    """Test all payment methods"""
    db = SessionLocal()
    
    try:
        # Get or create a test order
        product = db.query(Product).first()
        if not product:
            print("❌ No products found. Please run init_db.py first.")
            return
        
        # Create a test order
        order = Order(
            order_number="TEST-PAYMENT-001",
            customer_name="Test Customer",
            customer_phone="+1234567890",
            customer_email="test@example.com",
            status=OrderStatus.PENDING,
            total_amount=250.0,
            payment_status=PaymentStatus.PENDING
        )
        db.add(order)
        db.flush()
        
        item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=1,
            unit_price=product.price,
            subtotal=product.price
        )
        db.add(item)
        db.commit()
        db.refresh(order)
        
        print(f"✅ Created test order: #{order.order_number}")
        print(f"   Amount: GHS {order.total_amount:.2f}")
        print(f"   Status: {order.payment_status.value}")
        print("")
        
        payment_service = PaymentService()
        
        # Test each payment method
        payment_methods = [
            PaymentMethod.CASH,
            PaymentMethod.MOBILE_MONEY,
            PaymentMethod.HUBTEL,
            PaymentMethod.PAYSTACK,
        ]
        
        for method in payment_methods:
            print(f"🧪 Testing {method.value}...")
            
            # Reset order payment status
            order.payment_status = PaymentStatus.PENDING
            order.payment_method = None
            order.payment_reference = None
            db.commit()
            
            try:
                result = await payment_service.initiate_payment(order, method)
                print(f"   ✅ Success!")
                print(f"   Reference: {result.get('payment_reference')}")
                print(f"   Status: {result.get('status')}")
                if result.get('payment_url'):
                    print(f"   Payment URL: {result.get('payment_url')}")
                if result.get('message'):
                    print(f"   Note: {result.get('message')}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print("")
        
        # Cleanup
        db.delete(order)
        db.commit()
        print("✅ Test completed. Test order cleaned up.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_payment_methods())

