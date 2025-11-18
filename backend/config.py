from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database (defaults to SQLite for development)
    DATABASE_URL: str = "sqlite:///./chickorder.db"
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Admin
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    
    # Payment Providers
    HUBTEL_API_KEY: Optional[str] = None
    HUBTEL_CLIENT_ID: Optional[str] = None
    HUBTEL_CLIENT_SECRET: Optional[str] = None
    
    PAYSTACK_SECRET_KEY: Optional[str] = None
    PAYSTACK_PUBLIC_KEY: Optional[str] = None
    
    # Notifications
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    
    WHATSAPP_BUSINESS_ID: Optional[str] = None
    WHATSAPP_ACCESS_TOKEN: Optional[str] = None
    
    # App Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

