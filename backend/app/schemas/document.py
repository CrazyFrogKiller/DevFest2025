from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class DocumentBase(BaseModel):
    """Base document schema"""
    filename: str
    title: Optional[str] = None
    content_type: Optional[str] = None


class DocumentCreate(DocumentBase):
    """Schema for creating a document"""
    pass


class DocumentResponse(DocumentBase):
    """Schema for document response"""
    id: UUID
    file_size: Optional[int] = None
    uploaded_at: datetime
    doc_metadata: Optional[dict] = None
    
    class Config:
        from_attributes = True
