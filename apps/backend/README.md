# ⚡ Backend API

Python + FastAPI REST API server with PostgreSQL database.

## Structure

```
backend/
├── src/
│   ├── api/
│   │   ├── v1/                    # API version 1
│   │   │   ├── endpoints/         # Route handlers
│   │   │   │   ├── auth.py       # Authentication endpoints
│   │   │   │   ├── users.py      # User management
│   │   │   │   ├── homework.py   # Homework CRUD
│   │   │   │   ├── classes.py    # Class management
│   │   │   │   ├── notifications.py  # Notification endpoints
│   │   │   │   ├── analytics.py  # Reports & analytics
│   │   │   │   └── storage.py    # File upload/download
│   │   │   └── dependencies/     # Route dependencies
│   │   └── middleware/           # Custom middleware
│   ├── core/
│   │   ├── config/              # App configuration
│   │   └── security/            # JWT, hashing, permissions
│   ├── models/                  # SQLAlchemy ORM models
│   ├── schemas/                 # Pydantic schemas
│   ├── services/                # Business logic
│   │   ├── auth/               # Authentication service
│   │   ├── homework/           # Homework business logic
│   │   ├── notifications/      # Push & email notifications
│   │   ├── storage/            # File storage service
│   │   │   ├── local/         # Local file storage
│   │   │   └── cloud/         # AWS S3 / GCS integration
│   │   └── ai/                 # AI service integration
│   ├── db/
│   │   ├── migrations/         # Alembic migrations
│   │   └── seeds/              # Seed data
│   ├── utils/                  # Utility functions
│   └── workers/                # Background tasks (Celery)
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
├── alembic.ini
├── requirements.txt
├── Dockerfile
└── main.py                     # App entry point
```

## Key Features

- **JWT Authentication**: Role-based access control
- **Async Support**: Full async/await support
- **Background Tasks**: Celery for async processing
- **File Storage**: Local + Cloud storage abstraction

## Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Database

```bash
alembic upgrade head    # Run migrations
alembic revision -m "description"  # Create migration
```
