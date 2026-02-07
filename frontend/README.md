# Frontend - EduProof Web Dashboard

## Overview
React-based web application for Teachers, Parents, and Principals.

## Tech Stack
- React 18+
- Vite (build tool)
- Tailwind CSS
- React Router v6
- React Query (data fetching)
- Zustand (state management)
- Axios (HTTP client)

## Structure
```
frontend/
├── src/
│   ├── components/   # Reusable UI components
│   ├── pages/        # Page-level components (routes)
│   ├── layouts/      # Layout wrappers
│   ├── hooks/        # Custom React hooks
│   ├── services/     # API service functions
│   ├── stores/       # Zustand state stores
│   ├── utils/        # Helper utilities
│   ├── types/        # TypeScript type definitions
│   └── assets/       # Static assets (images, fonts)
├── public/           # Public static files
└── tests/            # Component and integration tests
```

## Setup
1. Install dependencies: `npm install`
2. Configure `.env` file
3. Start dev server: `npm run dev`
4. Build for production: `npm run build`
