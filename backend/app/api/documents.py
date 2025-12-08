"""
Document API endpoints
"""
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.schemas.document import DocumentResponse
from app.services.ingestion import IngestionService
from app.services.chunking import ChunkingService
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/documents", tags=["documents"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Query(None),
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    try:
        logger.info(f"📤 Uploading file: {file.filename}")
        
        # Validate file type
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ['pdf', 'txt', 'md', 'docx']:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}"
            )
        
        # Save file
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{file_id}.{file_ext}"
        
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        logger.info(f"✅ File saved to: {file_path}")
        
        # Create document in database with chunking
        logger.info(f"📝 Creating document in database...")
        document = IngestionService.create_document(
            db=db,
            filename=file.filename,
            file_type=file_ext,
            file_path=str(file_path),
            title=title or file.filename,
            content_type=f"application/{file_ext}"
        )
        logger.info(f"✅ Document created: {document.id}")
        logger.info(f"   Filename: {document.filename}")
        logger.info(f"   File size: {document.file_size} bytes")
        
        return document
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error uploading document: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db)):
    """Get document by ID"""
    document = IngestionService.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("", response_model=list)
def list_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all documents"""
    return IngestionService.list_documents(db, skip, limit)


@router.delete("/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)):
    """Delete document"""
    success = IngestionService.delete_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"success": True, "message": "Document deleted"}
