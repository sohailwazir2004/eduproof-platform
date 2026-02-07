# Database Schema

## Entity Relationship

```
User (1) ──────── (1) Student/Teacher/Parent/Principal
  │
  └── role, email, password_hash

School (1) ──────── (N) Class
  │
  └── name, address

Class (N) ──────── (N) Teacher
Class (1) ──────── (N) Student

Subject (N) ──────── (N) Teacher
Subject (N) ──────── (N) Class

Homework (N) ──────── (1) Teacher
Homework (N) ──────── (1) Class
Homework (N) ──────── (1) Subject
Homework (N) ──────── (0..1) Textbook

Submission (N) ──────── (1) Homework
Submission (N) ──────── (1) Student

Parent (1) ──────── (N) Student
```

## Tables

See individual model files in `backend/app/models/`.
