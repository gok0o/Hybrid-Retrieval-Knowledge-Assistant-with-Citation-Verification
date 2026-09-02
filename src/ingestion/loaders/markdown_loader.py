from pathlib import Path
from typing import Any

import yaml

from src.ingestion.models import Document


class MarkdownLoader:
    """Load Markdown files that use YAML frontmatter."""

    def load(self, path: str | Path) -> Document:
        path = Path(path)
        raw = path.read_text(encoding="utf-8")

        metadata, body = self._parse_frontmatter(raw)

        document_id = metadata.get("document_id")
        if not document_id:
            raise ValueError(f"Missing document_id: {path}")

        metadata = dict(metadata)
        metadata["source_path"] = str(path)
        metadata["file_name"] = path.name

        return Document(
            document_id=str(document_id),
            text=self._normalize(body),
            metadata=metadata,
        )

    @staticmethod
    def _parse_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
        if not raw.startswith("---"):
            raise ValueError("Markdown document must start with YAML frontmatter.")

        parts = raw.split("---", 2)
        if len(parts) != 3:
            raise ValueError("Invalid YAML frontmatter.")

        metadata = yaml.safe_load(parts[1]) or {}
        body = parts[2].lstrip()

        if not isinstance(metadata, dict):
            raise ValueError("Frontmatter must be a YAML mapping.")

        return metadata, body

    @staticmethod
    def _normalize(text: str) -> str:
        # Keep headings and paragraph boundaries, while removing
        # trailing whitespace and repeated blank lines.
        lines = [line.rstrip() for line in text.splitlines()]
        cleaned = []
        previous_blank = False

        for line in lines:
            if not line.strip():
                if not previous_blank:
                    cleaned.append("")
                previous_blank = True
            else:
                cleaned.append(line.strip())
                previous_blank = False

        return "\n".join(cleaned).strip()
