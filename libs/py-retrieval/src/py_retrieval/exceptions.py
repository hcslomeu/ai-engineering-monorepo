"""Exception hierarchy for py-retrieval."""

from py_core.exceptions import PyCorError


class VectorStoreError(PyCorError):
    """Base exception for vector store operations."""


class EmbeddingError(VectorStoreError):
    """Raised when embedding generation fails."""


class VectorStoreConnectionError(VectorStoreError):
    """Raised when connection to the vector store provider fails."""
