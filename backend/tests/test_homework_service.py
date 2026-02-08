# test_homework_service.py - Homework Service Tests
#
# Test homework CRUD operations

"""
Homework Service Tests

Test cases:
- Create homework
- Get homework by ID
- Update homework
- Delete homework
- List homework by teacher
- List homework by class
- Get submission stats
"""

import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.services.homework_service import HomeworkService
from app.schemas.homework import HomeworkCreate, HomeworkUpdate
from app.utils.exceptions import AppException


@pytest.mark.asyncio
async def test_create_homework(db_session, sample_teacher, sample_class):
    """Test creating a homework assignment."""
    service = HomeworkService(db_session)

    due_date = datetime.now(timezone.utc) + timedelta(days=7)
    data = HomeworkCreate(
        title="Test Homework",
        description="Complete exercises 1-10",
        class_id=sample_class.id,
        page_numbers="45-48",
        due_date=due_date
    )

    homework = await service.create_homework(
        teacher_id=sample_teacher.id,
        data=data
    )

    assert homework.id is not None
    assert homework.title == "Test Homework"
    assert homework.teacher_id == sample_teacher.id
    assert homework.class_id == sample_class.id


@pytest.mark.asyncio
async def test_get_homework(db_session, sample_homework):
    """Test getting homework by ID."""
    service = HomeworkService(db_session)

    result = await service.get_homework(sample_homework.id)

    assert result.id == sample_homework.id
    assert result.title == sample_homework.title


@pytest.mark.asyncio
async def test_get_homework_not_found(db_session):
    """Test getting non-existent homework."""
    service = HomeworkService(db_session)

    with pytest.raises(AppException) as exc_info:
        await service.get_homework(uuid4())

    assert exc_info.value.status_code == 404
    assert exc_info.value.error_code == "HOMEWORK_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_homework(db_session, sample_homework, sample_teacher):
    """Test updating homework."""
    service = HomeworkService(db_session)

    update_data = HomeworkUpdate(
        title="Updated Homework Title",
        description="Updated description"
    )

    homework = await service.update_homework(
        homework_id=sample_homework.id,
        teacher_id=sample_teacher.id,
        data=update_data
    )

    assert homework.title == "Updated Homework Title"
    assert homework.description == "Updated description"


@pytest.mark.asyncio
async def test_update_homework_unauthorized(db_session, sample_homework):
    """Test updating homework by different teacher."""
    service = HomeworkService(db_session)

    other_teacher_id = uuid4()
    update_data = HomeworkUpdate(title="Hacked!")

    with pytest.raises(AppException) as exc_info:
        await service.update_homework(
            homework_id=sample_homework.id,
            teacher_id=other_teacher_id,
            data=update_data
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.error_code == "NOT_HOMEWORK_OWNER"


@pytest.mark.asyncio
async def test_delete_homework(db_session, sample_homework, sample_teacher):
    """Test deleting homework."""
    service = HomeworkService(db_session)

    await service.delete_homework(
        homework_id=sample_homework.id,
        teacher_id=sample_teacher.id
    )

    # Verify it's deleted
    with pytest.raises(AppException):
        await service.get_homework(sample_homework.id)


@pytest.mark.asyncio
async def test_delete_homework_unauthorized(db_session, sample_homework):
    """Test deleting homework by different teacher."""
    service = HomeworkService(db_session)

    other_teacher_id = uuid4()

    with pytest.raises(AppException) as exc_info:
        await service.delete_homework(
            homework_id=sample_homework.id,
            teacher_id=other_teacher_id
        )

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_list_homework_by_teacher(db_session, sample_teacher, sample_class):
    """Test listing homework by teacher."""
    service = HomeworkService(db_session)

    # Create multiple homework
    for i in range(3):
        due_date = datetime.now(timezone.utc) + timedelta(days=i+1)
        data = HomeworkCreate(
            title=f"Homework {i+1}",
            description=f"Description {i+1}",
            class_id=sample_class.id,
            due_date=due_date
        )
        await service.create_homework(sample_teacher.id, data)

    # List homework
    homework_list, total = await service.list_homework_by_teacher(
        teacher_id=sample_teacher.id,
        skip=0,
        limit=10
    )

    assert total >= 3
    assert len(homework_list) >= 3


@pytest.mark.asyncio
async def test_list_homework_by_class(db_session, sample_teacher, sample_class):
    """Test listing homework by class."""
    service = HomeworkService(db_session)

    # Create homework for class
    due_date = datetime.now(timezone.utc) + timedelta(days=7)
    data = HomeworkCreate(
        title="Class Homework",
        description="For the whole class",
        class_id=sample_class.id,
        due_date=due_date
    )
    await service.create_homework(sample_teacher.id, data)

    # List homework
    homework_list, total = await service.list_homework_by_class(
        class_id=sample_class.id,
        skip=0,
        limit=10
    )

    assert total >= 1
    assert len(homework_list) >= 1
    assert all(h.class_id == sample_class.id for h in homework_list)


@pytest.mark.asyncio
async def test_list_homework_with_pagination(db_session, sample_teacher, sample_class):
    """Test homework listing pagination."""
    service = HomeworkService(db_session)

    # Create 5 homework
    for i in range(5):
        due_date = datetime.now(timezone.utc) + timedelta(days=i+1)
        data = HomeworkCreate(
            title=f"Homework {i+1}",
            class_id=sample_class.id,
            due_date=due_date
        )
        await service.create_homework(sample_teacher.id, data)

    # Test pagination
    page1, total = await service.list_homework_by_teacher(
        teacher_id=sample_teacher.id,
        skip=0,
        limit=2
    )

    page2, _ = await service.list_homework_by_teacher(
        teacher_id=sample_teacher.id,
        skip=2,
        limit=2
    )

    assert len(page1) == 2
    assert len(page2) == 2
    assert page1[0].id != page2[0].id  # Different items
    assert total >= 5
