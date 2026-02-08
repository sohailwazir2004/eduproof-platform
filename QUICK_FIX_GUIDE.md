# Quick Fix Guide - EduProof Platform

## Problem

Backend API endpoints returning 500 errors due to SQLAlchemy relationship mapping issue.

## Solution Applied

Fixed missing relationship in `backend/app/models/school.py`:

```python
# Added to SchoolClass model
textbooks: Mapped[List["Textbook"]] = relationship(
    "Textbook",
    back_populates="school_class"
)
```

## Action Required: RESTART BACKEND SERVER

The code fix has been applied, but the backend server is running cached code and needs to be restarted.

---

## How to Restart Backend (Choose ONE method)

### Method 1: If Running in Terminal

1. Find the terminal window running the backend
2. Press `Ctrl+C` to stop the server
3. Restart with:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --port 8000
   ```

### Method 2: Kill Process and Restart

1. Find Python processes:
   ```bash
   tasklist | findstr python
   ```

2. Kill the backend process (use the correct PID):
   ```bash
   taskkill /PID 11608 /F
   # or
   taskkill /PID 19804 /F
   ```

3. Restart backend:
   ```bash
   cd "C:\Users\HP\OneDrive\Desktop\AI School System\backend"
   python -m uvicorn app.main:app --reload --port 8000
   ```

### Method 3: Using Development Script (If Available)

```bash
cd "C:\Users\HP\OneDrive\Desktop\AI School System\backend"
python run_dev.py
```

---

## Verify the Fix

After restarting, run this test:

```bash
cd "C:\Users\HP\OneDrive\Desktop\AI School System\backend"
python test_simple.py
```

**Expected Output:**
```
[TEST 1] Health Endpoint - PASSED
[TEST 2] User Registration - PASSED
[TEST 3] User Login - PASSED
[TEST 4] Get Current User - PASSED
```

---

## Alternative: Quick Manual Test

Test registration endpoint directly:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@school.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123",
    "role": "teacher"
  }'
```

Should return 201 with user data instead of 500 error.

---

## What Changed

**File Modified:** `backend/app/models/school.py`

**Line ~106:** Added missing relationship mapping

**Before:**
```python
teachers: Mapped[List["Teacher"]] = relationship(...)
homework_assignments: Mapped[List["Homework"]] = relationship(...)
```

**After:**
```python
teachers: Mapped[List["Teacher"]] = relationship(...)
textbooks: Mapped[List["Textbook"]] = relationship(...)  # ADDED
homework_assignments: Mapped[List["Homework"]] = relationship(...)
```

This fixes the bidirectional relationship between `SchoolClass` and `Textbook` models.

---

## If Still Not Working

1. Check if models load correctly:
   ```bash
   cd backend
   python -c "from app.models import *; print('OK')"
   ```

2. Check database connection:
   ```bash
   cd backend
   python -c "import sqlite3; sqlite3.connect('eduproof.db').execute('SELECT 1'); print('OK')"
   ```

3. Check for any other Python processes:
   ```bash
   tasklist | findstr python
   ```

4. View server logs in the terminal where backend is running

---

## Summary

1. ✅ Bug identified: Missing SQLAlchemy relationship
2. ✅ Code fix applied: Added `textbooks` relationship to `SchoolClass`
3. ⏳ Action needed: Restart backend server
4. ✅ Verification: Run test_simple.py

**Once restarted, all API endpoints should work correctly.**
