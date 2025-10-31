# FrantAI Development Guide

## Local Development Setup

### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 16 (or use Docker)

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with local values

# Start PostgreSQL (Docker)
docker-compose up postgres -d

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

Backend available at: http://localhost:8000

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend available at: http://localhost:3000

### Ollama Setup
```bash
# Start Ollama
docker-compose up ollama -d

# Download model
docker-compose exec ollama ollama pull mistral:7b-instruct-q4_0
```

## Testing

### Backend Tests
```bash
cd backend

# Unit tests only
pytest -m unit -v

# Integration tests (requires database)
pytest -m integration -v

# All tests
pytest -v

# With coverage
pytest --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend

# Linting
npm run lint

# Build
npm run build
```

## Code Quality

### Backend
```bash
cd backend

# Run all linters
make lint

# Auto-fix issues
make ruff-fix

# Type checking
make mypy

# Format code
make format
```

### Frontend
```bash
cd frontend

# Lint
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix
```

## Database

### Create Migration
```bash
cd backend
alembic revision --autogenerate -m "description"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback
```bash
alembic downgrade -1
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

See main README.md for complete structure.

## Common Tasks

### Add New Profile Field

1. Update model in `backend/app/models/profile.py`
2. Create migration: `alembic revision --autogenerate`
3. Update schema in `backend/app/schemas/profile.py`
4. Update frontend component

### Add New Chat Feature

1. Update `backend/app/services/rag.py`
2. Modify chat endpoint in `backend/app/api/v1/chat.py`
3. Update frontend `ChatWindow.jsx`

## Debugging

### Backend
- Use `import pdb; pdb.set_trace()` for breakpoints
- Check logs: `docker-compose logs -f backend`

### Frontend
- Browser DevTools
- React DevTools extension

### Database
```bash
docker-compose exec postgres psql -U frantai
```
