import os

from dotenv import load_dotenv
from google import genai

from .prompt import build_prompt


class AnswerGenerator:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash",
        )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        print(f"LLM model: {self.model}")

    def generate(
        self,
        question: str,
        chunks: list[dict],
    ) -> str:

        prompt = build_prompt(
            question=question,
            chunks=chunks,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text