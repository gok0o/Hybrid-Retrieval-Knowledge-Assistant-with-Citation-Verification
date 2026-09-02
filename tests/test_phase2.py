from pathlib import Path

from src.ingestion.loaders.markdown_loader import MarkdownLoader
from src.chunking.heading_chunker import HeadingRecursiveChunker
from src.chunking.fixed_chunker import FixedSizeChunker
from src.ingestion.models import Document


def test_markdown_loader():
    path = Path("docs/api/rate-limits.md")
    if not path.exists():
        return
    doc = MarkdownLoader().load(path)
    assert doc.document_id == "API-006"
    assert doc.metadata["document_type"] == "api"
    assert "HTTP 429" in doc.text


def test_heading_chunker_keeps_parent_heading_with_content():
    doc = Document(
        document_id="TEST-001",
        text="# API\n\n## Auth\n\nUse a Bearer token.\n\n## Errors\n\n401 means authentication failed.",
        metadata={"document_type": "api"},
    )
    chunks = HeadingRecursiveChunker(max_chars=1000).chunk(doc)

    assert len(chunks) == 2
    assert chunks[0].metadata["section_heading"] == "Auth"
    assert chunks[1].metadata["section_heading"] == "Errors"
    assert "# API" in chunks[0].text
    assert "## Auth" in chunks[0].text
    assert "Use a Bearer token." in chunks[0].text
    assert all(c.metadata["chunking_strategy"] == "heading_recursive" for c in chunks)


def test_fixed_chunker():
    doc = Document(
        document_id="TEST-002",
        text="A" * 250,
        metadata={"document_type": "api"},
    )
    chunks = FixedSizeChunker(chunk_size=100, overlap=20).chunk(doc)
    assert len(chunks) == 3
    assert chunks[0].metadata["chunking_strategy"] == "fixed_overlap"
    assert chunks[1].metadata["chunk_start_char"] == 80
