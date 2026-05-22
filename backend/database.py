from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

# Use SQLite-specific settings if using SQLite
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    # PostgreSQL (Supabase)
    # - pool_pre_ping:  re-validates connections before use (avoids stale conn errors)
    # - pool_recycle:   recycle connections every 5 min (Supabase drops idle > 10 min)
    # - pool_size:      keep 5 persistent connections
    # - max_overflow:   allow up to 10 extra burst connections
    # - pool_timeout:   wait up to 30 s for a free connection before raising
    # - sslmode=require: Supabase requires SSL on all connections
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"sslmode": "require"},
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

