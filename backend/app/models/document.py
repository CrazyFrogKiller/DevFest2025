from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from app.models.base import Base


class Document(Base):
    """Document model for storing uploaded documents"""
    
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False, index=True)
    title = Column(String(500), nullable=True)
    content_type = Column(String(50), nullable=True)
    file_size = Column(Integer, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    doc_metadata = Column(JSONB, nullable=True)
