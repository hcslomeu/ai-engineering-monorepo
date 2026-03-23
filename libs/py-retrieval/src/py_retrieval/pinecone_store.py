"""Pinecone vector store implementation."""

from __future__ import annotations

import asyncio
import uuid
from typing import Any, Self

from pinecone import Pinecone

from py_core import get_logger
from py_retrieval.exceptions import VectorStoreConnectionError, VectorStoreError
from py_retrieval.models import Document, QueryResult, VectorStoreConfig
from py_retrieval.protocols import EmbeddingProvider

logger = get_logger("pinecone_store")

_UPSERT_BATCH_SIZE = 100


class PineconeVectorStore:
    """Pinecone implementation of the VectorStore protocol.

    Uses ``asyncio.to_thread`` to wrap the synchronous Pinecone SDK,
    keeping the async interface non-blocking.
    """

    def __init__(
        self,
        config: VectorStoreConfig,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        self._config = config
        self._embedding_provider = embedding_provider
        self._client: Pinecone | None = None
        self._index: Any = None

    async def __aenter__(self) -> Self:
        try:
            self._client = Pinecone(api_key=self._config.api_key.get_secret_value())

            if self._config.host:
                self._index = self._client.Index(host=self._config.host)
            else:
                self._index = self._client.Index(name=self._config.index_name)

            logger.info(
                "pinecone_connected",
                index=self._config.index_name,
                namespace=self._config.namespace,
            )
        except Exception as exc:
            raise VectorStoreConnectionError(f"Failed to connect to Pinecone: {exc}") from exc
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        self._index = None
        self._client = None
        logger.info("pinecone_disconnected", index=self._config.index_name)

    async def upsert(self, documents: list[Document]) -> list[str]:
        """Upsert documents into Pinecone.

        Generates embeddings for documents without pre-computed vectors,
        assigns UUIDs to documents without IDs, and batches upserts.

        Args:
            documents: Documents to upsert.

        Returns:
            List of document IDs that were upserted.
        """
        if not documents:
            return []

        # Assign IDs to documents that don't have one
        for doc in documents:
            if doc.id is None:
                doc.id = str(uuid.uuid4())

        # Generate embeddings for documents without pre-computed vectors
        docs_to_embed = [doc for doc in documents if doc.vector is None]
        if docs_to_embed:
            embeddings = await self._embedding_provider.embed(
                [doc.text for doc in docs_to_embed]
            )
            for doc, embedding in zip(docs_to_embed, embeddings, strict=True):
                doc.vector = embedding

        # Merge text into metadata for persistence (Pinecone stores metadata, not raw text)
        vectors = []
        for doc in documents:
            metadata = dict(doc.metadata or {})
            if doc.text is not None:
                metadata.setdefault("text", doc.text)
            vectors.append((doc.id, doc.vector, metadata))

        try:
            for i in range(0, len(vectors), _UPSERT_BATCH_SIZE):
                batch = vectors[i : i + _UPSERT_BATCH_SIZE]
                await asyncio.to_thread(
                    self._index.upsert,
                    vectors=batch,
                    namespace=self._config.namespace,
                )

            ids = [doc.id for doc in documents]
            logger.info(
                "pinecone_upserted",
                count=len(documents),
                namespace=self._config.namespace,
            )
            return ids  # type: ignore[return-value]
        except Exception as exc:
            raise VectorStoreError(f"Upsert failed: {exc}") from exc

    async def query(
        self,
        text: str,
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[QueryResult]:
        """Query Pinecone for similar documents.

        Args:
            text: Query text (will be embedded automatically).
            top_k: Number of results to return.
            filters: Optional metadata filters.

        Returns:
            Ranked list of query results.
        """
        embeddings = await self._embedding_provider.embed([text])
        query_vector = embeddings[0]

        try:
            response = await asyncio.to_thread(
                self._index.query,
                vector=query_vector,
                top_k=top_k,
                include_metadata=True,
                filter=filters,
                namespace=self._config.namespace,
            )

            results = [
                QueryResult(
                    id=match.id,
                    score=match.score,
                    text=match.metadata.get("text") if match.metadata else None,
                    metadata=match.metadata or {},
                )
                for match in response.matches
            ]

            logger.info(
                "pinecone_queried",
                top_k=top_k,
                results=len(results),
                namespace=self._config.namespace,
            )
            return results
        except Exception as exc:
            raise VectorStoreError(f"Query failed: {exc}") from exc

    async def delete(self, ids: list[str]) -> None:
        """Delete vectors by ID.

        Args:
            ids: Vector IDs to delete.
        """
        if not ids:
            return

        try:
            await asyncio.to_thread(
                self._index.delete,
                ids=ids,
                namespace=self._config.namespace,
            )
            logger.info(
                "pinecone_deleted",
                count=len(ids),
                namespace=self._config.namespace,
            )
        except Exception as exc:
            raise VectorStoreError(f"Delete failed: {exc}") from exc
