from typing import Any

from qdrant_client import QdrantClient, models


class QdrantStore:
    """Store dense vectors and chunk metadata in a Qdrant server."""

    def __init__(
        self,
        collection_name: str = "support_chunks",
        host: str = "localhost",
        port: int = 6333,
    ):
        self.collection_name = collection_name

        self.client = QdrantClient(
            host=host,
            port=port,
        )

    def recreate_collection(
        self,
        vector_size: int,
    ) -> None:

        if self.client.collection_exists(
            self.collection_name
        ):
            self.client.delete_collection(
                self.collection_name
            )

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    def upsert(
        self,
        chunks: list[dict[str, Any]],
        vectors: list[list[float]],
    ) -> None:

        points = []

        import uuid
        for chunk, vector in zip(
            chunks,
            vectors,
        ):
            payload = {
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "text": chunk["text"],
                "metadata": chunk["metadata"],
            }
            
            # Qdrant point IDs must be UUIDs or unsigned integers.
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk["chunk_id"]))

            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def count(self) -> int:

        result = self.client.count(
            collection_name=self.collection_name,
            exact=True,
        )

        return result.count