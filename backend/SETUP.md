# RAG System Setup Guide

## Project Overview

This is a complete **Retrieval-Augmented Generation (RAG) system** using Google Gemini API. The system allows users to:

1. Upload and process documents (PDF, TXT, MD, DOCX)
2. Intelligently chunk documents into semantic fragments
3. Generate embeddings using Google Gemini API
4. Perform semantic search on document chunks
5. Generate contextual answers using Gemini with proper source attribution

## Architecture

### Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection & session
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── document.py         # Document model
│   │   └── chunk.py            # Chunk/fragment model
│   ├── schemas/                # Pydantic validation schemas
│   │   ├── document.py
│   │   ├── chunk.py
│   │   ├── query.py
│   │   └── response.py
│   ├── api/                    # API route handlers
│   │   ├── documents.py        # Document endpoints
│   │   └── queries.py          # Query/search endpoints
│   ├── services/               # Business logic
│   │   ├── ingestion.py        # Document upload/storage
│   │   ├── chunking.py         # Text chunking logic
│   │   ├── embedding.py        # Gemini embedding service
│   │   ├── retrieval.py        # Semantic search service
│   │   └── synthesis.py        # Answer generation service
│   └── utils/
│       ├── file_parser.py      # PDF, DOCX, TXT, MD parsing
│       └── text_processor.py   # Text preprocessing & chunking
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project metadata
├── .env.example               # Environment variables template
└── README.md
```

### Frontend Structure

```
frontend/
├── src/
│   ├── App.tsx                # Main app component
│   ├── main.tsx               # React entry point
│   ├── components/            # React components
│   │   ├── Layout.tsx
│   │   ├── SourceReference.tsx
│   │   └── ui/                # shadcn/ui components
│   ├── features/
│   │   ├── documents/         # Document upload feature
│   │   │   ├── DocumentUpload.tsx
│   │   │   ├── documentsApi.ts
│   │   │   └── documentsSlice.ts
│   │   └── queries/           # Query/search feature
│   │       ├── QueryInput.tsx
│   │       ├── QueryResponse.tsx
│   │       ├── queriesApi.ts
│   │       └── queriesSlice.ts
│   ├── app/
│   │   └── store.ts           # Redux store configuration
│   └── hooks/
│       └── useAppDispatch.ts
├── package.json
├── vite.config.ts
├── tsconfig.json
└── eslint.config.js
```

## Installation & Setup

### Prerequisites

- Python 3.10+ (tested with 3.14)
- Node.js 16+
- PostgreSQL 15+ with pgvector extension
- Google Gemini API key

### Backend Setup

1. **Install Python dependencies:**

   ```bash
   cd backend
   uv sync
   ```

2. **Configure environment:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configuration:

   ```
   DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/rag_db
   GOOGLE_API_KEY=your_api_key_here
   CHUNK_SIZE=800
   CHUNK_OVERLAP=200
   TOP_K_CHUNKS=5
   SIMILARITY_THRESHOLD=0.5
   DEBUG=False
   ```

3. **Setup PostgreSQL database:**

   ```sql
   CREATE DATABASE rag_db;
   CREATE EXTENSION pgvector;
   ```

4. **Run database migrations (when needed):**

   ```bash
   alembic upgrade head
   ```

5. **Start backend server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install dependencies:**

   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**

   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

## API Endpoints

### Documents

- `POST /api/documents/upload` - Upload and process a document
- `GET /api/documents` - List all documents
- `GET /api/documents/{id}` - Get specific document
- `DELETE /api/documents/{id}` - Delete document

### Queries

- `POST /api/queries/ask` - Ask a question and get answer with sources

## Key Technologies

### Backend

- **FastAPI** - Modern web framework
- **SQLAlchemy 2.0** - ORM with async support
- **PostgreSQL + pgvector** - Vector database
- **Google Gemini API** - Embeddings & text generation
- **Pydantic** - Data validation

### Frontend

- **React 18** - UI framework
- **Redux Toolkit + RTK Query** - State management
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS + shadcn/ui** - Styling

## Configuration Details

### Chunking Strategy

- **Chunk Size**: 800 tokens (configurable)
- **Overlap**: 200 tokens for context continuity
- **Method**: Smart sentence-boundary aware chunking

### Retrieval Settings

- **Top-K Results**: 5 chunks
- **Similarity Threshold**: 0.5 (0-1 scale)
- **Embedding Model**: Gemini Embedding API (768 dimensions)

### Database Schema

**Documents Table**

- id, filename, original_filename, category
- content, file_type, created_at, updated_at

**Chunks Table**

- id, document_id, chunk_index
- content, start_char, end_char
- embedding (pgvector 768d), metadata, created_at

## Usage Workflow

1. **Upload Document**

   - POST `/api/documents/upload` with file
   - System automatically chunks and embeds the document

2. **Query the System**

   - POST `/api/queries/ask` with query text
   - System retrieves top-5 relevant chunks
   - Gemini generates answer with proper citations

3. **View Results**
   - Answer with source attributions
   - Similarity scores for each source
   - Preview of relevant text fragments

## Troubleshooting

### Import Errors

If you see import errors after syncing, the dependencies haven't been installed yet. Run:

```bash
uv sync
```

### Database Connection Issues

Ensure PostgreSQL is running and the connection string is correct in `.env`:

```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/rag_db
```

### Gemini API Key

Make sure your Google Gemini API key is valid and set in `.env`:

```
GOOGLE_API_KEY=your_actual_key_here
```

## Development Notes

### Project Requirements Analysis

This implementation fulfills the technical specification for a RAG system with:

✅ Document ingestion (PDF, TXT, MD, DOCX)
✅ Intelligent chunking (500-1000 tokens with overlap)
✅ Vector embeddings (Gemini Embeddings API)
✅ Semantic retrieval (pgvector similarity search)
✅ Answer synthesis (Gemini generation with context)
✅ Complete FastAPI backend
✅ React + Redux Toolkit frontend
✅ Proper error handling and validation
✅ Environment configuration management
✅ Source attribution

## Next Steps

1. Set up PostgreSQL database with pgvector
2. Obtain Google Gemini API key
3. Configure `.env` file with actual credentials
4. Run migrations
5. Start backend and frontend servers
6. Begin uploading documents and querying the system
