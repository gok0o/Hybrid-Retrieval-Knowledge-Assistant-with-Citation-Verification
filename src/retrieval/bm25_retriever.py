import pickle
from pathlib import Path
from typing import Any

from src.indexing.bm25_store import tokenize


class BM25Retriever:
    """Retrieve keyword-relevant chunks using BM25."""

    def __init__(
        self,
        index_path: str = "data/indexes/bm25/bm25_heading.pkl",
    ):
        self.index_path = Path(index_path)

        if not self.index_path.exists():
            raise FileNotFoundError(
                f"BM25 index not found: {self.index_path}"
            )

        with self.index_path.open("rb") as file:
            data = pickle.load(file)

        self.chunk_ids = data["chunk_ids"]
        self.chunks = data["chunks"]
        self.bm25 = data["bm25"]

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:

        scores = self.bm25.get_scores(
            tokenize(query)
        )

        ranked = sorted(
            enumerate(scores),
            key=lambda item: item[1],
            reverse=True,
        )[:top_k]

        results = []

        for rank, (index, score) in enumerate(
            ranked,
            start=1,
        ):
            chunk = self.chunks[index]

            results.append(
                {
                    "rank": rank,
                    "chunk_id": chunk["chunk_id"],
                    "document_id": chunk["document_id"],
                    "text": chunk["text"],
                    "metadata": chunk["metadata"],
                    "score": float(score),
                }
            )

        return results