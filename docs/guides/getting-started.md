# Getting Started

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker (optional)

## Quick Start with Docker

```bash
cd cloud/docker
docker-compose up -d
```

## Manual Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Mobile

```bash
cd mobile
npm install
npx expo start
```

## Environment Variables

See `.env.example` files in each directory.
