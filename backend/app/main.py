"""
FastAPI application main entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import documents, queries
from app.config import get_settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="RAG System with Gemini",
    description="Retrieval-Augmented Generation system using Google Gemini API",
    version="1.0.0",
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=["http://127.0.0.1:5173", "http://localhost:5173", "http://localhost:8001", "http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router)
app.include_router(queries.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "name": "RAG System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "RAG System API"
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("RAG System API starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("RAG System API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8001,
        reload=settings.DEBUG,
        reload_dirs=["app"],  # Only watch app directory, not .venv
        watch_filter=None
    )
