import pickle
import re
from pathlib import Path
from typing import Any

from rank_bm25 import BM25Okapi


TOKEN_RE = re.compile(
    r"[A-Za-z0-9_./:-]+"
)


def tokenize(text: str) -> list[str]:
    """
    Tokenize text while preserving useful identifiers
    such as HTTP-429 and API names.
    """

    return TOKEN_RE.findall(
        text.lower()
    )


class BM25Store:
    """Build and persist a BM25 index."""

    def __init__(self):

        self.chunk_ids: list[str] = []
        self.chunks: list[dict[str, Any]] = []
        self.bm25 = None

    def build(
        self,
        chunks: list[dict[str, Any]]
    ) -> None:

        self.chunks = chunks

        self.chunk_ids = [
            chunk["chunk_id"]
            for chunk in chunks
        ]

        tokenized_documents = [
            tokenize(chunk["text"])
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(
            tokenized_documents
        )

    def save(
        self,
        path: str | Path
    ) -> None:

        if self.bm25 is None:
            raise RuntimeError(
                "Build the BM25 index before saving."
            )

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with path.open(
            "wb"
        ) as file:

            pickle.dump(
                {
                    "chunk_ids": self.chunk_ids,
                    "chunks": self.chunks,
                    "bm25": self.bm25,
                },
                file,
            )

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[dict[str, Any]]:

        if self.bm25 is None:
            raise RuntimeError(
                "BM25 index has not been built."
            )

        scores = self.bm25.get_scores(
            tokenize(query)
        )

        ranked = sorted(
            enumerate(scores),
            key=lambda item: item[1],
            reverse=True,
        )[:top_k]

        results = []

        for index, score in ranked:

            result = dict(
                self.chunks[index]
            )

            result["score"] = float(
                score
            )

            results.append(result)

        return results