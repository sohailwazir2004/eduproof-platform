# users.py - User Management Routes
#
# CRUD operations for user profiles.

"""
User Endpoints

GET    /users/me           - Get current user profile
PUT    /users/me           - Update current user profile
GET    /users/{id}         - Get user by ID (admin only)
GET    /users              - List users with filters (admin only)
DELETE /users/{id}         - Deactivate user (admin only)
"""

from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    get_current_user_id,
    require_admin,
    require_principal,
    UserRole
)
from app.schemas.user import UserResponse, UserUpdate, UserWithRoleData
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.user_service import UserService
from app.utils.exceptions import AppException

router = APIRouter()


@router.get(
    "/me",
    response_model=UserWithRoleData,
    summary="Get current user profile",
    description="Get the authenticated user's profile with role-specific data"
)
async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current authenticated user's profile.

    Returns user data including role-specific information
    (student data, teacher data, parent data, or principal data).
    """
    user_service = UserService(db)
    user = await user_service.get_user_with_role_data(UUID(user_id))
    return user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
    description="Update the authenticated user's profile"
)
async def update_current_user(
    update_data: UserUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user's profile.

    - **first_name**: Optional first name update
    - **last_name**: Optional last name update
    - **phone**: Optional phone number update
    - **avatar_url**: Optional avatar URL update
    """
    user_service = UserService(db)
    user = await user_service.update_user(UUID(user_id), update_data)
    return user


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="List all users",
    description="List users with filters and pagination (admin/principal only)"
)
async def list_users(
    role: Optional[UserRole] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in name/email"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Records per page"),
    _: bool = Depends(require_principal),
    db: AsyncSession = Depends(get_db)
):
    """
    List all users with optional filters.

    Requires principal or admin role.
    """
    user_service = UserService(db)
    users, total = await user_service.list_users(
        role=role,
        is_active=is_active,
        search=search,
        skip=skip,
        limit=limit
    )

    return PaginatedResponse(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{user_id}",
    response_model=UserWithRoleData,
    summary="Get user by ID",
    description="Get specific user's profile (admin/principal only)"
)
async def get_user(
    user_id: UUID,
    _: bool = Depends(require_principal),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a user by ID.

    Requires principal or admin role.
    """
    user_service = UserService(db)
    user = await user_service.get_user_with_role_data(user_id)
    return user


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    summary="Deactivate user",
    description="Soft delete a user by deactivating their account"
)
async def deactivate_user(
    user_id: UUID,
    _: bool = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Deactivate a user account (soft delete).

    Requires admin role.
    """
    user_service = UserService(db)
    await user_service.deactivate_user(user_id)
    return MessageResponse(message="User deactivated successfully")


@router.post(
    "/{user_id}/activate",
    response_model=MessageResponse,
    summary="Reactivate user",
    description="Reactivate a previously deactivated user"
)
async def activate_user(
    user_id: UUID,
    _: bool = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Reactivate a user account.

    Requires admin role.
    """
    user_service = UserService(db)
    await user_service.activate_user(user_id)
    return MessageResponse(message="User activated successfully")


@router.post(
    "/{user_id}/verify",
    response_model=MessageResponse,
    summary="Verify user email",
    description="Mark user's email as verified"
)
async def verify_user(
    user_id: UUID,
    _: bool = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Verify a user's email address.

    Requires admin role.
    """
    user_service = UserService(db)
    await user_service.verify_user(user_id)
    return MessageResponse(message="User verified successfully")
