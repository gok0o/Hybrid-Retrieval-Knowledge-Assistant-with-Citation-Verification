from pathlib import Path
import hashlib
import json

from src.ingestion.loaders.markdown_loader import MarkdownLoader
from src.chunking.heading_chunker import HeadingRecursiveChunker
from src.chunking.fixed_chunker import FixedSizeChunker


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def discover_markdown(source: Path) -> list[Path]:
    return sorted(source.rglob("*.md"))


def ingest_markdown(
    source: str | Path,
    output: str | Path,
    strategy: str = "heading",
    rebuild: bool = False,
) -> list:
    source = Path(source)
    output = Path(output)

    if not source.exists():
        raise FileNotFoundError(f"Source directory not found: {source}")

    output.mkdir(parents=True, exist_ok=True)
    
    output_file = output / f"chunks_{strategy}.jsonl"

    if rebuild and output_file.exists():
        output_file.unlink()

    loader = MarkdownLoader()

    if strategy == "heading":
        chunker = HeadingRecursiveChunker(max_chars=1400)
    elif strategy == "fixed":
        chunker = FixedSizeChunker(chunk_size=1200, overlap=200)
    else:
        raise ValueError("strategy must be 'heading' or 'fixed'")

    all_chunks = []

    for path in discover_markdown(source):
        document = loader.load(path)

        for chunk in chunker.chunk(document):
            chunk.metadata["text_hash"] = text_hash(chunk.text)
            all_chunks.append(chunk)

    output_file = output / f"chunks_{strategy}.jsonl"

    with output_file.open("w", encoding="utf-8") as f:
        for chunk in all_chunks:
            record = {
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "text": chunk.text,
                "metadata": chunk.metadata,
            }
            f.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

    return all_chunks
