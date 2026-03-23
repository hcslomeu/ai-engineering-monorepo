# py-retrieval

Provider-agnostic vector store abstraction with Pinecone implementation.

## Usage

```python
import os

from pydantic import SecretStr

from py_retrieval import Document, VectorStoreConfig, create_vector_store

config = VectorStoreConfig(
    provider="pinecone",
    api_key=SecretStr(os.environ["PINECONE_API_KEY"]),
    index_name="my-index",
    embedding_model="text-embedding-3-small",
)

store = create_vector_store(config)

async with store:
    ids = await store.upsert([Document(text="Hello world")])
    results = await store.query("greeting", top_k=5)
```

## Architecture

- `VectorStore` Protocol — structural typing contract for any vector store
- `EmbeddingProvider` Protocol — pluggable embedding generation
- `PineconeVectorStore` — concrete Pinecone implementation
- `create_vector_store()` — factory for provider-agnostic instantiation
