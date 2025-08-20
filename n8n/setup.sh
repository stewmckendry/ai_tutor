#!/bin/bash

# n8n Setup Script for Maple AI Tutor Content Pipeline
# =====================================================

echo "🍁 Setting up n8n for Maple AI Tutor Content Pipeline..."

# Create necessary directories
echo "Creating data directories..."
mkdir -p n8n_data workflows

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Start n8n with Docker Compose
echo "Starting n8n container..."
docker-compose up -d

# Wait for n8n to be ready
echo "Waiting for n8n to start..."
sleep 10

# Check if n8n is running
if [ "$(docker ps -q -f name=n8n_maple_content_pipeline)" ]; then
    echo "✅ n8n is running successfully!"
    echo ""
    echo "📋 Access Details:"
    echo "==================="
    echo "URL: http://localhost:5678"
    echo "Username: admin"
    echo "Password: maple_tutor_2024"
    echo ""
    echo "📝 Next Steps:"
    echo "1. Open http://localhost:5678 in your browser"
    echo "2. Log in with the credentials above"
    echo "3. Import the workflow from workflows/weather_to_education_poc.json"
    echo "4. Configure credentials (OpenAI and Airtable)"
    echo ""
    echo "🛑 To stop n8n: docker-compose down"
    echo "📊 To view logs: docker-compose logs -f"
else
    echo "❌ Failed to start n8n. Check docker-compose logs for details."
    docker-compose logs
    exit 1
fi