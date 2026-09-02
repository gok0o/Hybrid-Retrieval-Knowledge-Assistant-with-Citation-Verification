# Phase 2 — Ingestion and Chunking

This phase currently targets the Markdown corpus created in Phase 1.

## What is implemented

1. Markdown loader with YAML frontmatter parsing
2. Text normalization
3. Common `Document` and `Chunk` models
4. Heading-aware recursive chunking
5. Fixed-size chunking with overlap
6. Metadata propagation to chunks
7. SHA-256 text hashes for debugging/deduplication
8. CLI ingestion command
9. JSONL processed chunk output

## Install

```bash
pip install -r requirements-phase2.txt
```

## Run heading-aware chunking

```bash
python ingest.py --source docs --strategy heading --rebuild
```

Output:

```text
data/processed/chunks_heading.jsonl
```

## Run fixed-size chunking

```bash
python ingest.py --source docs --strategy fixed --rebuild
```

Output:

```text
data/processed/chunks_fixed.jsonl
```

## Important

We are intentionally starting with Markdown only because the current corpus
contains Markdown files. PDF/HTML/TXT loaders can be added later without
changing the downstream chunk/retrieval interfaces.

Embeddings, Qdrant, and BM25 are the next indexing step; they are not hidden
inside this first ingestion implementation.
