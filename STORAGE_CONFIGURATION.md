# Storage Service Configuration Guide

## ✅ Storage Service is Complete!

The Storage Service at `backend/app/services/storage_service.py` is **fully implemented** and supports:
- ✅ AWS S3
- ✅ Cloudinary
- ✅ Local storage (development fallback)

## 🚀 Quick Setup (Choose One)

### Option A: Cloudinary (Recommended - Easiest)

**1. Sign up for free**: https://cloudinary.com/users/register/free

**2. Get your credentials** from Dashboard → Settings → Product Environment

**3. Add to `.env`**:
```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

**Free tier**: 25 GB storage, 25 GB bandwidth/month

---

### Option B: AWS S3

**1. Create AWS account**: https://aws.amazon.com/

**2. Create S3 bucket**:
```bash
aws s3 mb s3://eduproof-files --region us-east-1
```

**3. Create IAM user** with S3 permissions

**4. Add to `.env`**:
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=eduproof-files
AWS_REGION=us-east-1
```

---

### Option C: Local Storage (Development Only)

**No configuration needed!**

Files are saved to `uploads/` directory automatically.

---

## 📝 Environment Configuration

### Full `.env` Example:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/eduproof

# Storage (Choose ONE)
# Option A: Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Option B: AWS S3
# AWS_ACCESS_KEY_ID=your_access_key
# AWS_SECRET_ACCESS_KEY=your_secret_key
# AWS_S3_BUCKET=eduproof-files
# AWS_REGION=us-east-1

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Optional
DEBUG=True
ENVIRONMENT=development
```

---

## 🧪 Test Storage Service

### 1. Start backend:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 2. Test file upload:
```bash
curl -X POST http://localhost:8000/api/v1/submissions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "homework_id=UUID_HERE" \
  -F "file=@/path/to/file.pdf"
```

### 3. Check Swagger docs:
http://localhost:8000/api/v1/docs

---

## ✅ Features Supported

| Feature | Status |
|---------|--------|
| Upload images (JPEG, PNG) | ✅ |
| Upload PDFs | ✅ |
| Delete files | ✅ |
| Presigned URLs (S3) | ✅ |
| File type validation | ✅ |
| File size validation | ✅ |
| Multiple backends | ✅ |
| Local fallback | ✅ |

---

## 🔐 Security Best Practices

### 1. Never commit credentials
Add to `.gitignore`:
```
.env
.env.local
.env.*.local
```

### 2. Use environment-specific files
- `.env.development` - Local development
- `.env.production` - Production secrets
- `.env.test` - Testing

### 3. Rotate credentials regularly
- Change keys every 90 days
- Use AWS IAM roles in production
- Enable 2FA on cloud accounts

---

## 📊 Storage Costs

### Cloudinary (Free Tier)
- ✅ 25 GB storage
- ✅ 25 GB bandwidth/month
- ✅ Automatic image optimization
- ✅ CDN included
- **Cost**: $0/month (free tier)

### AWS S3 (Standard)
- First 5 GB: Free
- After 5 GB: $0.023/GB/month
- Bandwidth: $0.09/GB (after 100 GB free)
- **Estimated**: $1-5/month for small app

### Local Storage
- **Cost**: $0 (uses server disk)
- ⚠️ Not recommended for production

---

## 🚀 Production Deployment

### Cloudinary (Recommended)
```env
CLOUDINARY_CLOUD_NAME=eduproof-prod
CLOUDINARY_API_KEY=production_key
CLOUDINARY_API_SECRET=production_secret
```

### AWS S3 with CloudFront CDN
```env
AWS_ACCESS_KEY_ID=prod_access_key
AWS_SECRET_ACCESS_KEY=prod_secret_key
AWS_S3_BUCKET=eduproof-prod-files
AWS_REGION=us-east-1
CLOUDFRONT_DOMAIN=d123abc.cloudfront.net
```

---

## 🐛 Troubleshooting

### "No storage backend configured"
- Add credentials to `.env`
- Restart the server

### "Upload failed: Permission denied"
- Check S3 bucket policy
- Verify IAM user has `s3:PutObject` permission

### "Cloudinary upload failed"
- Verify credentials are correct
- Check file size (max 10 MB by default)
- Ensure content type is allowed

### "Local files not found"
- Check `uploads/` directory exists
- Verify file permissions

---

## ✅ Storage Service Status

**Status**: ✅ **COMPLETE AND PRODUCTION-READY**

The service is fully implemented with:
- ✅ Multi-backend support
- ✅ Error handling
- ✅ File validation
- ✅ Development fallback
- ✅ Used by Submission routes

Just add your credentials and you're ready to go!

---

## 📚 API Usage Examples

### Upload File (via Submission):
```python
# Python
import requests

url = "http://localhost:8000/api/v1/submissions"
headers = {"Authorization": f"Bearer {token}"}
files = {"file": open("homework.pdf", "rb")}
data = {"homework_id": "homework-uuid"}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.json())
```

### TypeScript (Frontend):
```typescript
// Upload from frontend
const formData = new FormData();
formData.append('homework_id', homeworkId);
formData.append('file', file);

const response = await fetch('/api/v1/submissions', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData
});
```

### React Native (Mobile):
```typescript
// Upload from mobile
const formData = new FormData();
formData.append('homework_id', homeworkId);
formData.append('file', {
  uri: imageUri,
  type: 'image/jpeg',
  name: 'homework.jpg'
});

const response = await api.post('/submissions', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

---

**Storage Service: COMPLETE ✅**

Ready for production with any storage backend!
