# FrantAI Deployment Guide

## Prerequisites

- Docker & Docker Compose installed
- Domain name (stan.frant.pro)
- SSL certificate (Let's Encrypt recommended)
- Hetzner server: 8 vCPU / 16 GB RAM / 160 GB SSD

## Initial Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/frantai.git
cd frantai
```

### 2. Configure Environment
```bash
cp .env.example .env
nano .env  # Edit with your values
```

Required variables:
- `DB_PASSWORD` - Secure PostgreSQL password
- `ENVIRONMENT=production`

### 3. Start Services
```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 4. Initialize Database
```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Verify pgvector
docker-compose exec postgres psql -U frantai -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

### 5. Download AI Models
```bash
./scripts/download-models.sh

# Verify
docker-compose exec ollama ollama list
```

### 6. Index Profile Data
```bash
# Via API (requires admin token)
curl -X POST http://localhost:8000/api/v1/admin/reindex \
  -H "X-Admin-Token: dev-admin-token"
```

## SSL Setup (Let's Encrypt)
```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d stan.frant.pro

# Certificates will be in /etc/letsencrypt/live/stan.frant.pro/
```

Update `nginx/nginx.conf` to enable HTTPS server block.

## Health Checks
```bash
# Backend
curl http://localhost:8000/api/v1/health

# Ollama
curl http://localhost:11434/api/tags

# Database
docker-compose exec postgres pg_isready -U frantai
```

## Monitoring
```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f ollama

# Resource usage
docker stats
```

## Backup
```bash
# Database backup
docker-compose exec postgres pg_dump -U frantai frantai > backup.sql

# Restore
docker-compose exec -T postgres psql -U frantai frantai < backup.sql
```

## Troubleshooting

### Backend won't start
- Check database connection: `docker-compose logs postgres`
- Verify migrations: `docker-compose exec backend alembic current`

### Ollama model not found
- Download model: `./scripts/download-models.sh`
- Check available models: `docker-compose exec ollama ollama list`

### Chat not responding
- Check Ollama is running: `docker-compose ps ollama`
- Verify model loaded: `docker-compose logs ollama`

## Updating
```bash
git pull origin main
./scripts/deploy.sh
```
