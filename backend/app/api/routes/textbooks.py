# textbooks.py - Textbook Management Routes
#
# Upload and manage PDF textbooks (teacher/admin access).

"""
Textbook Endpoints

POST   /textbooks                - Upload textbook PDF
GET    /textbooks                - List textbooks
GET    /textbooks/{id}           - Get textbook details
GET    /textbooks/{id}/download  - Download textbook file
DELETE /textbooks/{id}           - Delete textbook
POST   /textbooks/{id}/index     - Trigger AI indexing
"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    get_current_user_id,
    require_teacher,
    require_teacher_or_principal,
    UserRole
)
from app.schemas.common import MessageResponse, PaginatedResponse
from app.services.storage_service import StorageService
from app.services.user_service import UserService
from app.services.textbook_service import TextbookService
from app.utils.exceptions import AppException

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Upload textbook",
    description="Upload a PDF textbook file"
)
async def upload_textbook(
    title: str = Form(..., description="Textbook title"),
    subject_id: UUID = Form(..., description="Subject ID"),
    class_id: UUID = Form(..., description="Class ID"),
    file: UploadFile = File(..., description="PDF file"),
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a textbook PDF.

    Requires teacher role.

    - **title**: Textbook title
    - **subject_id**: Associated subject ID
    - **class_id**: Associated class ID
    - **file**: PDF file to upload
    """
    # Validate file type
    if file.content_type != "application/pdf":
        raise AppException(
            status_code=400,
            error_code="INVALID_FILE_TYPE",
            message="Only PDF files are allowed"
        )

    user_service = UserService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if not user.teacher:
        raise AppException(
            status_code=400,
            error_code="TEACHER_PROFILE_REQUIRED",
            message="Teacher profile not found"
        )

    # Upload file
    storage_service = StorageService()
    file_url = await storage_service.upload_file(
        file=file,
        folder=f"textbooks/{subject_id}"
    )

    # Create textbook record
    textbook_service = TextbookService(db)
    textbook = await textbook_service.create_textbook(
        title=title,
        subject_id=subject_id,
        class_id=class_id,
        file_url=file_url,
        uploaded_by=user.teacher.id
    )

    return textbook


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="List textbooks",
    description="List textbooks with filters"
)
async def list_textbooks(
    subject_id: Optional[UUID] = Query(None, description="Filter by subject"),
    class_id: Optional[UUID] = Query(None, description="Filter by class"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Records per page"),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    List textbooks with optional filters.
    """
    textbook_service = TextbookService(db)
    textbooks, total = await textbook_service.list_textbooks(
        subject_id=subject_id,
        class_id=class_id,
        skip=skip,
        limit=limit
    )

    return PaginatedResponse(
        items=textbooks,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{textbook_id}",
    summary="Get textbook details",
    description="Get detailed information about a textbook"
)
async def get_textbook(
    textbook_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get textbook details.
    """
    textbook_service = TextbookService(db)
    return await textbook_service.get_textbook(textbook_id)


@router.get(
    "/{textbook_id}/download",
    summary="Download textbook",
    description="Get download URL for textbook file"
)
async def download_textbook(
    textbook_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get download URL for textbook.
    Redirects to the file URL.
    """
    textbook_service = TextbookService(db)
    textbook = await textbook_service.get_textbook(textbook_id)

    storage_service = StorageService()
    download_url = storage_service.generate_presigned_url(
        textbook["file_url"],
        expiry_seconds=3600
    )

    return RedirectResponse(url=download_url)


@router.delete(
    "/{textbook_id}",
    response_model=MessageResponse,
    summary="Delete textbook",
    description="Delete a textbook"
)
async def delete_textbook(
    textbook_id: UUID,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher_or_principal),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a textbook.

    Requires teacher or principal role.
    """
    textbook_service = TextbookService(db)
    await textbook_service.delete_textbook(textbook_id)
    return MessageResponse(message="Textbook deleted successfully")


@router.post(
    "/{textbook_id}/index",
    response_model=MessageResponse,
    summary="Trigger AI indexing",
    description="Trigger AI indexing of textbook content"
)
async def index_textbook(
    textbook_id: UUID,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher),
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger AI indexing for a textbook.

    Queues the textbook for content extraction and indexing.
    """
    textbook_service = TextbookService(db)
    await textbook_service.trigger_indexing(textbook_id)
    return MessageResponse(message="Indexing triggered successfully")
