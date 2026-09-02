from src.ingestion.models import Chunk, Document


class FixedSizeChunker:
    """Character-based fixed-size chunker with overlap."""

    def __init__(self, chunk_size: int = 1200, overlap: int = 200):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive.")
        if overlap < 0 or overlap >= chunk_size:
            raise ValueError("overlap must be >= 0 and < chunk_size.")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, document: Document) -> list[Chunk]:
        text = document.text.strip()
        if not text:
            return []

        chunks = []
        step = self.chunk_size - self.overlap
        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                index = len(chunks)
                metadata = dict(document.metadata)
                metadata.update({
                    "chunk_index": index,
                    "chunking_strategy": "fixed_overlap",
                    "chunk_start_char": start,
                    "chunk_end_char": end,
                })

                chunks.append(
                    Chunk(
                        chunk_id=f"{document.document_id}-chunk-{index:03d}",
                        document_id=document.document_id,
                        text=chunk_text,
                        metadata=metadata,
                    )
                )

            if end >= len(text):
                break

            start += step

        return chunks
