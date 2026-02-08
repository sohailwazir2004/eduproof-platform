# homework.py - Homework Assignment Routes
#
# CRUD operations for homework assignments (teacher access).

"""
Homework Endpoints

POST   /homework                - Create homework assignment
GET    /homework                - List homework (filtered by role)
GET    /homework/{id}           - Get homework details
PUT    /homework/{id}           - Update homework (teacher only)
DELETE /homework/{id}           - Delete homework (teacher only)
GET    /homework/{id}/submissions - Get all submissions for homework
"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    get_current_user_id,
    require_teacher,
    require_teacher_or_principal,
    UserRole
)
from app.schemas.homework import (
    HomeworkCreate,
    HomeworkUpdate,
    HomeworkResponse,
    HomeworkListResponse
)
from app.schemas.common import MessageResponse, PaginatedResponse
from app.services.homework_service import HomeworkService
from app.services.user_service import UserService

router = APIRouter()


@router.post(
    "",
    response_model=HomeworkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create homework assignment",
    description="Create a new homework assignment for a class"
)
async def create_homework(
    data: HomeworkCreate,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new homework assignment.

    Requires teacher role.

    - **title**: Homework title
    - **description**: Detailed instructions
    - **class_id**: Target class ID
    - **subject_id**: Subject ID (optional)
    - **textbook_id**: Reference textbook ID (optional)
    - **page_numbers**: Textbook pages (optional)
    - **due_date**: Submission deadline
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if not user.teacher:
        from app.utils.exceptions import AppException
        raise AppException(
            status_code=400,
            error_code="TEACHER_PROFILE_REQUIRED",
            message="Teacher profile not found"
        )

    homework_service = HomeworkService(db)
    homework = await homework_service.create_homework(
        teacher_id=user.teacher.id,
        data=data
    )

    return await homework_service.get_homework(homework.id)


@router.get(
    "",
    response_model=HomeworkListResponse,
    summary="List homework assignments",
    description="List homework with filters based on user role"
)
async def list_homework(
    class_id: Optional[UUID] = Query(None, description="Filter by class"),
    subject_id: Optional[UUID] = Query(None, description="Filter by subject"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Records per page"),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    List homework assignments.

    - Teachers see homework they created
    - Students see homework for their class
    - Parents see homework for their children's classes
    - Principals see all homework
    """
    user_service = UserService(db)
    homework_service = HomeworkService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if user.role == UserRole.TEACHER and user.teacher:
        homework_list, total = await homework_service.list_homework_by_teacher(
            teacher_id=user.teacher.id,
            class_id=class_id,
            skip=skip,
            limit=limit
        )
    elif user.role == UserRole.STUDENT and user.student and user.student.class_id:
        homework_list, total = await homework_service.list_homework_by_class(
            class_id=user.student.class_id,
            subject_id=subject_id,
            skip=skip,
            limit=limit
        )
    elif class_id:
        homework_list, total = await homework_service.list_homework_by_class(
            class_id=class_id,
            subject_id=subject_id,
            skip=skip,
            limit=limit
        )
    else:
        homework_list, total = [], 0

    return HomeworkListResponse(
        items=[HomeworkResponse.model_validate(h) for h in homework_list],
        total=total,
        skip=skip,
        limit=limit,
        has_more=skip + len(homework_list) < total
    )


@router.get(
    "/{homework_id}",
    response_model=HomeworkResponse,
    summary="Get homework details",
    description="Get detailed information about a homework assignment"
)
async def get_homework(
    homework_id: UUID,
    include_stats: bool = Query(False, description="Include submission statistics"),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Get homework assignment details.

    - **include_stats**: Include submission statistics (teacher only)
    """
    homework_service = HomeworkService(db)
    return await homework_service.get_homework(homework_id, include_stats=include_stats)


@router.put(
    "/{homework_id}",
    response_model=HomeworkResponse,
    summary="Update homework",
    description="Update a homework assignment (teacher only)"
)
async def update_homework(
    homework_id: UUID,
    data: HomeworkUpdate,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a homework assignment.

    Requires teacher role. Teachers can only update their own assignments.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if not user.teacher:
        from app.utils.exceptions import AppException
        raise AppException(
            status_code=400,
            error_code="TEACHER_PROFILE_REQUIRED",
            message="Teacher profile not found"
        )

    homework_service = HomeworkService(db)
    await homework_service.update_homework(
        homework_id=homework_id,
        teacher_id=user.teacher.id,
        data=data
    )

    return await homework_service.get_homework(homework_id)


@router.delete(
    "/{homework_id}",
    response_model=MessageResponse,
    summary="Delete homework",
    description="Delete a homework assignment (teacher only)"
)
async def delete_homework(
    homework_id: UUID,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a homework assignment.

    Requires teacher role. Teachers can only delete their own assignments.
    This will also delete all associated submissions.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_id(UUID(user_id))

    if not user.teacher:
        from app.utils.exceptions import AppException
        raise AppException(
            status_code=400,
            error_code="TEACHER_PROFILE_REQUIRED",
            message="Teacher profile not found"
        )

    homework_service = HomeworkService(db)
    await homework_service.delete_homework(
        homework_id=homework_id,
        teacher_id=user.teacher.id
    )

    return MessageResponse(message="Homework deleted successfully")


@router.get(
    "/{homework_id}/submissions",
    response_model=PaginatedResponse,
    summary="Get homework submissions",
    description="Get all submissions for a homework assignment"
)
async def get_homework_submissions(
    homework_id: UUID,
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Records per page"),
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher_or_principal),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all submissions for a homework assignment.

    Requires teacher or principal role.
    """
    from app.services.submission_service import SubmissionService
    from app.schemas.submission import SubmissionResponse

    submission_service = SubmissionService(db)
    submissions, total = await submission_service.list_submissions_by_homework(
        homework_id=homework_id,
        status_filter=status_filter,
        skip=skip,
        limit=limit
    )

    return PaginatedResponse(
        items=[SubmissionResponse.model_validate(s) for s in submissions],
        total=total,
        skip=skip,
        limit=limit
    )
