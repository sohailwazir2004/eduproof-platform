# backend/app/main.py - FastAPI Application Entry Point
#
# Production-ready version for Railway deployment

from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.database import init_db, close_db
from app.utils.exceptions import AppException

# Import routers
from app.api.routes import auth, users, homework, submissions, textbooks, analytics, classes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup
    print(f"Starting {settings.app_name}...")
    await init_db()  # Make sure init_db uses DATABASE_URL from env
    print("Database initialized successfully")
    yield
    # Shutdown
    print(f"Shutting down {settings.app_name}...")
    await close_db()
    print("Database connections closed")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="AI-powered school homework management platform",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
    docs_url=f"{settings.api_v1_prefix}/docs",
    redoc_url=f"{settings.api_v1_prefix}/redoc",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
)


# Configure CORS - restrict origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins or ["*"],  # Replace "*" with actual frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": exc.errors()
            }
        }
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "A database error occurred",
                "details": str(exc) if settings.debug else None
            }
        }
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.environment
    }


# Include routers
app.include_router(auth.router, prefix=f"{settings.api_v1_prefix}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.api_v1_prefix}/users", tags=["Users"])
app.include_router(homework.router, prefix=f"{settings.api_v1_prefix}/homework", tags=["Homework"])
app.include_router(submissions.router, prefix=f"{settings.api_v1_prefix}/submissions", tags=["Submissions"])
app.include_router(textbooks.router, prefix=f"{settings.api_v1_prefix}/textbooks", tags=["Textbooks"])
app.include_router(classes.router, prefix=f"{settings.api_v1_prefix}/classes", tags=["Classes"])
app.include_router(analytics.router, prefix=f"{settings.api_v1_prefix}/analytics", tags=["Analytics"])


# Production-ready Uvicorn start
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))  # Use Railway port
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Always False in production
    )
