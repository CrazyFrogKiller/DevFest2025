"""
Base model for all SQLAlchemy models
"""
from sqlalchemy.orm import declarative_base

# Create a single Base instance for all models
Base = declarative_base()
