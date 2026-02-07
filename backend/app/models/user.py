# user.py - User Model
#
# Base user model with common fields for all user types.
# Links to role-specific models via one-to-one relationships.

import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.security import UserRole
from app.models.base import UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.teacher import Teacher
    from app.models.parent import Parent
    from app.models.principal import Principal


class User(Base, UUIDMixin, TimestampMixin):
    """
    Base user model for authentication.

    All users (students, teachers, parents, principals) have a User record.
    Role-specific data is stored in linked tables.
    """
    __tablename__ = "users"

    # Authentication fields
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Profile fields
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Role and status
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role", create_constraint=True),
        nullable=False,
        index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships to role-specific models
    student: Mapped[Optional["Student"]] = relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    teacher: Mapped[Optional["Teacher"]] = relationship(
        "Teacher",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    parent: Mapped[Optional["Parent"]] = relationship(
        "Parent",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    principal: Mapped[Optional["Principal"]] = relationship(
        "Principal",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    @property
    def full_name(self) -> str:
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
