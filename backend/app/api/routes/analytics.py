# analytics.py - Analytics and Dashboard Routes
#
# Statistics and reports for principals and teachers.

"""
Analytics Endpoints

GET    /analytics/overview           - School-wide overview (principal)
GET    /analytics/classes            - Class-wise analytics
GET    /analytics/classes/{id}       - Specific class analytics
GET    /analytics/students/{id}      - Individual student analytics
GET    /analytics/homework           - Homework completion stats
GET    /analytics/submissions        - Submission trends
GET    /analytics/ai-insights        - AI-generated insights
"""

from typing import Optional
from uuid import UUID
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    get_current_user_id,
    require_principal,
    require_teacher_or_principal,
    UserRole
)
from app.models.user import User
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.homework import Homework
from app.models.submission import Submission, SubmissionStatus
from app.models.school import SchoolClass
from app.services.user_service import UserService
from app.utils.exceptions import AppException

router = APIRouter()


@router.get(
    "/overview",
    summary="School overview",
    description="Get school-wide analytics overview"
)
async def get_overview(
    school_id: Optional[UUID] = Query(None, description="Filter by school"),
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_principal),
    db: AsyncSession = Depends(get_db)
):
    """
    Get school-wide analytics overview.

    Requires principal role.
    """
    # Count totals
    student_count = await db.execute(select(func.count(Student.id)))
    teacher_count = await db.execute(select(func.count(Teacher.id)))
    class_count = await db.execute(select(func.count(SchoolClass.id)))
    homework_count = await db.execute(select(func.count(Homework.id)))
    submission_count = await db.execute(select(func.count(Submission.id)))

    # Submission stats
    pending_count = await db.execute(
        select(func.count(Submission.id))
        .where(Submission.status == SubmissionStatus.PENDING)
    )
    graded_count = await db.execute(
        select(func.count(Submission.id))
        .where(Submission.status == SubmissionStatus.GRADED)
    )

    # Average grade
    avg_grade = await db.execute(
        select(func.avg(Submission.grade))
        .where(Submission.grade.isnot(None))
    )

    # Recent activity (last 7 days)
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    recent_submissions = await db.execute(
        select(func.count(Submission.id))
        .where(Submission.submitted_at >= week_ago)
    )
    recent_homework = await db.execute(
        select(func.count(Homework.id))
        .where(Homework.created_at >= week_ago)
    )

    return {
        "totals": {
            "students": student_count.scalar_one(),
            "teachers": teacher_count.scalar_one(),
            "classes": class_count.scalar_one(),
            "homework_assignments": homework_count.scalar_one(),
            "submissions": submission_count.scalar_one()
        },
        "submissions": {
            "pending": pending_count.scalar_one(),
            "graded": graded_count.scalar_one(),
            "average_grade": float(avg_grade.scalar_one() or 0)
        },
        "recent_activity": {
            "submissions_last_7_days": recent_submissions.scalar_one(),
            "homework_last_7_days": recent_homework.scalar_one()
        }
    }


@router.get(
    "/classes",
    summary="Class analytics",
    description="Get analytics for all classes"
)
async def get_class_analytics(
    school_id: Optional[UUID] = Query(None),
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher_or_principal),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics summary for all classes."""
    query = select(SchoolClass)
    if school_id:
        query = query.where(SchoolClass.school_id == school_id)
    query = query.order_by(SchoolClass.grade, SchoolClass.section)

    result = await db.execute(query)
    classes = result.scalars().all()

    class_stats = []
    for c in classes:
        # Get student count
        student_count = await db.execute(
            select(func.count(Student.id))
            .where(Student.class_id == c.id)
        )

        # Get homework count
        homework_count = await db.execute(
            select(func.count(Homework.id))
            .where(Homework.class_id == c.id)
        )

        # Get average grade for class
        avg_grade = await db.execute(
            select(func.avg(Submission.grade))
            .join(Homework, Submission.homework_id == Homework.id)
            .where(and_(
                Homework.class_id == c.id,
                Submission.grade.isnot(None)
            ))
        )

        class_stats.append({
            "id": str(c.id),
            "name": c.name,
            "grade": c.grade,
            "section": c.section,
            "student_count": student_count.scalar_one(),
            "homework_count": homework_count.scalar_one(),
            "average_grade": float(avg_grade.scalar_one() or 0)
        })

    return {"classes": class_stats}


@router.get(
    "/classes/{class_id}",
    summary="Specific class analytics",
    description="Get detailed analytics for a specific class"
)
async def get_class_detail_analytics(
    class_id: UUID,
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher_or_principal),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed analytics for a specific class."""
    # Verify class exists
    query = select(SchoolClass).where(SchoolClass.id == class_id)
    result = await db.execute(query)
    school_class = result.scalar_one_or_none()

    if not school_class:
        raise AppException(404, "CLASS_NOT_FOUND", "Class not found")

    # Student stats
    student_count = await db.execute(
        select(func.count(Student.id))
        .where(Student.class_id == class_id)
    )

    # Homework stats
    homework_count = await db.execute(
        select(func.count(Homework.id))
        .where(Homework.class_id == class_id)
    )

    # Submission stats
    submission_stats = await db.execute(
        select(
            func.count(Submission.id).label('total'),
            func.count(Submission.id).filter(
                Submission.status == SubmissionStatus.PENDING
            ).label('pending'),
            func.count(Submission.id).filter(
                Submission.status == SubmissionStatus.GRADED
            ).label('graded'),
            func.avg(Submission.grade).label('avg_grade')
        )
        .join(Homework, Submission.homework_id == Homework.id)
        .where(Homework.class_id == class_id)
    )
    stats = submission_stats.one()

    # Grade distribution
    grade_distribution = await db.execute(
        select(
            func.count(Submission.id).filter(Submission.grade >= 90).label('A'),
            func.count(Submission.id).filter(
                and_(Submission.grade >= 80, Submission.grade < 90)
            ).label('B'),
            func.count(Submission.id).filter(
                and_(Submission.grade >= 70, Submission.grade < 80)
            ).label('C'),
            func.count(Submission.id).filter(
                and_(Submission.grade >= 60, Submission.grade < 70)
            ).label('D'),
            func.count(Submission.id).filter(Submission.grade < 60).label('F')
        )
        .join(Homework, Submission.homework_id == Homework.id)
        .where(and_(
            Homework.class_id == class_id,
            Submission.grade.isnot(None)
        ))
    )
    grades = grade_distribution.one()

    return {
        "class": {
            "id": str(school_class.id),
            "name": school_class.name,
            "grade": school_class.grade,
            "section": school_class.section
        },
        "students": {
            "total": student_count.scalar_one()
        },
        "homework": {
            "total": homework_count.scalar_one()
        },
        "submissions": {
            "total": stats.total,
            "pending": stats.pending,
            "graded": stats.graded,
            "average_grade": float(stats.avg_grade or 0)
        },
        "grade_distribution": {
            "A": grades.A,
            "B": grades.B,
            "C": grades.C,
            "D": grades.D,
            "F": grades.F
        }
    }


@router.get(
    "/students/{student_id}",
    summary="Student analytics",
    description="Get analytics for a specific student"
)
async def get_student_analytics(
    student_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics for a specific student."""
    # Verify student exists
    query = select(Student).where(Student.id == student_id)
    result = await db.execute(query)
    student = result.scalar_one_or_none()

    if not student:
        raise AppException(404, "STUDENT_NOT_FOUND", "Student not found")

    # Submission stats
    submission_stats = await db.execute(
        select(
            func.count(Submission.id).label('total'),
            func.count(Submission.id).filter(
                Submission.status == SubmissionStatus.PENDING
            ).label('pending'),
            func.count(Submission.id).filter(
                Submission.status == SubmissionStatus.GRADED
            ).label('graded'),
            func.avg(Submission.grade).label('avg_grade'),
            func.min(Submission.grade).label('min_grade'),
            func.max(Submission.grade).label('max_grade')
        )
        .where(Submission.student_id == student_id)
    )
    stats = submission_stats.one()

    # Recent submissions
    recent = await db.execute(
        select(Submission)
        .where(Submission.student_id == student_id)
        .order_by(Submission.submitted_at.desc())
        .limit(5)
    )
    recent_submissions = recent.scalars().all()

    return {
        "student_id": str(student_id),
        "submissions": {
            "total": stats.total,
            "pending": stats.pending,
            "graded": stats.graded
        },
        "grades": {
            "average": float(stats.avg_grade or 0),
            "minimum": float(stats.min_grade or 0),
            "maximum": float(stats.max_grade or 0)
        },
        "recent_submissions": [
            {
                "id": str(s.id),
                "status": s.status.value,
                "grade": s.grade,
                "submitted_at": s.submitted_at.isoformat()
            }
            for s in recent_submissions
        ]
    }


@router.get(
    "/homework",
    summary="Homework analytics",
    description="Get homework completion statistics"
)
async def get_homework_analytics(
    class_id: Optional[UUID] = Query(None),
    days: int = Query(30, ge=1, le=365),
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher_or_principal),
    db: AsyncSession = Depends(get_db)
):
    """Get homework completion statistics."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    query = select(
        func.count(Homework.id).label('total'),
        func.count(Homework.id).filter(
            Homework.due_date >= datetime.now(timezone.utc)
        ).label('active')
    ).where(Homework.created_at >= cutoff)

    if class_id:
        query = query.where(Homework.class_id == class_id)

    result = await db.execute(query)
    stats = result.one()

    return {
        "period_days": days,
        "homework": {
            "total_created": stats.total,
            "currently_active": stats.active
        }
    }


@router.get(
    "/trends",
    summary="Submission trends",
    description="Get submission trends over time"
)
async def get_submission_trends(
    days: int = Query(30, ge=7, le=90),
    user_id: str = Depends(get_current_user_id),
    _: bool = Depends(require_teacher_or_principal),
    db: AsyncSession = Depends(get_db)
):
    """Get submission trends over time."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    # Daily submission counts
    result = await db.execute(
        select(
            func.date(Submission.submitted_at).label('date'),
            func.count(Submission.id).label('count')
        )
        .where(Submission.submitted_at >= cutoff)
        .group_by(func.date(Submission.submitted_at))
        .order_by(func.date(Submission.submitted_at))
    )

    trends = result.all()

    return {
        "period_days": days,
        "daily_submissions": [
            {
                "date": str(t.date),
                "count": t.count
            }
            for t in trends
        ]
    }
