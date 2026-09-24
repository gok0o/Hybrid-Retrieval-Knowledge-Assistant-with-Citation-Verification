import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from .prompt import build_prompt


class AnswerGenerator:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("OPENROUTER_API_KEY")

        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "openai/gpt-4o-mini",
        )

        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY is not set."
            )

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        return response.choices[0].message.content