"""Factory for creating vector store instances."""

from __future__ import annotations

from py_retrieval.embeddings import OpenAIEmbeddingProvider
from py_retrieval.exceptions import VectorStoreError
from py_retrieval.models import VectorStoreConfig
from py_retrieval.pinecone_store import PineconeVectorStore
from py_retrieval.protocols import VectorStore


def create_vector_store(config: VectorStoreConfig) -> VectorStore:
    """Create a vector store instance based on configuration.

    Args:
        config: Vector store configuration specifying provider and credentials.

    Returns:
        A configured vector store instance (use as async context manager).

    Raises:
        VectorStoreError: If the provider is not supported.
    """
    providers = {
        "pinecone": _create_pinecone,
    }

    builder = providers.get(config.provider)
    if builder is None:
        supported = ", ".join(sorted(providers.keys()))
        raise VectorStoreError(f"Unknown provider: '{config.provider}'. Supported: {supported}")

    return builder(config)


def _create_pinecone(config: VectorStoreConfig) -> PineconeVectorStore:
    """Build a PineconeVectorStore with its embedding provider."""
    embedding_provider = OpenAIEmbeddingProvider(
        api_key=config.api_key,
        model=config.embedding_model,
        dimensions=config.embedding_dimensions,
    )
    return PineconeVectorStore(config=config, embedding_provider=embedding_provider)
