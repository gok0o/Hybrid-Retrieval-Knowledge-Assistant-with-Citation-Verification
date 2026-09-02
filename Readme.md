# Hybrid Retrieval Knowledge Assistant with Citation Verification

A production-oriented **Retrieval-Augmented Generation (RAG)** system for answering support and knowledge-base questions using **hybrid retrieval, cross-encoder reranking, grounded generation, citation verification, and confidence scoring**.

The system is designed to reduce hallucinations by forcing the language model to answer only from retrieved documentation and by verifying whether generated citations are actually supported by the retrieved knowledge.

---

## Overview

Traditional RAG systems often rely only on vector similarity search. This can fail when a query contains exact keywords, error codes, identifiers, or terminology that lexical search handles better.

This project combines:

* **Dense vector retrieval** for semantic similarity
* **BM25 retrieval** for keyword/exact-match search
* **Reciprocal Rank Fusion (RRF)** to combine both retrieval methods
* **Cross-encoder reranking** to improve relevance
* **Grounded LLM generation** using retrieved documentation
* **Citation verification** to validate generated claims
* **Confidence scoring** based on retrieval and answer quality
* **Missing-knowledge detection** to avoid unsupported answers

### Current Pipeline

```text
                    User Question
                          │
                          ▼
                ┌───────────────────┐
                │   Query Input     │
                └─────────┬─────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
      Dense Retrieval             BM25 Retrieval
      BGE Embeddings              Keyword Search
             │                         │
             └────────────┬────────────┘
                          ▼
                 RRF Score Fusion
                          │
                          ▼
                Top-20 Candidates
                          │
                          ▼
              Cross-Encoder Reranker
              ms-marco-MiniLM-L-6-v2
                          │
                          ▼
                    Top-5 Chunks
                          │
                          ▼
                Grounded LLM Prompt
                          │
                          ▼
                  Gemini Generation
                          │
                          ▼
                Citation Verification
                          │
                          ▼
                 Confidence Scoring
                          │
                          ▼
                     Final Answer
```

---

# Key Features

## 1. Heading-Aware Document Chunking

Markdown support documents are processed using heading-aware chunking.

The system preserves:

* Document metadata
* Section headings
* Heading hierarchy
* Heading paths
* Chunk IDs
* Chunking strategy

Example:

```text
# API Authentication
## Bearer Tokens

FlowDesk API requests require a Bearer token...
```

The resulting chunk retains its structural context:

```text
heading_path:
[
    "API Authentication",
    "Bearer Tokens"
]
```

This provides the retriever and LLM with additional document context.

---

## 2. Dense Retrieval

The project uses:

```text
BAAI/bge-small-en-v1.5
```

to generate 384-dimensional embeddings.

Dense retrieval is useful for semantic queries where the wording of the question differs from the wording used in the documentation.

Example:

```text
Question:
Why can't I authenticate with the API?

Documentation:
API requests require a valid Bearer token.
```

Even though the wording differs, semantic retrieval can identify the relevant chunk.

---

## 3. BM25 Retrieval

The system also maintains a BM25 sparse retrieval index.

BM25 is particularly useful for:

* Error codes
* API names
* Product names
* Exact terminology
* Identifiers
* Technical keywords

For example:

```text
HTTP 401
429
API-008
Bearer token
```

Lexical retrieval can often find these exact terms more reliably than dense retrieval alone.

---

## 4. Hybrid Retrieval with Reciprocal Rank Fusion

Dense and BM25 results are combined using **Reciprocal Rank Fusion (RRF)**.

Conceptually:

```text
Dense Results
      +
BM25 Results
      ↓
   RRF Fusion
      ↓
Combined Ranking
```

The current implementation uses configurable weights for dense and BM25 retrieval.

This allows the system to benefit from both:

> semantic understanding + exact keyword matching

---

## 5. Cross-Encoder Reranking

The fused results are passed to:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

The reranker evaluates the relevance of the **question and document chunk together**.

Current flow:

```text
Hybrid Retrieval
      ↓
Top 20 candidates
      ↓
Cross-Encoder
      ↓
Top 5 chunks
```

This provides a more precise final context for the language model.

---

## 6. Grounded Answer Generation

The language model is instructed to answer **only from the retrieved documentation**.

The prompt enforces several rules:

* Do not invent information
* Do not use external knowledge
* Cite factual claims
* Use the exact chunk IDs
* Explicitly identify missing information

Example:

```text
An HTTP 401 error indicates an authentication failure
[API-008-chunk-000].
```

If the retrieved documentation does not contain the required solution, the system is instructed to say so instead of guessing.

---

## 7. Citation Verification

Generated answers are passed through a citation verification stage.

The verifier checks:

```text
Generated Claim
      ↓
Referenced Chunk
      ↓
Does the chunk support the claim?
      ↓
SUPPORTED / UNSUPPORTED
```

The system calculates:

```text
Citation Support Rate =
Supported Citations / Total Citations
```

Example:

```text
Total citations: 2
Supported citations: 2

Citation support rate: 100%
```

This helps detect cases where an LLM generates a citation that does not actually support its claim.

---

## 8. Confidence Scoring

The system produces a confidence score using multiple signals rather than relying solely on the LLM.

The current confidence calculation considers factors such as:

* Retrieval quality
* Citation support
* Answer completeness
* No-answer detection

Example:

```text
CONFIDENCE SCORE
----------------
Overall confidence: 0.71
Retrieval score:    0.82
Citation support:   1.00
Answer completeness: 0.60
No-answer detected: True
```

An important property of this design is that **high citation support does not automatically mean high answer confidence**.

For example, the retrieved chunks may correctly support the statements that were made, while still not containing the actual solution to the user's problem.

---

# Example

### Question

```text
What should I do if the API returns a 401 error?
```

### Retrieved Knowledge

```text
API-008-chunk-000
HTTP 401 indicates an authentication failure.

TRB-001-chunk-000
API requests returning HTTP 401 are listed under the
symptoms of API authentication problems.
```

### Generated Answer

```text
An HTTP 401 error indicates an authentication failure
[API-008-chunk-000].

The documentation lists HTTP 401 under the symptoms for
API authentication problems [TRB-001-chunk-000], but it
does not specify the troubleshooting steps required to
resolve the issue.

WHAT I COULD NOT VERIFY:

- Specific troubleshooting steps for resolving the
  API 401 error.
```

This is intentional.

Instead of hallucinating a solution, the system identifies the limitation of the available knowledge.

---

# Technology Stack

| Component         | Technology                             |
| ----------------- | -------------------------------------- |
| Language          | Python                                 |
| Embeddings        | `BAAI/bge-small-en-v1.5`               |
| Sparse Retrieval  | BM25                                   |
| Vector Database   | Qdrant                                 |
| Vector DB Runtime | Docker                                 |
| Hybrid Fusion     | Reciprocal Rank Fusion                 |
| Reranker          | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| LLM               | Gemini                                 |
| Document Format   | Markdown                               |
| Testing           | Pytest                                 |

---

# Project Structure

```text
Hybrid-Retrieval-Knowledge-Assistant-with-Citation-Verification/
│
├── config/
│
├── data/
│   ├── documents/
│   ├── indexes/
│   └── ...
│
├── docs/
│
├── evaluation/
│
├── src/
│   ├── chunking/
│   ├── generation/
│   ├── ingestion/
│   ├── retrieval/
│   └── ...
│
├── tests/
│
├── docker-compose.yml
├── index.py
├── ingest.py
├── retrieve.py
│
├── requirements-indexing.txt
├── requirements-phase2.txt
│
├── .gitignore
└── README.md
```

---

# Running the Project

## 1. Clone the repository

```bash
git clone https://github.com/gok0o/Hybrid-Retrieval-Knowledge-Assistant-with-Citation-Verification.git

cd Hybrid-Retrieval-Knowledge-Assistant-with-Citation-Verification
```

## 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

---

## 3. Install dependencies

Install the project dependencies from the appropriate requirements files.

```bash
pip install -r requirements-phase2.txt
pip install -r requirements-indexing.txt
```

---

## 4. Start Qdrant

The project uses Qdrant locally through Docker.

```bash
docker compose up -d
```

Verify that the Qdrant container is running:

```bash
docker ps
```

---

## 5. Configure Gemini

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.6-flash
```

**Never commit your `.env` file or API keys to GitHub.**

---

# Indexing the Knowledge Base

The project currently supports heading-based indexing.

Run:

```bash
python index.py --strategy heading --rebuild
```

The indexing pipeline:

```text
Markdown Documents
       ↓
Metadata Extraction
       ↓
Text Normalization
       ↓
Heading-Aware Chunking
       ↓
Chunk IDs + Metadata
       ↓
Embeddings
       ↓
Qdrant
       +
BM25 Index
```

The current knowledge base produces approximately **71 heading-aware chunks**.

---

# Running Retrieval + Generation

Run:

```bash
python retrieve.py
```

Enter a question when prompted:

```text
Enter your question: What should I do if the API returns a 401 error?
```

The system displays:

1. Dense retrieval results
2. BM25 retrieval results
3. RRF fused results
4. Cross-encoder reranked results
5. Grounded answer
6. Citation verification
7. Confidence score

---

# Testing

Run:

```bash
pytest
```

The project includes tests for core ingestion and chunking functionality.

---

# Current Project Status

### Completed

* [x] Markdown document ingestion
* [x] Metadata extraction
* [x] Text normalization
* [x] Document model
* [x] Heading-aware chunking
* [x] Fixed-size chunking with overlap
* [x] Metadata propagation
* [x] Stable chunk IDs
* [x] Text hashing
* [x] Dense embeddings
* [x] Qdrant vector indexing
* [x] BM25 indexing
* [x] Dense retrieval
* [x] BM25 retrieval
* [x] Hybrid RRF fusion
* [x] Cross-encoder reranking
* [x] Grounded LLM generation
* [x] Citation generation
* [x] Citation verification
* [x] Confidence scoring
* [x] Missing-knowledge handling
* [x] Dockerized local Qdrant

### In Progress / Planned

* [ ] Golden Q&A evaluation dataset
* [ ] Retrieval evaluation metrics
* [ ] Answer quality evaluation
* [ ] Dense vs hybrid comparison
* [ ] Evaluation dashboard
* [ ] Automated Markdown/HTML evaluation reports
* [ ] Improved citation verification using a dedicated NLI/entailment model
* [ ] Additional retrieval and latency optimizations

---

# Future Improvements

Potential future improvements include:

### Evaluation Suite

Build a 50–75 question golden dataset containing:

* Simple lookup questions
* Multi-document questions
* Ambiguous questions
* Outdated-document traps
* Questions with no answer in the corpus

### Retrieval Evaluation

Measure:

* Recall@K
* MRR
* Hit Rate
* Dense vs Hybrid performance

### Answer Evaluation

Measure:

* Answer correctness
* Answer completeness
* Citation validity
* No-answer accuracy
* Hallucination rate

### Citation Verification Optimization

The current citation verification approach can be improved by using a dedicated **NLI/entailment model** instead of relying on an LLM-based verification approach.

The existing MS MARCO cross-encoder is intentionally used for **retrieval reranking**, since relevance ranking and factual entailment are different tasks.

### Dashboard

A future dashboard will allow comparison between:

```text
Dense Retrieval
       VS
Hybrid Retrieval
```

and expose:

* Retrieved chunks
* Generated answers
* Citation verdicts
* Confidence breakdown
* Evaluation metrics

---

# Design Principles

This project follows several principles important for production RAG systems.

### 1. Retrieval before generation

The LLM should not be treated as the source of truth.

```text
Knowledge Base
      ↓
Retrieval
      ↓
Evidence
      ↓
Generation
```

### 2. Grounding over guessing

If the documentation does not contain the answer:

```text
"I could not verify this from the available documentation."
```

is preferable to an unsupported answer.

### 3. Separate retrieval from generation

A poor answer may be caused by:

```text
Bad Retrieval
```

or:

```text
Good Retrieval + Bad Generation
```

The architecture therefore evaluates these stages separately.

### 4. Citations are evidence, not decoration

A citation is only useful if the referenced chunk actually supports the generated claim.

### 5. Confidence should reflect uncertainty

A system should be able to say:

> "The information I found is reliable, but it is insufficient to fully answer your question."

---

# Why Hybrid Retrieval?

Dense and sparse retrieval have different strengths.

```text
                  Query
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
       Dense                 BM25
     Semantic             Exact Terms
          │                   │
          └─────────┬─────────┘
                    ▼
                   RRF
                    │
                    ▼
             Better Candidates
```

Dense retrieval handles semantic similarity.

BM25 handles exact lexical matches.

Combining them provides a more robust retrieval layer for technical support documentation.

---

# Learning Goals

This project is being developed to explore practical AI/ML engineering concepts including:

* Retrieval-Augmented Generation
* Information retrieval
* Dense embeddings
* Sparse retrieval
* Vector databases
* Hybrid search
* Reciprocal Rank Fusion
* Cross-encoder reranking
* Prompt engineering
* Grounded generation
* Citation verification
* Confidence estimation
* Evaluation of RAG systems
* Production-oriented AI system design

---

# Author

**Gokul M**

GitHub: [gok0o](https://github.com/gok0o?utm_source=chatgpt.com)

---

## Project

[Hybrid Retrieval Knowledge Assistant with Citation Verification](https://github.com/gok0o/Hybrid-Retrieval-Knowledge-Assistant-with-Citation-Verification?utm_source=chatgpt.com)

---

> **Note:** This project is actively being developed. The evaluation suite and dashboard are planned as the next major phase.
