from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.config import get_settings

settings = get_settings()

# Create database engine
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
    )
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    # If database connection fails during import, create a mock session for development
    import logging
    logging.warning(f"Database initialization warning: {e}. Using development mode.")
    SessionLocal = None
    engine = None


def get_db() -> Generator[Session, None, None]:
    """Dependency for getting database session"""
    if SessionLocal is None:
        raise RuntimeError(
            "Database not initialized. Please set DATABASE_URL in .env "
            "and ensure PostgreSQL is running."
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
