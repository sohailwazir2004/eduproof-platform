# Database Models Package
# Export all SQLAlchemy models for easy importing
# Import all models here to ensure SQLAlchemy can resolve relationships

from app.models.base import UUIDMixin, TimestampMixin
from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.parent import Parent
from app.models.principal import Principal
from app.models.school import School, SchoolClass, Subject
from app.models.homework import Homework
from app.models.submission import Submission
from app.models.textbook import Textbook

__all__ = [
    "UUIDMixin",
    "TimestampMixin",
    "User",
    "Student",
    "Teacher",
    "Parent",
    "Principal",
    "School",
    "SchoolClass",
    "Subject",
    "Homework",
    "Submission",
    "Textbook",
]
