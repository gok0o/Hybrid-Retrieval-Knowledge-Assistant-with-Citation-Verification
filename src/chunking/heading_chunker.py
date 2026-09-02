import re

from src.ingestion.models import Chunk, Document


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


class HeadingRecursiveChunker:
    """Heading-aware chunker that keeps headings with useful content."""

    def __init__(self, max_chars: int = 1400):
        if max_chars <= 0:
            raise ValueError("max_chars must be positive.")
        self.max_chars = max_chars

    def chunk(self, document: Document) -> list[Chunk]:
        sections = self._build_sections(document.text.splitlines())
        chunks: list[Chunk] = []

        for section in sections:
            for text, heading_path in self._split_section(
                section["text"], section["heading_path"]
            ):
                if not text.strip():
                    continue

                index = len(chunks)
                metadata = dict(document.metadata)
                metadata.update({
                    "section_heading": (
                        heading_path[-1]
                        if heading_path
                        else metadata.get("section_heading")
                    ),
                    "heading_path": heading_path,
                    "chunk_index": index,
                    "chunking_strategy": "heading_recursive",
                })

                chunks.append(Chunk(
                    chunk_id=f"{document.document_id}-chunk-{index:03d}",
                    document_id=document.document_id,
                    text=text.strip(),
                    metadata=metadata,
                ))

        return chunks

    def _build_sections(self, lines: list[str]) -> list[dict]:
        """Group each heading with the content belonging to it.

        A parent heading immediately followed by a subsection heading is
        retained as context instead of becoming a heading-only chunk.
        """
        sections: list[dict] = []
        current_lines: list[str] = []
        heading_path: list[str] = []

        for line in lines:
            match = HEADING_RE.match(line)

            if match:
                # Do not close on a heading if the current section has no
                # real prose yet. This prevents '# API' from becoming a
                # standalone chunk before '## Authentication'.
                if current_lines and self._has_non_heading_content(current_lines):
                    sections.append({
                        "text": "\n".join(current_lines).strip(),
                        "heading_path": heading_path.copy(),
                    })
                    current_lines = []

                level = len(match.group(1))
                title = match.group(2).strip()
                heading_path = heading_path[: level - 1]
                heading_path.append(title)
                current_lines.append(line)
            else:
                current_lines.append(line)

        if current_lines and self._has_non_heading_content(current_lines):
            sections.append({
                "text": "\n".join(current_lines).strip(),
                "heading_path": heading_path.copy(),
            })

        return sections

    @staticmethod
    def _has_non_heading_content(lines: list[str]) -> bool:
        return any(
            line.strip() and not HEADING_RE.match(line.strip())
            for line in lines
        )

    def _split_section(
        self, text: str, heading_path: list[str]
    ) -> list[tuple[str, list[str]]]:
        if not text:
            return []

        if len(text) <= self.max_chars:
            return [(text, heading_path)]

        paragraphs = re.split(r"\n\s*\n", text)
        pieces: list[tuple[str, list[str]]] = []
        current = ""

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            candidate = (
                f"{current}\n\n{paragraph}" if current else paragraph
            ).strip()

            if len(candidate) <= self.max_chars:
                current = candidate
            else:
                if current:
                    pieces.append((current, heading_path))
                current = paragraph

        if current:
            pieces.append((current, heading_path))

        final: list[tuple[str, list[str]]] = []
        for piece, path in pieces:
            if len(piece) <= self.max_chars:
                final.append((piece, path))
            else:
                for start in range(0, len(piece), self.max_chars):
                    final.append((piece[start:start + self.max_chars], path))

        return final
