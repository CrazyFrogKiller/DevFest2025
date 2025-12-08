#!/bin/bash
# Alembic Commands Reference
# RAG System Database Management

# ============================================
# CHECKING DATABASE STATUS
# ============================================

# Check database structure and status
uv run python verify_db.py

# Show current Alembic version
uv run alembic current

# Show migration history
uv run alembic history --indicate-current


# ============================================
# CREATING MIGRATIONS
# ============================================

# Create automatic migration (after model changes)
uv run alembic revision --autogenerate -m "Add new field to documents"

# Create manual migration
uv run alembic revision -m "Detailed description of changes"

# Example migrations
# uv run alembic revision --autogenerate -m "Add status field to chunks"
# uv run alembic revision --autogenerate -m "Create indexes"


# ============================================
# APPLYING MIGRATIONS
# ============================================

# Apply all pending migrations
uv run alembic upgrade head

# Apply specific migration
uv run alembic upgrade abc123def456

# Apply N migrations
uv run alembic upgrade +2


# ============================================
# REVERTING MIGRATIONS
# ============================================

# Revert one migration
uv run alembic downgrade -1

# Revert to specific version
uv run alembic downgrade abc123def456

# Revert all migrations
uv run alembic downgrade base


# ============================================
# ALTERNATIVE METHODS (if Alembic fails)
# ============================================

# Direct migration (when psycopg has issues)
uv run python migrate.py

# Verify database after migration
uv run python verify_db.py


# ============================================
# VIEWING MIGRATION FILES
# ============================================

# List migration files
ls alembic/versions/

# View specific migration
cat alembic/versions/001_initial.py


# ============================================
# DATABASE QUERIES
# ============================================

# Connect to database
psql -U victor -d rag_db -h localhost

# Common queries in psql:

# Show all tables
\dt

# Show documents table structure
\d documents

# Show chunks table structure
\d chunks

# Show indexes
\di

# Show extension info
SELECT * FROM pg_extension WHERE extname = 'vector';

# Check alembic version
SELECT * FROM alembic_version;


# ============================================
# COMMON WORKFLOWS
# ============================================

# WORKFLOW 1: Add new field to documents table
# 1. Edit app/models/document.py
# 2. Run: uv run alembic revision --autogenerate -m "Add new field"
# 3. Review alembic/versions/xxxxx_add_new_field.py
# 4. Run: uv run alembic upgrade head
# 5. Test: uv run python verify_db.py

# WORKFLOW 2: Fix database problems
# 1. Check status: uv run python verify_db.py
# 2. If broken: uv run python migrate.py
# 3. Verify again: uv run python verify_db.py

# WORKFLOW 3: Development and testing
# 1. Make model changes
# 2. Create migration: uv run alembic revision --autogenerate -m "description"
# 3. Apply: uv run alembic upgrade head
# 4. Test with: uv run python -m pytest
# 5. Commit migration files

# WORKFLOW 4: Production deployment
# 1. Test migrations locally first
# 2. Backup production database
# 3. Run: uv run alembic upgrade head
# 4. Verify: uv run python verify_db.py
# 5. Test application


# ============================================
# TROUBLESHOOTING
# ============================================

# ERROR: "no pq wrapper available"
# SOLUTION: Use migrate.py instead
# uv run python migrate.py

# ERROR: "relation does not exist"
# SOLUTION: Check if migration was applied
# Run: uv run python verify_db.py

# ERROR: "migration already exists"
# SOLUTION: Check alembic/versions/ and clean up if needed

# ERROR: "cannot execute in transaction"
# SOLUTION: Check if other migrations are running
# Run: uv run alembic current

# If stuck
# 1. Check database directly: psql -U victor -d rag_db
# 2. Check alembic_version: SELECT * FROM alembic_version;
# 3. Use migrate.py to recover: uv run python migrate.py
