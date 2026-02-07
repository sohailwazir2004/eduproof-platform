# exceptions.py - Custom Exception Classes
#
# Application-specific exceptions with proper HTTP status codes.

"""
Custom Exceptions

- NotFoundException: Resource not found (404)
- UnauthorizedException: Not authenticated (401)
- ForbiddenException: Not authorized (403)
- BadRequestException: Invalid request (400)
- ConflictException: Resource conflict (409)
- ValidationException: Validation error (422)
"""

from typing import Optional, Any


class AppException(Exception):
    """
    Base application exception with HTTP status code.
    All custom exceptions should inherit from this class.
    """

    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[Any] = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(message)


class NotFoundException(AppException):
    """Resource not found exception (404)."""

    def __init__(
        self,
        message: str = "Resource not found",
        error_code: str = "NOT_FOUND",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=404,
            error_code=error_code,
            message=message,
            details=details
        )


class UnauthorizedException(AppException):
    """Not authenticated exception (401)."""

    def __init__(
        self,
        message: str = "Authentication required",
        error_code: str = "UNAUTHORIZED",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=401,
            error_code=error_code,
            message=message,
            details=details
        )


class ForbiddenException(AppException):
    """Not authorized / insufficient permissions exception (403)."""

    def __init__(
        self,
        message: str = "Insufficient permissions",
        error_code: str = "FORBIDDEN",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=403,
            error_code=error_code,
            message=message,
            details=details
        )


class BadRequestException(AppException):
    """Invalid request exception (400)."""

    def __init__(
        self,
        message: str = "Invalid request",
        error_code: str = "BAD_REQUEST",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=400,
            error_code=error_code,
            message=message,
            details=details
        )


class ConflictException(AppException):
    """Resource conflict exception (409)."""

    def __init__(
        self,
        message: str = "Resource conflict",
        error_code: str = "CONFLICT",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=409,
            error_code=error_code,
            message=message,
            details=details
        )


class ValidationException(AppException):
    """Validation error exception (422)."""

    def __init__(
        self,
        message: str = "Validation error",
        error_code: str = "VALIDATION_ERROR",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=422,
            error_code=error_code,
            message=message,
            details=details
        )


class InternalServerException(AppException):
    """Internal server error exception (500)."""

    def __init__(
        self,
        message: str = "Internal server error",
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Any] = None
    ):
        super().__init__(
            status_code=500,
            error_code=error_code,
            message=message,
            details=details
        )
