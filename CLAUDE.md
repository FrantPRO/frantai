# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**FrantAI** is a RAG-powered (Retrieval-Augmented Generation) chatbot that provides intelligent responses about Stan Frant's professional background, skills, experience, and projects. Built with FastAPI, React 19, PostgreSQL with pgvector, and local Ollama LLM inference.

### Key Technologies

- **Backend**: FastAPI (Python 3.12), PostgreSQL + pgvector, Ollama (Mistral 7B)
- **Frontend**: React 19, Vite, Tailwind CSS
- **Infrastructure**: Docker Compose, Nginx reverse proxy
- **ML/AI**: Sentence Transformers (multilingual-e5-base), Mistral 7B via Ollama

## Architecture

### RAG Flow
1. **Indexing**: Profile data → Text chunks → Embeddings → pgvector storage
2. **Query**: User question → Embedding → Vector search → Top K relevant chunks
3. **Generation**: Context + Question → Ollama LLM → Streamed response (SSE)

### Docker Services
- `backend` - FastAPI application with RAG service
- `frontend` - React 19 application
- `postgres` - PostgreSQL 16 with pgvector extension
- `ollama` - Local LLM inference (Mistral 7B)
- `nginx` - Reverse proxy with rate limiting

## Important Implementation Details

### Model Caching

**Critical**: The embedding model (`intfloat/multilingual-e5-base`) is cached in a Docker volume to prevent re-downloading on every container restart.

- **Volume**: `huggingface_cache:/app/.cache/huggingface`
- **Environment**: `HF_HOME=/app/.cache/huggingface`, `TRANSFORMERS_CACHE=/app/.cache/huggingface`
- **First Run**: Takes 5-10 minutes to download the model (~500MB)
- **Subsequent Runs**: Model loads from cache in seconds

Location: `docker-compose.yml:65,108` and `backend/Dockerfile:23-25`

### Database Schema

**Profile Tables** (source data):
- `profile_basics` - Basic info (name, title, bio, contacts)
- `work_experience` - Employment history
- `skills` - Technical skills with proficiency levels
- `projects` - Portfolio projects
- `education`, `languages`, `certifications`

**Knowledge Base**:
- `knowledge_chunks` - Text chunks with embeddings (vector column)
- Indexed from all profile tables
- Supports semantic search via pgvector

**Chat System**:
- `chat_sessions` - User chat sessions (tracked by IP hash)
- `chat_messages` - Message history with retrieved chunk references

### API Endpoints

**Chat** (`backend/app/api/v1/chat.py`):
- `POST /api/v1/chat/message` - SSE streaming chat responses
- Session management and rate limiting (25/min, 100/hour)

**Profile** (`backend/app/api/v1/profile.py`):
- `GET /api/v1/profile` - Complete profile
- Separate endpoints for each section

**Admin** (`backend/app/api/v1/admin.py`):
- `POST /api/v1/admin/reindex` - Rebuild knowledge base
- `PUT /api/v1/admin/profile` - Update profile sections

### Services

**RAG Service** (`backend/app/services/rag.py`):
- Orchestrates vector search + LLM generation
- Handles multilingual detection (EN/RU/DE)
- Streams responses via async generators

**Embedding Service** (`backend/app/services/embeddings.py`):
- Uses Sentence Transformers (E5-base multilingual)
- Singleton pattern for model caching
- **Important**: Model loads on first use, cached in volume

**LLM Service** (`backend/app/services/llm.py`):
- Interfaces with Ollama API
- Supports both streaming and non-streaming generation
- Configurable temperature, max tokens

**Indexing Service** (`backend/app/services/indexing.py`):
- Converts profile data to text chunks
- Generates embeddings for each chunk
- Stores in `knowledge_chunks` table

## Development Workflow

### Local Setup (without Docker)

1. **Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

2. **Frontend**:
```bash
cd frontend
npm install
npm run dev
```

3. **Ollama** (install separately):
```bash
ollama pull mistral:7b-instruct-q4_0
ollama serve
```

### Docker Setup (recommended)

```bash
# Start all services
docker-compose up -d

# First time: download Ollama model
docker-compose exec ollama ollama pull mistral:7b-instruct-q4_0

# Run migrations
docker-compose exec backend alembic upgrade head

# Reindex knowledge base
curl -X POST http://localhost:8000/api/v1/admin/reindex \
  -H "X-Admin-Token: dev-admin-token"
```

### Testing

```bash
# Backend unit tests
cd backend
pytest -m unit -v

# Backend integration tests
pytest -m integration -v

# Code quality
make lint
make mypy
make format
```

### Debugging

**Check container logs**:
```bash
docker-compose logs -f backend
docker-compose logs -f ollama
```

**Test embedding service**:
```bash
docker-compose exec backend python -c "
from app.services.embeddings import get_embedding_service
svc = get_embedding_service()
emb = svc.create_query_embedding('test')
print(f'Embedding dim: {len(emb)}')
"
```

**Test Ollama connection**:
```bash
docker-compose exec backend curl http://ollama:11434/api/tags
```

## Common Issues

### Chat Not Responding After Container Restart

**Cause**: Embedding model not cached, downloading from HuggingFace.

**Solution**: The `huggingface_cache` volume now persists the model. First download takes 5-10 minutes, subsequent restarts are fast.

**Check progress**:
```bash
docker-compose logs backend | grep -i "download\|loading"
```

### Rate Limit Errors

**Location**: `backend/app/core/rate_limit.py`

Default limits: 25/min, 100/hour per IP. Adjust in `.env`:
```
RATE_LIMIT_PER_MINUTE=25
RATE_LIMIT_PER_HOUR=100
```

### Vector Search Returns No Results

**Cause**: Knowledge base not indexed.

**Solution**:
```bash
curl -X POST http://localhost:8000/api/v1/admin/reindex \
  -H "X-Admin-Token: dev-admin-token"
```

## Code Style

- **Python**: PEP 8, enforced by Ruff
- **Type Hints**: Required for all functions
- **Async**: Use `async/await` for I/O operations
- **Imports**: Sorted, absolute imports preferred

## Project Structure Notes

- **Services** (`app/services/`) - Business logic, stateless
- **Models** (`app/models/`) - SQLAlchemy ORM models
- **Schemas** (`app/schemas/`) - Pydantic validation models
- **API** (`app/api/v1/`) - FastAPI route handlers
- **Core** (`app/core/`) - Configuration, prompts, utilities

## Useful Commands

```bash
# Rebuild backend after Dockerfile changes
docker-compose build backend

# Reset database (DESTRUCTIVE)
docker-compose down -v
docker-compose up -d postgres
docker-compose exec backend alembic upgrade head

# Check volume usage
docker volume ls
docker volume inspect frantai_huggingface_cache

# Shell into container
docker-compose exec backend bash
docker-compose exec postgres psql -U frantai

# Monitor resource usage
docker stats
```

