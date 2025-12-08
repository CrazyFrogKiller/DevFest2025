from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    """Schema for query request"""
    query: str
    top_k: Optional[int] = 5


class QueryResponse(BaseModel):
    """Schema for query response"""
    query: str
    answer: str
    chunks: list
    sources: list
    total_tokens: Optional[int] = None
