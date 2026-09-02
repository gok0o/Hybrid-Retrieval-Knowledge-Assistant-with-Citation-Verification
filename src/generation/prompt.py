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
   to answer the question, clearly say so.
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
Document: {chunk["document_id"]}
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

If a claim cannot be verified from the documentation,
do not make the claim.

At the end, include:

WHAT I COULD NOT VERIFY:
- List information needed to answer the question that was
  not available in the documentation.
- If nothing is missing, write "Nothing."
"""