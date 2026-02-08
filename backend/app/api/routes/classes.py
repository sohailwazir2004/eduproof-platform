# classes.py - Class Management Routes
#
# CRUD operations for classes and subjects (admin access).

"""
Class Endpoints

POST   /classes                 - Create class
GET    /classes                 - List classes
GET    /classes/{id}            - Get class details
PUT    /classes/{id}            - Update class
DELETE /classes/{id}            - Delete class
GET    /classes/{id}/students   - Get students in class
GET    /classes/{id}/teachers   - Get teachers for class

Subject Endpoints

POST   /subjects                - Create subject
GET    /subjects                - List subjects
GET    /subjects/{id}           - Get subject details
PUT    /subjects/{id}           - Update subject
DELETE /subjects/{id}           - Delete subject
"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.core.security import (
    get_current_user_id,
    require_principal,
    require_admin
)
from app.models.school import SchoolClass, Subject
from app.schemas.common import MessageResponse, PaginatedResponse
from app.utils.exceptions import AppException

router = APIRouter()


# Schemas
class ClassCreate(BaseModel):
    name: str = Field(..., max_length=50)
    grade: int = Field(..., ge=1, le=12)
    section: str = Field(..., max_length=10)
    school_id: UUID


class ClassUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    grade: Optional[int] = Field(None, ge=1, le=12)
    section: Optional[str] = Field(None, max_length=10)


class SubjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=20)
    school_id: UUID
    description: Optional[str] = None


class SubjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None


# Class routes
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a class"
)
async def create_class(
    data: ClassCreate,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_principal),
    db: AsyncSession = Depends(get_db)
):
    """Create a new class. Requires principal role."""
    school_class = SchoolClass(
        name=data.name,
        grade=data.grade,
        section=data.section,
        school_id=data.school_id
    )

    db.add(school_class)
    await db.commit()
    await db.refresh(school_class)

    return {
        "id": str(school_class.id),
        "name": school_class.name,
        "grade": school_class.grade,
        "section": school_class.section,
        "school_id": str(school_class.school_id),
        "created_at": school_class.created_at.isoformat()
    }


@router.get(
    "",
    response_model=PaginatedResponse,
    summary="List classes"
)
async def list_classes(
    school_id: Optional[UUID] = Query(None),
    grade: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """List all classes with optional filters."""
    query = select(SchoolClass)

    if school_id:
        query = query.where(SchoolClass.school_id == school_id)
    if grade:
        query = query.where(SchoolClass.grade == grade)

    query = query.order_by(SchoolClass.grade, SchoolClass.section)
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    classes = result.scalars().all()

    count_query = select(func.count(SchoolClass.id))
    if school_id:
        count_query = count_query.where(SchoolClass.school_id == school_id)
    if grade:
        count_query = count_query.where(SchoolClass.grade == grade)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    return PaginatedResponse(
        items=[{
            "id": str(c.id),
            "name": c.name,
            "grade": c.grade,
            "section": c.section,
            "school_id": str(c.school_id)
        } for c in classes],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{class_id}",
    summary="Get class details"
)
async def get_class(
    class_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get class details with student/teacher counts."""
    query = (
        select(SchoolClass)
        .where(SchoolClass.id == class_id)
        .options(
            selectinload(SchoolClass.students),
            selectinload(SchoolClass.teachers),
            selectinload(SchoolClass.school)
        )
    )

    result = await db.execute(query)
    school_class = result.scalar_one_or_none()

    if not school_class:
        raise AppException(404, "CLASS_NOT_FOUND", "Class not found")

    return {
        "id": str(school_class.id),
        "name": school_class.name,
        "grade": school_class.grade,
        "section": school_class.section,
        "school_id": str(school_class.school_id),
        "student_count": len(school_class.students) if school_class.students else 0,
        "teacher_count": len(school_class.teachers) if school_class.teachers else 0,
        "school": {
            "id": str(school_class.school.id),
            "name": school_class.school.name
        } if school_class.school else None
    }


@router.put(
    "/{class_id}",
    summary="Update class"
)
async def update_class(
    class_id: UUID,
    data: ClassUpdate,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_principal),
    db: AsyncSession = Depends(get_db)
):
    """Update a class. Requires principal role."""
    query = select(SchoolClass).where(SchoolClass.id == class_id)
    result = await db.execute(query)
    school_class = result.scalar_one_or_none()

    if not school_class:
        raise AppException(404, "CLASS_NOT_FOUND", "Class not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(school_class, field, value)

    await db.commit()
    await db.refresh(school_class)

    return {
        "id": str(school_class.id),
        "name": school_class.name,
        "grade": school_class.grade,
        "section": school_class.section
    }


@router.delete(
    "/{class_id}",
    response_model=MessageResponse,
    summary="Delete class"
)
async def delete_class(
    class_id: UUID,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Delete a class. Requires admin role."""
    query = select(SchoolClass).where(SchoolClass.id == class_id)
    result = await db.execute(query)
    school_class = result.scalar_one_or_none()

    if not school_class:
        raise AppException(404, "CLASS_NOT_FOUND", "Class not found")

    await db.delete(school_class)
    await db.commit()

    return MessageResponse(message="Class deleted successfully")


@router.get(
    "/{class_id}/students",
    response_model=PaginatedResponse,
    summary="Get students in class"
)
async def get_class_students(
    class_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get all students enrolled in a class."""
    query = (
        select(SchoolClass)
        .where(SchoolClass.id == class_id)
        .options(selectinload(SchoolClass.students))
    )

    result = await db.execute(query)
    school_class = result.scalar_one_or_none()

    if not school_class:
        raise AppException(404, "CLASS_NOT_FOUND", "Class not found")

    students = school_class.students[skip:skip + limit] if school_class.students else []

    return PaginatedResponse(
        items=[{
            "id": str(s.id),
            "roll_number": s.roll_number,
            "admission_number": s.admission_number
        } for s in students],
        total=len(school_class.students) if school_class.students else 0,
        skip=skip,
        limit=limit
    )
