#!/bin/bash
# Deployment script for production

set -e

echo "🚀 Starting FrantAI deployment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Copy .env.example to .env and configure it."
    exit 1
fi

# Pull latest code
echo "📥 Pulling latest code..."
git pull origin main

# Build images
echo "🏗️  Building Docker images..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Run database migrations
echo "📊 Running database migrations..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml run --rm backend alembic upgrade head

# Start services
echo "🎬 Starting services..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Download Ollama models (if needed)
echo "📦 Checking Ollama models..."
docker-compose exec ollama ollama list | grep mistral || ./scripts/download-models.sh

# Health check
echo "🏥 Running health checks..."
curl -f http://localhost:8000/api/v1/health || echo "⚠️  Backend health check failed"

echo "✅ Deployment complete!"
echo "🌐 Access the application at: https://stan.frant.pro"
