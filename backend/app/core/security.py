# security.py - Authentication & Security Utilities
#
# Handles password hashing, JWT token creation/verification,
# and other security-related functions.

from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from enum import Enum

from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings


class UserRole(str, Enum):
    """User roles for role-based access control."""
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"
    PRINCIPAL = "principal"
    ADMIN = "admin"


# Password hashing context using argon2 (more modern and compatible with Python 3.13)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    # Truncate password to 72 bytes for bcrypt
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hashed password

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str,
    role: UserRole,
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[dict] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        subject: Token subject (usually user ID)
        role: User role for RBAC
        expires_delta: Custom expiration time
        additional_claims: Extra claims to include in token

    Returns:
        Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode = {
        "sub": subject,
        "role": role.value,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    }

    if additional_claims:
        to_encode.update(additional_claims)

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.jwt_algorithm
    )


def create_refresh_token(subject: str) -> str:
    """
    Create a JWT refresh token with longer expiration.

    Args:
        subject: Token subject (usually user ID)

    Returns:
        Encoded JWT refresh token string
    """
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )

    to_encode = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh"
    }

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.jwt_algorithm
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token string

    Returns:
        Token payload as dictionary

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependency to get current user ID from token.

    Args:
        token: JWT token from Authorization header

    Returns:
        User ID from token subject
    """
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    return user_id


async def get_current_user_role(token: str = Depends(oauth2_scheme)) -> UserRole:
    """
    Dependency to get current user role from token.

    Args:
        token: JWT token from Authorization header

    Returns:
        User role enum
    """
    payload = decode_token(token)
    role = payload.get("role")
    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    return UserRole(role)


class RoleChecker:
    """
    Dependency class for role-based access control.

    Usage:
        @router.get("/admin-only")
        async def admin_endpoint(
            _: None = Depends(RoleChecker([UserRole.ADMIN, UserRole.PRINCIPAL]))
        ):
            ...
    """

    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    async def __call__(self, token: str = Depends(oauth2_scheme)) -> bool:
        payload = decode_token(token)
        role = payload.get("role")

        if not role or UserRole(role) not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return True


# Pre-configured role checkers for common use cases
require_student = RoleChecker([UserRole.STUDENT])
require_teacher = RoleChecker([UserRole.TEACHER])
require_parent = RoleChecker([UserRole.PARENT])
require_principal = RoleChecker([UserRole.PRINCIPAL, UserRole.ADMIN])
require_admin = RoleChecker([UserRole.ADMIN])
require_teacher_or_principal = RoleChecker([UserRole.TEACHER, UserRole.PRINCIPAL, UserRole.ADMIN])
