# submission.py - Homework Submission Model
#
# Represents student homework submissions.

"""
Submission Model

Fields:
- id: UUID primary key
- homework_id: FK to Homework
- student_id: FK to Student
- file_url: Cloud storage URL for submitted file
- file_type: image/pdf
- status: Enum (pending, reviewed, graded)
- grade: Optional grade
- teacher_feedback: Optional feedback text
- ai_analysis: JSON field for AI analysis results
- submitted_at: Submission timestamp
- reviewed_at: Review timestamp

Relationships:
- homework: Many-to-one with Homework
- student: Many-to-one with Student
"""

import uuid
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum
from sqlalchemy import String, ForeignKey, DateTime, Text, Float, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.homework import Homework
    from app.models.student import Student


class SubmissionStatus(str, Enum):
    """Submission status enum."""
    PENDING = "pending"
    REVIEWED = "reviewed"
    GRADED = "graded"


class Submission(Base, UUIDMixin, TimestampMixin):
    """Homework submission model."""
    __tablename__ = "submissions"

    # Foreign keys
    homework_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("homework.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[SubmissionStatus] = mapped_column(
        SQLEnum(SubmissionStatus, name="submission_status"),
        default=SubmissionStatus.PENDING,
        nullable=False
    )
    grade: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    teacher_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_analysis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON stored as text
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    homework: Mapped["Homework"] = relationship("Homework", back_populates="submissions")
    student: Mapped["Student"] = relationship("Student", back_populates="submissions")
