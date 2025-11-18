"""
Initialize database with admin user and sample products
Run this script after setting up the database
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Product
from auth import get_password_hash
from config import settings

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()


def init_admin():
    """Create admin user"""
    admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if not admin:
        admin = User(
            name="Admin",
            email=settings.ADMIN_EMAIL,
            phone="+1234567890",  # Update with actual admin phone
            password_hash=get_password_hash(settings.ADMIN_PASSWORD),
            is_admin=True,
            is_active=True
        )
        db.add(admin)
        db.commit()
        print(f"Admin user created: {settings.ADMIN_EMAIL}")
    else:
        print(f"Admin user already exists: {settings.ADMIN_EMAIL}")


def init_sample_products():
    """Create sample products - Live chickens that are killed and dressed upon order"""
    sample_products = [
        {
            "name": "Layer",
            "description": "Live layer chicken. We kill and dress it fresh for you when you order. Ready for pickup when prepared.",
            "price": 130.00,
            "category": "live_chicken",
            "is_available": True
        },
        {
            "name": "Broiler",
            "description": "Live broiler chicken. We kill and dress it fresh for you when you order. Ready for pickup when prepared.",
            "price": 250.00,
            "category": "live_chicken",
            "is_available": True
        },
        {
            "name": "Cockerel",
            "description": "Live cockerel. We kill and dress it fresh for you when you order. Ready for pickup when prepared.",
            "price": 250.00,
            "category": "live_chicken",
            "is_available": True
        },
        {
            "name": "Guinea Fowl",
            "description": "Live guinea fowl. We kill and dress it fresh for you when you order. Ready for pickup when prepared.",
            "price": 250.00,
            "category": "live_chicken",
            "is_available": True
        },
        {
            "name": "Saso Layers",
            "description": "Live Saso layer chicken. We kill and dress it fresh for you when you order. Ready for pickup when prepared.",
            "price": 200.00,
            "category": "live_chicken",
            "is_available": True
        }
    ]
    
    for product_data in sample_products:
        existing = db.query(Product).filter(Product.name == product_data["name"]).first()
        if not existing:
            product = Product(**product_data)
            db.add(product)
            print(f"Created product: {product_data['name']}")
    
    db.commit()
    print("Sample products created")


if __name__ == "__main__":
    print("Initializing database...")
    init_admin()
    init_sample_products()
    print("Database initialization complete!")
    db.close()

