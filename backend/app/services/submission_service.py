# submission_service.py - Submission Service
#
# Business logic for homework submissions and grading.

"""
Submission Service

Methods:
- create_submission(student_id, homework_id, file) -> Submission
- get_submission(submission_id) -> Submission
- grade_submission(submission_id, grade, feedback) -> Submission
- list_submissions_for_homework(homework_id) -> List[Submission]
- list_submissions_for_student(student_id) -> List[Submission]
- trigger_ai_analysis(submission_id) -> None
- get_ai_analysis(submission_id) -> dict
"""

from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime, timezone
import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.submission import Submission, SubmissionStatus
from app.repositories.submission_repository import SubmissionRepository
from app.repositories.homework_repository import HomeworkRepository
from app.schemas.submission import SubmissionResponse, SubmissionGrade, SubmissionStats
from app.utils.exceptions import AppException


class SubmissionService:
    """Service for submission management operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.submission_repo = SubmissionRepository(db)
        self.homework_repo = HomeworkRepository(db)

    async def create_submission(
        self,
        student_id: UUID,
        homework_id: UUID,
        file_url: str,
        file_type: str
    ) -> Submission:
        """
        Create a new homework submission.

        Args:
            student_id: Student's ID
            homework_id: Homework assignment ID
            file_url: URL of uploaded file
            file_type: File type (image/pdf)

        Returns:
            Created Submission object
        """
        # Check if homework exists
        homework = await self.homework_repo.get_by_id(homework_id)
        if not homework:
            raise AppException(
                status_code=404,
                error_code="HOMEWORK_NOT_FOUND",
                message="Homework not found"
            )

        # Check if already submitted
        existing = await self.submission_repo.get_by_homework_and_student(
            homework_id=homework_id,
            student_id=student_id
        )
        if existing:
            raise AppException(
                status_code=400,
                error_code="ALREADY_SUBMITTED",
                message="You have already submitted this homework"
            )

        # Check if past due date
        if homework.due_date < datetime.now(timezone.utc):
            raise AppException(
                status_code=400,
                error_code="PAST_DUE_DATE",
                message="The submission deadline has passed"
            )

        submission_data = {
            "homework_id": homework_id,
            "student_id": student_id,
            "file_url": file_url,
            "file_type": file_type,
            "status": SubmissionStatus.PENDING,
            "submitted_at": datetime.now(timezone.utc)
        }

        submission = await self.submission_repo.create(submission_data)
        await self.db.commit()
        return submission

    async def get_submission(
        self,
        submission_id: UUID,
        include_ai_analysis: bool = False
    ) -> SubmissionResponse:
        """
        Get submission by ID.

        Args:
            submission_id: Submission UUID
            include_ai_analysis: Include AI analysis data

        Returns:
            SubmissionResponse object
        """
        submission = await self.submission_repo.get_by_id(
            submission_id,
            load_relationships=True
        )
        if not submission:
            raise AppException(
                status_code=404,
                error_code="SUBMISSION_NOT_FOUND",
                message="Submission not found"
            )

        response_data = {
            "id": submission.id,
            "homework_id": submission.homework_id,
            "student_id": submission.student_id,
            "file_url": submission.file_url,
            "file_type": submission.file_type,
            "status": submission.status,
            "grade": submission.grade,
            "teacher_feedback": submission.teacher_feedback,
            "submitted_at": submission.submitted_at,
            "reviewed_at": submission.reviewed_at,
            "created_at": submission.created_at,
            "updated_at": submission.updated_at
        }

        # Add related data
        if submission.student and submission.student.user:
            response_data["student"] = {
                "id": submission.student.id,
                "name": submission.student.user.full_name,
                "roll_number": submission.student.roll_number
            }

        if submission.homework:
            response_data["homework"] = {
                "id": submission.homework.id,
                "title": submission.homework.title,
                "due_date": submission.homework.due_date
            }

        if include_ai_analysis and submission.ai_analysis:
            try:
                response_data["ai_analysis"] = json.loads(submission.ai_analysis)
            except json.JSONDecodeError:
                response_data["ai_analysis"] = None

        return SubmissionResponse(**response_data)

    async def grade_submission(
        self,
        submission_id: UUID,
        teacher_id: UUID,
        grade_data: SubmissionGrade
    ) -> Submission:
        """
        Grade a submission.

        Args:
            submission_id: Submission UUID
            teacher_id: Teacher ID (for authorization)
            grade_data: Grade and feedback

        Returns:
            Updated Submission object
        """
        submission = await self.submission_repo.get_by_id(
            submission_id,
            load_relationships=True
        )
        if not submission:
            raise AppException(
                status_code=404,
                error_code="SUBMISSION_NOT_FOUND",
                message="Submission not found"
            )

        # Check if teacher owns this homework
        homework = await self.homework_repo.get_by_id(submission.homework_id)
        if homework.teacher_id != teacher_id:
            raise AppException(
                status_code=403,
                error_code="NOT_HOMEWORK_OWNER",
                message="You can only grade submissions for your own homework"
            )

        update_data = {
            "grade": grade_data.grade,
            "teacher_feedback": grade_data.feedback,
            "status": SubmissionStatus.GRADED,
            "reviewed_at": datetime.now(timezone.utc)
        }

        submission = await self.submission_repo.update(submission_id, update_data)
        await self.db.commit()
        return submission

    async def add_feedback(
        self,
        submission_id: UUID,
        teacher_id: UUID,
        feedback: str
    ) -> Submission:
        """
        Add feedback without grading.

        Args:
            submission_id: Submission UUID
            teacher_id: Teacher ID
            feedback: Feedback text

        Returns:
            Updated Submission object
        """
        submission = await self.submission_repo.get_by_id(
            submission_id,
            load_relationships=True
        )
        if not submission:
            raise AppException(
                status_code=404,
                error_code="SUBMISSION_NOT_FOUND",
                message="Submission not found"
            )

        homework = await self.homework_repo.get_by_id(submission.homework_id)
        if homework.teacher_id != teacher_id:
            raise AppException(
                status_code=403,
                error_code="NOT_HOMEWORK_OWNER",
                message="You can only add feedback to submissions for your own homework"
            )

        update_data = {
            "teacher_feedback": feedback,
            "status": SubmissionStatus.REVIEWED,
            "reviewed_at": datetime.now(timezone.utc)
        }

        submission = await self.submission_repo.update(submission_id, update_data)
        await self.db.commit()
        return submission

    async def list_submissions_by_homework(
        self,
        homework_id: UUID,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Submission], int]:
        """
        List submissions for a homework assignment.

        Args:
            homework_id: Homework UUID
            status_filter: Optional status filter
            skip: Records to skip
            limit: Max records

        Returns:
            Tuple of (submissions list, total count)
        """
        status = None
        if status_filter:
            try:
                status = SubmissionStatus(status_filter)
            except ValueError:
                pass

        submissions = await self.submission_repo.list_by_homework(
            homework_id=homework_id,
            status=status,
            skip=skip,
            limit=limit
        )
        total = await self.submission_repo.count_by_homework(homework_id, status)
        return submissions, total

    async def list_submissions_by_student(
        self,
        student_id: UUID,
        status_filter: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Submission], int]:
        """
        List submissions by a student.

        Args:
            student_id: Student UUID
            status_filter: Optional status filter
            skip: Records to skip
            limit: Max records

        Returns:
            Tuple of (submissions list, total count)
        """
        status = None
        if status_filter:
            try:
                status = SubmissionStatus(status_filter)
            except ValueError:
                pass

        submissions = await self.submission_repo.list_by_student(
            student_id=student_id,
            status=status,
            skip=skip,
            limit=limit
        )
        total = await self.submission_repo.count_by_student(student_id, status)
        return submissions, total

    async def get_pending_for_teacher(
        self,
        teacher_id: UUID,
        skip: int = 0,
        limit: int = 20
    ) -> List[Submission]:
        """
        Get pending submissions for a teacher.

        Args:
            teacher_id: Teacher UUID
            skip: Records to skip
            limit: Max records

        Returns:
            List of pending submissions
        """
        return await self.submission_repo.get_pending_review_for_teacher(
            teacher_id=teacher_id,
            skip=skip,
            limit=limit
        )

    async def get_student_stats(self, student_id: UUID) -> SubmissionStats:
        """
        Get submission statistics for a student.

        Args:
            student_id: Student UUID

        Returns:
            SubmissionStats object
        """
        stats = await self.submission_repo.get_student_stats(student_id)
        return SubmissionStats(**stats)

    async def trigger_ai_analysis(self, submission_id: UUID) -> None:
        """
        Trigger AI analysis for a submission.

        Args:
            submission_id: Submission UUID
        """
        submission = await self.submission_repo.get_by_id(submission_id)
        if not submission:
            raise AppException(
                status_code=404,
                error_code="SUBMISSION_NOT_FOUND",
                message="Submission not found"
            )

        # TODO: Integrate with AI service
        # For now, we'll just store a placeholder
        ai_result = {
            "status": "pending",
            "message": "AI analysis queued",
            "queued_at": datetime.now(timezone.utc).isoformat()
        }

        await self.submission_repo.update(
            submission_id,
            {"ai_analysis": json.dumps(ai_result)}
        )
        await self.db.commit()

    async def delete_submission(
        self,
        submission_id: UUID,
        student_id: UUID
    ) -> None:
        """
        Delete a submission (student only, before grading).

        Args:
            submission_id: Submission UUID
            student_id: Student ID (for authorization)
        """
        submission = await self.submission_repo.get_by_id(submission_id)
        if not submission:
            raise AppException(
                status_code=404,
                error_code="SUBMISSION_NOT_FOUND",
                message="Submission not found"
            )

        if submission.student_id != student_id:
            raise AppException(
                status_code=403,
                error_code="NOT_SUBMISSION_OWNER",
                message="You can only delete your own submissions"
            )

        if submission.status != SubmissionStatus.PENDING:
            raise AppException(
                status_code=400,
                error_code="CANNOT_DELETE_GRADED",
                message="Cannot delete submissions that have been reviewed or graded"
            )

        await self.submission_repo.delete(submission_id)
        await self.db.commit()
