"""
Ingestion service for document handling
"""
from sqlalchemy.orm import Session
from app.models.document import Document
from app.utils.file_parser import FileParser
from app.services.chunking import ChunkingService
from app.services.embedding import EmbeddingService
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class IngestionService:
    """Service for ingesting and storing documents"""
    
    @staticmethod
    def create_document(
        db: Session,
        filename: str,
        file_type: str,
        file_path: str,
        title: str = None,
        content_type: str = None,
        metadata: dict = None
    ) -> Document:
        """
        Create a new document in the database
        
        Args:
            db: Database session
            filename: Filename
            file_type: Type of file (pdf, txt, md, docx)
            file_path: Path to file for parsing
            title: Document title
            content_type: MIME type
            metadata: Additional metadata
            
        Returns:
            Created Document instance
        """
        # Parse file content
        content = FileParser.parse_file(file_path, file_type)
        
        # Get file size
        import os
        file_size = os.path.getsize(file_path)
        
        # Create document
        document = Document(
            id=uuid.uuid4(),
            filename=filename,
            title=title or filename,
            content_type=content_type or f"application/{file_type}",
            file_size=file_size,
            uploaded_at=datetime.utcnow(),
            doc_metadata=metadata or {}
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        logger.info(f"✅ Document saved to DB: {document.id}")
        
        # Chunk the document content
        try:
            logger.info(f"🔄 Starting chunking process for document {document.id}...")
            chunks = ChunkingService.chunk_document(
                db=db,
                document_id=document.id,  # Pass UUID object directly
                content=content
            )
            logger.info(f"✅ Created {len(chunks)} chunks for document {document.id}")
            
            # Generate embeddings for chunks
            chunk_ids = [chunk.id for chunk in chunks]
            logger.info(f"🔄 Starting embedding generation for {len(chunk_ids)} chunks...")
            embeddings_count = EmbeddingService.embed_chunks(db, chunk_ids)
            logger.info(f"✅ Generated embeddings for {embeddings_count} chunks")
        except Exception as e:
            logger.error(f"❌ Error during chunking/embedding: {str(e)}", exc_info=True)
            db.rollback()
            # Continue anyway - document is created even if chunking fails
        
        return document
    
    @staticmethod
    def get_document(db: Session, document_id: str) -> Document:
        """Get document by ID"""
        return db.query(Document).filter(Document.id == document_id).first()
    
    @staticmethod
    def list_documents(db: Session, skip: int = 0, limit: int = 100) -> list:
        """List all documents"""
        return db.query(Document).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete_document(db: Session, document_id: str) -> bool:
        """Delete document by ID"""
        document = db.query(Document).filter(Document.id == document_id).first()
        if document:
            db.delete(document)
            db.commit()
            return True
        return False
