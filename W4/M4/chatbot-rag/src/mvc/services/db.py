"""ChromaDB vector store connection manager (singleton)."""

from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever


class ChromaDB:
    """Wraps a persistent ChromaDB collection.

    Instantiate once in main.py and pass the instance into Workflow.
    The underlying Chroma client is lazy — no network or disk I/O
    happens until the first query or ingest call.
    """

    def __init__(
        self,
        path: str,
        collection: str,
        embedding_function: Embeddings,
    ) -> None:
        self._store = Chroma(
            persist_directory=path,
            collection_name=collection,
            embedding_function=embedding_function,
        )

    # ------------------------------------------------------------------
    # Retrieval helpers
    # ------------------------------------------------------------------

    def as_retriever(self, k: int = 4) -> VectorStoreRetriever:
        """Return a LangChain retriever that fetches the top-k chunks."""
        return self._store.as_retriever(search_kwargs={"k": k})

    def similarity_search(self, query: str, k: int = 4):
        """Direct similarity search; returns a list of Document objects."""
        return self._store.similarity_search(query, k=k)

    # ------------------------------------------------------------------
    # Ingest helper (used by scripts/ingest.py)
    # ------------------------------------------------------------------

    def add_documents(self, documents) -> None:
        """Add pre-split Document objects to the store."""
        self._store.add_documents(documents)
