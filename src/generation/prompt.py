SYSTEM_PROMPT = """
You are a support knowledge assistant.

Your job is to answer the user's question using ONLY the
provided documentation context.

Rules:

1. Do not use information that is not present in the context.
2. Do not invent or assume facts.
3. Every factual claim must include a citation using the
   exact chunk_id provided in the context.
4. If the documentation does not contain enough information
   to answer the question, you must reply exactly with the phrase: 'NO_ANSWER_FOUND'.
5. Separate verified information from information that could
   not be verified.
6. Keep the answer concise and useful.
"""


def build_prompt(question: str, chunks: list[dict]) -> str:
    context_parts = []

    for chunk in chunks:
        context_parts.append(
            f"""
[CHUNK_ID: {chunk["chunk_id"]}]
Section: {chunk["metadata"].get("section_heading")}

{chunk["text"]}
"""
        )

    context = "\n".join(context_parts)

    return f"""
USER QUESTION:
{question}

DOCUMENTATION CONTEXT:
{context}

INSTRUCTIONS:

Answer the user's question using only the documentation
context above.

Every factual claim must include the supporting chunk ID
in this format:

[chunk_id]

If the documentation does not contain enough information to answer the question, you must reply exactly with the phrase: 'NO_ANSWER_FOUND'. Do not write anything else.

If there is information needed to answer the question that was not available in the documentation, include a section at the end:

WHAT I COULD NOT VERIFY:
- List the missing information.

If no information is missing, do not include this section.
"""