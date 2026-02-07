# Cloud Services - EduProof Storage & Infrastructure

## Overview
Cloud storage and infrastructure configuration for the platform.

## Tech Stack
- AWS S3 / Cloudinary (file storage)
- Firebase (notifications)
- AWS Lambda (optional serverless functions)
- Docker & Docker Compose

## Structure
```
cloud/
├── storage/          # S3/Cloudinary integration
├── notifications/    # Firebase push/email services
├── infrastructure/   # Terraform/CloudFormation configs
├── docker/           # Docker configurations
└── scripts/          # Deployment & utility scripts
```

## Services
1. **Storage**: Secure file upload/download for PDFs and images
2. **Notifications**: Push and email notifications via Firebase
3. **Infrastructure**: IaC templates for cloud deployment

## Setup
1. Configure AWS/Cloudinary credentials
2. Set up Firebase project
3. Run `docker-compose up` for local development
