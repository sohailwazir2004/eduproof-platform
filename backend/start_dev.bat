@echo off
REM EduProof Backend - Development Startup Script
REM This script starts the FastAPI backend server in development mode

echo =====================================
echo  EduProof Backend - Starting Server
echo =====================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Please create a .env file with required configuration.
    echo See .env.example or QUICK_START.md for details.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo Starting FastAPI server...
echo.
echo API Documentation: http://localhost:8000/api/v1/docs
echo Alternative Docs:  http://localhost:8000/api/v1/redoc
echo Health Check:      http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
