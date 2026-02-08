# school.py - School, Class, Subject Models
#
# Core organizational models for the school structure.

import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Table, Column, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.teacher import Teacher
    from app.models.principal import Principal
    from app.models.textbook import Textbook
    from app.models.homework import Homework


# Association table for Teacher <-> Subject (many-to-many)
teacher_subjects = Table(
    "teacher_subjects",
    Base.metadata,
    Column("teacher_id", UUID(as_uuid=True), ForeignKey("teachers.id", ondelete="CASCADE"), primary_key=True),
    Column("subject_id", UUID(as_uuid=True), ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True),
)

# Association table for Teacher <-> Class (many-to-many)
teacher_classes = Table(
    "teacher_classes",
    Base.metadata,
    Column("teacher_id", UUID(as_uuid=True), ForeignKey("teachers.id", ondelete="CASCADE"), primary_key=True),
    Column("class_id", UUID(as_uuid=True), ForeignKey("classes.id", ondelete="CASCADE"), primary_key=True),
)


class School(Base, UUIDMixin, TimestampMixin):
    """
    School model representing an educational institution.

    A school has multiple classes, teachers, and a principal.
    """
    __tablename__ = "schools"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), default="India", nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    classes: Mapped[List["SchoolClass"]] = relationship(
        "SchoolClass",
        back_populates="school",
        cascade="all, delete-orphan"
    )
    principals: Mapped[List["Principal"]] = relationship(
        "Principal",
        back_populates="school"
    )
    teachers: Mapped[List["Teacher"]] = relationship(
        "Teacher",
        back_populates="school"
    )

    def __repr__(self) -> str:
        return f"<School(id={self.id}, name={self.name})>"


class SchoolClass(Base, UUIDMixin, TimestampMixin):
    """
    Class/Grade model (e.g., Class 5-A, Grade 10-B).

    A class belongs to a school and has multiple students.
    """
    __tablename__ = "classes"

    name: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "5-A", "10-B"
    grade: Mapped[int] = mapped_column(Integer, nullable=False)  # e.g., 5, 10
    section: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # e.g., "A", "B"
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)  # e.g., "2024-2025"

    # Foreign keys
    school_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Relationships
    school: Mapped["School"] = relationship("School", back_populates="classes")
    students: Mapped[List["Student"]] = relationship(
        "Student",
        back_populates="school_class",
        cascade="all, delete-orphan"
    )
    teachers: Mapped[List["Teacher"]] = relationship(
        "Teacher",
        secondary=teacher_classes,
        back_populates="classes"
    )
    textbooks: Mapped[List["Textbook"]] = relationship(
        "Textbook",
        back_populates="school_class"
    )
    homework_assignments: Mapped[List["Homework"]] = relationship(
        "Homework",
        back_populates="school_class"
    )

    def __repr__(self) -> str:
        return f"<SchoolClass(id={self.id}, name={self.name}, grade={self.grade})>"


class Subject(Base, UUIDMixin, TimestampMixin):
    """
    Subject model (e.g., Mathematics, English, Science).

    Subjects are taught by teachers and have associated textbooks.
    """
    __tablename__ = "subjects"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # e.g., "MATH101"
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # Icon name for UI

    # Relationships
    teachers: Mapped[List["Teacher"]] = relationship(
        "Teacher",
        secondary=teacher_subjects,
        back_populates="subjects"
    )
    textbooks: Mapped[List["Textbook"]] = relationship(
        "Textbook",
        back_populates="subject"
    )
    homework_assignments: Mapped[List["Homework"]] = relationship(
        "Homework",
        back_populates="subject"
    )

    def __repr__(self) -> str:
        return f"<Subject(id={self.id}, name={self.name})>"
