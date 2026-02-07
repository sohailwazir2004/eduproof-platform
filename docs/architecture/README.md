# System Architecture

## Overview

EduProof is a microservices-based platform with the following components:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Web App   │     │  Mobile App │     │  Admin App  │
│   (React)   │     │(React Native│     │   (React)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │   API GW    │
                    │  (FastAPI)  │
                    └──────┬──────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
│  AI Service │     │  PostgreSQL │     │  S3/Cloud   │
│  (FastAPI)  │     │  Database   │     │   Storage   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Components

1. **Backend API** - FastAPI REST API
2. **AI Service** - OCR and homework analysis
3. **PostgreSQL** - Primary database
4. **Redis** - Caching and job queues
5. **S3/Cloudinary** - File storage
6. **Firebase** - Push notifications
