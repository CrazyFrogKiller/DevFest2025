"""
Query API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.schemas.query import QueryRequest, QueryResponse
from app.services.retrieval import RetrievalService
from app.services.synthesis import SynthesisService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/queries", tags=["queries"])


@router.post("/ask", response_model=QueryResponse)
def ask_question(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """Ask a question and get an answer with sources"""
    try:
        # Validate input
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Retrieve relevant chunks
        chunks = RetrievalService.retrieve_chunks(
            db,
            request.query,
            top_k=request.top_k or 5
        )
        
        if not chunks:
            return QueryResponse(
                query=request.query,
                answer="I don't have any relevant information to answer your question.",
                chunks=[],
                sources=[]
            )
        
        # Generate answer
        answer = SynthesisService.generate_answer(request.query, chunks)
        
        # Format sources
        sources = SynthesisService.format_sources(chunks)
        
        # Format chunks for response
        formatted_chunks = [
            {
                "id": chunk.id,
                "content": chunk.content[:300] + "..." if len(chunk.content) > 300 else chunk.content,
                "score": score,
                "source": chunk.chunk_metadata.get("document_filename") if chunk.chunk_metadata else "Unknown"
            }
            for chunk, score in chunks
        ]
        
        return QueryResponse(
            query=request.query,
            answer=answer,
            chunks=formatted_chunks,
            sources=sources
        )
    
    except ValueError as e:
        error_msg = str(e)
        # Check if it's a quota error
        if "quota" in error_msg.lower():
            logger.error(f"API quota exceeded: {error_msg}")
            raise HTTPException(
                status_code=429,
                detail=error_msg
            )
        # Other value errors
        logger.error(f"Validation error: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)
    
    except HTTPException:
        raise
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Unexpected error in ask_question: {error_msg}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {error_msg}"
        )
