from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import OrderStatus, PaymentStatus, PaymentMethod


# User Schemas
class UserBase(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str


class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_available: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Order Item Schemas
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    customization: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: Optional[str] = None
    quantity: int
    unit_price: float
    customization: Optional[str] = None
    subtotal: float
    
    @classmethod
    def from_orm_with_product(cls, order_item):
        """Create response with product name from relationship"""
        return cls(
            id=order_item.id,
            product_id=order_item.product_id,
            product_name=order_item.product.name if order_item.product else None,
            quantity=order_item.quantity,
            unit_price=order_item.unit_price,
            customization=order_item.customization,
            subtotal=order_item.subtotal
        )
    
    class Config:
        from_attributes = True


# Order Schemas
class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: Optional[EmailStr] = None
    items: List[OrderItemCreate]
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    notes: Optional[str] = None
    pickup_time: Optional[datetime] = None


class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer_id: Optional[int] = None
    customer_name: str
    customer_phone: str
    customer_email: Optional[str] = None
    status: OrderStatus
    total_amount: float
    payment_status: PaymentStatus
    payment_method: Optional[PaymentMethod] = None
    payment_reference: Optional[str] = None
    notes: Optional[str] = None
    pickup_time: Optional[datetime] = None
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @classmethod
    def from_orm_with_items(cls, order):
        """Create response with properly serialized items"""
        return cls(
            id=order.id,
            order_number=order.order_number,
            customer_id=order.customer_id,
            customer_name=order.customer_name,
            customer_phone=order.customer_phone,
            customer_email=order.customer_email,
            status=order.status,
            total_amount=order.total_amount,
            payment_status=order.payment_status,
            payment_method=order.payment_method,
            payment_reference=order.payment_reference,
            notes=order.notes,
            pickup_time=order.pickup_time,
            items=[OrderItemResponse.from_orm_with_product(item) for item in order.items],
            created_at=order.created_at,
            updated_at=order.updated_at,
            completed_at=order.completed_at
        )
    
    class Config:
        from_attributes = True


# Payment Schemas
class PaymentInitiate(BaseModel):
    order_id: int
    payment_method: PaymentMethod


class PaymentResponse(BaseModel):
    payment_reference: str
    payment_url: Optional[str] = None
    status: PaymentStatus


# Dashboard Schemas
class DashboardStats(BaseModel):
    total_orders: int
    pending_orders: int
    completed_orders: int
    total_revenue: float
    today_revenue: float
    average_wait_time: Optional[float] = None
    digital_payment_percentage: float

