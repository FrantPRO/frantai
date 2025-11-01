# FrantAI

**Intelligent AI Assistant for Stan Frant's Professional Portfolio**

FrantAI is a RAG-powered (Retrieval-Augmented Generation) chatbot that provides intelligent responses about Stan Frant's professional background, skills, experience, and projects. Built with modern web technologies and local LLM inference.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120-green.svg)]
(https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61dafb.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Mistral_7B-black.svg)](https://ollama.ai/)

## Features

- **Intelligent Chat**: Natural language conversations about Stan's professional profile
- **Multilingual Support**: Responds in English, Russian, and German
- **RAG Architecture**: Vector-based semantic search with LLM generation
- **SSE Streaming**: Real-time streaming responses for better UX
- **Profile Management**: Admin panel for updating profile information
- **Session Management**: Track conversation history and context
- **Rate Limiting**: Built-in rate limiting for API protection
- **Docker Deployment**: Production-ready containerized setup

## Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **PostgreSQL** - Primary database with pgvector extension
- **pgvector** - Vector similarity search for embeddings
- **Ollama** - Local LLM inference (Mistral 7B)
- **Sentence Transformers** - Multilingual embeddings (E5-base)
- **SQLAlchemy** - Async ORM with PostgreSQL
- **Alembic** - Database migrations
- **LangDetect** - Automatic language detection

### Frontend
- **React 19** - Latest React with modern features
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icon library

### Infrastructure
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy with rate limiting
- **GitHub Actions** - CI/CD pipeline

## Architecture

```
┌─────────────────┐
│   React 19      │  Frontend (Vite + Tailwind)
│   Frontend      │
└────────┬────────┘
         │
         │ HTTP/SSE
         │
┌────────▼────────┐
│     Nginx       │  Reverse Proxy + Rate Limiting
└────────┬────────┘
         │
         │
┌────────▼────────┐
│  FastAPI        │  Backend API + RAG Service
│  Backend        │
└────┬───────┬────┘
     │       │
     │       │
┌────▼────┐ ┌▼───────────┐
│PostgreSQL│ │   Ollama   │
│+pgvector │ │ (Mistral7B)│
└──────────┘ └────────────┘
```

### RAG Flow

1. **Indexing**: Profile data → Text chunks → Embeddings → pgvector
2. **Query**: User question → Embedding → Vector search → Top K chunks
3. **Generation**: Context + Prompt → Ollama LLM → Streamed response

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/frantai.git
cd frantai
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Start services:
```bash
docker-compose up -d
```

4. Download Ollama model:
```bash
./scripts/download-models.sh
```

5. Run database migrations:
```bash
docker-compose exec backend alembic upgrade head
```

6. Index profile data:
```bash
curl -X POST http://localhost:8000/api/v1/admin/reindex \
  -H "X-Admin-Token: dev-admin-token"
```

7. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Development

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed development setup and guidelines.

### Local Development Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Backend unit tests
cd backend
pytest -m unit -v

# Backend integration tests
pytest -m integration -v

# Frontend linting
cd frontend
npm run lint
```

### Code Quality

```bash
# Backend linting
make lint

# Auto-fix issues
make ruff-fix

# Type checking
make mypy

# Format code
make format
```

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment guide.

### Production Deployment

```bash
# Build and start production services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Or use the deployment script
./scripts/deploy.sh
```

## Project Structure

```
frantai/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   ├── deps.py        # Dependencies
│   │   │   └── v1/            # API v1 endpoints
│   │   │       ├── admin.py   # Admin endpoints
│   │   │       ├── chat.py    # Chat endpoints
│   │   │       └── profile.py # Profile endpoints
│   │   ├── core/              # Core functionality
│   │   │   ├── config.py      # Configuration
│   │   │   └── prompts.py     # LLM prompts (EN/RU/DE)
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── chat.py        # Chat sessions & messages
│   │   │   ├── knowledge.py   # Knowledge chunks
│   │   │   └── profile.py     # Profile tables
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   │   ├── embeddings.py  # Embedding generation
│   │   │   ├── indexing.py    # Profile indexing
│   │   │   ├── llm.py         # Ollama service
│   │   │   └── rag.py         # RAG orchestration
│   │   ├── database.py        # DB connection
│   │   └── main.py            # FastAPI app
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Unit & integration tests
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ruff.toml              # Linting config
│
├── frontend/                   # React 19 frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── ChatWindow.jsx # Chat interface
│   │   │   ├── ProfilePage.jsx# Profile display
│   │   │   └── ThemeToggle.jsx# Dark mode toggle
│   │   ├── App.jsx            # Main app
│   │   └── main.jsx           # Entry point
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
│
├── nginx/
│   └── nginx.conf             # Nginx configuration
│
├── scripts/
│   ├── init-db.sh             # PostgreSQL init
│   ├── download-models.sh     # Download Ollama models
│   └── deploy.sh              # Production deployment
│
├── docs/
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── DEVELOPMENT.md         # Development guide
│
├── .github/
│   └── workflows/
│       └── deploy.yml         # CI/CD pipeline
│
├── docker-compose.yml         # Development setup
├── docker-compose.prod.yml    # Production overrides
├── .env.example               # Environment template
├── .dockerignore
└── README.md
```

## API Documentation

### Endpoints

**Profile:**
- `GET /api/v1/profile` - Get complete profile
- `GET /api/v1/profile/basics` - Get basic information
- `GET /api/v1/profile/skills` - Get skills
- `GET /api/v1/profile/experience` - Get work experience
- `GET /api/v1/profile/projects` - Get projects
- `GET /api/v1/profile/education` - Get education
- `GET /api/v1/profile/languages` - Get languages
- `GET /api/v1/profile/certifications` - Get certifications

**Chat:**
- `POST /api/v1/chat/message` - Send message (SSE streaming)
- `GET /api/v1/chat/sessions` - List chat sessions
- `GET /api/v1/chat/sessions/{id}` - Get session details
- `DELETE /api/v1/chat/sessions/{id}` - Delete session

**Admin:**
- `PUT /api/v1/admin/profile` - Update profile section
- `DELETE /api/v1/admin/profile/section/{table}/{id}` - Delete item
- `POST /api/v1/admin/reindex` - Reindex knowledge base

**Health:**
- `GET /api/v1/health` - Health check

Interactive API documentation: http://localhost:8000/docs

## Environment Variables

```bash
# Database
DB_PASSWORD=your_secure_password

# Environment
ENVIRONMENT=development

# Ollama
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=mistral:7b-instruct-q4_0

# Embeddings
EMBEDDING_MODEL=intfloat/multilingual-e5-base

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=25
RATE_LIMIT_PER_HOUR=100
RATE_LIMIT_PER_DAY=500
```

## Features in Detail

### RAG System

The RAG (Retrieval-Augmented Generation) system provides accurate answers by:

1. **Semantic Search**: Uses pgvector for fast similarity search
2. **Context-Aware**: Retrieves relevant profile chunks for each query
3. **Multilingual**: Supports English, Russian, and German
4. **Streaming**: Real-time response generation via SSE

### Profile Management

- Complete CRUD operations for all profile sections
- Automatic knowledge base reindexing
- Structured data storage in PostgreSQL
- RESTful API for profile access

### Chat Experience

- Streaming responses for better UX
- Session management with history
- Rate limiting for abuse prevention
- Automatic language detection
- Dark mode support

## Performance

- **Response Time**: < 500ms for vector search
- **LLM Generation**: ~2-3s for 200 token response (Mistral 7B)
- **Embedding**: ~100ms per query
- **Rate Limits**: 25 req/min per IP

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run linters and tests
5. Submit a pull request

## License

This project is private and proprietary.

## Author

**Stan Frant**
- Backend Developer specializing in Python, Go, and modern web technologies
- Portfolio: https://stan.frant.pro

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Ollama](https://ollama.ai/) and [Mistral AI](https://mistral.ai/)
- Vector search by [pgvector](https://github.com/pgvector/pgvector)
- Frontend with [React 19](https://react.dev/)

---

Built with by Stan Frant | Generated with [Claude Code](https://claude.com/claude-code)
