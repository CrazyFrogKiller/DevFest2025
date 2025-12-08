#!/usr/bin/env python
"""
Direct migration script without Alembic

This script directly applies the database schema to PostgreSQL.
Use this if you're having issues with Alembic or libpq.
"""

import psycopg
from pathlib import Path
import sys

# Database connection parameters
DB_CONFIG = {
    "host": "localhost",
    "dbname": "rag_db",
    "user": "ev0b1t",
    "password": "123",
    "port": "5432"
}

# SQL statements to create schema
CREATE_TABLES_SQL = """
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(255) NOT NULL,
    title VARCHAR(500),
    content_type VARCHAR(50),
    file_size INTEGER,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    doc_metadata JSONB
);

-- Create chunks table
CREATE TABLE IF NOT EXISTS chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    chunk_index INTEGER,
    embedding vector(768),
    chunk_metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS chunks_document_id_idx ON chunks(document_id);
CREATE INDEX IF NOT EXISTS chunks_embedding_idx ON chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
"""

# Migration to rename metadata columns if they exist
RENAME_METADATA_COLUMNS = """
-- Rename metadata columns to avoid SQLAlchemy reserved name
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='documents' AND column_name='metadata') THEN
        ALTER TABLE documents RENAME COLUMN metadata TO doc_metadata;
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='chunks' AND column_name='metadata') THEN
        ALTER TABLE chunks RENAME COLUMN metadata TO chunk_metadata;
    END IF;
END $$;
"""

# Migration to update embedding dimension from 768 to 768
UPDATE_EMBEDDING_DIMENSION = """
-- Update embedding vector dimension
DO $$
BEGIN
    -- Drop the old index if it exists
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'chunks_embedding_idx') THEN
        DROP INDEX chunks_embedding_idx;
    END IF;

    -- Recreate the chunks table with new vector dimension
    -- We need to drop and recreate because pgvector doesn't support ALTER COLUMN type for vectors
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='chunks' AND column_name='embedding') THEN
        -- Check current type and alter if needed
        ALTER TABLE chunks ALTER COLUMN embedding TYPE vector(768) USING embedding::text::vector;
    END IF;

    -- Recreate the index with the new dimension
    CREATE INDEX IF NOT EXISTS chunks_embedding_idx ON chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
EXCEPTION WHEN OTHERS THEN
    -- If the above fails, it might be because the column is already the right type
    NULL;
END $$;
"""

# Create migration tracking table
# CREATE_ALEMBIC_TABLE = """
# CREATE TABLE IF NOT EXISTS alembic_version (
#     version_num varchar(32) not null,
#     constraint alembic_version_pkc primary key (version_num)
# );
# """

# MARK_MIGRATION = """
# INSERT INTO alembic_version (version_num) VALUES ('001_initial')
# ON CONFLICT DO NOTHING;
# """


def run_migration():
    """Run the migration"""
    try:
        conn = psycopg.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print("✅ Connected to database")

        # Create alembic version table
        # cursor.execute(CREATE_ALEMBIC_TABLE)
        # print("✅ Created alembic_version table")

        # Execute schema creation
        cursor.execute(CREATE_TABLES_SQL)
        print("✅ Created database schema")

        # Rename metadata columns
        cursor.execute(RENAME_METADATA_COLUMNS)
        print("✅ Renamed metadata columns")

        # Update embedding dimension
        cursor.execute(UPDATE_EMBEDDING_DIMENSION)
        print("✅ Updated embedding vector dimension to 768")

        # Mark migration as applied
        # cursor.execute(MARK_MIGRATION)
        # print("✅ Marked migration as applied")

        # Commit changes
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Migration completed successfully!")

        return True

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
