# textbook_service.py - Textbook Service
#
# Business logic for textbook management and indexing.

"""
Textbook Service

Methods:
- create_textbook(title, subject_id, class_id, file_url, uploaded_by) -> Textbook
- get_textbook(textbook_id) -> dict
- delete_textbook(textbook_id) -> None
- list_textbooks(filters) -> List[dict]
- trigger_indexing(textbook_id) -> None
"""

from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.textbook import Textbook
from app.utils.exceptions import AppException


class TextbookService:
    """Service for textbook management operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_textbook(
        self,
        title: str,
        subject_id: UUID,
        class_id: UUID,
        file_url: str,
        uploaded_by: UUID
    ) -> dict:
        """
        Create a new textbook record.

        Args:
            title: Textbook title
            subject_id: Subject ID
            class_id: Class ID
            file_url: URL of uploaded PDF
            uploaded_by: Teacher ID

        Returns:
            Created textbook data
        """
        textbook = Textbook(
            title=title,
            subject_id=subject_id,
            class_id=class_id,
            file_url=file_url,
            uploaded_by=uploaded_by,
            is_indexed=False
        )

        self.db.add(textbook)
        await self.db.commit()
        await self.db.refresh(textbook)

        return {
            "id": str(textbook.id),
            "title": textbook.title,
            "subject_id": str(textbook.subject_id),
            "class_id": str(textbook.class_id),
            "file_url": textbook.file_url,
            "is_indexed": textbook.is_indexed,
            "created_at": textbook.created_at.isoformat()
        }

    async def get_textbook(self, textbook_id: UUID) -> dict:
        """
        Get textbook by ID.

        Args:
            textbook_id: Textbook UUID

        Returns:
            Textbook data
        """
        query = (
            select(Textbook)
            .where(Textbook.id == textbook_id)
            .options(
                selectinload(Textbook.subject),
                selectinload(Textbook.school_class)
            )
        )

        result = await self.db.execute(query)
        textbook = result.scalar_one_or_none()

        if not textbook:
            raise AppException(
                status_code=404,
                error_code="TEXTBOOK_NOT_FOUND",
                message="Textbook not found"
            )

        return {
            "id": str(textbook.id),
            "title": textbook.title,
            "subject_id": str(textbook.subject_id),
            "class_id": str(textbook.class_id),
            "file_url": textbook.file_url,
            "page_count": textbook.page_count,
            "is_indexed": textbook.is_indexed,
            "subject": {
                "id": str(textbook.subject.id),
                "name": textbook.subject.name
            } if textbook.subject else None,
            "school_class": {
                "id": str(textbook.school_class.id),
                "name": textbook.school_class.name,
                "grade": textbook.school_class.grade
            } if textbook.school_class else None,
            "created_at": textbook.created_at.isoformat(),
            "updated_at": textbook.updated_at.isoformat()
        }

    async def delete_textbook(self, textbook_id: UUID) -> None:
        """
        Delete a textbook.

        Args:
            textbook_id: Textbook UUID
        """
        query = select(Textbook).where(Textbook.id == textbook_id)
        result = await self.db.execute(query)
        textbook = result.scalar_one_or_none()

        if not textbook:
            raise AppException(
                status_code=404,
                error_code="TEXTBOOK_NOT_FOUND",
                message="Textbook not found"
            )

        await self.db.delete(textbook)
        await self.db.commit()

    async def list_textbooks(
        self,
        subject_id: Optional[UUID] = None,
        class_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[List[dict], int]:
        """
        List textbooks with optional filters.

        Args:
            subject_id: Filter by subject
            class_id: Filter by class
            skip: Records to skip
            limit: Max records

        Returns:
            Tuple of (textbook list, total count)
        """
        query = select(Textbook)

        filters = []
        if subject_id:
            filters.append(Textbook.subject_id == subject_id)
        if class_id:
            filters.append(Textbook.class_id == class_id)

        if filters:
            query = query.where(and_(*filters))

        query = query.options(
            selectinload(Textbook.subject),
            selectinload(Textbook.school_class)
        )
        query = query.order_by(Textbook.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        textbooks = result.scalars().all()

        # Count total
        count_query = select(func.count(Textbook.id))
        if filters:
            count_query = count_query.where(and_(*filters))
        count_result = await self.db.execute(count_query)
        total = count_result.scalar_one()

        textbook_list = [
            {
                "id": str(t.id),
                "title": t.title,
                "subject_id": str(t.subject_id),
                "class_id": str(t.class_id),
                "file_url": t.file_url,
                "page_count": t.page_count,
                "is_indexed": t.is_indexed,
                "subject": {
                    "id": str(t.subject.id),
                    "name": t.subject.name
                } if t.subject else None,
                "school_class": {
                    "id": str(t.school_class.id),
                    "name": t.school_class.name,
                    "grade": t.school_class.grade
                } if t.school_class else None,
                "created_at": t.created_at.isoformat()
            }
            for t in textbooks
        ]

        return textbook_list, total

    async def trigger_indexing(self, textbook_id: UUID) -> None:
        """
        Trigger AI indexing for a textbook.

        Args:
            textbook_id: Textbook UUID
        """
        query = select(Textbook).where(Textbook.id == textbook_id)
        result = await self.db.execute(query)
        textbook = result.scalar_one_or_none()

        if not textbook:
            raise AppException(
                status_code=404,
                error_code="TEXTBOOK_NOT_FOUND",
                message="Textbook not found"
            )

        # TODO: Integrate with AI service for PDF indexing
        # For now, just mark as pending indexing
        # This would typically queue a background job
        pass

    async def update_page_count(self, textbook_id: UUID, page_count: int) -> None:
        """
        Update textbook page count.

        Args:
            textbook_id: Textbook UUID
            page_count: Number of pages
        """
        query = select(Textbook).where(Textbook.id == textbook_id)
        result = await self.db.execute(query)
        textbook = result.scalar_one_or_none()

        if textbook:
            textbook.page_count = page_count
            await self.db.commit()

    async def mark_as_indexed(self, textbook_id: UUID) -> None:
        """
        Mark textbook as indexed.

        Args:
            textbook_id: Textbook UUID
        """
        query = select(Textbook).where(Textbook.id == textbook_id)
        result = await self.db.execute(query)
        textbook = result.scalar_one_or_none()

        if textbook:
            textbook.is_indexed = True
            await self.db.commit()
