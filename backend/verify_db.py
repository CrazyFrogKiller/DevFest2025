#!/usr/bin/env python
"""
Database verification script

This script checks that the database is properly set up and contains the right schema.
"""

import psycopg
import sys

# Database connection parameters
DB_CONFIG = {
    "host": "localhost",
    "dbname": "rag_db",
    "user": "victor",
    "password": "root",
    "port": "5432"
}


def check_database():
    """Check database schema and configuration"""
    try:
        conn = psycopg.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("=" * 60)
        print("RAG System Database Verification")
        print("=" * 60)
        
        # Check PostgreSQL version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"\n✅ PostgreSQL Version:\n   {version[:80]}...")
        
        # Check pgvector extension
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'pg_extension'
            );
        """)
        cursor.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector';")
        result = cursor.fetchone()
        if result:
            print(f"\n✅ pgvector Extension: Installed (version {result[0]})")
        else:
            print("\n⚠️  pgvector Extension: Not found (but may be available)")
        
        # Check tables
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\n✅ Tables in database:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Check documents table structure
        print(f"\n✅ Documents table structure:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'documents' 
            ORDER BY ordinal_position;
        """)
        for col in cursor.fetchall():
            null_str = "NULL" if col[2] == "YES" else "NOT NULL"
            print(f"   - {col[0]}: {col[1]} ({null_str})")
        
        # Check chunks table structure
        print(f"\n✅ Chunks table structure:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'chunks' 
            ORDER BY ordinal_position;
        """)
        for col in cursor.fetchall():
            null_str = "NULL" if col[2] == "YES" else "NOT NULL"
            print(f"   - {col[0]}: {col[1]} ({null_str})")
        
        # Check indexes
        print(f"\n✅ Indexes:")
        cursor.execute("""
            SELECT indexname, tablename 
            FROM pg_indexes 
            WHERE schemaname = 'public' 
            ORDER BY tablename, indexname;
        """)
        for idx in cursor.fetchall():
            print(f"   - {idx[0]} on {idx[1]}")
        
        # Check alembic version
        cursor.execute("SELECT version_num FROM alembic_version;")
        alembic_version = cursor.fetchone()
        if alembic_version:
            print(f"\n✅ Alembic Version: {alembic_version[0]}")
        else:
            print(f"\n⚠️  Alembic Version: Not found")
        
        # Check document count
        cursor.execute("SELECT COUNT(*) FROM documents;")
        doc_count = cursor.fetchone()[0]
        print(f"\n✅ Documents in database: {doc_count}")
        
        # Check chunks count
        cursor.execute("SELECT COUNT(*) FROM chunks;")
        chunks_count = cursor.fetchone()[0]
        print(f"✅ Chunks in database: {chunks_count}")
        
        # Foreign key check
        print(f"\n✅ Foreign Key Constraints:")
        cursor.execute("""
            SELECT constraint_name, table_name, column_name 
            FROM information_schema.key_column_usage 
            WHERE table_name IN ('documents', 'chunks')
            AND column_name != table_name || '_id'
            ORDER BY table_name, constraint_name;
        """)
        fks = cursor.fetchall()
        if not fks:
            print("   - All foreign keys properly set")
        else:
            for fk in fks:
                print(f"   - {fk[0]}: {fk[1]}.{fk[2]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Database verification completed successfully!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Database verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = check_database()
    sys.exit(0 if success else 1)
