from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Product, User
from schemas import ProductCreate, ProductUpdate, ProductResponse
from auth import get_current_admin

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    category: str = None,
    available_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all products (public endpoint)"""
    query = db.query(Product)
    
    if available_only:
        query = query.filter(Product.is_available == True)
    
    if category:
        query = query.filter(Product.category == category)
    
    products = query.all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a single product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Create a new product (admin only)"""
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Update a product (admin only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    update_data = product_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Delete a product (admin only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    return None

