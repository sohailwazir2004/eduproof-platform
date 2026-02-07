#!/bin/bash
# EduProof Backend - Development Startup Script
# This script starts the FastAPI backend server in development mode

echo "====================================="
echo " EduProof Backend - Starting Server"
echo "====================================="
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "[ERROR] .env file not found!"
    echo "Please create a .env file with required configuration."
    echo "See .env.example or QUICK_START.md for details."
    echo ""
    exit 1
fi

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Starting FastAPI server..."
echo ""
echo "API Documentation: http://localhost:8000/api/v1/docs"
echo "Alternative Docs:  http://localhost:8000/api/v1/redoc"
echo "Health Check:      http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
