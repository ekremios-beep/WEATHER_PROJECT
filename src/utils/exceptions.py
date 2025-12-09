# src/utils/exceptions.py
"""
Custom exception hierarchy used throughout the weather project.

All project-specific exceptions inherit from `BaseAppError`,
allowing predictable and unified error handling.
"""

from __future__ import annotations


class BaseAppError(Exception):
    """
    Base class for all custom exceptions in the project.

    This allows catching all project-level errors with:

        except BaseAppError:

    Each derived exception can optionally include a readable message
    or an underlying cause.
    """

    def __init__(self, message: str = "", *, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        if self.cause:
            return f"{super().__str__()} (Caused by: {self.cause})"
        return super().__str__()


class WeatherApiError(BaseAppError):
    """
    Raised when the weather API request fails,
    returns invalid data,
    or responds with unexpected structure.
    """


class DatabaseError(BaseAppError):
    """
    Raised for database-related failures,
    such as connection errors or failed writes.
    """


class EmailSendError(BaseAppError):
    """
    Raised when sending an email fails, whether due to:
    - SMTP connection issues
    - Authentication failure
    - TLS negotiation problems
    - Unexpected server responses
    """
