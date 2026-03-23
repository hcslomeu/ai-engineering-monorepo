"""Protocol definitions for vector store and embedding providers."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from py_retrieval.models import Document, QueryResult


@runtime_checkable
class EmbeddingProvider(Protocol):
    """Contract for embedding generation providers.

    Any class with a matching ``embed`` method satisfies this protocol
    without explicit inheritance (structural subtyping).
    """

    async def embed(self, texts: list[str]) -> list[list[float]]: ...


@runtime_checkable
class VectorStore(Protocol):
    """Contract for vector store providers.

    Implementations must support async context manager protocol
    (``__aenter__`` / ``__aexit__``) for resource management.
    """

    async def __aenter__(self) -> VectorStore: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None: ...

    async def upsert(self, documents: list[Document]) -> list[str]: ...

    async def query(
        self,
        text: str,
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[QueryResult]: ...

    async def delete(self, ids: list[str]) -> None: ...
