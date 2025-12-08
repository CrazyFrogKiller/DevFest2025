from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
from datetime import datetime
import uuid
from app.models.base import Base
from app.config import get_settings


class Chunk(Base):
    """Chunk model for storing document fragments"""
    
    __tablename__ = "chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=True)
    # Use configured embedding dimension from settings to keep a single source of truth
    embedding = Column(Vector(get_settings().EMBEDDING_DIMENSION), nullable=True)
    chunk_metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
