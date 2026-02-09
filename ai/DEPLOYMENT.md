# AI Service Deployment Guide (Railway)

## Overview

The AI service is a standalone FastAPI microservice that handles:
- OCR (text extraction from images)
- Homework relevance checking
- AI-assisted grading
- Textbook content indexing
- Submission summarization

## Pre-deployment Checklist

- [ ] OpenAI or Anthropic API key ready
- [ ] Railway account created
- [ ] Backend deployed (for CORS configuration)
- [ ] Optional: Google Cloud Vision API credentials

## Important Notes

**Current Status**: AI service has basic structure but routes are not fully implemented.

The service will deploy successfully with health check and placeholder endpoints. Full AI functionality requires implementing route handlers in:
- `ocr/`
- `homework_analysis/`
- `summarization/`
- `textbook_parser/`

## Railway Setup

### 1. Initialize Railway Project

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Navigate to AI directory
cd ai

# Initialize
railway init
```

### 2. Configure Environment Variables

Set these in Railway dashboard:

```env
# Required: At least one LLM API key
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Google Cloud Vision for OCR
GOOGLE_APPLICATION_CREDENTIALS=/app/google-credentials.json

# OCR Configuration (automatically set in Docker)
TESSERACT_PATH=/usr/bin/tesseract

# Model Cache
MODEL_CACHE_DIR=/app/models/cache

# Service Config
LOG_LEVEL=INFO

# CORS: Backend URL (IMPORTANT)
BACKEND_URL=https://your-backend.railway.app
```

### 3. Deploy

#### Option A: Railway CLI
```bash
cd ai
railway up
```

#### Option B: GitHub
1. Push to GitHub
2. Railway Dashboard → "New" → "GitHub Repo"
3. Select repository
4. Set root directory to `/ai`
5. Railway auto-detects Dockerfile

### 4. Update Backend Configuration

After AI service is deployed, update backend environment:

In Railway backend dashboard:
```env
AI_SERVICE_URL=https://your-ai-service.railway.app
```

Redeploy backend.

## Post-Deployment

### Verify Health Check
```bash
curl https://your-ai-service.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "EduProof AI Service",
  "version": "1.0.0"
}
```

### Access API Documentation
```
https://your-ai-service.railway.app/docs
```

### Test Endpoint Availability
```bash
curl https://your-ai-service.railway.app/
```

## Google Cloud Vision Setup (Optional)

If using Google Cloud Vision for OCR:

### 1. Create Service Account
1. Go to Google Cloud Console
2. Create service account
3. Download JSON credentials

### 2. Upload to Railway

Option A: Base64 encode and use env var
```bash
base64 google-credentials.json | tr -d '\n'
```

Add to Railway as `GOOGLE_CREDENTIALS_BASE64`, then in Dockerfile:
```dockerfile
RUN echo $GOOGLE_CREDENTIALS_BASE64 | base64 -d > /app/google-credentials.json
```

Option B: Mount as Railway volume (Pro plan only)

## Model Downloads

The AI service uses sentence-transformers for embeddings. First request will download models (~400MB).

To pre-download during build, add to Dockerfile:
```dockerfile
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

## Implementing AI Routes

Current structure allows for modular route addition:

### Example: OCR Router

Create `ai/ocr/routes.py`:
```python
from fastapi import APIRouter, UploadFile, File
from .extractor import extract_text

router = APIRouter()

@router.post("/extract")
async def extract_text_endpoint(file: UploadFile = File(...)):
    """Extract text from uploaded image"""
    content = await file.read()
    text = extract_text(content)
    return {"text": text, "success": True}
```

Add to `main.py`:
```python
from ocr.routes import router as ocr_router
app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
```

## Resource Requirements

Railway Resource Recommendations:
- **Memory**: 1GB minimum (2GB recommended for ML models)
- **CPU**: 1 vCPU minimum
- **Disk**: 2GB for model cache

Adjust in Railway dashboard if needed.

## Performance Optimization

### 1. Model Caching
Ensure `MODEL_CACHE_DIR` persists between deployments:
- Use Railway volumes (Pro plan)
- Or download models on startup

### 2. Async Processing
For heavy AI tasks, consider:
- Background job queues (Celery + Redis)
- Separate worker service on Railway
- Webhook callbacks instead of synchronous responses

### 3. Rate Limiting
Add rate limiting for API calls:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

## Monitoring

### Check Logs
```bash
railway logs
```

### Monitor Resource Usage
Railway dashboard shows:
- Memory usage
- CPU usage
- Request volume
- Response times

### Error Tracking

Add Sentry for error monitoring:
```bash
pip install sentry-sdk[fastapi]
```

In `main.py`:
```python
import sentry_sdk
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"))
```

## Troubleshooting

### High Memory Usage
- Models loading on every request
- Solution: Load models once at startup
```python
@app.on_event("startup")
async def load_models():
    global model
    model = SentenceTransformer('all-MiniLM-L6-v2')
```

### Slow First Request
- Model download on first use
- Solution: Pre-download in Dockerfile or at startup

### Connection Refused from Backend
- CORS misconfiguration
- Check `BACKEND_URL` environment variable
- Verify backend has `AI_SERVICE_URL` set correctly

### API Key Errors
- Verify keys are set in Railway dashboard
- Check logs for authentication errors
- Ensure keys have required permissions

## Scaling

For production load:
1. Enable Railway autoscaling (Pro plan)
2. Use Redis for caching frequent AI requests
3. Consider dedicated GPU service for heavy ML models
4. Implement request queuing for batch processing

## Security Notes

1. Never commit API keys or credentials
2. Use Railway secrets for all sensitive data
3. Implement API key authentication for AI endpoints
4. Rate limit to prevent abuse
5. Validate file uploads (size, type, content)

## Cost Estimation

Railway:
- Free tier: $5 credit/month (good for testing)
- Developer: $20/month (recommended for production)

External APIs:
- OpenAI: Pay per token (GPT-4: ~$0.03-0.06/1K tokens)
- Anthropic: Pay per token (Claude: ~$0.008-0.024/1K tokens)
- Google Vision: $1.50/1000 images (first 1000 free)

## Next Steps

After deployment:
1. Implement route handlers for each AI module
2. Add authentication to protect endpoints
3. Integrate with backend homework/submission flows
4. Add monitoring and alerting
5. Load test with expected production volume
