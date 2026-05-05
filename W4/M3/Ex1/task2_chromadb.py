import os
"""
M3.Ex1 — Task 2: RAG with Persistent ChromaDB
----------------------------------------------
Replaces InMemoryVectorStore from Task 1 with ChromaDB.

Steps:
  1. Create a persistent ChromaDB vector store on disk  (./chroma_db/).
  2. Ingest documents — skipped if collection already has data.
  3. Query by embedding similarity via ChromaDB's HNSW index.
  4. Restart verification: DB loads from disk, embeddings NOT recomputed.
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from shared import get_corpus, chunk_text

TOP_K           = 4
DB_PATH         = "./chroma_db"
COLLECTION_NAME = "ml_lecture_notes"

# ── ChromaVectorStore ─────────────────────────────────────────────────────────

class ChromaVectorStore:
    """
    Persistent vector store backed by ChromaDB.
    Data survives process restarts. Embeddings are computed only once.
    """

    def __init__(self, db_path: str, collection_name: str,
                 model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

        # PersistentClient writes SQLite + HNSW index to db_path/
        self.client = chromadb.PersistentClient(path=db_path)

        # get_or_create is idempotent — safe to call on every restart
        self.collection = self.client.get_or_create_collection(
            name     = collection_name,
            metadata = {"hnsw:space": "cosine"},   # cosine distance ANN index
        )

        n = self.collection.count()
        print(f"  ChromaDB collection '{collection_name}' — {n} documents on disk.")

    @property
    def is_empty(self) -> bool:
        return self.collection.count() == 0

    # Step 2 — ingest ──────────────────────────────────────────────────────────

    def ingest(self, chunks: list[str]) -> None:
        """Embed and store chunks. No-op if collection already populated."""
        if not self.is_empty:
            print(f"  Skipping ingestion — {self.collection.count()} chunks already in DB.")
            return

        print(f"  Embedding {len(chunks)} chunks (first run only)...")
        embeddings = self.model.encode(chunks, show_progress_bar=True).tolist()

        self.collection.add(
            ids        = [f"chunk_{i}" for i in range(len(chunks))],
            documents  = chunks,
            embeddings = embeddings,
        )
        print(f"  Ingestion complete. DB now holds {self.collection.count()} chunks.")

    # Step 3 — query ───────────────────────────────────────────────────────────

    def query(self, question: str, top_k: int = TOP_K) -> list[str]:
        q_vec   = self.model.encode([question])[0].tolist()
        results = self.collection.query(
            query_embeddings = [q_vec],
            n_results        = top_k,
            include          = ["documents"],
        )
        return results["documents"][0]   # list[str] of top-k chunks


# ── RAG chain ─────────────────────────────────────────────────────────────────

def answer(question: str, store: ChromaVectorStore) -> str:
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
    print("=== Task 2: RAG with Persistent ChromaDB ===\n")

    # Step 1 — connect (or create) persistent DB
    print(f"1. Connecting to ChromaDB at '{os.path.abspath(DB_PATH)}'...")
    store = ChromaVectorStore(DB_PATH, COLLECTION_NAME)

    # Steps 2 — ingest only on first run
    if store.is_empty:
        print("\n2. First run — loading corpus...")
        corpus = get_corpus(source="sample")   # swap to YouTube ID here
        print(f"   Corpus length: {len(corpus):,} chars")

        print("\n3. Chunking...")
        chunks = chunk_text(corpus)
        print(f"   Total chunks: {len(chunks)}")

        print("\n4. Ingesting into ChromaDB...")
        store.ingest(chunks)
    else:
        print("\n2-4. DB already populated — skipping corpus fetch, chunk, and embed.")
        print(f"     {store.collection.count()} chunks loaded from disk instantly.")

    # Step 3 — query
    print("\n5. Querying...\n")
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

    # Step 4 — persistence confirmation
    print("\n=== Persistence verification ===")
    print(f"DB path : {os.path.abspath(DB_PATH)}")
    print(f"Contents: {os.listdir(DB_PATH)}")
    print("Run this script again — it will skip steps 2-4 entirely.")
    print("Embeddings are NOT recomputed on subsequent runs.")
