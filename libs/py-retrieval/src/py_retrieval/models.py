"""Data models for vector store operations."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, SecretStr


class Document(BaseModel):
    """A document to be stored in the vector store."""

    id: str | None = None
    text: str
    vector: list[float] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class QueryResult(BaseModel):
    """A single result from a vector store query."""

    id: str
    score: float
    text: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class VectorStoreConfig(BaseModel):
    """Configuration for creating a vector store instance."""

    provider: str
    api_key: SecretStr
    index_name: str
    namespace: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    host: str | None = None
