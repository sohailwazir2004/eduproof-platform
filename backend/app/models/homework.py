# homework.py - Homework Assignment Model
#
# Represents homework assignments created by teachers.

"""
Homework Model

Fields:
- id: UUID primary key
- title: Assignment title
- description: Detailed instructions
- teacher_id: FK to Teacher (creator)
- class_id: FK to Class
- subject_id: FK to Subject
- textbook_id: FK to Textbook (optional)
- page_numbers: Pages from textbook
- due_date: Submission deadline
- created_at, updated_at: Timestamps

Relationships:
- teacher: Many-to-one with Teacher
- class_: Many-to-one with Class
- subject: Many-to-one with Subject
- textbook: Many-to-one with Textbook
- submissions: One-to-many with Submission
"""

import uuid
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.teacher import Teacher
    from app.models.school import SchoolClass, Subject
    from app.models.textbook import Textbook
    from app.models.submission import Submission


class Homework(Base, UUIDMixin, TimestampMixin):
    """Homework assignment model."""
    __tablename__ = "homework"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Foreign keys
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teachers.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    class_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("classes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    subject_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    textbook_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("textbooks.id", ondelete="SET NULL"),
        nullable=True
    )

    page_numbers: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Relationships
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="homework_assignments")
    school_class: Mapped["SchoolClass"] = relationship("SchoolClass", back_populates="homework_assignments")
    subject: Mapped[Optional["Subject"]] = relationship("Subject", back_populates="homework_assignments")
    textbook: Mapped[Optional["Textbook"]] = relationship("Textbook", back_populates="homework_assignments")
    submissions: Mapped[List["Submission"]] = relationship(
        "Submission",
        back_populates="homework",
        cascade="all, delete-orphan"
    )
