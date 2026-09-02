from typing import Any

from src.embeddings.embedder import LocalEmbedder
from src.indexing.qdrant_store import QdrantStore


class DenseRetriever:
    """Retrieve semantically similar chunks from Qdrant."""

    def __init__(
        self,
        collection_name: str = "support_chunks_heading",
        host: str = "localhost",
        port: int = 6333,
    ):
        self.embedder = LocalEmbedder()

        self.qdrant = QdrantStore(
            collection_name=collection_name,
            host=host,
            port=port,
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:

        # Convert the user question into an embedding
        query_vector = self.embedder.embed_query(query)

        # Search Qdrant using cosine similarity
        results = self.qdrant.client.query_points(
            collection_name=self.qdrant.collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,
        ).points

        retrieved_chunks = []

        for rank, result in enumerate(results, start=1):

            payload = result.payload

            retrieved_chunks.append(
                {
                    "rank": rank,
                    "chunk_id": payload["chunk_id"],
                    "document_id": payload["document_id"],
                    "text": payload["text"],
                    "metadata": payload["metadata"],
                    "score": float(result.score),
                }
            )

        return retrieved_chunks