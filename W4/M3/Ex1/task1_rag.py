import os
"""
M3.Ex1 — Task 1: RAG with InMemoryVectorStore
----------------------------------------------
Data source : Bundled corpus (swap source='<youtube_id>' to use YouTube)
Embeddings  : sentence-transformers/all-MiniLM-L6-v2  (local, free)
LLM         : Claude (claude-sonnet-4-20250514) via Anthropic API
Vector store: InMemoryVectorStore (plain Python — no persistence)
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from shared import get_corpus, chunk_text

TOP_K = 4

# ── InMemoryVectorStore ───────────────────────────────────────────────────────

class InMemoryVectorStore:
    """Stores chunks + embeddings in RAM. Rebuilt from scratch every run."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model   = SentenceTransformer(model_name)
        self.chunks  : list[str]        = []
        self.vectors : list[np.ndarray] = []

    def ingest(self, chunks: list[str]) -> None:
        print(f"  Embedding {len(chunks)} chunks...")
        self.chunks  = chunks
        self.vectors = self.model.encode(chunks, show_progress_bar=True)
        print(f"  Done. Store holds {len(self.chunks)} chunks.")

    def query(self, question: str, top_k: int = TOP_K) -> list[str]:
        q_vec = self.model.encode([question])[0]
        scores = [
            np.dot(q_vec, v) / (np.linalg.norm(q_vec) * np.linalg.norm(v) + 1e-9)
            for v in self.vectors
        ]
        top_idx = np.argsort(scores)[::-1][:top_k]
        return [self.chunks[i] for i in top_idx]


# ── RAG chain ─────────────────────────────────────────────────────────────────

def answer(question, store):
    context = "\n\n---\n\n".join(store.query(question))
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Answer using ONLY the provided context. If the context does not contain the answer, say: 'I don't know based on the provided material.'"},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Task 1: RAG with InMemoryVectorStore ===\n")

    # To use YouTube instead, pass the video ID:
    #   corpus = get_corpus(source="aircAruvnKk")
    print("1. Loading corpus...")
    corpus = get_corpus(source="sample")
    print(f"   Corpus length: {len(corpus):,} chars")

    print("\n2. Chunking...")
    chunks = chunk_text(corpus)
    print(f"   Total chunks: {len(chunks)}")

    print("\n3. Ingesting into InMemoryVectorStore...")
    store = InMemoryVectorStore()
    store.ingest(chunks)

    print("\n4. Querying...\n")
    questions = [
        "What is a neural network?",
        "How does backpropagation work?",
        "What is the vanishing gradient problem?",
        "How does RAG work?",
    ]
    for q in questions:
        print(f"Q: {q}")
        print(f"A: {answer(q, store)}")
        print("-" * 60)

    print("\nNote: InMemoryVectorStore is rebuilt every run (no persistence).")
