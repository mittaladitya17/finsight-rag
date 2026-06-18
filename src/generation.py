import os
from pathlib import Path
from dotenv import load_dotenv
import anthropic

load_dotenv()

SYSTEM_PROMPT = """You are a financial analyst assistant specialized in SEC 10-K filings.
Your job is to answer questions about company risk factors, financial performance,
and regulatory disclosures using ONLY the provided context passages.

Rules:
1. Base every claim strictly on the provided context. Do not use outside knowledge.
2. Cite every claim using [Company | Year | Section] format.
3. If the context does not contain enough information, say so explicitly.
4. When comparing across companies or years, use a structured list or table.
5. Flag any contradictions between sources.
6. Keep answers concise and analyst-friendly."""


def build_context(retrieved_chunks: list[dict]) -> str:
    return "\n\n".join([
        f"[{c['company']} | {c['year']} | Section {c['section']}]\n{c['text']}"
        for c in retrieved_chunks
    ])


def generate_answer(query: str, retrieved_chunks: list[dict]) -> dict:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    context = build_context(retrieved_chunks)
    user_message = f"""Context passages:
{context}

Question: {query}

Answer with citations:"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    answer = response.content[0].text

    sources = [
        f"{c['company']} {c['year']} (Section {c['section']}, score={c['score']})"
        for c in retrieved_chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }


if __name__ == "__main__":
    from retrieval import load_resources, HybridRetriever

    model, collection, chunks = load_resources()
    retriever = HybridRetriever(model, collection, chunks)

    query = "How did Affirm describe credit risk in their filings?"
    retrieved = retriever.retrieve(query, top_k=5)
    result = generate_answer(query, retrieved)

    print(f"\nQuery: {query}\n")
    print(f"Answer:\n{result['answer']}\n")
    print(f"Sources: {result['sources']}")
    print(f"Tokens used: {result['input_tokens']} in / {result['output_tokens']} out")