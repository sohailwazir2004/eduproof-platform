# config.py - Application Configuration
#
# Manages environment variables and application settings
# using Pydantic Settings for type-safe configuration.

import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    All settings are type-validated using Pydantic.
    """

    # Application
    app_name: str = "EduProof"
    debug: bool = False
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/eduproof"

    # JWT Authentication
    secret_key: str = "your-secret-key-here-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # AWS S3 (File Storage)
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    s3_bucket_name: str = "eduproof-files"

    # Cloudinary (Alternative Storage)
    cloudinary_cloud_name: Optional[str] = None
    cloudinary_api_key: Optional[str] = None
    cloudinary_api_secret: Optional[str] = None

    # Firebase (Notifications)
    firebase_project_id: Optional[str] = None
    firebase_credentials_path: Optional[str] = None

    # AI Service
    ai_service_url: str = "http://localhost:8001"
    openai_api_key: Optional[str] = None

    # Email (SMTP)
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None

    # CORS
    # Add production frontend URLs here
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    @property
    def all_cors_origins(self) -> list[str]:
        """Get all CORS origins including environment variable"""
        origins = self.cors_origins.copy()
        frontend_url = os.getenv("FRONTEND_URL")
        if frontend_url and frontend_url not in origins:
            origins.append(frontend_url)
        return origins

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Returns cached settings instance.
    Uses lru_cache to avoid reading .env file on every request.
    """
    return Settings()


# Global settings instance
settings = get_settings()
