# EduProof Platform - Testing Checklist

Use this checklist to systematically test all features after the backend restart.

---

## Pre-Testing Setup

### 1. Verify Services Running

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Database file exists: `backend/eduproof.db`

### 2. Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Expected: {"status":"healthy","app":"EduProof","environment":"development"}
```

- [ ] Backend health check returns 200 OK
- [ ] Frontend loads in browser
- [ ] No console errors in browser DevTools

---

## Phase 1: Authentication & User Management

### Test Script

```bash
cd backend
python test_simple.py
```

### Manual Testing

#### 1.1 User Registration

**Test Case:** Register new teacher
- [ ] Navigate to http://localhost:3000/register
- [ ] Fill in form:
  - Email: teacher1@school.com
  - Password: SecurePass123
  - First Name: John
  - Last Name: Doe
  - Role: Teacher
- [ ] Submit form
- [ ] Verify: Success message shown
- [ ] Verify: User created in database

**API Test:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher1@school.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123",
    "role": "teacher"
  }'
```

Expected: 201 Created with user data

#### 1.2 User Login

**Test Case:** Login with created user
- [ ] Navigate to http://localhost:3000/login
- [ ] Enter credentials:
  - Email: teacher1@school.com
  - Password: SecurePass123
- [ ] Submit form
- [ ] Verify: Redirected to dashboard
- [ ] Verify: Token stored in localStorage
- [ ] Verify: User info displayed

**API Test:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher1@school.com",
    "password": "SecurePass123"
  }'
```

Expected: 200 OK with access_token and refresh_token

#### 1.3 Get Current User

**Test Case:** Fetch logged-in user data
- [ ] Use access token from login
- [ ] Call GET /api/v1/users/me
- [ ] Verify: User data returned

**API Test:**
```bash
# First login and get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"teacher1@school.com","password":"SecurePass123"}' \
  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# Then get user info
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"
```

Expected: 200 OK with user profile

#### 1.4 Password Change

**Test Case:** Change user password
- [ ] Login first
- [ ] Navigate to profile/settings
- [ ] Change password
- [ ] Verify: Success message
- [ ] Logout and login with new password
- [ ] Verify: Can login with new password

#### 1.5 Password Reset

**Test Case:** Reset forgotten password
- [ ] Request password reset
- [ ] Get reset token (in development, it's returned)
- [ ] Use token to reset password
- [ ] Login with new password

---

## Phase 2: Role-Specific Features

### 2.1 Teacher Role

#### Create Class
- [ ] Teacher can create a new class
- [ ] Specify grade, section, academic year
- [ ] Class appears in teacher's class list

#### Upload Textbook
- [ ] Teacher can upload PDF textbook
- [ ] Select subject and class
- [ ] File uploads successfully
- [ ] Textbook appears in list

#### Create Homework Assignment
- [ ] Teacher selects textbook
- [ ] Specifies page range
- [ ] Sets due date
- [ ] Assigns to class
- [ ] Homework appears in class feed

#### View Submissions
- [ ] Teacher can see all submissions for homework
- [ ] Can view student's submitted work
- [ ] Can grade submission
- [ ] Can add feedback

### 2.2 Student Role

#### Register as Student
- [ ] Register with student role
- [ ] Provide grade level
- [ ] Link to parent (optional)

#### View Homework
- [ ] Student sees assigned homework
- [ ] Can view textbook pages
- [ ] Sees due date and requirements

#### Submit Homework
- [ ] Student can upload image/PDF
- [ ] Submission is recorded
- [ ] Can view submission status

#### View Grades
- [ ] Student can see grades
- [ ] Can view teacher feedback

### 2.3 Parent Role

#### Register as Parent
- [ ] Register with parent role
- [ ] Link to student(s)

#### View Child's Homework
- [ ] Parent sees child's assigned homework
- [ ] Can view submission status
- [ ] Cannot submit on behalf of child

#### View Child's Performance
- [ ] Parent sees grades
- [ ] View teacher feedback
- [ ] Track progress over time

### 2.4 Principal Role

#### Register as Principal
- [ ] Register with principal role
- [ ] Link to school

#### View Analytics
- [ ] Overall submission rates
- [ ] Grade distributions
- [ ] Teacher performance
- [ ] Class performance

#### Manage Users
- [ ] View all teachers
- [ ] View all students
- [ ] Activate/deactivate accounts

---

## Phase 3: File Upload & Storage

### 3.1 Textbook Upload

**Test Case:** Upload PDF textbook
- [ ] Teacher uploads PDF file
- [ ] File size validation works
- [ ] File type validation works
- [ ] Progress indicator shows
- [ ] File stored in cloud/local storage
- [ ] URL saved in database

**API Test:**
```bash
curl -X POST http://localhost:8000/api/v1/textbooks/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@sample.pdf" \
  -F "title=Mathematics Grade 10" \
  -F "subject_id=uuid" \
  -F "class_id=uuid"
```

### 3.2 Homework Submission Upload

**Test Case:** Student uploads homework
- [ ] Student selects homework
- [ ] Uploads image or PDF
- [ ] File validated
- [ ] File stored
- [ ] Submission recorded

---

## Phase 4: Database Operations

### 4.1 Data Integrity

**Check Users:**
```bash
cd backend
python -c "
import sqlite3
conn = sqlite3.connect('eduproof.db')
cursor = conn.cursor()
cursor.execute('SELECT email, role, is_active FROM users')
print('Users:', cursor.fetchall())
conn.close()
"
```

**Check Relationships:**
```bash
python -c "
import sqlite3
conn = sqlite3.connect('eduproof.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM teacher_classes')
print('Teacher-Class links:', cursor.fetchone()[0])
cursor.execute('SELECT COUNT(*) FROM teacher_subjects')
print('Teacher-Subject links:', cursor.fetchone()[0])
conn.close()
"
```

### 4.2 Data Validation

- [ ] Email uniqueness enforced
- [ ] Password strength validated
- [ ] Foreign key constraints work
- [ ] Cascade deletes work correctly

---

## Phase 5: API Error Handling

### 5.1 Authentication Errors

**Test invalid credentials:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"wrong@email.com","password":"wrong"}'
```
- [ ] Returns 401 Unauthorized
- [ ] Clear error message

**Test expired token:**
- [ ] Create token with past expiry
- [ ] Try to use it
- [ ] Should return 401

**Test missing token:**
```bash
curl http://localhost:8000/api/v1/users/me
```
- [ ] Returns 401 Unauthorized

### 5.2 Validation Errors

**Test weak password:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@test.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "weak",
    "confirm_password": "weak",
    "role": "student"
  }'
```
- [ ] Returns 422 Validation Error
- [ ] Clear error message about password requirements

**Test duplicate email:**
- [ ] Try to register with existing email
- [ ] Should return 409 Conflict

**Test invalid email format:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "not-an-email",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123",
    "role": "student"
  }'
```
- [ ] Returns 422 Validation Error

---

## Phase 6: Frontend Integration

### 6.1 Navigation

- [ ] All routes work
- [ ] Protected routes redirect to login
- [ ] Role-based route protection works

### 6.2 Forms

- [ ] All forms validate input
- [ ] Error messages display correctly
- [ ] Success messages display correctly
- [ ] Loading states work

### 6.3 API Integration

- [ ] API calls include auth token
- [ ] 401 errors trigger token refresh
- [ ] Failed refresh redirects to login
- [ ] Network errors handled gracefully

### 6.4 Browser Console

- [ ] No JavaScript errors
- [ ] No React warnings
- [ ] API responses logged (in dev mode)

---

## Phase 7: Performance

### 7.1 Response Times

- [ ] Health check: < 100ms
- [ ] Login: < 500ms
- [ ] Get user: < 200ms
- [ ] List queries: < 1s
- [ ] File uploads: Progress indicator works

### 7.2 Concurrent Users

- [ ] Multiple users can login simultaneously
- [ ] No race conditions
- [ ] Database connections handled properly

---

## Phase 8: AI Features (Future)

### 8.1 OCR

- [ ] Handwritten text recognized
- [ ] Math equations recognized
- [ ] Diagrams preserved

### 8.2 Homework Analysis

- [ ] Content validated against textbook
- [ ] Completeness checked
- [ ] Suggestions provided

---

## Test Results Summary

### Critical Issues
- [ ] No critical bugs blocking functionality

### High Priority Issues
- [ ] List any high priority bugs found

### Medium Priority Issues
- [ ] List medium priority issues

### Low Priority Issues
- [ ] List cosmetic or minor issues

### Enhancement Suggestions
- [ ] List feature improvements

---

## Sign-Off

**Tested By:** _________________
**Date:** _________________
**Backend Version:** _________________
**Frontend Version:** _________________

**Overall Status:**
- [ ] Ready for Production
- [ ] Ready for Staging
- [ ] Needs Fixes
- [ ] Major Issues Found

**Notes:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
