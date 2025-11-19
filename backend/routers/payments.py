from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Order, PaymentMethod, PaymentStatus
from services.payment_service import PaymentService
from auth import get_current_admin

router = APIRouter(prefix="/payments", tags=["Payments"])

payment_service = PaymentService()


@router.post("/verify/{order_id}")
async def verify_payment(
    order_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    """Verify payment status for an order (admin only)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if not order.payment_method or not order.payment_reference:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order has no payment method or reference"
        )
    
    try:
        result = await payment_service.verify_payment(
            order.payment_reference,
            order.payment_method
        )
        
        # Update order payment status if verified
        if result.get("verified"):
            order.payment_status = PaymentStatus.COMPLETED
            db.commit()
        
        return {
            "order_id": order_id,
            "payment_reference": order.payment_reference,
            "payment_method": order.payment_method.value,
            "verification_result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment verification failed: {str(e)}"
        )


@router.post("/complete/{order_id}")
async def complete_payment_manually(
    order_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    """Manually mark payment as completed (admin only)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.payment_status = PaymentStatus.COMPLETED
    db.commit()
    db.refresh(order)
    
    return {
        "message": "Payment marked as completed",
        "order_id": order_id,
        "payment_status": order.payment_status.value
    }

