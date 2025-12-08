"""
Embedding service using Google Gemini API
"""
import google.generativeai as genai
import time
import logging
from sqlalchemy.orm import Session
from app.models.chunk import Chunk
from app.config import get_settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings using Gemini API"""
    
    settings = get_settings()
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    
    def __init__(self):
        """Initialize Gemini API"""
        if not self.settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not set in environment")
        
        genai.configure(api_key=self.settings.GOOGLE_API_KEY)
    
    @staticmethod
    def embed_text(text: str, retry_count: int = 0) -> list:
        """
        Generate embedding for text using Gemini with retry logic
        
        Args:
            text: Text to embed
            retry_count: Current retry attempt
            
        Returns:
            Embedding vector
            
        Raises:
            ValueError: If embedding fails after retries or quota exceeded
        """
        service = EmbeddingService()
        try:
            result = genai.embed_content(
                model="models/gemini-embedding-001",
                content=text,
                task_type="RETRIEVAL_DOCUMENT"
            )
            emb = result.get('embedding') or result.get('embeddings')
            if emb is None:
                raise ValueError(f"Embedding response missing 'embedding' field: {result}")

            # Ensure embedding length matches expected dimension
            expected_dim = EmbeddingService.settings.EMBEDDING_DIMENSION
            if len(emb) != expected_dim:
                # If embedding is longer, truncate with a warning to avoid DB errors.
                # Truncation may reduce quality; a better long-term fix is to regenerate
                # stored embeddings with the new model and update the DB vector size.
                if len(emb) > expected_dim:
                    logger.warning(
                        f"Embedding length {len(emb)} != expected {expected_dim}. Truncating to {expected_dim}."
                    )
                    emb = emb[:expected_dim]
                else:
                    # If shorter, fail explicitly
                    raise ValueError(f"Embedding length {len(emb)} shorter than expected {expected_dim}")

            return emb
        except Exception as e:
            error_msg = str(e)
            
            # Check if it's a quota error
            if "429" in error_msg or "quota" in error_msg.lower():
                quota_msg = (
                    "Google Gemini API quota exceeded for today. "
                    "Free tier limits: 1 request per minute, 100 requests per day. "
                    "Please wait until tomorrow or upgrade your API plan at https://ai.google.dev"
                )
                logger.error(f"Quota exceeded: {error_msg}")
                raise ValueError(quota_msg)
            
            # Retry for temporary errors
            if retry_count < EmbeddingService.MAX_RETRIES and ("deadline exceeded" in error_msg.lower() or "temporarily unavailable" in error_msg.lower()):
                logger.warning(f"Retry {retry_count + 1}/{EmbeddingService.MAX_RETRIES} for embedding. Error: {error_msg}")
                time.sleep(EmbeddingService.RETRY_DELAY)
                return EmbeddingService.embed_text(text, retry_count + 1)
            
            raise ValueError(f"Failed to embed text: {error_msg}")
    
    
    @staticmethod
    def embed_chunks(db: Session, chunk_ids: list = None) -> int:
        """
        Generate embeddings for chunks
        
        Args:
            db: Database session
            chunk_ids: Specific chunk IDs to embed (can be strings or UUID objects)
                       If None, all chunks without embeddings
            
        Returns:
            Number of chunks embedded
        """
        import uuid as uuid_module
        
        if chunk_ids:
            # Convert string UUIDs to actual UUID objects
            uuid_list = []
            for cid in chunk_ids:
                if isinstance(cid, str):
                    try:
                        uuid_list.append(uuid_module.UUID(cid))
                    except ValueError:
                        uuid_list.append(cid)
                else:
                    uuid_list.append(cid)
            chunks = db.query(Chunk).filter(Chunk.id.in_(uuid_list)).all()
        else:
            chunks = db.query(Chunk).filter(Chunk.embedding == None).all()
        
        count = 0
        for chunk in chunks:
            try:
                embedding = EmbeddingService.embed_text(chunk.content)
                chunk.embedding = embedding
                count += 1
            except ValueError as e:
                if "quota" in str(e).lower():
                    logger.error(f"Quota exceeded while embedding chunk {chunk.id}. Stopping.")
                    break
                logger.warning(f"Failed to embed chunk {chunk.id}: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error embedding chunk {chunk.id}: {str(e)}")
                continue
        
        if count > 0:
            db.commit()
        return count
