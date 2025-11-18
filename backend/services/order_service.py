from sqlalchemy.orm import Session
from typing import Optional
from models import Order, OrderItem, Product, OrderStatus, PaymentStatus
from schemas import OrderCreate, OrderUpdate
from datetime import datetime
import random
import string


class OrderService:
    """Service for order management and state machine"""
    
    @staticmethod
    def generate_order_number() -> str:
        """Generate unique order number"""
        timestamp = datetime.now().strftime("%Y%m%d")
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"CHK-{timestamp}-{random_str}"
    
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate, customer_id: Optional[int] = None) -> Order:
        """Create a new order"""
        # Calculate total and create order items
        total_amount = 0.0
        order_items_data = []
        
        for item_data in order_data.items:
            product = db.query(Product).filter(Product.id == item_data.product_id).first()
            if not product:
                raise ValueError(f"Product with id {item_data.product_id} not found")
            if not product.is_available:
                raise ValueError(f"Product {product.name} is not available")
            
            subtotal = product.price * item_data.quantity
            total_amount += subtotal
            
            order_items_data.append({
                "product": product,
                "quantity": item_data.quantity,
                "unit_price": product.price,
                "customization": item_data.customization,
                "subtotal": subtotal
            })
        
        # Create order
        order = Order(
            order_number=OrderService.generate_order_number(),
            customer_id=customer_id,
            customer_name=order_data.customer_name,
            customer_phone=order_data.customer_phone,
            customer_email=order_data.customer_email,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
            payment_status=PaymentStatus.PENDING,
            payment_method=order_data.payment_method,
            notes=order_data.notes
        )
        
        db.add(order)
        db.flush()  # Get order ID
        
        # Create order items
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data["product"].id,
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                customization=item_data["customization"],
                subtotal=item_data["subtotal"]
            )
            db.add(order_item)
        
        db.commit()
        db.refresh(order)
        return order
    
    @staticmethod
    def update_order_status(
        db: Session,
        order_id: int,
        status: OrderStatus,
        payment_status: Optional[PaymentStatus] = None
    ) -> Order:
        """Update order status with state machine validation"""
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError("Order not found")
        
        # State machine validation
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
            OrderStatus.PREPARING: [OrderStatus.READY, OrderStatus.CANCELLED],
            OrderStatus.READY: [OrderStatus.COMPLETED],
            OrderStatus.COMPLETED: [],
            OrderStatus.CANCELLED: []
        }
        
        if status not in valid_transitions.get(order.status, []):
            raise ValueError(
                f"Invalid status transition from {order.status.value} to {status.value}"
            )
        
        order.status = status
        
        if status == OrderStatus.COMPLETED:
            order.completed_at = datetime.utcnow()
        
        if payment_status:
            order.payment_status = payment_status
        
        order.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(order)
        return order

