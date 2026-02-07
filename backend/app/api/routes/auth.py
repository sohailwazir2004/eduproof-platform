# auth.py - Authentication Routes
#
# Handles login, registration, token refresh, and password operations.

"""
Authentication Endpoints

POST /auth/login          - User login, returns JWT
POST /auth/register       - New user registration
POST /auth/refresh        - Refresh access token
POST /auth/forgot-password - Request password reset
POST /auth/reset-password  - Reset password with token
POST /auth/logout         - Logout (invalidate token)
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordChangeRequest
)
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with role selection"
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.

    - **email**: Valid email address (must be unique)
    - **password**: Strong password (min 8 chars, uppercase, lowercase, digit)
    - **first_name**: First name
    - **last_name**: Last name
    - **role**: User role (student, teacher, parent, principal)
    - **phone**: Optional phone number
    """
    auth_service = AuthService(db)
    user = await auth_service.register_user(user_data)
    return UserResponse.from_orm(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User login",
    description="Authenticate user and return JWT tokens"
)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.

    Returns access token and refresh token for authenticated requests.

    - **email**: User email address
    - **password**: User password
    """
    auth_service = AuthService(db)

    # Authenticate user
    user = await auth_service.authenticate_user(
        credentials.email,
        credentials.password
    )

    # Generate tokens
    return auth_service.generate_tokens(user)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Get a new access token using refresh token"
)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token.

    Provide a valid refresh token to get a new access token.

    - **refresh_token**: Valid refresh token
    """
    auth_service = AuthService(db)
    return await auth_service.refresh_access_token(request.refresh_token)


@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Change password",
    description="Change password for authenticated user"
)
async def change_password(
    request: PasswordChangeRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Change password for authenticated user.

    - **current_password**: Current password for verification
    - **new_password**: New password (must be different)
    - **confirm_password**: Password confirmation
    """
    auth_service = AuthService(db)
    await auth_service.change_password(
        user_id,
        request.current_password,
        request.new_password
    )
    return {"message": "Password changed successfully"}


@router.post(
    "/forgot-password",
    status_code=status.HTTP_200_OK,
    summary="Request password reset",
    description="Request password reset link via email"
)
async def forgot_password(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Request password reset.

    Sends a password reset token to the user's email.
    In production, this token should be sent via email.

    - **email**: User email address
    """
    auth_service = AuthService(db)
    reset_token = await auth_service.request_password_reset(request.email)

    # In production, send email instead of returning token
    return {
        "message": "If this email exists, a reset link has been sent",
        "reset_token": reset_token  # Remove this in production
    }


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
    summary="Reset password",
    description="Reset password using reset token"
)
async def reset_password(
    request: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    """
    Reset password using reset token.

    - **token**: Reset token from email
    - **new_password**: New password
    - **confirm_password**: Password confirmation
    """
    auth_service = AuthService(db)
    await auth_service.reset_password(request.token, request.new_password)
    return {"message": "Password reset successful"}


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout",
    description="Logout user (client should discard tokens)"
)
async def logout(
    user_id: str = Depends(get_current_user_id)
):
    """
    Logout user.

    In a stateless JWT system, logout is handled client-side by discarding tokens.
    For token blacklisting, implement a token revocation mechanism.
    """
    # In production, could add token to blacklist/revocation list
    return {"message": "Logged out successfully"}
