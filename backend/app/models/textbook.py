# textbook.py - Textbook Model
#
# Represents uploaded PDF textbooks.

"""
Textbook Model

Fields:
- id: UUID primary key
- title: Textbook title
- subject_id: FK to Subject
- class_id: FK to Class
- file_url: Cloud storage URL
- page_count: Number of pages
- is_indexed: Whether AI has indexed content
- uploaded_by: FK to Teacher
- uploaded_at: Upload timestamp

Relationships:
- subject: Many-to-one with Subject
- class_: Many-to-one with Class
- homework_assignments: One-to-many with Homework
"""

import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.school import SchoolClass, Subject
    from app.models.teacher import Teacher
    from app.models.homework import Homework


class Textbook(Base, UUIDMixin, TimestampMixin):
    """Textbook model."""
    __tablename__ = "textbooks"

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    # Foreign keys
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    class_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("classes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teachers.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    page_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_indexed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    subject: Mapped["Subject"] = relationship("Subject", back_populates="textbooks")
    school_class: Mapped["SchoolClass"] = relationship("SchoolClass", back_populates="textbooks")
    teacher: Mapped[Optional["Teacher"]] = relationship("Teacher", back_populates="uploaded_textbooks")
    homework_assignments: Mapped[List["Homework"]] = relationship("Homework", back_populates="textbook")
