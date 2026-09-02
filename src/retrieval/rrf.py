from typing import Any


class RRFFuser:
    """Fuse dense and BM25 rankings using Reciprocal Rank Fusion."""

    def __init__(
        self,
        k: int = 60,
        dense_weight: float = 1.0,
        bm25_weight: float = 1.0,
    ):
        self.k = k
        self.dense_weight = dense_weight
        self.bm25_weight = bm25_weight

    def fuse(
        self,
        dense_results: list[dict[str, Any]],
        bm25_results: list[dict[str, Any]],
        top_k: int = 10,
    ) -> list[dict[str, Any]]:

        fused = {}

        # Add dense retrieval contribution
        for result in dense_results:
            chunk_id = result["chunk_id"]

            if chunk_id not in fused:
                fused[chunk_id] = {
                    "chunk_id": chunk_id,
                    "document_id": result["document_id"],
                    "text": result["text"],
                    "metadata": result["metadata"],
                    "dense_rank": None,
                    "bm25_rank": None,
                    "dense_score": None,
                    "bm25_score": None,
                    "rrf_score": 0.0,
                }

            fused[chunk_id]["dense_rank"] = result["rank"]
            fused[chunk_id]["dense_score"] = result["score"]

            fused[chunk_id]["rrf_score"] += (
                self.dense_weight
                / (self.k + result["rank"])
            )

        # Add BM25 retrieval contribution
        for result in bm25_results:
            chunk_id = result["chunk_id"]

            if chunk_id not in fused:
                fused[chunk_id] = {
                    "chunk_id": chunk_id,
                    "document_id": result["document_id"],
                    "text": result["text"],
                    "metadata": result["metadata"],
                    "dense_rank": None,
                    "bm25_rank": None,
                    "dense_score": None,
                    "bm25_score": None,
                    "rrf_score": 0.0,
                }

            fused[chunk_id]["bm25_rank"] = result["rank"]
            fused[chunk_id]["bm25_score"] = result["score"]

            fused[chunk_id]["rrf_score"] += (
                self.bm25_weight
                / (self.k + result["rank"])
            )

        # Sort by combined RRF score
        results = sorted(
            fused.values(),
            key=lambda item: item["rrf_score"],
            reverse=True,
        )

        # Add final rank
        for rank, result in enumerate(
            results[:top_k],
            start=1,
        ):
            result["rank"] = rank

        return results[:top_k]