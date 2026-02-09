# Backend Deployment Guide (Railway)

## Pre-deployment Checklist

- [ ] PostgreSQL database configured in Railway
- [ ] Environment variables set in Railway dashboard
- [ ] AWS S3 or Cloudinary credentials ready
- [ ] JWT SECRET_KEY generated (use: `openssl rand -hex 32`)
- [ ] Frontend URL for CORS configuration

## Railway Setup

### 1. Create New Project
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init
```

### 2. Add PostgreSQL Database
- Go to Railway dashboard
- Click "New" → "Database" → "PostgreSQL"
- Railway automatically creates `DATABASE_URL` environment variable

### 3. Configure Environment Variables

Set these in Railway dashboard (Variables tab):

```env
# Application
APP_NAME=EduProof
DEBUG=false
ENVIRONMENT=production

# Database (automatically provided by Railway PostgreSQL)
DATABASE_URL=<provided-by-railway>

# JWT Authentication (REQUIRED)
SECRET_KEY=<generate-with-openssl-rand-hex-32>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS (REQUIRED)
FRONTEND_URL=https://your-frontend.vercel.app

# AWS S3 (File Storage)
AWS_ACCESS_KEY_ID=<your-aws-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret>
AWS_REGION=us-east-1
S3_BUCKET_NAME=eduproof-files

# Cloudinary (Alternative to S3)
CLOUDINARY_CLOUD_NAME=<your-cloud-name>
CLOUDINARY_API_KEY=<your-api-key>
CLOUDINARY_API_SECRET=<your-api-secret>

# AI Service URL (after deploying AI service)
AI_SERVICE_URL=https://your-ai-service.railway.app

# Optional: Firebase (Notifications)
FIREBASE_PROJECT_ID=<your-project-id>
# Upload firebase-credentials.json separately

# Optional: Email SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<your-email>
SMTP_PASSWORD=<your-app-password>
```

### 4. Deploy

#### Option A: Using Railway CLI
```bash
cd backend
railway up
```

#### Option B: Using GitHub
1. Push code to GitHub
2. In Railway dashboard: "New" → "GitHub Repo"
3. Select your repository
4. Set root directory to `/backend`
5. Railway auto-detects Dockerfile and deploys

### 5. Run Database Migrations

After first deployment:
```bash
railway run alembic upgrade head
```

Or connect via Railway CLI:
```bash
railway link
railway run python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"
```

## Post-Deployment

### Verify Health Check
```bash
curl https://your-backend.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "EduProof",
  "environment": "production"
}
```

### Access API Documentation
```
https://your-backend.railway.app/api/v1/docs
```

### Monitor Logs
```bash
railway logs
```

## Database Connection Notes

Railway provides `DATABASE_URL` in this format:
```
postgresql://user:pass@host:port/db
```

Our app expects:
```
postgresql+asyncpg://user:pass@host:port/db
```

Add this to Railway environment if needed:
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
```

Or Railway will auto-convert it correctly.

## Troubleshooting

### Connection Issues
- Verify `DATABASE_URL` has `+asyncpg` driver
- Check Railway logs for startup errors
- Ensure all required env vars are set

### CORS Errors
- Add frontend URL to `FRONTEND_URL` env variable
- Verify URL has no trailing slash

### Database Migration Errors
```bash
railway run alembic revision --autogenerate -m "Initial migration"
railway run alembic upgrade head
```

## Estimated Costs

Railway Free Tier:
- $5 usage credit monthly
- Suitable for development/testing
- Upgrade to Developer plan for production ($20/month)

## Security Notes

1. Never commit `.env` file
2. Use strong SECRET_KEY (32+ characters)
3. Enable Railway's built-in DDoS protection
4. Use environment variables for all secrets
5. Enable SSL (Railway provides this automatically)
