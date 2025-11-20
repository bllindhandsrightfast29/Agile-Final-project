#!/bin/bash

# Cyber Defense Visualization System - Startup Script

set -e

echo "🎮 Cyber Defense Visualization System"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is running${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}   Please edit .env and add your ANTHROPIC_API_KEY if you want enhanced narration.${NC}"
fi

# Check if running in cloud or local
MODE=${1:-docker}

if [ "$MODE" == "docker" ]; then
    echo ""
    echo "🐳 Starting with Docker Compose..."
    echo ""

    # Build and start containers
    docker-compose up --build -d

    echo ""
    echo -e "${GREEN}✅ System started!${NC}"
    echo ""
    echo "📍 Access points:"
    echo "   - Frontend: http://localhost:3000"
    echo "   - Backend API: http://localhost:8000"
    echo "   - API Docs: http://localhost:8000/docs"
    echo ""
    echo "📊 View logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 Stop system:"
    echo "   docker-compose down"
    echo ""

elif [ "$MODE" == "local" ]; then
    echo ""
    echo "💻 Starting in local development mode..."
    echo ""

    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is not installed${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ Python 3 found${NC}"

    # Install Python dependencies
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt

    # Start backend in background
    echo "🚀 Starting backend server..."
    cd backend
    python main.py &
    BACKEND_PID=$!
    cd ..

    echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"

    # Start simple HTTP server for frontend
    echo "🚀 Starting frontend server..."
    cd frontend
    python -m http.server 3000 &
    FRONTEND_PID=$!
    cd ..

    echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
    echo ""
    echo "📍 Access points:"
    echo "   - Frontend: http://localhost:3000"
    echo "   - Backend API: http://localhost:8000"
    echo ""
    echo "🛑 Stop system:"
    echo "   kill $BACKEND_PID $FRONTEND_PID"
    echo ""

    # Save PIDs for stopping
    echo "$BACKEND_PID $FRONTEND_PID" > .pids

else
    echo "Usage: ./start.sh [docker|local]"
    echo "  docker - Run with Docker Compose (recommended)"
    echo "  local  - Run locally without Docker"
    exit 1
fi

echo "🎬 Ready to visualize cyber attacks!"
echo "   Open http://localhost:3000 in your browser"
echo ""
