import os
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

class Citation(BaseModel):
    chunk_id: str
    supported: bool
    reason: str

class CitationVerificationResult(BaseModel):
    total_citations: int
    supported_citations: int
    citation_support_rate: float
    citations: list[Citation]

class CitationVerifier:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=api_key)
        
    def verify(self, answer: str, chunks: list[dict]) -> dict:
        context_parts = []
        for chunk in chunks:
            context_parts.append(
                f"[CHUNK_ID: {chunk['chunk_id']}]\n{chunk['text']}"
            )
        context = "\n\n".join(context_parts)
        
        prompt = f"""
You are an expert citation verifier.
Given an answer containing citations in the format [chunk_id], and the original context chunks provided below, verify if each cited chunk actually supports the claims made in the answer preceding the citation.

Context chunks:
{context}

Answer to verify:
{answer}

Please analyze each citation in the answer and determine if the corresponding context chunk supports the claim. Return the results as a JSON object matching the requested schema. Calculate the total_citations, supported_citations, and citation_support_rate correctly based on your analysis.
"""
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": CitationVerificationResult,
            }
        )
        
        result_dict = json.loads(response.text)
        return result_dict
