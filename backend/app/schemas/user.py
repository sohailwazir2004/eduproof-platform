# user.py - User Pydantic Schemas
#
# Request/response schemas for user operations.

"""
User Schemas

- UserBase: Shared fields
- UserCreate: Registration request
- UserUpdate: Profile update request
- UserResponse: API response
- UserInDB: Internal with hashed password
"""

from pydantic import BaseModel, EmailStr, Field, validator, UUID4
from typing import Optional
from datetime import datetime
from app.core.security import UserRole


class UserBase(BaseModel):
    """Base user schema with shared fields."""
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8, description="User password")
    confirm_password: str = Field(..., min_length=8, description="Password confirmation")
    role: UserRole = Field(..., description="User role")

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@school.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+1234567890",
                "password": "SecurePass123",
                "confirm_password": "SecurePass123",
                "role": "teacher"
            }
        }


class UserUpdate(BaseModel):
    """User update schema (all fields optional)."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+1234567890"
            }
        }


class UserResponse(UserBase):
    """User response schema (returned to client)."""
    id: UUID4 = Field(..., description="User ID")
    role: UserRole = Field(..., description="User role")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    is_active: bool = Field(..., description="Active status")
    is_verified: bool = Field(..., description="Email verification status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "john.doe@school.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+1234567890",
                "role": "teacher",
                "avatar_url": "https://example.com/avatar.jpg",
                "is_active": True,
                "is_verified": True,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }


class UserInDB(UserResponse):
    """User schema with sensitive fields (internal use only)."""
    hashed_password: str = Field(..., description="Hashed password")


# Role-specific creation schemas

class StudentRegistration(BaseModel):
    """Student-specific registration fields."""
    grade_level: str = Field(..., description="Grade level")
    class_id: Optional[UUID4] = Field(None, description="Assigned class ID")
    parent_id: Optional[UUID4] = Field(None, description="Parent/Guardian ID")


class TeacherRegistration(BaseModel):
    """Teacher-specific registration fields."""
    subject: str = Field(..., description="Primary subject taught")
    qualification: Optional[str] = Field(None, description="Highest qualification")


class ParentRegistration(BaseModel):
    """Parent-specific registration fields."""
    relationship: str = Field(..., description="Relationship to student (father/mother/guardian)")


class PrincipalRegistration(BaseModel):
    """Principal-specific registration fields."""
    school_id: Optional[UUID4] = Field(None, description="School ID")


class UserWithRoleData(UserResponse):
    """User response with role-specific data included."""
    student_data: Optional[dict] = None
    teacher_data: Optional[dict] = None
    parent_data: Optional[dict] = None
    principal_data: Optional[dict] = None

    class Config:
        from_attributes = True
