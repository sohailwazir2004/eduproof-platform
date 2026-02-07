# API Documentation

## Overview

EduProof REST API documentation.

## Base URL

- Development: `http://localhost:8000`
- Production: `https://api.eduproof.com`

## Authentication

All endpoints (except `/auth/login` and `/auth/register`) require JWT authentication.

```
Authorization: Bearer <token>
```

## Endpoints

See individual documentation files:
- [Authentication](./authentication.md)
- [Users](./users.md)
- [Homework](./homework.md)
- [Submissions](./submissions.md)
- [Textbooks](./textbooks.md)
- [Analytics](./analytics.md)

## Error Codes

| Code | Description |
|------|-------------|
| 400  | Bad Request |
| 401  | Unauthorized |
| 403  | Forbidden |
| 404  | Not Found |
| 422  | Validation Error |
| 500  | Internal Server Error |
