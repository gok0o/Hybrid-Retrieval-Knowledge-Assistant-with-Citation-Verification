import os
import json
from dotenv import load_dotenv
from openai import OpenAI
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
        api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is not set.")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
    def verify(self, answer: str, chunks: list[dict]) -> dict:
        context_parts = []
        for chunk in chunks:
            context_parts.append(
                f"[CHUNK_ID: {chunk['chunk_id']}]\n{chunk['text']}"
            )
        context = "\n\n".join(context_parts)
        
        prompt = f"""
You are an expert citation verifier.
Given an answer containing citations in the format [chunk_id], and the original context chunks provided below, verify if each cited chunk actually supports the claims made in the answer.

Context chunks:
{context}

Answer to verify:
{answer}

Instructions:
1. Identify all citations in the answer. They are formatted as [chunk_id].
2. For each citation, find the corresponding chunk in the Context chunks.
3. Determine if the information in the chunk supports the claim(s) made in the sentence containing the citation.
4. If a citation's chunk_id is not found in the Context chunks, it is NOT supported.

Return the results as a JSON object matching this structure:
{{
  "total_citations": 0,
  "supported_citations": 0,
  "citation_support_rate": 0.0,
  "citations": [
    {{
      "chunk_id": "string",
      "supported": true,
      "reason": "string"
    }}
  ]
}}
Calculate the total_citations, supported_citations, and citation_support_rate accurately based on your analysis.
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={
                "type": "json_object"
            }
        )
        
        result_dict = json.loads(response.choices[0].message.content)
        return result_dict
