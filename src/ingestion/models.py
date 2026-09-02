from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    """Normalized document before chunking."""
    document_id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Chunk:
    """Retrievable unit produced from a document."""
    chunk_id: str
    document_id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
