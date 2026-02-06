"""Base exception classes for py-core."""


class PyCorError(Exception):
    """Base exception for all py-core errors."""

    def __init__(self, message: str, *, details: dict | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(message)


class ConfigurationError(PyCorError):
    """Raised when configuration is invalid or missing."""


class ValidationError(PyCorError):
    """Raised when data validation fails."""
