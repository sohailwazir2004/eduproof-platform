# EduProof - AI School Homework Management Platform

A comprehensive, modular, and AI-powered platform for managing school homework across web and mobile applications.

## Overview

EduProof helps schools manage homework assignments, submissions, and grading with AI assistance for OCR and content analysis.

### Roles
- **Student**: Submit homework via mobile camera
- **Teacher**: Assign homework, grade submissions with AI assistance
- **Parent**: Monitor child's progress and submissions
- **Principal**: School-wide analytics and oversight

## Project Structure

```
eduproof/
├── backend/              # FastAPI REST API
│   ├── app/
│   │   ├── api/routes/   # API endpoints
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── core/         # Config, security, database
│   ├── migrations/       # Alembic migrations
│   └── tests/            # Backend tests
│
├── frontend/             # React + Vite + Tailwind
│   └── src/
│       ├── components/   # Reusable UI components
│       ├── pages/        # Page components
│       ├── hooks/        # Custom React hooks
│       ├── services/     # API services
│       ├── stores/       # Zustand state
│       └── types/        # TypeScript types
│
├── mobile/               # React Native + Expo
│   └── src/
│       ├── screens/      # Screen components
│       ├── components/   # Reusable components
│       ├── navigation/   # React Navigation
│       ├── hooks/        # Custom hooks
│       └── services/     # API services
│
├── ai/                   # AI/ML Services
│   ├── ocr/              # Text extraction
│   ├── homework_analysis/# Grading assistance
│   ├── summarization/    # Content summaries
│   └── textbook_parser/  # PDF processing
│
├── cloud/                # Cloud Infrastructure
│   ├── storage/          # S3/Cloudinary
│   ├── notifications/    # Firebase
│   ├── docker/           # Docker configs
│   └── infrastructure/   # Terraform
│
└── docs/                 # Documentation
    ├── api/              # API docs
    ├── architecture/     # System design
    └── guides/           # Developer guides
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend API | Python 3.11+, FastAPI, SQLAlchemy |
| Database | PostgreSQL 15+ |
| Web Frontend | React 18, Vite, Tailwind CSS |
| Mobile App | React Native, Expo SDK 50 |
| AI Services | OpenAI/Anthropic, Tesseract OCR |
| Cloud Storage | AWS S3 / Cloudinary |
| Notifications | Firebase Cloud Messaging |
| Deployment | Docker, AWS ECS, Terraform |

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker (optional)

### With Docker (Recommended)

```bash
cd cloud/docker
docker-compose up -d
```

### Manual Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Mobile
cd mobile
npm install
npx expo start
```

## Key Features

- **Role-Based Access**: Secure JWT authentication with role-specific dashboards
- **AI-Powered OCR**: Extract text from handwritten homework submissions
- **Smart Grading**: AI-assisted grade suggestions and feedback generation
- **PDF Textbook Integration**: Upload, index, and reference textbook content
- **Real-time Notifications**: Push notifications for assignments and grades
- **Analytics Dashboard**: School-wide performance insights for principals

## Documentation

- [Getting Started](docs/guides/getting-started.md)
- [API Documentation](docs/api/README.md)
- [Architecture](docs/architecture/README.md)
- [Deployment Guide](docs/guides/deployment.md)

## Development

```bash
# Run all tests
make test

# Build for production
make build

# Deploy
make deploy
```

## License

MIT License - See [LICENSE](LICENSE) for details.
