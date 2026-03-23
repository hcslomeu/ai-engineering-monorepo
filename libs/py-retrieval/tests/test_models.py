"""Tests for py_retrieval data models."""

from __future__ import annotations

import pytest
from pydantic import SecretStr, ValidationError

from py_retrieval.models import Document, QueryResult, VectorStoreConfig


class TestDocument:
    def test_minimal_document(self) -> None:
        doc = Document(text="hello world")
        assert doc.text == "hello world"
        assert doc.id is None
        assert doc.vector is None
        assert doc.metadata == {}

    def test_document_with_all_fields(self) -> None:
        doc = Document(
            id="doc-1",
            text="test content",
            vector=[0.1, 0.2, 0.3],
            metadata={"source": "test"},
        )
        assert doc.id == "doc-1"
        assert doc.vector == [0.1, 0.2, 0.3]
        assert doc.metadata["source"] == "test"

    def test_document_requires_text(self) -> None:
        with pytest.raises(ValidationError):
            Document()  # type: ignore[call-arg]

    def test_metadata_isolation(self) -> None:
        """Each document gets its own metadata dict."""
        doc1 = Document(text="a")
        doc2 = Document(text="b")
        doc1.metadata["key"] = "value"
        assert "key" not in doc2.metadata


class TestQueryResult:
    def test_query_result(self) -> None:
        result = QueryResult(id="vec-1", score=0.95, text="matched text")
        assert result.id == "vec-1"
        assert result.score == 0.95
        assert result.text == "matched text"

    def test_query_result_without_text(self) -> None:
        result = QueryResult(id="vec-1", score=0.8)
        assert result.text is None
        assert result.metadata == {}

    def test_query_result_requires_id_and_score(self) -> None:
        with pytest.raises(ValidationError):
            QueryResult()  # type: ignore[call-arg]


class TestVectorStoreConfig:
    def test_full_config(self) -> None:
        config = VectorStoreConfig(
            provider="pinecone",
            api_key=SecretStr("secret-key"),
            index_name="my-index",
        )
        assert config.provider == "pinecone"
        assert config.api_key.get_secret_value() == "secret-key"
        assert config.index_name == "my-index"
        assert config.namespace == ""
        assert config.embedding_model == "text-embedding-3-small"
        assert config.embedding_dimensions == 1536
        assert config.host is None

    def test_api_key_is_secret(self) -> None:
        config = VectorStoreConfig(
            provider="pinecone",
            api_key=SecretStr("my-secret"),
            index_name="idx",
        )
        assert "my-secret" not in str(config)
        assert "my-secret" not in repr(config)

    def test_config_with_host(self) -> None:
        config = VectorStoreConfig(
            provider="pinecone",
            api_key=SecretStr("key"),
            index_name="idx",
            host="my-index-abc123.svc.us-east1-aws.pinecone.io",
        )
        assert config.host is not None

    def test_config_requires_provider_and_key(self) -> None:
        with pytest.raises(ValidationError):
            VectorStoreConfig(index_name="idx")  # type: ignore[call-arg]
