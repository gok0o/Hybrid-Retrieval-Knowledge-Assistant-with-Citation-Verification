import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
import json
from pathlib import Path

from src.embeddings.embedder import LocalEmbedder
from src.indexing.bm25_store import BM25Store
from src.indexing.qdrant_store import QdrantStore


def load_chunks(path: Path) -> list[dict]:
    """Load processed chunks from JSONL."""
    if not path.exists():
        raise FileNotFoundError(f"Chunk file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return [
            json.loads(line)
            for line in file
            if line.strip()
        ]


def main():
    parser = argparse.ArgumentParser(
        description="Build dense and sparse indexes for the Support Knowledge Copilot."
    )

    parser.add_argument(
        "--strategy",
        choices=["heading", "fixed"],
        default="heading",
        help="Which chunking strategy to index.",
    )

    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Recreate the selected Qdrant collection.",
    )

    parser.add_argument(
        "--qdrant-local",
        default="data/indexes/qdrant",
        help="Local directory used by Qdrant.",
    )

    parser.add_argument(
        "--bm25-output",
        default="data/indexes/bm25",
        help="Directory where the BM25 index is saved.",
    )

    args = parser.parse_args()

    # ---------------------------------------------------------
    # 1. Load chunks
    # ---------------------------------------------------------

    chunk_file = (
        Path("data/processed")
        / f"chunks_{args.strategy}.jsonl"
    )

    chunks = load_chunks(chunk_file)

    if not chunks:
        raise RuntimeError("No chunks found.")

    print(f"Loaded {len(chunks)} chunks.")

    # ---------------------------------------------------------
    # 2. Generate embeddings
    # ---------------------------------------------------------

    print("Loading embedding model...")

    embedder = LocalEmbedder()

    print(
        f"Embedding model: {embedder.model_name}"
    )

    print(
        f"Embedding dimension: {embedder.dimension}"
    )

    print("Generating embeddings...")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    vectors = embedder.embed_documents(texts)

    print(
        f"Generated {len(vectors)} embeddings."
    )

    # ---------------------------------------------------------
    # 3. Store embeddings in Qdrant
    # ---------------------------------------------------------

    collection_name = (
        f"support_chunks_{args.strategy}"
    )

    qdrant = QdrantStore(
        collection_name=collection_name,
        host="localhost",
        port=6333,
    )

    if args.rebuild:
        print(
            f"Recreating Qdrant collection: {collection_name}"
        )

        qdrant.recreate_collection(
            embedder.dimension
        )

    print("Storing embeddings in Qdrant...")

    qdrant.upsert(
        chunks,
        vectors,
    )

    print(
        f"Qdrant points: {qdrant.count()}"
    )

    # ---------------------------------------------------------
    # 4. Build BM25 index
    # ---------------------------------------------------------

    print("Building BM25 index...")

    bm25 = BM25Store()

    bm25.build(chunks)

    bm25_path = (
        Path(args.bm25_output)
        / f"bm25_{args.strategy}.pkl"
    )

    bm25.save(bm25_path)

    print(
        f"BM25 index saved to: {bm25_path}"
    )

    # ---------------------------------------------------------
    # 5. Done
    # ---------------------------------------------------------

    print("\nIndexing complete.")
    print(f"Strategy: {args.strategy}")
    print(f"Chunks indexed: {len(chunks)}")
    print(f"Qdrant collection: {collection_name}")
    print(f"BM25 index: {bm25_path}")


if __name__ == "__main__":
    main()