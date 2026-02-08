# homework_service.py - Homework Service
#
# Business logic for homework assignment management.

"""
Homework Service

Methods:
- create_homework(teacher_id, data) -> Homework
- get_homework(homework_id) -> Homework
- update_homework(homework_id, data) -> Homework
- delete_homework(homework_id) -> None
- list_homework_for_class(class_id) -> List[Homework]
- list_homework_for_student(student_id) -> List[Homework]
- get_homework_with_submissions(homework_id) -> Homework
"""

from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.homework import Homework
from app.repositories.homework_repository import HomeworkRepository
from app.schemas.homework import HomeworkCreate, HomeworkUpdate, HomeworkResponse, SubmissionSummary
from app.utils.exceptions import AppException


class HomeworkService:
    """Service for homework management operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.homework_repo = HomeworkRepository(db)

    async def create_homework(
        self,
        teacher_id: UUID,
        data: HomeworkCreate
    ) -> Homework:
        """
        Create a new homework assignment.

        Args:
            teacher_id: Teacher's ID (from their Teacher profile)
            data: Homework creation data

        Returns:
            Created Homework object
        """
        homework_data = {
            "title": data.title,
            "description": data.description,
            "teacher_id": teacher_id,
            "class_id": data.class_id,
            "subject_id": data.subject_id,
            "textbook_id": data.textbook_id,
            "page_numbers": data.page_numbers,
            "due_date": data.due_date
        }

        homework = await self.homework_repo.create(homework_data)
        await self.db.commit()
        return homework

    async def get_homework(
        self,
        homework_id: UUID,
        include_stats: bool = False
    ) -> HomeworkResponse:
        """
        Get homework by ID.

        Args:
            homework_id: Homework UUID
            include_stats: Include submission statistics

        Returns:
            HomeworkResponse object
        """
        homework = await self.homework_repo.get_by_id(homework_id, load_relationships=True)
        if not homework:
            raise AppException(
                status_code=404,
                error_code="HOMEWORK_NOT_FOUND",
                message="Homework not found"
            )

        response_data = {
            "id": homework.id,
            "title": homework.title,
            "description": homework.description,
            "teacher_id": homework.teacher_id,
            "class_id": homework.class_id,
            "subject_id": homework.subject_id,
            "textbook_id": homework.textbook_id,
            "page_numbers": homework.page_numbers,
            "due_date": homework.due_date,
            "created_at": homework.created_at,
            "updated_at": homework.updated_at
        }

        # Add related data if available
        if homework.teacher and homework.teacher.user:
            response_data["teacher"] = {
                "id": homework.teacher.id,
                "name": homework.teacher.user.full_name,
                "email": homework.teacher.user.email
            }

        if homework.school_class:
            response_data["school_class"] = {
                "id": homework.school_class.id,
                "name": homework.school_class.name,
                "grade": homework.school_class.grade
            }

        if homework.subject:
            response_data["subject"] = {
                "id": homework.subject.id,
                "name": homework.subject.name,
                "code": homework.subject.code
            }

        if homework.textbook:
            response_data["textbook"] = {
                "id": homework.textbook.id,
                "title": homework.textbook.title
            }

        if include_stats:
            stats = await self.homework_repo.get_submission_stats(homework_id)
            response_data["submission_summary"] = SubmissionSummary(**stats)

        return HomeworkResponse(**response_data)

    async def update_homework(
        self,
        homework_id: UUID,
        teacher_id: UUID,
        data: HomeworkUpdate
    ) -> Homework:
        """
        Update homework assignment.

        Args:
            homework_id: Homework UUID
            teacher_id: Teacher ID (for authorization)
            data: Update data

        Returns:
            Updated Homework object
        """
        homework = await self.homework_repo.get_by_id(homework_id)
        if not homework:
            raise AppException(
                status_code=404,
                error_code="HOMEWORK_NOT_FOUND",
                message="Homework not found"
            )

        # Check ownership
        if homework.teacher_id != teacher_id:
            raise AppException(
                status_code=403,
                error_code="NOT_HOMEWORK_OWNER",
                message="You can only update your own homework assignments"
            )

        update_dict = data.model_dump(exclude_unset=True)
        homework = await self.homework_repo.update(homework_id, update_dict)
        await self.db.commit()
        return homework

    async def delete_homework(
        self,
        homework_id: UUID,
        teacher_id: UUID
    ) -> None:
        """
        Delete homework assignment.

        Args:
            homework_id: Homework UUID
            teacher_id: Teacher ID (for authorization)
        """
        homework = await self.homework_repo.get_by_id(homework_id)
        if not homework:
            raise AppException(
                status_code=404,
                error_code="HOMEWORK_NOT_FOUND",
                message="Homework not found"
            )

        if homework.teacher_id != teacher_id:
            raise AppException(
                status_code=403,
                error_code="NOT_HOMEWORK_OWNER",
                message="You can only delete your own homework assignments"
            )

        await self.homework_repo.delete(homework_id)
        await self.db.commit()

    async def list_homework_by_teacher(
        self,
        teacher_id: UUID,
        class_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Homework], int]:
        """
        List homework created by a teacher.

        Args:
            teacher_id: Teacher UUID
            class_id: Optional class filter
            skip: Records to skip
            limit: Max records

        Returns:
            Tuple of (homework list, total count)
        """
        homework_list = await self.homework_repo.list_by_teacher(
            teacher_id=teacher_id,
            class_id=class_id,
            skip=skip,
            limit=limit
        )
        total = await self.homework_repo.count_by_teacher(teacher_id, class_id)
        return homework_list, total

    async def list_homework_by_class(
        self,
        class_id: UUID,
        subject_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[Homework], int]:
        """
        List homework for a class.

        Args:
            class_id: Class UUID
            subject_id: Optional subject filter
            skip: Records to skip
            limit: Max records

        Returns:
            Tuple of (homework list, total count)
        """
        homework_list = await self.homework_repo.list_by_class(
            class_id=class_id,
            subject_id=subject_id,
            skip=skip,
            limit=limit
        )
        total = await self.homework_repo.count_by_class(class_id, subject_id)
        return homework_list, total

    async def list_pending_homework_for_student(
        self,
        student_id: UUID,
        class_id: UUID,
        skip: int = 0,
        limit: int = 20
    ) -> List[Homework]:
        """
        List homework not yet submitted by a student.

        Args:
            student_id: Student UUID
            class_id: Student's class UUID
            skip: Records to skip
            limit: Max records

        Returns:
            List of pending homework
        """
        return await self.homework_repo.list_pending_for_student(
            student_id=student_id,
            class_id=class_id,
            skip=skip,
            limit=limit
        )

    async def list_all_homework_for_student(
        self,
        class_id: UUID,
        skip: int = 0,
        limit: int = 20
    ) -> List[Homework]:
        """
        List all homework for a student's class.

        Args:
            class_id: Student's class UUID
            skip: Records to skip
            limit: Max records

        Returns:
            List of all homework
        """
        return await self.homework_repo.list_all_for_student(
            class_id=class_id,
            skip=skip,
            limit=limit
        )
