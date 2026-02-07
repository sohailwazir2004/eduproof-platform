# EduProof Backend - Quick Start Guide

## Backend API Implementation Progress

### ✅ Completed Components

1. **Core Infrastructure**
   - FastAPI application setup (`app/main.py`)
   - Database configuration with SQLAlchemy async (`app/core/database.py`)
   - Application settings and environment config (`app/core/config.py`)
   - JWT authentication and security (`app/core/security.py`)
   - Custom exception handlers (`app/utils/exceptions.py`)

2. **Authentication System**
   - User registration with role selection
   - Login with JWT tokens (access + refresh)
   - Password change for authenticated users
   - Password reset flow (forgot password)
   - Token refresh endpoint
   - Complete auth routes (`app/api/routes/auth.py`)
   - Auth service with business logic (`app/services/auth_service.py`)
   - User repository for database operations (`app/repositories/user_repository.py`)

3. **Data Models**
   - User model with role-based relationships
   - Student, Teacher, Parent, Principal models
   - Homework model
   - Submission model
   - Textbook model
   - Base models with UUID and timestamp mixins

4. **Pydantic Schemas**
   - Authentication schemas (login, register, token, password reset)
   - User schemas (create, update, response)
   - Role-specific registration schemas

5. **Security Features**
   - Password hashing with bcrypt
   - JWT access and refresh tokens
   - Role-based access control (RBAC)
   - Token validation and expiration
   - Role checkers for route protection

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Application
APP_NAME=EduProof
DEBUG=True
ENVIRONMENT=development
API_V1_PREFIX=/api/v1

# Database (PostgreSQL)
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/eduproof

# JWT Authentication
SECRET_KEY=your-super-secret-key-change-in-production-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Origins
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=eduproof-files

# OpenAI API (Optional)
OPENAI_API_KEY=your-openai-api-key

# AI Service
AI_SERVICE_URL=http://localhost:8001

# SMTP Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 3. Setup PostgreSQL Database

```bash
# Create database
createdb eduproof

# Or using psql
psql -U postgres
CREATE DATABASE eduproof;
\q
```

### 4. Run Database Migrations

```bash
cd backend
alembic upgrade head
```

### 5. Start the Server

```bash
# From backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use Python directly:

```bash
python -m app.main
```

### 6. Access the API

- **API Documentation**: http://localhost:8000/api/v1/docs
- **Alternative Docs**: http://localhost:8000/api/v1/redoc
- **Health Check**: http://localhost:8000/health

## Testing the Authentication Flow

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher@school.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123",
    "role": "teacher"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher@school.com",
    "password": "SecurePass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "role": "teacher"
}
```

### 3. Access Protected Routes

Use the access token in the Authorization header:

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Next Steps - Components to Implement

### High Priority
1. **User Routes** (`app/api/routes/users.py`)
   - Get current user profile
   - Update user profile
   - User management (admin)

2. **Homework Routes** (`app/api/routes/homework.py`)
   - Create homework assignment (teacher)
   - List homework (role-filtered)
   - Get homework details
   - Update/delete homework

3. **Submission Routes** (`app/api/routes/submissions.py`)
   - Submit homework (student)
   - Grade submission (teacher)
   - AI analysis integration

4. **Class Management** (`app/api/routes/classes.py`)
   - CRUD for classes
   - Student-class assignments

### Medium Priority
5. **Textbook Management** (`app/api/routes/textbooks.py`)
   - Upload PDFs
   - AI indexing integration

6. **Analytics Dashboard** (`app/api/routes/analytics.py`)
   - Principal overview
   - Student progress tracking

7. **File Storage Integration**
   - S3/Cloudinary client implementation
   - File upload handling

8. **AI Service Integration**
   - OCR for handwritten homework
   - Homework relevance checking
   - Auto-grading assistance

### Low Priority
9. **Notification System**
   - Firebase push notifications
   - Email notifications

10. **Advanced Features**
    - Real-time updates with WebSockets
    - Bulk operations
    - Advanced search and filtering

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/         # API endpoints
│   │       ├── auth.py     # ✅ Authentication (COMPLETE)
│   │       ├── users.py    # ⏳ User management (TODO)
│   │       ├── homework.py # ⏳ Homework CRUD (TODO)
│   │       ├── submissions.py # ⏳ Submissions (TODO)
│   │       ├── textbooks.py   # ⏳ Textbooks (TODO)
│   │       ├── classes.py     # ⏳ Classes (TODO)
│   │       └── analytics.py   # ⏳ Analytics (TODO)
│   ├── core/
│   │   ├── config.py       # ✅ Settings
│   │   ├── database.py     # ✅ DB connection
│   │   └── security.py     # ✅ Auth & JWT
│   ├── models/             # ✅ SQLAlchemy models
│   ├── schemas/            # ✅ Pydantic schemas
│   ├── services/           # ⏳ Business logic
│   ├── repositories/       # ⏳ Data access
│   ├── utils/              # ✅ Helpers
│   └── main.py             # ✅ FastAPI app
├── migrations/             # Alembic migrations
├── tests/                  # Unit tests
├── requirements.txt        # ✅ Dependencies
└── .env                    # Environment variables
```

## Available User Roles

- **student**: Can view and submit homework
- **teacher**: Can create homework, view submissions, grade
- **parent**: Can view their children's homework and progress
- **principal**: Can view analytics and manage school
- **admin**: Full system access

## Development Tips

1. Use the interactive API docs at `/api/v1/docs` for testing
2. Check logs for detailed error messages when debug=True
3. All passwords must have: 8+ chars, uppercase, lowercase, digit
4. JWT tokens expire after 30 minutes by default
5. Use refresh token to get new access token without re-login

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists

### Import Errors
- Make sure all dependencies are installed
- Check Python version (3.10+)
- Activate virtual environment if using one

### Token Errors
- Check SECRET_KEY is set in .env
- Verify token hasn't expired
- Ensure Authorization header format: `Bearer <token>`

## Support

For issues or questions:
1. Check the API documentation at `/api/v1/docs`
2. Review error messages in console logs
3. Verify environment variables are set correctly
