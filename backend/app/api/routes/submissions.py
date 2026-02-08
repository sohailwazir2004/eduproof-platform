# submissions.py - Homework Submission Routes
#
# Submission operations for students and grading for teachers.

"""
Submission Endpoints

POST   /submissions                  - Submit homework (student)
GET    /submissions/{id}             - Get submission details
PUT    /submissions/{id}/grade       - Grade submission (teacher)
PUT    /submissions/{id}/feedback    - Add feedback (teacher)
GET    /submissions/{id}/ai-analysis - Get AI analysis results
DELETE /submissions/{id}             - Delete submission (student, before deadline)
GET    /submissions/my               - Get student's own submissions
GET    /submissions/pending          - Get pending submissions for teacher
"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    get_current_user_id,
    require_student,
    require_teacher,
    UserRole
)
from app.schemas.submission import (
    SubmissionResponse,
    SubmissionGrade,
    SubmissionFeedback,
    SubmissionListResponse,
    SubmissionStats
)
from app.schemas.common import MessageResponse, PaginatedResponse
from app.services.submission_service import SubmissionService
from app.services.storage_service import StorageService
from app.services.user_service import UserService
from app.utils.exceptions import AppException

router = APIRouter()


@router.post(
    "",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit homework",
    description="Submit homework with file upload (student only)"
)
async def submit_homework(
    homework_id: UUID = Form(..., description="Homework assignment ID"),
    file: UploadFile = File(..., description="Submission file (image or PDF)"),
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_student),
    db: AsyncSession = Depends(get_db)
):
    """
    Submit homework assignment.

    Requires student role. Uploads file and creates submission record.

    - **homework_id**: ID of the homework assignment
    - **file**: Image or PDF file of completed homework
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if not user.student:
        raise AppException(
            status_code=400,
            error_code="STUDENT_PROFILE_REQUIRED",
            message="Student profile not found"
        )

    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise AppException(
            status_code=400,
            error_code="INVALID_FILE_TYPE",
            message="Only JPEG, PNG, and PDF files are allowed"
        )

    # Upload file
    storage_service = StorageService()
    file_url = await storage_service.upload_file(
        file=file,
        folder=f"submissions/{homework_id}"
    )

    file_type = "pdf" if file.content_type == "application/pdf" else "image"

    # Create submission
    submission_service = SubmissionService(db)
    submission = await submission_service.create_submission(
        student_id=user.student.id,
        homework_id=homework_id,
        file_url=file_url,
        file_type=file_type
    )

    return await submission_service.get_submission(submission.id)


@router.get(
    "/my",
    response_model=SubmissionListResponse,
    summary="Get my submissions",
    description="Get current student's submissions"
)
async def get_my_submissions(
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Records per page"),
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_student),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current student's submissions.

    Requires student role.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if not user.student:
        raise AppException(
            status_code=400,
            error_code="STUDENT_PROFILE_REQUIRED",
            message="Student profile not found"
        )

    submission_service = SubmissionService(db)
    submissions, total = await submission_service.list_submissions_by_student(
        student_id=user.student.id,
        status_filter=status_filter,
        skip=skip,
        limit=limit
    )

    return SubmissionListResponse(
        items=[SubmissionResponse.model_validate(s) for s in submissions],
        total=total,
        skip=skip,
        limit=limit,
        has_more=skip + len(submissions) < total
    )


@router.get(
    "/pending",
    response_model=PaginatedResponse,
    summary="Get pending submissions",
    description="Get submissions pending review for teacher"
)
async def get_pending_submissions(
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Records per page"),
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher),
    db: AsyncSession = Depends(get_db)
):
    """
    Get pending submissions for teacher review.

    Requires teacher role.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if not user.teacher:
        raise AppException(
            status_code=400,
            error_code="TEACHER_PROFILE_REQUIRED",
            message="Teacher profile not found"
        )

    submission_service = SubmissionService(db)
    submissions = await submission_service.get_pending_for_teacher(
        teacher_id=user.teacher.id,
        skip=skip,
        limit=limit
    )

    return PaginatedResponse(
        items=[SubmissionResponse.model_validate(s) for s in submissions],
        total=len(submissions),
        skip=skip,
        limit=limit
    )


@router.get(
    "/stats",
    response_model=SubmissionStats,
    summary="Get my submission stats",
    description="Get submission statistics for current student"
)
async def get_my_stats(
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_student),
    db: AsyncSession = Depends(get_db)
):
    """
    Get submission statistics for current student.

    Requires student role.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if not user.student:
        raise AppException(
            status_code=400,
            error_code="STUDENT_PROFILE_REQUIRED",
            message="Student profile not found"
        )

    submission_service = SubmissionService(db)
    return await submission_service.get_student_stats(user.student.id)


@router.get(
    "/{submission_id}",
    response_model=SubmissionResponse,
    summary="Get submission details",
    description="Get detailed information about a submission"
)
async def get_submission(
    submission_id: UUID,
    include_ai: bool = Query(False, description="Include AI analysis"),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get submission details.

    Access is controlled based on role:
    - Students can view their own submissions
    - Teachers can view submissions for their homework
    - Principals can view all submissions
    """
    submission_service = SubmissionService(db)
    return await submission_service.get_submission(
        submission_id,
        include_ai_analysis=include_ai
    )


@router.put(
    "/{submission_id}/grade",
    response_model=SubmissionResponse,
    summary="Grade submission",
    description="Grade a submission with optional feedback"
)
async def grade_submission(
    submission_id: UUID,
    grade_data: SubmissionGrade,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher),
    db: AsyncSession = Depends(get_db)
):
    """
    Grade a submission.

    Requires teacher role. Teachers can only grade submissions
    for their own homework assignments.

    - **grade**: Numeric grade (0-100)
    - **feedback**: Optional feedback text
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if not user.teacher:
        raise AppException(
            status_code=400,
            error_code="TEACHER_PROFILE_REQUIRED",
            message="Teacher profile not found"
        )

    submission_service = SubmissionService(db)
    await submission_service.grade_submission(
        submission_id=submission_id,
        teacher_id=user.teacher.id,
        grade_data=grade_data
    )

    return await submission_service.get_submission(submission_id)


@router.put(
    "/{submission_id}/feedback",
    response_model=SubmissionResponse,
    summary="Add feedback",
    description="Add feedback to a submission without grading"
)
async def add_feedback(
    submission_id: UUID,
    feedback_data: SubmissionFeedback,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher),
    db: AsyncSession = Depends(get_db)
):
    """
    Add feedback to a submission.

    Requires teacher role. Marks submission as reviewed.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if not user.teacher:
        raise AppException(
            status_code=400,
            error_code="TEACHER_PROFILE_REQUIRED",
            message="Teacher profile not found"
        )

    submission_service = SubmissionService(db)
    await submission_service.add_feedback(
        submission_id=submission_id,
        teacher_id=user.teacher.id,
        feedback=feedback_data.feedback
    )

    return await submission_service.get_submission(submission_id)


@router.post(
    "/{submission_id}/ai-analysis",
    response_model=MessageResponse,
    summary="Trigger AI analysis",
    description="Trigger AI analysis for a submission"
)
async def trigger_ai_analysis(
    submission_id: UUID,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher),
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger AI analysis for a submission.

    Requires teacher role. Queues the submission for AI processing.
    """
    submission_service = SubmissionService(db)
    await submission_service.trigger_ai_analysis(submission_id)
    return MessageResponse(message="AI analysis triggered successfully")


@router.delete(
    "/{submission_id}",
    response_model=MessageResponse,
    summary="Delete submission",
    description="Delete a submission (student only, before grading)"
)
async def delete_submission(
    submission_id: UUID,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_student),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a submission.

    Requires student role. Students can only delete their own
    submissions that have not been reviewed or graded.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if not user.student:
        raise AppException(
            status_code=400,
            error_code="STUDENT_PROFILE_REQUIRED",
            message="Student profile not found"
        )

    submission_service = SubmissionService(db)
    await submission_service.delete_submission(
        submission_id=submission_id,
        student_id=user.student.id
    )

    return MessageResponse(message="Submission deleted successfully")
