"""Tests for PineconeVectorStore."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import SecretStr

from py_retrieval.exceptions import VectorStoreConnectionError, VectorStoreError
from py_retrieval.models import Document, VectorStoreConfig
from py_retrieval.pinecone_store import PineconeVectorStore


@pytest.fixture
def config() -> VectorStoreConfig:
    return VectorStoreConfig(
        provider="pinecone",
        api_key=SecretStr("test-key"),
        index_name="test-index",
        namespace="test-ns",
        embedding_dimensions=3,
    )


@pytest.fixture
def mock_embedding_provider() -> AsyncMock:
    provider = AsyncMock()
    provider.embed = AsyncMock(return_value=[[0.1, 0.2, 0.3]])
    return provider


@pytest.fixture
def mock_index() -> MagicMock:
    index = MagicMock()
    index.upsert = MagicMock()
    index.query = MagicMock()
    index.delete = MagicMock()
    return index


@pytest.fixture
def store(
    config: VectorStoreConfig,
    mock_embedding_provider: AsyncMock,
    mock_index: MagicMock,
) -> PineconeVectorStore:
    s = PineconeVectorStore(config=config, embedding_provider=mock_embedding_provider)
    s._index = mock_index
    s._client = MagicMock()
    return s


class TestUpsert:
    async def test_upsert_generates_embeddings(
        self, store: PineconeVectorStore, mock_embedding_provider: AsyncMock
    ) -> None:
        mock_embedding_provider.embed.return_value = [[0.1, 0.2, 0.3]]
        docs = [Document(id="doc-1", text="hello")]

        ids = await store.upsert(docs)

        assert ids == ["doc-1"]
        mock_embedding_provider.embed.assert_called_once_with(["hello"])

    async def test_upsert_skips_embedding_for_precomputed(
        self, store: PineconeVectorStore, mock_embedding_provider: AsyncMock
    ) -> None:
        docs = [Document(id="doc-1", text="hello", vector=[0.4, 0.5, 0.6])]

        ids = await store.upsert(docs)

        assert ids == ["doc-1"]
        mock_embedding_provider.embed.assert_not_called()

    async def test_upsert_assigns_uuid_when_id_is_none(
        self, store: PineconeVectorStore, mock_embedding_provider: AsyncMock
    ) -> None:
        mock_embedding_provider.embed.return_value = [[0.1, 0.2, 0.3]]
        docs = [Document(text="no id")]

        ids = await store.upsert(docs)

        assert len(ids) == 1
        assert ids[0] is not None
        assert len(ids[0]) == 36  # UUID format

    async def test_upsert_empty_list(self, store: PineconeVectorStore) -> None:
        ids = await store.upsert([])
        assert ids == []

    async def test_upsert_calls_pinecone(
        self, store: PineconeVectorStore, mock_index: MagicMock, mock_embedding_provider: AsyncMock
    ) -> None:
        mock_embedding_provider.embed.return_value = [[0.1, 0.2, 0.3]]
        docs = [Document(id="doc-1", text="hello")]

        await store.upsert(docs)

        mock_index.upsert.assert_called_once()
        call_kwargs = mock_index.upsert.call_args
        vectors = call_kwargs.kwargs.get("vectors") or call_kwargs[1].get("vectors")
        assert vectors[0][0] == "doc-1"
        assert vectors[0][1] == [0.1, 0.2, 0.3]
        assert vectors[0][2]["text"] == "hello"

    async def test_upsert_preserves_existing_text_in_metadata(
        self, store: PineconeVectorStore, mock_index: MagicMock, mock_embedding_provider: AsyncMock
    ) -> None:
        mock_embedding_provider.embed.return_value = [[0.1, 0.2, 0.3]]
        docs = [Document(id="doc-1", text="hello", metadata={"text": "custom text"})]

        await store.upsert(docs)

        call_kwargs = mock_index.upsert.call_args
        vectors = call_kwargs.kwargs.get("vectors") or call_kwargs[1].get("vectors")
        assert vectors[0][2]["text"] == "custom text"

    async def test_upsert_error_raises_vectorstore_error(
        self,
        store: PineconeVectorStore,
        mock_index: MagicMock,
        mock_embedding_provider: AsyncMock,
    ) -> None:
        mock_embedding_provider.embed.return_value = [[0.1, 0.2, 0.3]]
        mock_index.upsert.side_effect = RuntimeError("connection lost")

        with pytest.raises(VectorStoreError, match="Upsert failed"):
            await store.upsert([Document(id="doc-1", text="hello")])


class TestQuery:
    async def test_query_returns_results(
        self,
        store: PineconeVectorStore,
        mock_index: MagicMock,
        mock_embedding_provider: AsyncMock,
    ) -> None:
        mock_embedding_provider.embed.return_value = [[0.1, 0.2, 0.3]]
        match = MagicMock(id="vec-1", score=0.95, metadata={"source": "test", "text": "hello world"})
        mock_index.query.return_value = MagicMock(matches=[match])

        results = await store.query("hello", top_k=3)

        assert len(results) == 1
        assert results[0].id == "vec-1"
        assert results[0].score == 0.95
        assert results[0].text == "hello world"
        assert results[0].metadata == {"source": "test", "text": "hello world"}

    async def test_query_passes_filters(
        self,
        store: PineconeVectorStore,
        mock_index: MagicMock,
        mock_embedding_provider: AsyncMock,
    ) -> None:
        mock_embedding_provider.embed.return_value = [[0.1, 0.2, 0.3]]
        mock_index.query.return_value = MagicMock(matches=[])

        await store.query("hello", top_k=5, filters={"category": "finance"})

        mock_index.query.assert_called_once()
        call_kwargs = mock_index.query.call_args.kwargs
        assert call_kwargs["filter"] == {"category": "finance"}
        assert call_kwargs["top_k"] == 5

    async def test_query_error_raises_vectorstore_error(
        self,
        store: PineconeVectorStore,
        mock_index: MagicMock,
        mock_embedding_provider: AsyncMock,
    ) -> None:
        mock_embedding_provider.embed.return_value = [[0.1, 0.2, 0.3]]
        mock_index.query.side_effect = RuntimeError("timeout")

        with pytest.raises(VectorStoreError, match="Query failed"):
            await store.query("hello")


class TestDelete:
    async def test_delete_calls_pinecone(
        self, store: PineconeVectorStore, mock_index: MagicMock
    ) -> None:
        await store.delete(["vec-1", "vec-2"])

        mock_index.delete.assert_called_once()
        call_kwargs = mock_index.delete.call_args.kwargs
        assert call_kwargs["ids"] == ["vec-1", "vec-2"]
        assert call_kwargs["namespace"] == "test-ns"

    async def test_delete_empty_list(
        self, store: PineconeVectorStore, mock_index: MagicMock
    ) -> None:
        await store.delete([])
        mock_index.delete.assert_not_called()

    async def test_delete_error_raises_vectorstore_error(
        self, store: PineconeVectorStore, mock_index: MagicMock
    ) -> None:
        mock_index.delete.side_effect = RuntimeError("forbidden")

        with pytest.raises(VectorStoreError, match="Delete failed"):
            await store.delete(["vec-1"])


class TestContextManager:
    async def test_connect_via_host(self, config: VectorStoreConfig) -> None:
        config_with_host = config.model_copy(update={"host": "my-index.svc.pinecone.io"})
        store = PineconeVectorStore(config=config_with_host, embedding_provider=AsyncMock())

        with patch("py_retrieval.pinecone_store.Pinecone") as mock_pc:
            mock_pc.return_value.Index.return_value = MagicMock()
            async with store:
                mock_pc.return_value.Index.assert_called_once_with(host="my-index.svc.pinecone.io")

    async def test_connect_via_name(self, config: VectorStoreConfig) -> None:
        store = PineconeVectorStore(config=config, embedding_provider=AsyncMock())

        with patch("py_retrieval.pinecone_store.Pinecone") as mock_pc:
            mock_pc.return_value.Index.return_value = MagicMock()
            async with store:
                mock_pc.return_value.Index.assert_called_once_with(name="test-index")

    async def test_connection_error(self, config: VectorStoreConfig) -> None:
        store = PineconeVectorStore(config=config, embedding_provider=AsyncMock())

        with patch("py_retrieval.pinecone_store.Pinecone", side_effect=RuntimeError("bad key")):
            with pytest.raises(VectorStoreConnectionError, match="Failed to connect"):
                async with store:
                    pass
