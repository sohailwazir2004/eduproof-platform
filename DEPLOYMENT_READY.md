# EduProof Platform - Complete Deployment Guide

## Overview

EduProof consists of 4 independently deployable services:

| Service | Technology | Platform | Purpose |
|---------|-----------|----------|---------|
| **Backend** | FastAPI + PostgreSQL | Railway | Main API, authentication, database |
| **Frontend** | React + Vite | Vercel | Web interface (teacher, parent, principal) |
| **AI Service** | FastAPI + ML | Railway | OCR, homework analysis, AI features |
| **Mobile** | React Native + Expo | Expo EAS | Student/parent mobile app |

## Deployment Order

**IMPORTANT**: Deploy in this order to ensure services can reference each other:

1. **Backend** (Railway) → Get API URL
2. **AI Service** (Railway) → Get AI URL, update backend
3. **Frontend** (Vercel) → Use backend URL
4. **Mobile** (Expo EAS) → Use backend URL

## Quick Start Commands

### Backend
```bash
cd backend
railway login
railway init
railway up
```

### Frontend
```bash
cd frontend
vercel
vercel --prod
```

### AI Service
```bash
cd ai
railway login
railway init
railway up
```

### Mobile
```bash
cd mobile
eas login
eas build --profile production --platform all
```

## Detailed Guides

Each service has its own comprehensive deployment guide:

- [Backend Deployment](./backend/DEPLOYMENT.md) - FastAPI + PostgreSQL on Railway
- [Frontend Deployment](./frontend/DEPLOYMENT.md) - React + Vite on Vercel
- [AI Service Deployment](./ai/DEPLOYMENT.md) - AI microservice on Railway
- [Mobile Deployment](./mobile/DEPLOYMENT.md) - React Native on Expo EAS

See full guide in **DEPLOYMENT_READY.md**
