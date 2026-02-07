# user_repository.py - User Repository
#
# Data access layer for User model.

"""
User Repository

Methods:
- get_by_id(user_id) -> User | None
- get_by_email(email) -> User | None
- create(user_data) -> User
- update(user_id, data) -> User
- delete(user_id) -> None
- list_all(filters, pagination) -> List[User]
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.core.security import UserRole


class UserRepository:
    """
    Repository for User model database operations.
    Provides abstraction layer between service and database.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        user_id: UUID,
        load_relationships: bool = False
    ) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User UUID
            load_relationships: Whether to eager load relationships

        Returns:
            User object or None if not found
        """
        query = select(User).where(User.id == user_id)

        if load_relationships:
            query = query.options(
                selectinload(User.student),
                selectinload(User.teacher),
                selectinload(User.parent),
                selectinload(User.principal)
            )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        email: str,
        load_relationships: bool = False
    ) -> Optional[User]:
        """
        Get user by email address.

        Args:
            email: User email
            load_relationships: Whether to eager load relationships

        Returns:
            User object or None if not found
        """
        query = select(User).where(User.email == email)

        if load_relationships:
            query = query.options(
                selectinload(User.student),
                selectinload(User.teacher),
                selectinload(User.parent),
                selectinload(User.principal)
            )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user_data: dict) -> User:
        """
        Create a new user.

        Args:
            user_data: Dictionary with user fields

        Returns:
            Created User object
        """
        user = User(**user_data)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: UUID, update_data: dict) -> Optional[User]:
        """
        Update user by ID.

        Args:
            user_id: User UUID
            update_data: Dictionary with fields to update

        Returns:
            Updated User object or None if not found
        """
        user = await self.get_by_id(user_id)
        if not user:
            return None

        for field, value in update_data.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)

        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> bool:
        """
        Delete user by ID (soft delete by setting is_active=False).

        Args:
            user_id: User UUID

        Returns:
            True if deleted, False if not found
        """
        user = await self.get_by_id(user_id)
        if not user:
            return False

        user.is_active = False
        await self.db.flush()
        return True

    async def list_all(
        self,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """
        List users with optional filters and pagination.

        Args:
            role: Filter by user role
            is_active: Filter by active status
            search: Search in name and email
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of User objects
        """
        query = select(User)

        # Apply filters
        filters = []
        if role:
            filters.append(User.role == role)
        if is_active is not None:
            filters.append(User.is_active == is_active)
        if search:
            search_term = f"%{search}%"
            filters.append(
                or_(
                    User.email.ilike(search_term),
                    User.first_name.ilike(search_term),
                    User.last_name.ilike(search_term)
                )
            )

        if filters:
            query = query.where(and_(*filters))

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count(
        self,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """
        Count users with optional filters.

        Args:
            role: Filter by user role
            is_active: Filter by active status

        Returns:
            Count of matching users
        """
        from sqlalchemy import func
        query = select(func.count(User.id))

        filters = []
        if role:
            filters.append(User.role == role)
        if is_active is not None:
            filters.append(User.is_active == is_active)

        if filters:
            query = query.where(and_(*filters))

        result = await self.db.execute(query)
        return result.scalar_one()

    async def exists_by_email(self, email: str) -> bool:
        """
        Check if user exists by email.

        Args:
            email: Email to check

        Returns:
            True if user exists, False otherwise
        """
        from sqlalchemy import exists
        query = select(exists().where(User.email == email))
        result = await self.db.execute(query)
        return result.scalar()
