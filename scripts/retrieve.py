import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.generation import confidence
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.dense_retriever import DenseRetriever
from src.retrieval.rrf import RRFFuser
from src.retrieval.reranker import Reranker
from src.generation.generator import AnswerGenerator
from src.generation.citation_verifier import CitationVerifier
from src.generation.confidence import ConfidenceScorer

def print_results(
    title: str,
    results: list[dict],
):
    print(f"\n{title}")
    print("=" * 60)

    for result in results:
        print(f"\nRank: {result['rank']}")
        print(f"Score: {result['score']:.4f}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Document ID: {result['document_id']}")
        print(
            f"Section: "
            f"{result['metadata'].get('section_heading')}"
        )
        print(f"Text:\n{result['text']}")

def print_rrf_results(results):

    print("\nRRF HYBRID RETRIEVAL")
    print("=" * 60)

    for result in results:

        print(f"\nRank: {result['rank']}")
        print(f"RRF Score: {result['rrf_score']:.6f}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Document ID: {result['document_id']}")

        print(
            f"Dense Rank: {result['dense_rank']}"
        )

        print(
            f"BM25 Rank: {result['bm25_rank']}"
        )

        print(
            f"Dense Score: {result['dense_score']}"
        )

        print(
            f"BM25 Score: {result['bm25_score']}"
        )

        print(
            f"Section: "
            f"{result['metadata'].get('section_heading')}"
        )

        print(f"Text:\n{result['text']}")

def print_reranked_results(results):

    print("\nRERANKED RESULTS")
    print("=" * 60)

    for result in results:

        print(f"\nRank: {result['reranker_rank']}")
        print(
            f"Reranker Score: "
            f"{result['reranker_score']:.4f}"
        )

        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Document ID: {result['document_id']}")

        print(
            f"Previous RRF Rank: "
            f"{result['rank']}"
        )

        print(
            f"Section: "
            f"{result['metadata'].get('section_heading')}"
        )

        print(f"Text:\n{result['text']}")


def main():

    query = input("Enter your question: ")

    dense_retriever = DenseRetriever()
    bm25_retriever = BM25Retriever()

    dense_results = dense_retriever.search(
        query=query,
        top_k=5,
    )

    bm25_results = bm25_retriever.search(
        query=query,
        top_k=5,
    )
    rrf = RRFFuser(
    k=60,
    dense_weight=1.0,
    bm25_weight=1.0,
)

    fused_results = rrf.fuse(
        dense_results=dense_results,
        bm25_results=bm25_results,
        top_k=20,
    ) 
    reranker = Reranker()

    reranked_results = reranker.rerank(
        query=query,
        results=fused_results,
        top_k=5,
    )
    
    generator = AnswerGenerator()

    answer = generator.generate(
        question=query,
        chunks=reranked_results,
    )

    verifier = CitationVerifier()

    citation_result = verifier.verify(
        answer=answer,
        chunks=reranked_results,
    )

    confidence_scorer = ConfidenceScorer()

    confidence = confidence_scorer.calculate(
        reranked_results=reranked_results,
        citation_support_rate= citation_result["citation_support_rate"],
        answer=answer,
    )
    
    print("\nCONFIDENCE SCORES")
    print("=" * 60)

    for key, value in confidence.items():
        if isinstance(value, float):
            print(f"{key.capitalize()}: {value:.2%}")
        else:
            print(f"{key.capitalize()}: {value}")

    print_results(
        "DENSE RETRIEVAL",
        dense_results,
    )

    print_results(
        "BM25 RETRIEVAL",
        bm25_results,
    )

    print_rrf_results(fused_results)

    print_reranked_results(reranked_results)

 

    print("\nGROUNDED ANSWER")
    print("=" * 60)
    print(answer)

    print("\nCITATION VERIFICATION")
    print("=" * 60)

    print(
        f"Total citations: "
        f"{citation_result['total_citations']}"
    )

    print(
        f"Supported citations: "
        f"{citation_result['supported_citations']}"
    )

    print(
        f"Citation support rate: "
        f"{citation_result['citation_support_rate']:.2%}"
    )

    for result in citation_result["citations"]:

        status = "SUPPORTED" if result["supported"] else "NOT SUPPORTED"

        print(
            f"\n{result['chunk_id']}: {status}"
        )

        print(
            f"Reason: {result['reason']}"
        )
    
    print("\nCONFIDENCE SCORE")
    print("=" * 60)

    print(f"Overall confidence: {confidence['overall']:.2f}")
    print(
        f"Retrieval score: "
        f"{confidence['retrieval_score']:.2f}"
    )
    print(
        f"Citation support: "
        f"{confidence['citation_support_rate']:.2f}"
    )
    print(
        f"Answer completeness: "
        f"{confidence['answer_completeness']:.2f}"
    )
    print(
        f"No-answer detected: "
        f"{confidence['no_answer']}"
    )
    
    threshold = 0.5

    if confidence["overall"] < threshold:
        print("\n⚠️  LOW CONFIDENCE DETECTED - consider human review")

if __name__ == "__main__":
    main()