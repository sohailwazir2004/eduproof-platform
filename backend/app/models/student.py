# student.py - Student Model
#
# Student-specific model linked to User.
# Contains academic information and relationships.

import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import date

from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.parent import Parent
    from app.models.school import SchoolClass
    from app.models.submission import Submission


class Student(Base, UUIDMixin, TimestampMixin):
    """
    Student model with academic information.

    Linked to a User for authentication and to a Class for enrollment.
    """
    __tablename__ = "students"

    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    class_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("classes.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("parents.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Student-specific fields
    roll_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    admission_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    blood_group: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="student")
    school_class: Mapped[Optional["SchoolClass"]] = relationship(
        "SchoolClass",
        back_populates="students"
    )
    parent: Mapped[Optional["Parent"]] = relationship(
        "Parent",
        back_populates="children"
    )
    submissions: Mapped[List["Submission"]] = relationship(
        "Submission",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Student(id={self.id}, roll_number={self.roll_number})>"
