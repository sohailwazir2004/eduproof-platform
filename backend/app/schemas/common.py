# common.py - Common Pydantic Schemas
#
# Shared schemas used across the application.

"""
Common Schemas

- PaginationParams: Pagination query parameters
- PaginatedResponse: Generic paginated response wrapper
- MessageResponse: Simple message response
- ErrorResponse: Error response structure
"""

from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, Field

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    skip: int = Field(0, ge=0, description="Number of records to skip")
    limit: int = Field(20, ge=1, le=100, description="Maximum records to return")


class PaginatedResponse(BaseModel):
    """Generic paginated response wrapper."""
    items: List[Any] = Field(..., description="List of items")
    total: int = Field(..., ge=0, description="Total number of items")
    skip: int = Field(..., ge=0, description="Number of skipped items")
    limit: int = Field(..., ge=1, description="Maximum items per page")
    has_more: bool = Field(default=False, description="More items available")

    def __init__(self, **data):
        super().__init__(**data)
        object.__setattr__(self, 'has_more', self.skip + len(self.items) < self.total)


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str = Field(..., description="Response message")
    success: bool = Field(default=True, description="Operation success status")


class ErrorDetail(BaseModel):
    """Error detail structure."""
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Any] = Field(None, description="Additional error details")


class ErrorResponse(BaseModel):
    """Error response structure."""
    success: bool = Field(default=False, description="Always false for errors")
    error: ErrorDetail = Field(..., description="Error details")


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Health status")
    app: str = Field(..., description="Application name")
    environment: str = Field(..., description="Environment name")


class FileUploadResponse(BaseModel):
    """File upload response."""
    file_url: str = Field(..., description="URL of uploaded file")
    file_name: str = Field(..., description="Original file name")
    file_size: int = Field(..., description="File size in bytes")
    content_type: str = Field(..., description="File content type")
