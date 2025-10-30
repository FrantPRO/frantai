# FrantAI Backend

FastAPI backend for FrantAI project with RAG, Ollama, and PostgreSQL support.

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example configuration
cp .env.example .env

# Edit .env if needed
nano .env
```

### 3. Start Server

```bash
# Development mode with hot reload
uvicorn app.main:app --reload

# Or using python
python -m app.main
```

Server will be available at http://localhost:8000

## Available Endpoints

- `GET /` - Root endpoint
- `GET /api/v1/health` - Health check
- `GET /docs` - Swagger UI (interactive documentation)
- `GET /redoc` - ReDoc (alternative documentation)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration
│   └── database.py      # SQLAlchemy setup
├── requirements.txt     # Python dependencies
├── .env.example         # Example configuration
├── .env                 # Local configuration (don't commit!)
├── Dockerfile           # Docker image
└── README.md           # This file
```

## Testing

### Unit Tests (without DB)

```bash
# Run all unit tests
pytest -m unit -v

# Run model tests
pytest tests/test_models.py -v
```

### Integration Tests (require PostgreSQL)

```bash
# Run integration tests
pytest -m integration -v

# Run database connection tests
pytest tests/test_database.py -v
```

### All Tests

```bash
# Run all tests
pytest -v

# With code coverage
pytest --cov=app --cov-report=html
```

**See [tests/README.md](tests/README.md) for detailed testing documentation.**

### API Verification

```bash
# Check health endpoint
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status": "healthy", "version": "1.0.0", "environment": "development"}
```

## Docker

```bash
# Build image
docker build -t frantai-backend .

# Run container
docker run -p 8000:8000 --env-file .env frantai-backend
```

## Development

When adding new dependencies:

```bash
pip install <package>
pip freeze > requirements.txt
```

## Dependencies

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** - ORM for database
- **AsyncPG** - Async PostgreSQL driver
- **pgvector** - Vector operations in PostgreSQL
- **Sentence Transformers** - Embedding models
- **httpx** - HTTP client for Ollama
- **slowapi** - Rate limiting
