from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Any


class ChunkBase(BaseModel):
    """Base chunk schema"""
    content: str
    start_char: int
    end_char: int


class ChunkCreate(ChunkBase):
    """Schema for creating a chunk"""
    document_id: int
    chunk_index: int
    chunk_metadata: Optional[dict] = None


class ChunkResponse(ChunkBase):
    """Schema for chunk response"""
    id: int
    document_id: int
    chunk_index: int
    created_at: datetime
    chunk_metadata: Optional[dict] = None
    
    class Config:
        from_attributes = True


class ChunkWithScore(ChunkResponse):
    """Chunk with similarity score"""
    similarity_score: float = Field(..., ge=0, le=1)
