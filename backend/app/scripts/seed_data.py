# seed_data.py - Database Seed Script
#
# Populates database with sample data for testing and demo

"""
Database Seed Script

Creates:
- 1 School
- 1 Principal
- 5 Teachers
- 3 Subjects (Math, Science, English)
- 5 Classes (Grade 6-10)
- 20 Students (4 per class)
- 3 Parents (for some students)
- 15 Homework assignments
- 30 Submissions (with grades)
- 3 Textbooks

Usage:
    python -m app.scripts.seed_data
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
from uuid import uuid4

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import select
from app.core.database import get_async_session, init_db
from app.core.security import get_password_hash, UserRole
from app.models.user import User
from app.models.teacher import Teacher
from app.models.student import Student
from app.models.parent import Parent
from app.models.principal import Principal
from app.models.school import School, SchoolClass, Subject
from app.models.homework import Homework
from app.models.submission import Submission, SubmissionStatus
from app.models.textbook import Textbook


async def clear_data(db):
    """Clear existing data."""
    print("🗑️  Clearing existing data...")

    # Delete in correct order (respecting foreign keys)
    await db.execute("DELETE FROM submissions")
    await db.execute("DELETE FROM homework")
    await db.execute("DELETE FROM textbooks")
    await db.execute("DELETE FROM students")
    await db.execute("DELETE FROM teachers")
    await db.execute("DELETE FROM parents")
    await db.execute("DELETE FROM principals")
    await db.execute("DELETE FROM subjects")
    await db.execute("DELETE FROM classes")
    await db.execute("DELETE FROM schools")
    await db.execute("DELETE FROM users")

    await db.commit()
    print("✅ Data cleared")


async def create_school(db):
    """Create school."""
    print("\n🏫 Creating school...")

    school = School(
        name="Springfield High School",
        address="742 Evergreen Terrace, Springfield",
        phone="+1-555-0100",
        email="info@springfield-high.edu",
        website="https://springfield-high.edu"
    )
    db.add(school)
    await db.flush()
    await db.refresh(school)

    print(f"✅ Created school: {school.name}")
    return school


async def create_subjects(db, school):
    """Create subjects."""
    print("\n📚 Creating subjects...")

    subjects_data = [
        {"name": "Mathematics", "code": "MATH", "description": "Math and Algebra"},
        {"name": "Science", "code": "SCI", "description": "Physics and Chemistry"},
        {"name": "English", "code": "ENG", "description": "English Literature"}
    ]

    subjects = []
    for data in subjects_data:
        subject = Subject(
            name=data["name"],
            code=data["code"],
            description=data["description"],
            school_id=school.id
        )
        db.add(subject)
        subjects.append(subject)

    await db.flush()
    print(f"✅ Created {len(subjects)} subjects")
    return subjects


async def create_classes(db, school):
    """Create classes."""
    print("\n🎓 Creating classes...")

    classes = []
    for grade in range(6, 11):  # Grades 6-10
        school_class = SchoolClass(
            name=f"Class {grade}A",
            grade=grade,
            section="A",
            school_id=school.id,
            academic_year="2024-2025"
        )
        db.add(school_class)
        classes.append(school_class)

    await db.flush()
    print(f"✅ Created {len(classes)} classes")
    return classes


async def create_principal(db, school):
    """Create principal user."""
    print("\n👔 Creating principal...")

    user = User(
        email="principal@springfield-high.edu",
        first_name="Seymour",
        last_name="Skinner",
        phone="+1-555-0101",
        role=UserRole.PRINCIPAL,
        hashed_password=get_password_hash("principal123"),
        is_verified=True,
        is_active=True
    )
    db.add(user)
    await db.flush()

    principal = Principal(
        user_id=user.id,
        school_id=school.id,
        employee_id="P001",
        qualification="Ph.D. Education",
        date_of_joining=datetime(2010, 8, 1),
        years_of_experience=25
    )
    db.add(principal)
    await db.flush()

    print(f"✅ Created principal: {user.email}")
    print(f"   Password: principal123")
    return principal


async def create_teachers(db, school, subjects):
    """Create teachers."""
    print("\n👨‍🏫 Creating teachers...")

    teachers_data = [
        {"first_name": "Edna", "last_name": "Krabappel", "email": "edna.k@springfield-high.edu", "subject": "English"},
        {"first_name": "Elizabeth", "last_name": "Hoover", "email": "elizabeth.h@springfield-high.edu", "subject": "Mathematics"},
        {"first_name": "John", "last_name": "Frink", "email": "john.f@springfield-high.edu", "subject": "Science"},
        {"first_name": "Dewey", "last_name": "Largo", "email": "dewey.l@springfield-high.edu", "subject": "Mathematics"},
        {"first_name": "Groundskeeper", "last_name": "Willie", "email": "willie@springfield-high.edu", "subject": "Science"}
    ]

    teachers = []
    for i, data in enumerate(teachers_data):
        user = User(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=f"+1-555-010{i+2}",
            role=UserRole.TEACHER,
            hashed_password=get_password_hash("teacher123"),
            is_verified=True,
            is_active=True
        )
        db.add(user)
        await db.flush()

        teacher = Teacher(
            user_id=user.id,
            school_id=school.id,
            employee_id=f"T{i+1:03d}",
            department=data["subject"],
            qualification="M.Ed.",
            specialization=data["subject"],
            date_of_joining=datetime(2015 + i, 9, 1)
        )
        db.add(teacher)
        teachers.append(teacher)

    await db.flush()
    print(f"✅ Created {len(teachers)} teachers")
    print(f"   Password for all: teacher123")
    return teachers


async def create_students(db, classes):
    """Create students."""
    print("\n👦 Creating students...")

    first_names = ["Bart", "Lisa", "Milhouse", "Ralph", "Nelson", "Martin", "Sherri", "Terri", "Wendell", "Database",
                   "Jimbo", "Dolph", "Kearney", "Jessica", "Allison", "Janey", "Lewis", "Richard", "Uter", "Rod"]
    last_names = ["Simpson", "Van Houten", "Wiggum", "Muntz", "Prince", "Bouvier", "Powell", "Jones", "Brown", "Smith",
                  "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Garcia", "Martinez", "Robinson"]

    students = []
    student_idx = 0

    for class_obj in classes:
        for i in range(4):  # 4 students per class
            if student_idx >= len(first_names):
                break

            user = User(
                email=f"student{student_idx+1}@springfield-high.edu",
                first_name=first_names[student_idx],
                last_name=last_names[student_idx],
                phone=f"+1-555-020{student_idx}",
                role=UserRole.STUDENT,
                hashed_password=get_password_hash("student123"),
                is_verified=True,
                is_active=True
            )
            db.add(user)
            await db.flush()

            student = Student(
                user_id=user.id,
                class_id=class_obj.id,
                roll_number=f"S{class_obj.grade:02d}{i+1:02d}",
                admission_number=f"ADM{2024}{student_idx+1:04d}",
                admission_date=datetime(2024, 4, 1),
                date_of_birth=datetime(2024 - class_obj.grade - 6, 5, 15),
                gender="Male" if student_idx % 2 == 0 else "Female",
                blood_group=["A+", "B+", "O+", "AB+"][student_idx % 4],
                address=f"{742 + student_idx} Evergreen Terrace, Springfield"
            )
            db.add(student)
            students.append(student)
            student_idx += 1

    await db.flush()
    print(f"✅ Created {len(students)} students")
    print(f"   Password for all: student123")
    return students


async def create_parents(db, students):
    """Create parents for some students."""
    print("\n👪 Creating parents...")

    parents = []
    for i in range(0, min(6, len(students)), 2):  # Create 3 parents
        student = students[i]

        user = User(
            email=f"parent{i//2+1}@springfield-high.edu",
            first_name=student.user.first_name + "'s",
            last_name="Parent",
            phone=f"+1-555-030{i}",
            role=UserRole.PARENT,
            hashed_password=get_password_hash("parent123"),
            is_verified=True,
            is_active=True
        )
        db.add(user)
        await db.flush()

        parent = Parent(
            user_id=user.id,
            occupation="Engineer" if i % 2 == 0 else "Doctor",
            work_phone=f"+1-555-031{i}",
            address=student.address,
            emergency_contact=user.phone,
            relationship_type="Father" if i % 2 == 0 else "Mother"
        )
        db.add(parent)
        parents.append(parent)

    await db.flush()
    print(f"✅ Created {len(parents)} parents")
    print(f"   Password for all: parent123")
    return parents


async def create_textbooks(db, classes, subjects):
    """Create textbooks."""
    print("\n📖 Creating textbooks...")

    textbooks = []
    for i, subject in enumerate(subjects[:3]):  # Create 3 textbooks
        class_obj = classes[i % len(classes)]

        textbook = Textbook(
            title=f"{subject.name} Grade {class_obj.grade}",
            subject_id=subject.id,
            class_id=class_obj.id,
            file_url=f"https://example.com/textbooks/{subject.code.lower()}_grade_{class_obj.grade}.pdf",
            uploaded_by=uuid4(),  # Placeholder
            page_count=200 + (i * 50),
            is_indexed=True
        )
        db.add(textbook)
        textbooks.append(textbook)

    await db.flush()
    print(f"✅ Created {len(textbooks)} textbooks")
    return textbooks


async def create_homework(db, teachers, classes, subjects):
    """Create homework assignments."""
    print("\n📝 Creating homework assignments...")

    homework_list = []
    homework_titles = [
        "Chapter 1 Exercises",
        "Weekly Assignment",
        "Practice Problems",
        "Review Questions",
        "Lab Report"
    ]

    for i, teacher in enumerate(teachers):
        for j in range(3):  # 3 homework per teacher
            class_obj = classes[i % len(classes)]
            subject = subjects[i % len(subjects)]

            due_days = [3, 7, 14][j]

            homework = Homework(
                title=f"{subject.name}: {homework_titles[j]}",
                description=f"Complete {homework_titles[j]} from textbook pages {20 + (j*10)}-{30 + (j*10)}",
                teacher_id=teacher.id,
                class_id=class_obj.id,
                subject_id=subject.id,
                page_numbers=f"{20 + (j*10)}-{30 + (j*10)}",
                due_date=datetime.now(timezone.utc) + timedelta(days=due_days),
                created_at=datetime.now(timezone.utc) - timedelta(days=2)
            )
            db.add(homework)
            homework_list.append(homework)

    await db.flush()
    print(f"✅ Created {len(homework_list)} homework assignments")
    return homework_list


async def create_submissions(db, homework_list, students):
    """Create submissions."""
    print("\n📤 Creating submissions...")

    submissions = []
    statuses = [SubmissionStatus.PENDING, SubmissionStatus.REVIEWED, SubmissionStatus.GRADED]

    for i, homework in enumerate(homework_list[:10]):  # First 10 homework
        # Create 2-3 submissions per homework
        num_submissions = min(3, len(students))
        for j in range(num_submissions):
            student = students[(i * 3 + j) % len(students)]
            status = statuses[j % 3]

            submission = Submission(
                homework_id=homework.id,
                student_id=student.id,
                file_url=f"https://example.com/submissions/{homework.id}_{student.id}.pdf",
                file_type="pdf",
                status=status,
                submitted_at=datetime.now(timezone.utc) - timedelta(days=(10-i), hours=j),
                grade=None if status == SubmissionStatus.PENDING else (75 + (j * 5) + (i % 15)),
                teacher_feedback=None if status == SubmissionStatus.PENDING else f"Good work! Keep it up.",
                reviewed_at=None if status == SubmissionStatus.PENDING else datetime.now(timezone.utc) - timedelta(days=(9-i))
            )
            db.add(submission)
            submissions.append(submission)

    await db.flush()
    print(f"✅ Created {len(submissions)} submissions")
    return submissions


async def seed_database():
    """Main seed function."""
    print("\n" + "="*60)
    print("🌱 SEEDING DATABASE")
    print("="*60)

    try:
        # Initialize database
        await init_db()

        # Get session
        async for db in get_async_session():
            # Clear existing data
            await clear_data(db)

            # Create data
            school = await create_school(db)
            subjects = await create_subjects(db, school)
            classes = await create_classes(db, school)
            principal = await create_principal(db, school)
            teachers = await create_teachers(db, school, subjects)
            students = await create_students(db, classes)
            parents = await create_parents(db, students)
            textbooks = await create_textbooks(db, classes, subjects)
            homework_list = await create_homework(db, teachers, classes, subjects)
            submissions = await create_submissions(db, homework_list, students)

            # Commit all
            await db.commit()

            # Summary
            print("\n" + "="*60)
            print("✅ DATABASE SEEDING COMPLETE!")
            print("="*60)
            print("\n📊 Summary:")
            print(f"   • 1 School: {school.name}")
            print(f"   • 1 Principal")
            print(f"   • {len(teachers)} Teachers")
            print(f"   • {len(subjects)} Subjects")
            print(f"   • {len(classes)} Classes")
            print(f"   • {len(students)} Students")
            print(f"   • {len(parents)} Parents")
            print(f"   • {len(textbooks)} Textbooks")
            print(f"   • {len(homework_list)} Homework Assignments")
            print(f"   • {len(submissions)} Submissions")

            print("\n🔑 Login Credentials:")
            print(f"   Principal: principal@springfield-high.edu / principal123")
            print(f"   Teacher:   edna.k@springfield-high.edu / teacher123")
            print(f"   Student:   student1@springfield-high.edu / student123")
            print(f"   Parent:    parent1@springfield-high.edu / parent123")

            print("\n🚀 Start the server:")
            print("   cd backend")
            print("   python -m uvicorn app.main:app --reload")
            print("   Open: http://localhost:8000/api/v1/docs")
            print("\n" + "="*60 + "\n")

            break

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(seed_database())
