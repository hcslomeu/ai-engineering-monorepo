"""Embedding provider implementations."""

from __future__ import annotations

import openai
from pydantic import SecretStr
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from py_core import get_logger
from py_retrieval.exceptions import EmbeddingError

logger = get_logger("embeddings")

# OpenAI allows up to 2048 texts per request
_MAX_BATCH_SIZE = 2048


class OpenAIEmbeddingProvider:
    """Generate embeddings via OpenAI API.

    Satisfies the ``EmbeddingProvider`` protocol via structural subtyping.
    """

    def __init__(
        self,
        api_key: SecretStr,
        model: str = "text-embedding-3-small",
        dimensions: int = 1536,
    ) -> None:
        self._model = model
        self._dimensions = dimensions
        self._client = openai.AsyncOpenAI(api_key=api_key.get_secret_value())

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=0.5, max=5.0),
        retry=retry_if_exception_type((openai.RateLimitError, openai.APITimeoutError)),
        reraise=True,
    )
    async def _call_api(self, batch: list[str]) -> list[list[float]]:
        """Call OpenAI embeddings API for a single batch with retry."""
        response = await self._client.embeddings.create(
            model=self._model,
            input=batch,
            dimensions=self._dimensions,
        )
        sorted_data = sorted(response.data, key=lambda item: item.index)
        return [item.embedding for item in sorted_data]

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts.

        Handles batching automatically when input exceeds the API limit.
        Retries on transient OpenAI errors.

        Args:
            texts: Texts to embed.

        Returns:
            Embedding vectors in the same order as input texts.

        Raises:
            EmbeddingError: If the OpenAI API call fails after retries.
        """
        if not texts:
            return []

        all_embeddings: list[list[float]] = []

        try:
            for i in range(0, len(texts), _MAX_BATCH_SIZE):
                batch = texts[i : i + _MAX_BATCH_SIZE]
                embeddings = await self._call_api(batch)
                all_embeddings.extend(embeddings)

            logger.info(
                "embeddings_generated",
                total_texts=len(texts),
                batches=len(range(0, len(texts), _MAX_BATCH_SIZE)),
                model=self._model,
                dimensions=self._dimensions,
            )
        except Exception as exc:
            logger.error(
                "embeddings_failed",
                total_texts=len(texts),
                model=self._model,
                error_type=type(exc).__name__,
            )
            raise EmbeddingError("Failed to generate embeddings") from exc

        return all_embeddings
