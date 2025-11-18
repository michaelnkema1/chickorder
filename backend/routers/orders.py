from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from database import get_db
from models import Order, OrderStatus, PaymentStatus, User, OrderItem
from schemas import OrderCreate, OrderUpdate, OrderResponse, OrderItemResponse
from auth import get_current_user, get_current_admin, get_optional_user
from services.order_service import OrderService
from services.payment_service import PaymentService
from services.notification_service import NotificationService
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["Orders"])

order_service = OrderService()
payment_service = PaymentService()
notification_service = NotificationService()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Create a new order (public endpoint)"""
    try:
        customer_id = current_user.id if current_user else None
        order = order_service.create_order(db, order_data, customer_id)
        
        # Send confirmation notification
        await notification_service.send_order_confirmation(order)
        
        # Reload order with items and products
        db.refresh(order)
        for item in order.items:
            db.refresh(item)
            if item.product:
                db.refresh(item.product)
        
        return OrderResponse.from_orm_with_items(order)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    status_filter: Optional[OrderStatus] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Get orders (customers see their own, admins see all)"""
    query = db.query(Order).options(joinedload(Order.items).joinedload(OrderItem.product))
    
    if current_user and not current_user.is_admin:
        # Customers see only their orders
        query = query.filter(Order.customer_id == current_user.id)
    
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    orders = query.order_by(Order.created_at.desc()).all()
    return [OrderResponse.from_orm_with_items(order) for order in orders]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """Get a single order"""
    order = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check permissions
    if current_user and not current_user.is_admin:
        if order.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this order"
            )
    
    return OrderResponse.from_orm_with_items(order)


@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_update: OrderUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Update order status (admin only)"""
    try:
        if status_update.status:
            order = order_service.update_order_status(
                db,
                order_id,
                status_update.status,
                status_update.payment_status
            )
            
            # Send status update notification
            await notification_service.send_status_update(order)
            
            # Reload order with items and products
            db.refresh(order)
            for item in order.items:
                db.refresh(item)
                if item.product:
                    db.refresh(item.product)
            
            return OrderResponse.from_orm_with_items(order)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status is required"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{order_id}/payment", response_model=dict)
async def initiate_payment(
    order_id: int,
    payment_method: str,
    db: Session = Depends(get_db)
):
    """Initiate payment for an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    try:
        from models import PaymentMethod
        payment_method_enum = PaymentMethod(payment_method)
        result = await payment_service.initiate_payment(order, payment_method_enum)
        
        # Update order with payment reference
        order.payment_method = payment_method_enum
        order.payment_reference = result["payment_reference"]
        order.payment_status = PaymentStatus.PROCESSING
        db.commit()
        
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

