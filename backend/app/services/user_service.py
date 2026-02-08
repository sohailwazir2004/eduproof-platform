# user_service.py - User Service
#
# Business logic for user management.

"""
User Service

Methods:
- get_user_by_id(user_id) -> User
- get_user_by_email(email) -> User
- get_user_with_role_data(user_id) -> UserWithRoleData
- update_user(user_id, data) -> User
- deactivate_user(user_id) -> None
- activate_user(user_id) -> None
- verify_user(user_id) -> None
- list_users(filters, pagination) -> List[User]
"""

from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import UserRole
from app.schemas.user import UserUpdate, UserWithRoleData
from app.utils.exceptions import AppException


class UserService:
    """
    Service for user management operations.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def get_user_by_id(self, user_id: UUID) -> User:
        """
        Get user by ID.

        Args:
            user_id: User UUID

        Returns:
            User object

        Raises:
            AppException: If user not found
        """
        user = await self.user_repo.get_by_id(user_id, load_relationships=True)
        if not user:
            raise AppException(
                status_code=404,
                error_code="USER_NOT_FOUND",
                message="User not found"
            )
        return user

    async def get_user_with_role_data(self, user_id: UUID) -> UserWithRoleData:
        """
        Get user with role-specific data.

        Args:
            user_id: User UUID

        Returns:
            UserWithRoleData with nested role data
        """
        user = await self.get_user_by_id(user_id)

        # Build response with role-specific data
        response_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "role": user.role,
            "avatar_url": user.avatar_url,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }

        # Add role-specific data
        if user.role == UserRole.STUDENT and user.student:
            response_data["student_data"] = {
                "id": str(user.student.id),
                "roll_number": user.student.roll_number,
                "admission_number": user.student.admission_number,
                "class_id": str(user.student.class_id) if user.student.class_id else None,
                "date_of_birth": user.student.date_of_birth.isoformat() if user.student.date_of_birth else None,
                "gender": user.student.gender,
                "blood_group": user.student.blood_group,
                "address": user.student.address
            }
        elif user.role == UserRole.TEACHER and user.teacher:
            response_data["teacher_data"] = {
                "id": str(user.teacher.id),
                "employee_id": user.teacher.employee_id,
                "school_id": str(user.teacher.school_id) if user.teacher.school_id else None,
                "department": user.teacher.department,
                "qualification": user.teacher.qualification,
                "date_of_joining": user.teacher.date_of_joining.isoformat() if user.teacher.date_of_joining else None,
                "specialization": user.teacher.specialization
            }
        elif user.role == UserRole.PARENT and user.parent:
            response_data["parent_data"] = {
                "id": str(user.parent.id),
                "occupation": user.parent.occupation,
                "work_phone": user.parent.work_phone,
                "address": user.parent.address,
                "emergency_contact": user.parent.emergency_contact,
                "relationship_type": user.parent.relationship_type
            }
        elif user.role == UserRole.PRINCIPAL and user.principal:
            response_data["principal_data"] = {
                "id": str(user.principal.id),
                "employee_id": user.principal.employee_id,
                "school_id": str(user.principal.school_id) if user.principal.school_id else None,
                "qualification": user.principal.qualification,
                "date_of_joining": user.principal.date_of_joining.isoformat() if user.principal.date_of_joining else None,
                "years_of_experience": user.principal.years_of_experience
            }

        return UserWithRoleData(**response_data)

    async def update_user(self, user_id: UUID, update_data: UserUpdate) -> User:
        """
        Update user profile.

        Args:
            user_id: User UUID
            update_data: Update schema

        Returns:
            Updated User object
        """
        await self.get_user_by_id(user_id)
        update_dict = update_data.model_dump(exclude_unset=True)
        user = await self.user_repo.update(user_id, update_dict)
        await self.db.commit()
        return user

    async def deactivate_user(self, user_id: UUID) -> None:
        """
        Deactivate a user account.

        Args:
            user_id: User UUID
        """
        user = await self.get_user_by_id(user_id)
        if not user.is_active:
            raise AppException(
                status_code=400,
                error_code="ALREADY_INACTIVE",
                message="User is already inactive"
            )
        await self.user_repo.update(user_id, {"is_active": False})
        await self.db.commit()

    async def activate_user(self, user_id: UUID) -> None:
        """
        Activate a user account.

        Args:
            user_id: User UUID
        """
        user = await self.get_user_by_id(user_id)
        if user.is_active:
            raise AppException(
                status_code=400,
                error_code="ALREADY_ACTIVE",
                message="User is already active"
            )
        await self.user_repo.update(user_id, {"is_active": True})
        await self.db.commit()

    async def verify_user(self, user_id: UUID) -> None:
        """
        Mark user as verified.

        Args:
            user_id: User UUID
        """
        user = await self.get_user_by_id(user_id)
        if user.is_verified:
            raise AppException(
                status_code=400,
                error_code="ALREADY_VERIFIED",
                message="User is already verified"
            )
        await self.user_repo.update(user_id, {"is_verified": True})
        await self.db.commit()

    async def list_users(
        self,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[User], int]:
        """
        List users with filters and pagination.

        Args:
            role: Filter by role
            is_active: Filter by active status
            search: Search term
            skip: Records to skip
            limit: Max records

        Returns:
            Tuple of (users list, total count)
        """
        users = await self.user_repo.list_all(
            role=role,
            is_active=is_active,
            search=search,
            skip=skip,
            limit=limit
        )
        total = await self.user_repo.count(role=role, is_active=is_active)
        return users, total
