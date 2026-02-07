# Backend - EduProof API

## Overview
FastAPI-based REST API server for the EduProof platform.

## Tech Stack
- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Alembic (migrations)
- JWT Authentication

## Structure
```
backend/
├── app/
│   ├── api/          # API route handlers
│   ├── core/         # Core config, security, dependencies
│   ├── models/       # SQLAlchemy database models
│   ├── schemas/      # Pydantic request/response schemas
│   ├── services/     # Business logic layer
│   ├── repositories/ # Data access layer
│   └── utils/        # Helper utilities
├── migrations/       # Alembic database migrations
├── tests/            # Unit and integration tests
└── requirements.txt  # Python dependencies
```

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env` file
5. Run migrations: `alembic upgrade head`
6. Start server: `uvicorn app.main:app --reload`
