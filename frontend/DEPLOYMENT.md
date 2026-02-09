# Frontend Deployment Guide (Vercel)

## Pre-deployment Checklist

- [ ] Backend deployed and URL obtained
- [ ] Build tested locally (`npm run build`)
- [ ] Environment variables prepared
- [ ] Vercel account created

## Local Build Test

Before deploying, verify the build works:

```bash
cd frontend
npm install
npm run build
npm run preview
```

Visit `http://localhost:4173` to test the production build.

## Vercel Deployment

### Option A: Deploy via Vercel CLI (Recommended)

#### 1. Install Vercel CLI
```bash
npm i -g vercel
```

#### 2. Login to Vercel
```bash
vercel login
```

#### 3. Deploy
```bash
cd frontend
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? Select your account
- Link to existing project? **N**
- Project name? **eduproof-frontend** (or your choice)
- In which directory is your code? **./**
- Want to override settings? **N**

#### 4. Set Environment Variables
```bash
vercel env add VITE_API_BASE_URL production
# Enter: https://your-backend.railway.app/api/v1

vercel env add VITE_APP_NAME production
# Enter: EduProof

vercel env add VITE_APP_ENV production
# Enter: production
```

#### 5. Deploy to Production
```bash
vercel --prod
```

### Option B: Deploy via GitHub (Auto-deploy)

#### 1. Push to GitHub
```bash
git add .
git commit -m "Prepare frontend for deployment"
git push origin main
```

#### 2. Import to Vercel
1. Go to https://vercel.com/new
2. Click "Import Project"
3. Select your GitHub repository
4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

#### 3. Add Environment Variables

In Vercel dashboard (Project → Settings → Environment Variables):

| Name | Value | Environment |
|------|-------|-------------|
| `VITE_API_BASE_URL` | `https://your-backend.railway.app/api/v1` | Production |
| `VITE_APP_NAME` | `EduProof` | Production |
| `VITE_APP_ENV` | `production` | Production |

#### 4. Deploy
Click "Deploy" - Vercel will build and deploy automatically.

## Post-Deployment

### 1. Update Backend CORS

Add your Vercel URL to backend environment variables:

In Railway backend dashboard:
```env
FRONTEND_URL=https://your-frontend.vercel.app
```

Redeploy backend if needed.

### 2. Verify Deployment

Visit your Vercel URL:
```
https://your-frontend.vercel.app
```

Test:
- [ ] Login page loads
- [ ] Can authenticate (check API calls in Network tab)
- [ ] No CORS errors
- [ ] All pages accessible

### 3. Get Deployment URLs

```bash
# List all deployments
vercel ls

# Get production URL
vercel ls --prod
```

## Custom Domain (Optional)

### Add Custom Domain

```bash
vercel domains add yourdomain.com
```

Or in Vercel dashboard:
1. Project → Settings → Domains
2. Add domain
3. Follow DNS configuration instructions

## Environment Management

### View Current Environment Variables
```bash
vercel env ls
```

### Update Environment Variable
```bash
vercel env rm VITE_API_BASE_URL production
vercel env add VITE_API_BASE_URL production
# Enter new value
```

### Pull Environment Variables Locally
```bash
vercel env pull .env.local
```

## Automatic Deployments

Vercel automatically deploys on:
- **Push to main**: Production deployment
- **Push to other branches**: Preview deployment
- **Pull requests**: Preview deployment with unique URL

## Rollback

If deployment fails or has issues:

```bash
# List recent deployments
vercel ls

# Promote a previous deployment to production
vercel promote <deployment-url>
```

Or via Vercel dashboard:
1. Go to Deployments
2. Find working deployment
3. Click "..." → "Promote to Production"

## Build Optimization

The `vercel.json` is configured for optimal performance:
- SPA routing (all routes go to index.html)
- Static asset caching (1 year for immutable assets)
- Compressed builds

## Troubleshooting

### Build Fails

Check build logs:
```bash
vercel logs <deployment-url>
```

Common issues:
- TypeScript errors: Fix locally first
- Missing dependencies: Check package.json
- Environment variables: Verify all VITE_* vars are set

### API Connection Fails

1. Check browser console for errors
2. Verify `VITE_API_BASE_URL` is correct
3. Check backend CORS configuration
4. Ensure backend is running (visit `/health` endpoint)

### 404 on Page Refresh

Ensure `vercel.json` has the rewrite rule:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

## Performance Monitoring

Vercel provides built-in analytics:
- Go to Project → Analytics
- View page load times, Core Web Vitals
- Monitor API response times

## Costs

Vercel Pricing:
- **Hobby (Free)**:
  - 100GB bandwidth/month
  - Unlimited deployments
  - Perfect for this project
- **Pro ($20/month)**:
  - 1TB bandwidth
  - Team collaboration
  - Advanced analytics

## Security Notes

1. Never commit `.env` files
2. Use environment variables for all API URLs
3. Vercel provides automatic HTTPS
4. Enable Vercel's Security Headers (optional)
5. Set up authentication on sensitive routes

## Preview Deployments

Every branch/PR gets a unique preview URL:
```
https://eduproof-frontend-<hash>.vercel.app
```

Share preview URLs for testing before production.
