# submission.py - Submission Pydantic Schemas
#
# Schemas for homework submission operations.

"""
Submission Schemas

- SubmissionBase: Shared fields
- SubmissionCreate: Submit homework request
- SubmissionUpdate: Grade/feedback update
- SubmissionResponse: API response with AI analysis
- SubmissionList: Paginated list response
"""

from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, UUID4


class SubmissionStatus(str, Enum):
    """Submission status enum."""
    PENDING = "pending"
    REVIEWED = "reviewed"
    GRADED = "graded"


class SubmissionCreate(BaseModel):
    """Submission creation schema."""
    homework_id: UUID4 = Field(..., description="Homework assignment ID")

    class Config:
        json_schema_extra = {
            "example": {
                "homework_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class SubmissionGrade(BaseModel):
    """Schema for grading a submission."""
    grade: float = Field(..., ge=0, le=100, description="Grade (0-100)")
    feedback: Optional[str] = Field(None, description="Teacher feedback")

    class Config:
        json_schema_extra = {
            "example": {
                "grade": 85.5,
                "feedback": "Good work! Consider showing more steps in your solution."
            }
        }


class SubmissionFeedback(BaseModel):
    """Schema for adding feedback without grade."""
    feedback: str = Field(..., min_length=1, description="Teacher feedback")


class StudentInfo(BaseModel):
    """Student info for submission response."""
    id: UUID4
    name: str
    roll_number: Optional[str]

    class Config:
        from_attributes = True


class HomeworkInfo(BaseModel):
    """Homework info for submission response."""
    id: UUID4
    title: str
    due_date: datetime

    class Config:
        from_attributes = True


class AIAnalysisResult(BaseModel):
    """AI analysis result structure."""
    relevance_score: Optional[float] = Field(None, description="0-1 relevance score")
    content_summary: Optional[str] = Field(None, description="Summary of submission content")
    extracted_text: Optional[str] = Field(None, description="OCR extracted text")
    suggested_grade: Optional[float] = Field(None, description="AI suggested grade")
    feedback_suggestions: Optional[List[str]] = Field(None, description="AI feedback suggestions")
    errors_detected: Optional[List[str]] = Field(None, description="Detected errors")
    analyzed_at: Optional[datetime] = Field(None, description="Analysis timestamp")


class SubmissionResponse(BaseModel):
    """Submission response schema."""
    id: UUID4
    homework_id: UUID4
    student_id: UUID4
    file_url: str
    file_type: str
    status: SubmissionStatus
    grade: Optional[float]
    teacher_feedback: Optional[str]
    submitted_at: datetime
    reviewed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    # Optional nested data
    student: Optional[StudentInfo] = None
    homework: Optional[HomeworkInfo] = None
    ai_analysis: Optional[AIAnalysisResult] = None

    class Config:
        from_attributes = True


class SubmissionListResponse(BaseModel):
    """Paginated submission list response."""
    items: List[SubmissionResponse]
    total: int
    skip: int
    limit: int
    has_more: bool = False


class SubmissionStats(BaseModel):
    """Submission statistics for a student."""
    total_submissions: int
    pending: int
    reviewed: int
    graded: int
    average_grade: Optional[float]
    on_time_rate: Optional[float]
