from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration"""
    
    # Database
    DATABASE_URL: str = "postgresql+psycopg://user:password@localhost:5432/rag_db"
    
    # Google Gemini API
    GOOGLE_API_KEY: str = ""
    
    # Embedding config
    CHUNK_SIZE: int = 800  # tokens
    CHUNK_OVERLAP: int = 200  # tokens
    # Embedding vector dimension used for storage and retrieval (default Gemini 768)
    EMBEDDING_DIMENSION: int = 768
    
    # Retrieval config
    TOP_K_CHUNKS: int = 5
    SIMILARITY_THRESHOLD: float = 0.5
    
    # App
    DEBUG: bool = False
    # Generation model for synthesis (can be overridden via .env). If you want Gemini,
    # set this to a supported Gemini model available in your account (example: 'models/gemini-1.0').
    GENERATION_MODEL: str = "models/gemini-2.5-flash"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
