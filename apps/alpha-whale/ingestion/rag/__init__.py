"""RAG pipeline for financial document retrieval (WP-121).

Bronze → Silver → Gold Medallion pipeline:
- Bronze: EDGAR 10-K/10-Q filings + Firecrawl news ingestion
- Silver: SentenceSplitter chunking with financial metadata
- Gold: OpenAI embeddings indexed in Pinecone
- Retrieval: BM25 + Vector hybrid search with Cohere reranking
"""

from ingestion.rag.chunking import chunk_articles, chunk_filings
from ingestion.rag.config import RAGSettings
from ingestion.rag.edgar import EdgarClient, EdgarFiling, EdgarSearchResult, FilingType
from ingestion.rag.firecrawl_source import FirecrawlNewsSource, NewsArticle, NewsArticleMetadata

__all__ = [
    "EdgarClient",
    "EdgarFiling",
    "EdgarSearchResult",
    "FilingType",
    "FirecrawlNewsSource",
    "NewsArticle",
    "NewsArticleMetadata",
    "RAGSettings",
    "chunk_articles",
    "chunk_filings",
]
