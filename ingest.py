import argparse

from src.ingestion.pipeline import ingest_markdown


def main():
    parser = argparse.ArgumentParser(
        description="Ingest and chunk the Support Knowledge Copilot corpus."
    )

    parser.add_argument(
        "--source",
        default="docs",
        help="Directory containing Markdown documents.",
    )
    parser.add_argument(
        "--output",
        default="data/processed",
        help="Directory for processed chunk files.",
    )
    parser.add_argument(
        "--strategy",
        choices=["heading", "fixed"],
        default="heading",
        help="Chunking strategy.",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Remove previous processed files before ingestion.",
    )

    args = parser.parse_args()

    chunks = ingest_markdown(
        source=args.source,
        output=args.output,
        strategy=args.strategy,
        rebuild=args.rebuild,
    )

    print("Ingestion complete.")
    print(f"Source: {args.source}")
    print(f"Strategy: {args.strategy}")
    print(f"Chunks created: {len(chunks)}")


if __name__ == "__main__":
    main()
