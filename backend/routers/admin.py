from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from database import get_db
from models import Order, OrderStatus, PaymentStatus, PaymentMethod, User, OrderItem
from schemas import DashboardStats, OrderResponse
from auth import get_current_admin
from datetime import datetime, timedelta
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get dashboard statistics (admin only)"""
    # Total orders
    total_orders = db.query(func.count(Order.id)).scalar() or 0
    
    # Pending orders (orders not yet completed)
    pending_orders = db.query(func.count(Order.id)).filter(
        Order.status.in_([OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.READY])
    ).scalar() or 0
    
    # Completed orders
    completed_orders = db.query(func.count(Order.id)).filter(
        Order.status == OrderStatus.COMPLETED
    ).scalar() or 0
    
    # Total revenue
    total_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.payment_status == PaymentStatus.COMPLETED
    ).scalar() or 0.0
    
    # Today's revenue
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.payment_status == PaymentStatus.COMPLETED,
        Order.created_at >= today_start
    ).scalar() or 0.0
    
    # Average wait time (time from created to completed)
    completed_orders_with_time = db.query(Order).filter(
        Order.status == OrderStatus.COMPLETED,
        Order.completed_at.isnot(None)
    ).all()
    
    average_wait_time = None
    if completed_orders_with_time:
        wait_times = []
        for order in completed_orders_with_time:
            if order.completed_at:
                wait_time = (order.completed_at - order.created_at).total_seconds() / 60  # minutes
                wait_times.append(wait_time)
        if wait_times:
            average_wait_time = sum(wait_times) / len(wait_times)
    
    # Digital payment percentage
    total_paid_orders = db.query(func.count(Order.id)).filter(
        Order.payment_status == PaymentStatus.COMPLETED
    ).scalar() or 0
    
    digital_paid_orders = db.query(func.count(Order.id)).filter(
        Order.payment_status == PaymentStatus.COMPLETED,
        Order.payment_method.in_([PaymentMethod.HUBTEL, PaymentMethod.PAYSTACK, PaymentMethod.MOBILE_MONEY, PaymentMethod.CARD])
    ).scalar() or 0
    
    digital_payment_percentage = (digital_paid_orders / total_paid_orders * 100) if total_paid_orders > 0 else 0.0
    
    return DashboardStats(
        total_orders=total_orders,
        pending_orders=pending_orders,
        completed_orders=completed_orders,
        total_revenue=float(total_revenue),
        today_revenue=float(today_revenue),
        average_wait_time=average_wait_time,
        digital_payment_percentage=round(digital_payment_percentage, 2)
    )


@router.get("/orders/pending", response_model=List[OrderResponse])
async def get_pending_orders(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get all pending orders (admin only)"""
    orders = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter(
        Order.status.in_([OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.READY])
    ).order_by(Order.created_at.asc()).all()
    return [OrderResponse.from_orm_with_items(order) for order in orders]

