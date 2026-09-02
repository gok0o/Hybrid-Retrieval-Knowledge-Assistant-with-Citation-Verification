from typing import Any

from sentence_transformers import CrossEncoder


class Reranker:
    """Rerank retrieved chunks using a cross-encoder."""

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        print("Loading reranker model...")

        self.model = CrossEncoder(model_name)

        print(f"Reranker model: {model_name}")

    def rerank(
        self,
        query: str,
        results: list[dict[str, Any]],
        top_k: int = 5,
    ) -> list[dict[str, Any]]:

        if not results:
            return []

        # Create (query, document) pairs
        pairs = [
            (query, result["text"])
            for result in results
        ]

        # Score each query-document pair
        scores = self.model.predict(pairs)

        reranked = []

        for result, score in zip(results, scores):

            item = result.copy()

            item["reranker_score"] = float(score)

            reranked.append(item)

        # Sort by reranker score
        reranked.sort(
            key=lambda item: item["reranker_score"],
            reverse=True,
        )

        # Keep only the best chunks
        reranked = reranked[:top_k]

        # Assign final reranker rank
        for rank, result in enumerate(
            reranked,
            start=1,
        ):
            result["reranker_rank"] = rank

        return reranked