"""Custom exceptions for the application."""

from typing import Any


class AppError(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppError):
    """Resource not found exception."""

    def __init__(
        self,
        message: str = "Resource not found",
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code=404, error_code=error_code, details=details)


class ValidationError(AppError):
    """Validation error exception."""

    def __init__(
        self,
        message: str = "Validation error",
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code=422, error_code=error_code, details=details)


class UnauthorizedError(AppError):
    """Unauthorized access exception."""

    def __init__(
        self,
        message: str = "Unauthorized",
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code=401, error_code=error_code, details=details)


class ForbiddenError(AppError):
    """Forbidden access exception."""

    def __init__(
        self,
        message: str = "Forbidden",
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code=403, error_code=error_code, details=details)


class ConflictError(AppError):
    """Resource conflict exception."""

    def __init__(
        self,
        message: str = "Resource conflict",
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message, status_code=409, error_code=error_code, details=details)
