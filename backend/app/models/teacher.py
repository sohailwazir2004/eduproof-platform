# teacher.py - Teacher Model
#
# Teacher-specific model linked to User.
# Contains subject assignments and class relationships.

import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import date

from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin
from app.models.school import teacher_subjects, teacher_classes

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.school import School, SchoolClass, Subject
    from app.models.homework import Homework
    from app.models.textbook import Textbook


class Teacher(Base, UUIDMixin, TimestampMixin):
    """
    Teacher model with professional information.

    Linked to a User for authentication and to Classes/Subjects for assignments.
    """
    __tablename__ = "teachers"

    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    school_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Teacher-specific fields
    employee_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        nullable=True
    )
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    qualification: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    date_of_joining: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    specialization: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="teacher")
    school: Mapped[Optional["School"]] = relationship("School", back_populates="teachers")
    classes: Mapped[List["SchoolClass"]] = relationship(
        "SchoolClass",
        secondary=teacher_classes,
        back_populates="teachers"
    )
    subjects: Mapped[List["Subject"]] = relationship(
        "Subject",
        secondary=teacher_subjects,
        back_populates="teachers"
    )
    homework_assignments: Mapped[List["Homework"]] = relationship(
        "Homework",
        back_populates="teacher",
        cascade="all, delete-orphan"
    )
    uploaded_textbooks: Mapped[List["Textbook"]] = relationship(
        "Textbook",
        back_populates="teacher",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Teacher(id={self.id}, employee_id={self.employee_id})>"
