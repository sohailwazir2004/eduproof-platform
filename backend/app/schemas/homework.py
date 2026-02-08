# homework.py - Homework Pydantic Schemas
#
# Schemas for homework assignment operations.

"""
Homework Schemas

- HomeworkBase: Shared fields
- HomeworkCreate: Create assignment request
- HomeworkUpdate: Update assignment request
- HomeworkResponse: API response with relationships
- HomeworkList: Paginated list response
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, UUID4


class HomeworkBase(BaseModel):
    """Base homework schema with shared fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Homework title")
    description: Optional[str] = Field(None, description="Detailed instructions")
    page_numbers: Optional[str] = Field(None, max_length=100, description="Textbook pages")
    due_date: datetime = Field(..., description="Submission deadline")


class HomeworkCreate(HomeworkBase):
    """Homework creation schema."""
    class_id: UUID4 = Field(..., description="Class ID")
    subject_id: Optional[UUID4] = Field(None, description="Subject ID")
    textbook_id: Optional[UUID4] = Field(None, description="Reference textbook ID")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Chapter 5 Exercises",
                "description": "Complete exercises 1-10 from Chapter 5",
                "class_id": "123e4567-e89b-12d3-a456-426614174000",
                "subject_id": "123e4567-e89b-12d3-a456-426614174001",
                "textbook_id": "123e4567-e89b-12d3-a456-426614174002",
                "page_numbers": "45-48",
                "due_date": "2024-02-15T23:59:59Z"
            }
        }


class HomeworkUpdate(BaseModel):
    """Homework update schema (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    page_numbers: Optional[str] = Field(None, max_length=100)
    due_date: Optional[datetime] = None
    subject_id: Optional[UUID4] = None
    textbook_id: Optional[UUID4] = None


class TeacherInfo(BaseModel):
    """Teacher info for homework response."""
    id: UUID4
    name: str
    email: str

    class Config:
        from_attributes = True


class ClassInfo(BaseModel):
    """Class info for homework response."""
    id: UUID4
    name: str
    grade: int

    class Config:
        from_attributes = True


class SubjectInfo(BaseModel):
    """Subject info for homework response."""
    id: UUID4
    name: str
    code: Optional[str]

    class Config:
        from_attributes = True


class TextbookInfo(BaseModel):
    """Textbook info for homework response."""
    id: UUID4
    title: str

    class Config:
        from_attributes = True


class SubmissionSummary(BaseModel):
    """Submission summary for homework response."""
    total: int = 0
    pending: int = 0
    reviewed: int = 0
    graded: int = 0


class HomeworkResponse(HomeworkBase):
    """Homework response schema with relationships."""
    id: UUID4
    teacher_id: UUID4
    class_id: UUID4
    subject_id: Optional[UUID4]
    textbook_id: Optional[UUID4]
    created_at: datetime
    updated_at: datetime

    # Optional nested data
    teacher: Optional[TeacherInfo] = None
    school_class: Optional[ClassInfo] = None
    subject: Optional[SubjectInfo] = None
    textbook: Optional[TextbookInfo] = None
    submission_summary: Optional[SubmissionSummary] = None

    class Config:
        from_attributes = True


class HomeworkListResponse(BaseModel):
    """Paginated homework list response."""
    items: List[HomeworkResponse]
    total: int
    skip: int
    limit: int
    has_more: bool = False
