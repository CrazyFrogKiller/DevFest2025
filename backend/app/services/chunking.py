from sqlalchemy.orm import Session
from app.models.chunk import Chunk
from app.models.document import Document
from app.utils.text_processor import TextProcessor
from app.config import get_settings
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class ChunkingService:
    """Service for chunking documents"""
    
    settings = get_settings()
    
    @staticmethod
    def chunk_document(
        db: Session,
        document_id,  # Can be UUID or string
        content: str = None,
        chunk_size: int = None,
        overlap: int = None
    ) -> list:
        """
        Chunk a document and store chunks in database
        
        Args:
            db: Database session
            document_id: ID of document to chunk (UUID or string)
            content: Document content (if not fetching from DB)
            chunk_size: Size of chunks in tokens
            overlap: Overlap between chunks
            
        Returns:
            List of created Chunk instances
        """
        if chunk_size is None:
            chunk_size = ChunkingService.settings.CHUNK_SIZE
        if overlap is None:
            overlap = ChunkingService.settings.CHUNK_OVERLAP
        
        logger.info(f"🔍 Chunk document params: size={chunk_size}, overlap={overlap}")
        
        # Convert string to UUID if necessary
        import uuid as uuid_module
        if isinstance(document_id, str):
            try:
                document_id = uuid_module.UUID(document_id)
            except (ValueError, AttributeError):
                raise ValueError(f"Invalid document_id format: {document_id}")
        
        # Get document to extract filename for metadata
        logger.info(f"📋 Fetching document {document_id} from DB...")
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError(f"Document {document_id} not found")
        logger.info(f"✅ Found document: {document.filename}")
        
        if content is None:
            raise ValueError("Content must be provided for chunking")
        
        logger.info(f"📏 Content length: {len(content)} chars")
        
        # Chunk text
        logger.info(f"✂️  Processing chunks...")
        chunk_data = TextProcessor.smart_chunk_text(
            content,
            chunk_size=chunk_size,
            overlap=overlap
        )
        logger.info(f"✅ Generated {len(chunk_data)} chunks from text")
        
        doc_filename = document.filename if document else "Unknown"
        
        # Create chunk records
        chunks = []
        for idx, (chunk_text, start_char, end_char) in enumerate(chunk_data):
            chunk = Chunk(
                id=uuid_module.uuid4(),
                document_id=document_id,
                content=chunk_text,
                chunk_index=idx,
                chunk_metadata={
                    "start_char": start_char,
                    "end_char": end_char,
                    "document_filename": doc_filename,
                    "category": "document"
                },
                created_at=datetime.utcnow()
            )
            chunks.append(chunk)
            db.add(chunk)
        
        logger.info(f"💾 Saving {len(chunks)} chunks to DB...")
        db.commit()
        logger.info(f"✅ Chunks committed to DB")
        
        return chunks
    
    @staticmethod
    def get_document_chunks(db: Session, document_id: str) -> list:
        """Get all chunks for a document"""
        return db.query(Chunk).filter(Chunk.document_id == document_id).all()
    
    @staticmethod
    def delete_document_chunks(db: Session, document_id: str) -> int:
        """Delete all chunks for a document"""
        count = db.query(Chunk).filter(Chunk.document_id == document_id).delete()
        db.commit()
        return count
