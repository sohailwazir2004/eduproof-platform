# Claude Instructions - EduProof (AI Homework Platform)

## Project Overview
EduProof is an AI-powered school homework management platform. Teachers assign homework from textbooks (PDFs), students submit handwritten work via mobile or web, parents monitor progress, and principals oversee overall academic discipline. AI assists with homework validation and analysis.

## Platforms
- Web App (React + Vite + Tailwind) for Teachers, Parents, Principals
- Mobile App (React Native + Expo) for Students and Parents
- Backend (Python + FastAPI + PostgreSQL)
- Cloud Storage (AWS S3 / Cloudinary)
- AI Services (OCR + Homework Analysis)

## Roles
- Student
- Teacher
- Parent
- Principal / Admin

## Primary Features to Implement
1. Role-based login & JWT authentication
2. PDF textbook upload & indexing
3. Homework assignment by teacher
4. Homework submission by student (image / PDF)
5. Parent-only dashboard for their child
6. Principal dashboard for analytics
7. AI-assisted homework validation & summaries
8. Push/email notifications via Firebase
9. Secure cloud storage for files

## Skills Claude Should Use
- Full-stack web development (React, React Native, Python, FastAPI)
- Database design & ORM (PostgreSQL, SQLAlchemy)
- AI integration (OCR, content analysis)
- Cloud storage & secure file management
- Notifications & real-time alerts
- Testing & deployment best practices

## Workflow Guidelines for Claude
- Always generate **modular, clean, production-ready code**
- Give **comments** explaining each module/file
- Suggest **folder structure and file placement**
- Generate **API routes**, models, frontend components, and mobile screens separately
- Build **MVP first**, AI features later
- Write **only code when requested**, no explanations unless explicitly asked
- Include **sample test cases** for every module

## Next Steps for Claude
1. Create folder structure (web, mobile, backend, AI, cloud, docs)
2. Generate database models
3. Generate backend API routes
4. Generate frontend components
5. Generate mobile screens
6. Integrate AI modules
7. Add notifications and cloud storage integration
8. Prepare deployment scripts
