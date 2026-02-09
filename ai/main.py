# main.py - AI Service Entry Point
#
# FastAPI microservice for AI operations.

"""
EduProof AI Service

Endpoints:
- POST /ocr/extract - Extract text from image
- POST /analysis/relevance - Check homework relevance
- POST /analysis/grade - AI-assisted grading
- POST /summarize - Generate submission summary
- POST /textbook/index - Index textbook content

Usage:
    uvicorn main:app --host 0.0.0.0 --port 8001
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import AI_SERVICE_PORT, LOG_LEVEL
import os

# Create FastAPI app
app = FastAPI(
    title="EduProof AI Service",
    description="AI microservice for OCR, homework analysis, and textbook processing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS - allow backend to communicate
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[BACKEND_URL, "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "EduProof AI Service",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service info"""
    return {
        "service": "EduProof AI Service",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "ocr": "/ocr/* (TODO)",
            "analysis": "/analysis/* (TODO)",
            "summarize": "/summarize (TODO)",
            "textbook": "/textbook/* (TODO)"
        }
    }

# TODO: Include routers when AI modules are fully implemented
# from ocr.routes import router as ocr_router
# from homework_analysis.routes import router as analysis_router
# from summarization.routes import router as summary_router
# from textbook_parser.routes import router as textbook_router
#
# app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
# app.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])
# app.include_router(summary_router, prefix="/summarize", tags=["Summary"])
# app.include_router(textbook_router, prefix="/textbook", tags=["Textbook"])

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", AI_SERVICE_PORT))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level=LOG_LEVEL.lower()
    )
