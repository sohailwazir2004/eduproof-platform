# submission_repository.py - Submission Repository
#
# Data access layer for Submission model.

"""
Submission Repository

Methods:
- get_by_id(submission_id) -> Submission | None
- create(submission_data) -> Submission
- update(submission_id, data) -> Submission
- delete(submission_id) -> None
- list_by_homework(homework_id) -> List[Submission]
- list_by_student(student_id) -> List[Submission]
- get_pending_review(teacher_id) -> List[Submission]
"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.submission import Submission, SubmissionStatus
from app.models.homework import Homework


class SubmissionRepository:
    """Repository for Submission model database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        submission_id: UUID,
        load_relationships: bool = False
    ) -> Optional[Submission]:
        """Get submission by ID."""
        query = select(Submission).where(Submission.id == submission_id)

        if load_relationships:
            query = query.options(
                selectinload(Submission.student),
                selectinload(Submission.homework)
            )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, submission_data: dict) -> Submission:
        """Create a new submission."""
        submission = Submission(**submission_data)
        self.db.add(submission)
        await self.db.flush()
        await self.db.refresh(submission)
        return submission

    async def update(self, submission_id: UUID, update_data: dict) -> Optional[Submission]:
        """Update submission by ID."""
        submission = await self.get_by_id(submission_id)
        if not submission:
            return None

        for field, value in update_data.items():
            if hasattr(submission, field) and value is not None:
                setattr(submission, field, value)

        await self.db.flush()
        await self.db.refresh(submission)
        return submission

    async def delete(self, submission_id: UUID) -> bool:
        """Delete submission by ID."""
        submission = await self.get_by_id(submission_id)
        if not submission:
            return False

        await self.db.delete(submission)
        await self.db.flush()
        return True

    async def list_by_homework(
        self,
        homework_id: UUID,
        status: Optional[SubmissionStatus] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Submission]:
        """List submissions for a homework assignment."""
        query = select(Submission).where(Submission.homework_id == homework_id)

        if status:
            query = query.where(Submission.status == status)

        query = query.options(selectinload(Submission.student))
        query = query.order_by(Submission.submitted_at.desc())
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def list_by_student(
        self,
        student_id: UUID,
        status: Optional[SubmissionStatus] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Submission]:
        """List submissions by a student."""
        query = select(Submission).where(Submission.student_id == student_id)

        if status:
            query = query.where(Submission.status == status)

        query = query.options(selectinload(Submission.homework))
        query = query.order_by(Submission.submitted_at.desc())
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_homework_and_student(
        self,
        homework_id: UUID,
        student_id: UUID
    ) -> Optional[Submission]:
        """Get submission for a specific homework by a specific student."""
        query = select(Submission).where(
            and_(
                Submission.homework_id == homework_id,
                Submission.student_id == student_id
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_pending_review_for_teacher(
        self,
        teacher_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> List[Submission]:
        """Get pending submissions for a teacher's homework."""
        query = (
            select(Submission)
            .join(Homework, Submission.homework_id == Homework.id)
            .where(
                and_(
                    Homework.teacher_id == teacher_id,
                    Submission.status == SubmissionStatus.PENDING
                )
            )
            .options(
                selectinload(Submission.student),
                selectinload(Submission.homework)
            )
            .order_by(Submission.submitted_at.asc())
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_by_homework(
        self,
        homework_id: UUID,
        status: Optional[SubmissionStatus] = None
    ) -> int:
        """Count submissions for a homework."""
        query = select(func.count(Submission.id)).where(
            Submission.homework_id == homework_id
        )

        if status:
            query = query.where(Submission.status == status)

        result = await self.db.execute(query)
        return result.scalar_one()

    async def count_by_student(
        self,
        student_id: UUID,
        status: Optional[SubmissionStatus] = None
    ) -> int:
        """Count submissions by a student."""
        query = select(func.count(Submission.id)).where(
            Submission.student_id == student_id
        )

        if status:
            query = query.where(Submission.status == status)

        result = await self.db.execute(query)
        return result.scalar_one()

    async def get_student_stats(self, student_id: UUID) -> dict:
        """Get submission statistics for a student."""
        # Count by status
        query = (
            select(
                func.count(Submission.id).label('total'),
                func.count(Submission.id).filter(
                    Submission.status == SubmissionStatus.PENDING
                ).label('pending'),
                func.count(Submission.id).filter(
                    Submission.status == SubmissionStatus.REVIEWED
                ).label('reviewed'),
                func.count(Submission.id).filter(
                    Submission.status == SubmissionStatus.GRADED
                ).label('graded'),
                func.avg(Submission.grade).label('average_grade')
            )
            .where(Submission.student_id == student_id)
        )

        result = await self.db.execute(query)
        row = result.one()

        return {
            'total_submissions': row.total,
            'pending': row.pending,
            'reviewed': row.reviewed,
            'graded': row.graded,
            'average_grade': float(row.average_grade) if row.average_grade else None
        }

    async def exists_for_homework(
        self,
        homework_id: UUID,
        student_id: UUID
    ) -> bool:
        """Check if student has already submitted for this homework."""
        from sqlalchemy import exists
        query = select(exists().where(
            and_(
                Submission.homework_id == homework_id,
                Submission.student_id == student_id
            )
        ))
        result = await self.db.execute(query)
        return result.scalar()
