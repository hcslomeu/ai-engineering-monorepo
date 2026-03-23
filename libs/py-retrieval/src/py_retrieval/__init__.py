"""Provider-agnostic vector store abstraction with Pinecone implementation."""

from py_retrieval.embeddings import OpenAIEmbeddingProvider
from py_retrieval.exceptions import EmbeddingError, VectorStoreConnectionError, VectorStoreError
from py_retrieval.factory import create_vector_store
from py_retrieval.models import Document, QueryResult, VectorStoreConfig
from py_retrieval.pinecone_store import PineconeVectorStore
from py_retrieval.protocols import EmbeddingProvider, VectorStore

__all__ = [
    "Document",
    "EmbeddingError",
    "EmbeddingProvider",
    "OpenAIEmbeddingProvider",
    "PineconeVectorStore",
    "QueryResult",
    "VectorStore",
    "VectorStoreConfig",
    "VectorStoreConnectionError",
    "VectorStoreError",
    "create_vector_store",
]
