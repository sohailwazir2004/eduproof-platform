# auth.py - Authentication Pydantic Schemas
#
# Schemas for login, registration, and token operations.

"""
Authentication Schemas

- LoginRequest: Email and password
- TokenResponse: Access token and token type
- TokenPayload: JWT payload structure
- PasswordReset: Password reset request
- PasswordChange: Password change request
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from app.core.security import UserRole


class LoginRequest(BaseModel):
    """Login credentials schema."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "teacher@school.com",
                "password": "password123"
            }
        }


class TokenResponse(BaseModel):
    """Token response after successful authentication."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user_id: str = Field(..., description="User ID")
    role: UserRole = Field(..., description="User role")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "role": "teacher"
            }
        }


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str = Field(..., description="Valid refresh token")


class TokenPayload(BaseModel):
    """JWT token payload structure."""
    sub: str = Field(..., description="Subject (user ID)")
    role: str = Field(..., description="User role")
    exp: int = Field(..., description="Expiration timestamp")
    iat: int = Field(..., description="Issued at timestamp")
    type: str = Field(..., description="Token type (access/refresh)")


class PasswordResetRequest(BaseModel):
    """Password reset request schema."""
    email: EmailStr = Field(..., description="Email address for password reset")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@school.com"
            }
        }


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema."""
    token: str = Field(..., description="Reset token from email")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., min_length=8, description="Password confirmation")

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "token": "reset-token-here",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123"
            }
        }


class PasswordChangeRequest(BaseModel):
    """Password change request schema (authenticated user)."""
    current_password: str = Field(..., min_length=6, description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., min_length=8, description="Password confirmation")

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('new_password')
    def new_password_different(cls, v, values):
        """Validate that new password is different from current."""
        if 'current_password' in values and v == values['current_password']:
            raise ValueError('New password must be different from current password')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "oldpassword123",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123"
            }
        }
