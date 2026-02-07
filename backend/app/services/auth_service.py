# auth_service.py - Authentication Service
#
# Business logic for authentication operations.

"""
Auth Service

Methods:
- authenticate_user(email, password) -> User
- create_user(user_data) -> User
- create_access_token(user) -> str
- verify_token(token) -> TokenPayload
- request_password_reset(email) -> None
- reset_password(token, new_password) -> None
"""

from typing import Optional
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    UserRole
)
from app.core.config import settings
from app.schemas.auth import TokenResponse
from app.schemas.user import UserCreate
from app.utils.exceptions import AppException


class AuthService:
    """
    Service for handling authentication operations.
    Coordinates between repositories and implements business logic.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def authenticate_user(
        self,
        email: str,
        password: str
    ) -> User:
        """
        Authenticate user with email and password.

        Args:
            email: User email
            password: Plain text password

        Returns:
            Authenticated User object

        Raises:
            AppException: If authentication fails
        """
        # Get user by email
        user = await self.user_repo.get_by_email(email, load_relationships=True)

        if not user:
            raise AppException(
                status_code=401,
                error_code="INVALID_CREDENTIALS",
                message="Invalid email or password"
            )

        # Verify password
        if not verify_password(password, user.hashed_password):
            raise AppException(
                status_code=401,
                error_code="INVALID_CREDENTIALS",
                message="Invalid email or password"
            )

        # Check if user is active
        if not user.is_active:
            raise AppException(
                status_code=403,
                error_code="ACCOUNT_INACTIVE",
                message="Your account has been deactivated"
            )

        return user

    async def register_user(
        self,
        user_data: UserCreate
    ) -> User:
        """
        Register a new user.

        Args:
            user_data: User creation schema

        Returns:
            Created User object

        Raises:
            AppException: If email already exists
        """
        # Check if email already exists
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise AppException(
                status_code=409,
                error_code="EMAIL_EXISTS",
                message="An account with this email already exists"
            )

        # Hash password
        hashed_password = hash_password(user_data.password)

        # Create user data dict
        user_dict = {
            "email": user_data.email,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "phone": user_data.phone,
            "hashed_password": hashed_password,
            "role": user_data.role,
            "is_active": True,
            "is_verified": False
        }

        # Create user
        user = await self.user_repo.create(user_dict)
        await self.db.commit()

        return user

    def generate_tokens(self, user: User) -> TokenResponse:
        """
        Generate access and refresh tokens for user.

        Args:
            user: User object

        Returns:
            TokenResponse with access and refresh tokens
        """
        # Create access token
        access_token = create_access_token(
            subject=str(user.id),
            role=user.role
        )

        # Create refresh token
        refresh_token = create_refresh_token(
            subject=str(user.id)
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            user_id=str(user.id),
            role=user.role
        )

    async def refresh_access_token(
        self,
        refresh_token: str
    ) -> TokenResponse:
        """
        Refresh access token using refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            TokenResponse with new access token

        Raises:
            AppException: If refresh token is invalid
        """
        try:
            # Decode refresh token
            payload = decode_token(refresh_token)

            # Verify token type
            if payload.get("type") != "refresh":
                raise AppException(
                    status_code=401,
                    error_code="INVALID_TOKEN_TYPE",
                    message="Invalid token type"
                )

            # Get user ID
            user_id = payload.get("sub")
            if not user_id:
                raise AppException(
                    status_code=401,
                    error_code="INVALID_TOKEN",
                    message="Invalid token payload"
                )

            # Get user from database
            from uuid import UUID
            user = await self.user_repo.get_by_id(UUID(user_id))

            if not user:
                raise AppException(
                    status_code=401,
                    error_code="USER_NOT_FOUND",
                    message="User not found"
                )

            if not user.is_active:
                raise AppException(
                    status_code=403,
                    error_code="ACCOUNT_INACTIVE",
                    message="Account is inactive"
                )

            # Generate new tokens
            return self.generate_tokens(user)

        except Exception as e:
            if isinstance(e, AppException):
                raise
            raise AppException(
                status_code=401,
                error_code="INVALID_REFRESH_TOKEN",
                message="Invalid or expired refresh token"
            )

    async def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str
    ) -> None:
        """
        Change user password.

        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password

        Raises:
            AppException: If current password is incorrect
        """
        from uuid import UUID
        user = await self.user_repo.get_by_id(UUID(user_id))

        if not user:
            raise AppException(
                status_code=404,
                error_code="USER_NOT_FOUND",
                message="User not found"
            )

        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            raise AppException(
                status_code=401,
                error_code="INVALID_PASSWORD",
                message="Current password is incorrect"
            )

        # Hash and update new password
        hashed_password = hash_password(new_password)
        await self.user_repo.update(UUID(user_id), {"hashed_password": hashed_password})
        await self.db.commit()

    async def request_password_reset(self, email: str) -> str:
        """
        Request password reset (generates reset token).

        Args:
            email: User email

        Returns:
            Reset token (in production, this should be sent via email)

        Raises:
            AppException: If email not found
        """
        user = await self.user_repo.get_by_email(email)

        if not user:
            # Don't reveal that email doesn't exist (security best practice)
            # But still raise for demonstration
            raise AppException(
                status_code=404,
                error_code="EMAIL_NOT_FOUND",
                message="If this email exists, a reset link has been sent"
            )

        # Create reset token (access token with 1 hour expiry)
        reset_token = create_access_token(
            subject=str(user.id),
            role=user.role,
            expires_delta=timedelta(hours=1),
            additional_claims={"type": "password_reset"}
        )

        # TODO: Send email with reset token
        # await email_service.send_password_reset_email(user.email, reset_token)

        return reset_token

    async def reset_password(
        self,
        token: str,
        new_password: str
    ) -> None:
        """
        Reset password using reset token.

        Args:
            token: Password reset token
            new_password: New password

        Raises:
            AppException: If token is invalid
        """
        try:
            payload = decode_token(token)

            # Verify this is a password reset token
            if payload.get("type") != "password_reset":
                raise AppException(
                    status_code=401,
                    error_code="INVALID_TOKEN_TYPE",
                    message="Invalid reset token"
                )

            user_id = payload.get("sub")
            if not user_id:
                raise AppException(
                    status_code=401,
                    error_code="INVALID_TOKEN",
                    message="Invalid token payload"
                )

            # Update password
            from uuid import UUID
            hashed_password = hash_password(new_password)
            updated = await self.user_repo.update(
                UUID(user_id),
                {"hashed_password": hashed_password}
            )

            if not updated:
                raise AppException(
                    status_code=404,
                    error_code="USER_NOT_FOUND",
                    message="User not found"
                )

            await self.db.commit()

        except Exception as e:
            if isinstance(e, AppException):
                raise
            raise AppException(
                status_code=401,
                error_code="INVALID_RESET_TOKEN",
                message="Invalid or expired reset token"
            )
