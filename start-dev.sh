#!/bin/bash

# Development startup script for AI Tutor
# This script starts both backend and frontend services

echo "🍁 Starting AI Tutor Development Environment..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ Backend .env file not found!${NC}"
    echo "Please copy backend/.env.example to backend/.env and add your API keys"
    exit 1
fi

# Check if frontend .env exists
if [ ! -f "packages/web/.env" ]; then
    echo -e "${YELLOW}⚠️  Frontend .env file not found. Creating with defaults...${NC}"
    echo "VITE_API_URL=http://localhost:8000" > packages/web/.env
fi

# Function to kill processes on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Set up trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Start backend
echo -e "\n${GREEN}Starting backend API server...${NC}"
cd backend
python -m uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to be ready..."
sleep 5

# Test backend health
curl -s http://localhost:8000/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backend is running at http://localhost:8000${NC}"
    echo -e "${GREEN}   API docs available at http://localhost:8000/docs${NC}"
else
    echo -e "${RED}❌ Backend failed to start. Check the logs above.${NC}"
    exit 1
fi

# Install frontend dependencies if needed
if [ ! -d "packages/web/node_modules" ]; then
    echo -e "\n${YELLOW}Installing frontend dependencies...${NC}"
    cd packages/web
    npm install
    cd ../..
fi

# Start frontend
echo -e "\n${GREEN}Starting frontend development server...${NC}"
cd packages/web
npm run dev &
FRONTEND_PID=$!
cd ../..

# Wait for frontend to start
sleep 5

echo -e "\n${GREEN}=============================================="
echo -e "🎉 AI Tutor is ready!"
echo -e "=============================================="
echo -e "Frontend: http://localhost:5173"
echo -e "Backend:  http://localhost:8000"
echo -e "API Docs: http://localhost:8000/docs${NC}"
echo -e "\nPress Ctrl+C to stop all services"

# Wait for processes
wait