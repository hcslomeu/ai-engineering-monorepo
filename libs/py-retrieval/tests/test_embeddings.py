"""Tests for OpenAIEmbeddingProvider."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import SecretStr

from py_retrieval.embeddings import _MAX_BATCH_SIZE, OpenAIEmbeddingProvider
from py_retrieval.exceptions import EmbeddingError


def _make_embedding_response(vectors: list[list[float]]) -> MagicMock:
    """Build a mock OpenAI embedding response."""
    data = []
    for i, vec in enumerate(vectors):
        item = MagicMock()
        item.index = i
        item.embedding = vec
        data.append(item)
    response = MagicMock()
    response.data = data
    return response


@pytest.fixture
def provider() -> OpenAIEmbeddingProvider:
    return OpenAIEmbeddingProvider(
        api_key=SecretStr("test-key"),
        model="text-embedding-3-small",
        dimensions=3,
    )


class TestEmbed:
    async def test_single_text(self, provider: OpenAIEmbeddingProvider) -> None:
        mock_response = _make_embedding_response([[0.1, 0.2, 0.3]])
        provider._client.embeddings.create = AsyncMock(return_value=mock_response)

        result = await provider.embed(["hello"])

        assert result == [[0.1, 0.2, 0.3]]
        provider._client.embeddings.create.assert_called_once_with(
            model="text-embedding-3-small",
            input=["hello"],
            dimensions=3,
        )

    async def test_multiple_texts(self, provider: OpenAIEmbeddingProvider) -> None:
        mock_response = _make_embedding_response([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
        provider._client.embeddings.create = AsyncMock(return_value=mock_response)

        result = await provider.embed(["text1", "text2"])

        assert len(result) == 2
        assert result[0] == [0.1, 0.2, 0.3]
        assert result[1] == [0.4, 0.5, 0.6]

    async def test_empty_list(self, provider: OpenAIEmbeddingProvider) -> None:
        result = await provider.embed([])
        assert result == []

    async def test_preserves_order_from_api(self, provider: OpenAIEmbeddingProvider) -> None:
        """Response items may arrive out of order; embed() must sort by index."""
        item_1 = MagicMock(index=1, embedding=[0.4, 0.5, 0.6])
        item_0 = MagicMock(index=0, embedding=[0.1, 0.2, 0.3])
        response = MagicMock(data=[item_1, item_0])  # reversed order
        provider._client.embeddings.create = AsyncMock(return_value=response)

        result = await provider.embed(["first", "second"])

        assert result[0] == [0.1, 0.2, 0.3]  # index 0
        assert result[1] == [0.4, 0.5, 0.6]  # index 1

    async def test_batching(self, provider: OpenAIEmbeddingProvider) -> None:
        """Texts exceeding _MAX_BATCH_SIZE are split into multiple API calls."""
        texts = [f"text-{i}" for i in range(_MAX_BATCH_SIZE + 10)]

        batch1_response = _make_embedding_response([[float(i)] for i in range(_MAX_BATCH_SIZE)])
        batch2_response = _make_embedding_response([[float(i)] for i in range(10)])
        provider._client.embeddings.create = AsyncMock(
            side_effect=[batch1_response, batch2_response]
        )

        result = await provider.embed(texts)

        assert len(result) == _MAX_BATCH_SIZE + 10
        assert provider._client.embeddings.create.call_count == 2

    @patch("py_retrieval.embeddings.logger")
    async def test_api_error_raises_embedding_error(
        self, _mock_logger: MagicMock, provider: OpenAIEmbeddingProvider
    ) -> None:
        provider._client.embeddings.create = AsyncMock(side_effect=ValueError("unexpected error"))

        with pytest.raises(EmbeddingError, match="Failed to generate embeddings"):
            await provider.embed(["hello"])

    async def test_api_key_not_leaked(self) -> None:
        provider = OpenAIEmbeddingProvider(api_key=SecretStr("super-secret"))
        assert "super-secret" not in str(provider._model)
        assert "super-secret" not in repr(provider._dimensions)
