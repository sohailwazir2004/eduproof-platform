"""
Test script for EduProof API endpoints
"""
import httpx
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint"""
    print("\n1. Testing Health Endpoint...")
    try:
        response = httpx.get("http://localhost:8000/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_register():
    """Test user registration"""
    print("\n2. Testing User Registration...")

    user_data = {
        "email": "test.teacher@school.com",
        "first_name": "Test",
        "last_name": "Teacher",
        "phone": "+1234567890",
        "password": "SecurePass123",
        "confirm_password": "SecurePass123",
        "role": "teacher"
    }

    try:
        response = httpx.post(
            f"{BASE_URL}/auth/register",
            json=user_data,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:500]}")

        if response.status_code == 201:
            return response.json()
        return None
    except Exception as e:
        print(f"   Error: {e}")
        return None

def test_login(email="test.teacher@school.com", password="SecurePass123"):
    """Test user login"""
    print("\n3. Testing User Login...")

    credentials = {
        "email": email,
        "password": password
    }

    try:
        response = httpx.post(
            f"{BASE_URL}/auth/login",
            json=credentials,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:500]}")

        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"   Error: {e}")
        return None

def test_get_me(access_token):
    """Test get current user endpoint"""
    print("\n4. Testing Get Current User...")

    try:
        response = httpx.get(
            f"{BASE_URL}/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:500]}")

        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"   Error: {e}")
        return None

def main():
    """Run all tests"""
    print("=" * 60)
    print("EduProof API End-to-End Tests")
    print("=" * 60)

    # Test 1: Health check
    health_ok = test_health()

    # Test 2: Register user
    user_response = test_register()

    # Test 3: Login
    token_response = test_login()

    # Test 4: Get current user
    if token_response and 'access_token' in token_response:
        user_me = test_get_me(token_response['access_token'])

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"1. Health Check: {'✓ PASSED' if health_ok else '✗ FAILED'}")
    print(f"2. User Registration: {'✓ PASSED' if user_response else '✗ FAILED'}")
    print(f"3. User Login: {'✓ PASSED' if token_response else '✗ FAILED'}")
    print(f"4. Get Current User: {'✓ PASSED' if token_response and user_me else '✗ FAILED'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
