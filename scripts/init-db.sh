#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS vector;

    -- Verify extension
    SELECT * FROM pg_extension WHERE extname = 'vector';
EOSQL

echo "pgvector extension installed successfully"
