"""Tests for vector store factory."""

from __future__ import annotations

import pytest
from pydantic import SecretStr

from py_retrieval.exceptions import VectorStoreError
from py_retrieval.factory import create_vector_store
from py_retrieval.models import VectorStoreConfig
from py_retrieval.pinecone_store import PineconeVectorStore
from py_retrieval.protocols import VectorStore


@pytest.fixture
def pinecone_config() -> VectorStoreConfig:
    return VectorStoreConfig(
        provider="pinecone",
        api_key=SecretStr("test-key"),
        index_name="test-index",
    )


class TestCreateVectorStore:
    def test_creates_pinecone_store(self, pinecone_config: VectorStoreConfig) -> None:
        store = create_vector_store(pinecone_config)
        assert isinstance(store, PineconeVectorStore)

    def test_pinecone_store_satisfies_protocol(self, pinecone_config: VectorStoreConfig) -> None:
        store = create_vector_store(pinecone_config)
        assert isinstance(store, VectorStore)

    def test_unknown_provider_raises_error(self) -> None:
        config = VectorStoreConfig(
            provider="unknown-db",
            api_key=SecretStr("key"),
            index_name="idx",
        )
        with pytest.raises(VectorStoreError, match="Unknown provider: 'unknown-db'"):
            create_vector_store(config)

    def test_error_message_lists_supported_providers(self) -> None:
        config = VectorStoreConfig(
            provider="qdrant",
            api_key=SecretStr("key"),
            index_name="idx",
        )
        with pytest.raises(VectorStoreError, match="Supported: pinecone"):
            create_vector_store(config)

    def test_passes_config_to_store(self, pinecone_config: VectorStoreConfig) -> None:
        store = create_vector_store(pinecone_config)
        assert store._config.index_name == "test-index"
        assert store._config.embedding_model == "text-embedding-3-small"
