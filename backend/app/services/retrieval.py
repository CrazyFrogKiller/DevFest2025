"""
Retrieval service for semantic search
"""
from sqlalchemy.orm import Session
from sqlalchemy import Float
import logging
from app.models.chunk import Chunk
from app.services.embedding import EmbeddingService
from app.config import get_settings

logger = logging.getLogger(__name__)


class RetrievalService:
    """Service for retrieving relevant chunks based on query"""
    
    settings = get_settings()
    EMBEDDING_DIMENSION = settings.EMBEDDING_DIMENSION
    
    @staticmethod
    def retrieve_chunks(
        db: Session,
        query: str,
        top_k: int = None,
        threshold: float = None
    ) -> list:
        """
        Retrieve relevant chunks for a query
        
        Args:
            db: Database session
            query: Query text
            top_k: Number of chunks to retrieve
            threshold: Minimum similarity threshold
            
        Returns:
            List of (Chunk, similarity_score) tuples
            
        Raises:
            ValueError: If embedding fails
        """
        if top_k is None:
            top_k = RetrievalService.settings.TOP_K_CHUNKS
        if threshold is None:
            threshold = RetrievalService.settings.SIMILARITY_THRESHOLD
        
        try:
            # Generate query embedding
            query_embedding = EmbeddingService.embed_text(query)

            # Validate embedding dimension for query
            if len(query_embedding) != RetrievalService.EMBEDDING_DIMENSION:
                logger.warning(
                    f"Query embedding length {len(query_embedding)} != expected {RetrievalService.EMBEDDING_DIMENSION}."
                )
        except ValueError as e:
            logger.error(f"Failed to generate query embedding: {str(e)}")
            raise
        
        # Query chunks with similarity scores using pgvector's <-> operator
        # The <-> operator returns cosine distance (0 = most similar, 2 = most dissimilar for normalized vectors)
        results = db.query(
            Chunk,
            # Use the <-> operator for cosine distance
            Chunk.embedding.op('<->', return_type=Float)(query_embedding).label('similarity')
        ).filter(
            Chunk.embedding != None
        ).order_by(
            'similarity'
        ).limit(top_k).all()
        
        # Convert similarity distance to score (1 - distance)
        scored_results = [
            (chunk, 1 - score) for chunk, score in results
            if (1 - score) >= threshold
        ]
        
        logger.info(f"Retrieved {len(scored_results)} relevant chunks for query")
        return scored_results
    
    @staticmethod
    def search(
        db: Session,
        query: str,
        top_k: int = 5
    ) -> list:
        """
        Simple search interface
        
        Args:
            db: Database session
            query: Query text
            top_k: Number of results
            
        Returns:
            List of chunks with scores
        """
        return RetrievalService.retrieve_chunks(db, query, top_k)
