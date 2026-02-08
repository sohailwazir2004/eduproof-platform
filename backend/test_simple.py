"""
Simple API test without special characters
"""
import httpx
import json

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 60)
print("EduProof API Tests")
print("=" * 60)

# Test 1: Health check
print("\n[TEST 1] Health Endpoint")
try:
    response = httpx.get("http://localhost:8000/health", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    health_ok = response.status_code == 200
    print("Result: PASSED" if health_ok else "Result: FAILED")
except Exception as e:
    print(f"Error: {e}")
    print("Result: FAILED")
    health_ok = False

# Test 2: Register user
print("\n[TEST 2] User Registration")
user_data = {
    "email": "test.teacher2@school.com",
    "first_name": "Test",
    "last_name": "Teacher",
    "phone": "+1234567890",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123",
    "role": "teacher"
}

try:
    response = httpx.post(f"{BASE_URL}/auth/register", json=user_data, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("Result: PASSED")
        register_ok = True
    else:
        print(f"Response: {response.text}")
        print("Result: FAILED")
        register_ok = False
except Exception as e:
    print(f"Error: {e}")
    print("Result: FAILED")
    register_ok = False

# Test 3: Login
print("\n[TEST 3] User Login")
credentials = {
    "email": "test.teacher2@school.com",
    "password": "SecurePass123"
}

try:
    response = httpx.post(f"{BASE_URL}/auth/login", json=credentials, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        print(f"Access Token: {token_data.get('access_token', '')[:50]}...")
        print(f"Role: {token_data.get('role')}")
        print("Result: PASSED")
        login_ok = True
        access_token = token_data.get('access_token')
    else:
        print(f"Response: {response.text}")
        print("Result: FAILED")
        login_ok = False
        access_token = None
except Exception as e:
    print(f"Error: {e}")
    print("Result: FAILED")
    login_ok = False
    access_token = None

# Test 4: Get current user
if access_token:
    print("\n[TEST 4] Get Current User")
    try:
        response = httpx.get(
            f"{BASE_URL}/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"User: {user_data.get('first_name')} {user_data.get('last_name')}")
            print(f"Email: {user_data.get('email')}")
            print(f"Role: {user_data.get('role')}")
            print("Result: PASSED")
            me_ok = True
        else:
            print(f"Response: {response.text}")
            print("Result: FAILED")
            me_ok = False
    except Exception as e:
        print(f"Error: {e}")
        print("Result: FAILED")
        me_ok = False
else:
    print("\n[TEST 4] Get Current User - SKIPPED (no token)")
    me_ok = False

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"1. Health Check: {'PASSED' if health_ok else 'FAILED'}")
print(f"2. User Registration: {'PASSED' if register_ok else 'FAILED'}")
print(f"3. User Login: {'PASSED' if login_ok else 'FAILED'}")
print(f"4. Get Current User: {'PASSED' if me_ok else 'FAILED'}")
print("=" * 60)
