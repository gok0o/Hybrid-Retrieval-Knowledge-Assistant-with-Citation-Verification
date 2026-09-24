from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any

from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.dense_retriever import DenseRetriever
from src.retrieval.rrf import RRFFuser
from src.retrieval.reranker import Reranker
from src.generation.generator import AnswerGenerator
from src.generation.citation_verifier import CitationVerifier
from src.generation.confidence import ConfidenceScorer

# Global model references
dense_retriever = None
bm25_retriever = None
rrf = None
reranker = None
generator = None
verifier = None
scorer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global dense_retriever, bm25_retriever, rrf, reranker, generator, verifier, scorer
    print("Loading RAG models and components...")
    dense_retriever = DenseRetriever()
    bm25_retriever = BM25Retriever()
    rrf = RRFFuser(k=60, dense_weight=1.0, bm25_weight=1.0)
    reranker = Reranker()
    generator = AnswerGenerator()
    verifier = CitationVerifier()
    scorer = ConfidenceScorer()
    print("RAG components loaded successfully.")
    yield
    print("Shutting down...")

app = FastAPI(
    title="Production RAG API",
    description="API layer for the RAG pipeline",
    version="1.0.0",
    lifespan=lifespan
)

class AskRequest(BaseModel):
    question: str

class CitationModel(BaseModel):
    chunk_id: str
    supported: bool
    reason: str

class AskResponse(BaseModel):
    answer: str
    citations: List[CitationModel]
    confidence: dict
    retrieved_chunk_ids: Optional[List[str]] = None

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/ask", response_model=AskResponse)
def ask_question(req: AskRequest):
    try:
        # 1. Retrieve chunks using dense and bm25
        d_res = dense_retriever.search(query=req.question, top_k=20)
        b_res = bm25_retriever.search(query=req.question, top_k=20)
        
        # 2. Fuse and Rerank
        fused = rrf.fuse(dense_results=d_res, bm25_results=b_res, top_k=20)
        retrieved_results = reranker.rerank(query=req.question, results=fused, top_k=10)
        
        # 3. Generate Answer
        answer = generator.generate(question=req.question, chunks=retrieved_results)
        
        # 4. Verify Citations
        try:
            citation_result = verifier.verify(answer=answer, chunks=retrieved_results)
            citation_support_rate = citation_result.get('citation_support_rate', 0.0)
            citations_list = citation_result.get('citations', [])
        except Exception as e:
            print(f"Citation verification failed: {e}")
            citation_support_rate = 0.0
            citations_list = []
            
        # 5. Calculate Confidence Score
        confidence_metrics = scorer.calculate(
            reranked_results=retrieved_results,
            citation_support_rate=citation_support_rate,
            answer=answer
        )
        
        # Extract chunk IDs for the response
        chunk_ids = [r['chunk_id'] for r in retrieved_results]
        
        return AskResponse(
            answer=answer,
            citations=citations_list,
            confidence=confidence_metrics,
            retrieved_chunk_ids=chunk_ids
        )
    except Exception as e:
        print(f"Error during RAG pipeline execution: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during processing")
