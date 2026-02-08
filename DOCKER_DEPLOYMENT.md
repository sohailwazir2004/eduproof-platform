# Docker Deployment Guide - EduProof Platform

Complete guide for deploying EduProof using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum (8GB recommended)
- 20GB disk space

## Quick Start

### 1. Environment Setup

Copy environment configuration:
```bash
cp .env.docker .env
```

Edit `.env` and update the following:
- `SECRET_KEY` - Generate a secure secret key
- `POSTGRES_PASSWORD` - Set a strong database password
- Cloud storage credentials (AWS S3 or Cloudinary)
- OpenAI API key (for AI features)

### 2. Build and Start Services

**Development Mode:**
```bash
# Build images
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build

# Start services
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# View logs
docker-compose logs -f
```

**Production Mode:**
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Initialize Database

Run migrations:
```bash
docker-compose exec backend alembic upgrade head
```

Create admin user (optional):
```bash
docker-compose exec backend python -m app.scripts.create_admin
```

### 4. Access Application

- **Frontend Web App**: http://localhost:80 (production) or http://localhost:5173 (dev)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs
- **AI Service**: http://localhost:8001

## Services Architecture

```
┌─────────────────────────────────────────────────┐
│                   Frontend                      │
│              (React + Vite + Nginx)             │
│                   Port: 80/5173                 │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────┴─────────────────────────────┐
│                Backend API                      │
│           (FastAPI + Python + SQLAlchemy)       │
│                   Port: 8000                    │
└───────┬────────────────────────────┬────────────┘
        │                            │
┌───────┴────────┐          ┌────────┴───────────┐
│   PostgreSQL   │          │    AI Service      │
│   Port: 5432   │          │    Port: 8001      │
└────────────────┘          └────────────────────┘
        │
┌───────┴────────┐
│     Redis      │
│   Port: 6379   │
└────────────────┘
```

## Service Details

### Backend API
- **Framework**: FastAPI
- **Port**: 8000
- **Health Check**: http://localhost:8000/health
- **Dependencies**: PostgreSQL, Redis

### Frontend Web App
- **Framework**: React + Vite
- **Port**: 80 (prod), 5173 (dev)
- **Web Server**: Nginx (production)

### PostgreSQL Database
- **Version**: 15
- **Port**: 5432
- **Database**: eduproof
- **Volume**: postgres_data

### Redis Cache
- **Version**: 7
- **Port**: 6379
- **Volume**: redis_data

### AI Service
- **Framework**: FastAPI + PyTorch
- **Port**: 8001
- **Features**: OCR, Homework Analysis

## Docker Commands

### Using Makefile
```bash
# Build all images
make -f Makefile.docker build

# Start services
make -f Makefile.docker up

# Start in development mode
make -f Makefile.docker up-dev

# Stop services
make -f Makefile.docker down

# View logs
make -f Makefile.docker logs

# Run migrations
make -f Makefile.docker migrate

# Run tests
make -f Makefile.docker test

# Clean everything
make -f Makefile.docker clean
```

### Direct Docker Compose Commands
```bash
# Build specific service
docker-compose build backend

# Start specific service
docker-compose up -d backend

# Stop all services
docker-compose down

# Remove volumes
docker-compose down -v

# View service logs
docker-compose logs -f backend

# Execute command in container
docker-compose exec backend bash

# Rebuild and restart
docker-compose up -d --build
```

## Database Management

### Run Migrations
```bash
docker-compose exec backend alembic upgrade head
```

### Create Migration
```bash
docker-compose exec backend alembic revision --autogenerate -m "description"
```

### Rollback Migration
```bash
docker-compose exec backend alembic downgrade -1
```

### Access Database Shell
```bash
docker-compose exec postgres psql -U eduproof -d eduproof
```

### Backup Database
```bash
docker-compose exec postgres pg_dump -U eduproof eduproof > backup.sql
```

### Restore Database
```bash
cat backup.sql | docker-compose exec -T postgres psql -U eduproof eduproof
```

## Development Workflow

### Hot Reload (Development Mode)
```bash
# Start with hot reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Backend changes auto-reload
# Frontend changes auto-reload at http://localhost:5173
```

### Run Tests
```bash
# Backend tests
docker-compose exec backend pytest

# Backend tests with coverage
docker-compose exec backend pytest --cov=app --cov-report=html
```

### Access Container Shell
```bash
# Backend shell
docker-compose exec backend bash

# Database shell
docker-compose exec postgres psql -U eduproof -d eduproof

# Redis CLI
docker-compose exec redis redis-cli
```

## Production Deployment

### 1. Update Environment Variables
```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update .env
SECRET_KEY=<generated-secret>
POSTGRES_PASSWORD=<secure-password>
```

### 2. Configure Cloud Storage
Set up AWS S3 or Cloudinary credentials in `.env`:
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=your-bucket-name
```

### 3. Build Production Images
```bash
docker-compose build --no-cache
```

### 4. Start Services
```bash
docker-compose up -d
```

### 5. SSL/TLS Configuration (Optional)
Enable nginx proxy with SSL:
```bash
docker-compose --profile production up -d
```

## Monitoring

### View Resource Usage
```bash
docker stats
```

### View Service Status
```bash
docker-compose ps
```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:80/health

# AI Service health
curl http://localhost:8001/health
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs backend

# Rebuild image
docker-compose build --no-cache backend

# Remove and recreate
docker-compose down
docker-compose up -d
```

### Database connection issues
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Test connection
docker-compose exec backend python -c "from app.core.database import engine; print(engine)"
```

### Permission issues
```bash
# Fix volume permissions
docker-compose exec backend chown -R appuser:appuser /app
```

### Clear all data and restart
```bash
# WARNING: This will delete all data
docker-compose down -v
docker-compose up -d
```

## Scaling

### Scale specific service
```bash
# Scale backend to 3 instances
docker-compose up -d --scale backend=3
```

### Load Balancing
Add nginx as reverse proxy for multiple backend instances.

## Backup Strategy

### Automated Backups
```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U eduproof eduproof > backup_$DATE.sql
```

### Volume Backups
```bash
# Backup volumes
docker run --rm -v eduproof_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_data.tar.gz /data
```

## Security Recommendations

1. **Change default passwords** in `.env`
2. **Use secrets management** (Docker Secrets, Vault)
3. **Enable SSL/TLS** for production
4. **Regular security updates** - rebuild images monthly
5. **Limit exposed ports** - use reverse proxy
6. **Enable firewall** rules
7. **Monitor logs** for suspicious activity

## Performance Optimization

1. **Resource Limits** - Add to docker-compose.yml:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

2. **Enable Redis Caching** - Configure in backend

3. **Database Connection Pooling** - Already configured in SQLAlchemy

4. **Static Asset CDN** - Configure Cloudinary/S3

## Support

For issues and questions:
- Check logs: `docker-compose logs -f`
- Review documentation: `/docs`
- GitHub Issues: Create an issue with logs

## License

EduProof Platform - See LICENSE file
