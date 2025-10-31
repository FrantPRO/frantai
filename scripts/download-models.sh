#!/bin/bash
# Download Ollama models

set -e

echo "Downloading Mistral 7B model..."
docker-compose exec ollama ollama pull mistral:7b-instruct-q4_0

echo "Model downloaded successfully!"
echo "To verify: docker-compose exec ollama ollama list"
