# homework_repository.py - Homework Repository
#
# Data access layer for Homework model.

"""
Homework Repository

Methods:
- get_by_id(homework_id) -> Homework | None
- create(homework_data) -> Homework
- update(homework_id, data) -> Homework
- delete(homework_id) -> None
- list_by_class(class_id) -> List[Homework]
- list_by_teacher(teacher_id) -> List[Homework]
- list_pending_for_student(student_id) -> List[Homework]
"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.homework import Homework
from app.models.submission import Submission, SubmissionStatus


class HomeworkRepository:
    """Repository for Homework model database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        homework_id: UUID,
        load_relationships: bool = False
    ) -> Optional[Homework]:
        """Get homework by ID."""
        query = select(Homework).where(Homework.id == homework_id)

        if load_relationships:
            query = query.options(
                selectinload(Homework.teacher),
                selectinload(Homework.school_class),
                selectinload(Homework.subject),
                selectinload(Homework.textbook),
                selectinload(Homework.submissions)
            )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, homework_data: dict) -> Homework:
        """Create a new homework assignment."""
        homework = Homework(**homework_data)
        self.db.add(homework)
        await self.db.flush()
        await self.db.refresh(homework)
        return homework

    async def update(self, homework_id: UUID, update_data: dict) -> Optional[Homework]:
        """Update homework by ID."""
        homework = await self.get_by_id(homework_id)
        if not homework:
            return None

        for field, value in update_data.items():
            if hasattr(homework, field) and value is not None:
                setattr(homework, field, value)

        await self.db.flush()
        await self.db.refresh(homework)
        return homework

    async def delete(self, homework_id: UUID) -> bool:
        """Delete homework by ID."""
        homework = await self.get_by_id(homework_id)
        if not homework:
            return False

        await self.db.delete(homework)
        await self.db.flush()
        return True

    async def list_by_class(
        self,
        class_id: UUID,
        subject_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Homework]:
        """List homework for a class."""
        query = select(Homework).where(Homework.class_id == class_id)

        if subject_id:
            query = query.where(Homework.subject_id == subject_id)

        query = query.order_by(Homework.due_date.desc())
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def list_by_teacher(
        self,
        teacher_id: UUID,
        class_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Homework]:
        """List homework created by a teacher."""
        query = select(Homework).where(Homework.teacher_id == teacher_id)

        if class_id:
            query = query.where(Homework.class_id == class_id)

        query = query.options(
            selectinload(Homework.school_class),
            selectinload(Homework.subject)
        )
        query = query.order_by(Homework.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def list_pending_for_student(
        self,
        student_id: UUID,
        class_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> List[Homework]:
        """List homework not yet submitted by a student."""
        # Get all homework for the class that is not yet submitted by this student
        subquery = (
            select(Submission.homework_id)
            .where(Submission.student_id == student_id)
        )

        query = (
            select(Homework)
            .where(
                and_(
                    Homework.class_id == class_id,
                    Homework.due_date >= datetime.now(timezone.utc),
                    ~Homework.id.in_(subquery)
                )
            )
            .order_by(Homework.due_date.asc())
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def list_all_for_student(
        self,
        class_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> List[Homework]:
        """List all homework for a student's class."""
        query = (
            select(Homework)
            .where(Homework.class_id == class_id)
            .options(
                selectinload(Homework.subject),
                selectinload(Homework.teacher)
            )
            .order_by(Homework.due_date.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_by_class(
        self,
        class_id: UUID,
        subject_id: Optional[UUID] = None
    ) -> int:
        """Count homework for a class."""
        query = select(func.count(Homework.id)).where(Homework.class_id == class_id)

        if subject_id:
            query = query.where(Homework.subject_id == subject_id)

        result = await self.db.execute(query)
        return result.scalar_one()

    async def count_by_teacher(
        self,
        teacher_id: UUID,
        class_id: Optional[UUID] = None
    ) -> int:
        """Count homework by teacher."""
        query = select(func.count(Homework.id)).where(Homework.teacher_id == teacher_id)

        if class_id:
            query = query.where(Homework.class_id == class_id)

        result = await self.db.execute(query)
        return result.scalar_one()

    async def get_submission_stats(self, homework_id: UUID) -> dict:
        """Get submission statistics for a homework assignment."""
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
                ).label('graded')
            )
            .where(Submission.homework_id == homework_id)
        )

        result = await self.db.execute(query)
        row = result.one()
        return {
            'total': row.total,
            'pending': row.pending,
            'reviewed': row.reviewed,
            'graded': row.graded
        }
