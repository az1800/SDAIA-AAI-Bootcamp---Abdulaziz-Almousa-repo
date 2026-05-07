"""Ingest documents into ChromaDB.

Usage
-----
    uv run python scripts/ingest.py                     # ingest ./docs/
    uv run python scripts/ingest.py --docs path/to/dir  # custom folder
    uv run python scripts/ingest.py --clear             # wipe collection first

Supported file types
--------------------
    .txt  .md   — plain text (TextLoader)
    .pdf        — PDF (PyPDFLoader)
    .docx       — Word (Docx2txtLoader)
    .html .htm  — HTML (BSHTMLLoader via BeautifulSoup)
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    BSHTMLLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from mvc.config import CHROMA_PATH, CHROMA_COLLECTION
from mvc.services.db import ChromaDB
from mvc.services.embedding import new_embedding_function


LOADER_MAP = {
    ".txt":  TextLoader,
    ".md":   TextLoader,       # Markdown is plain text — no heavy parser needed
    ".pdf":  PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".html": BSHTMLLoader,
    ".htm":  BSHTMLLoader,
}


def load_documents(docs_dir: Path) -> list[Document]:
    if not docs_dir.exists():
        print(f"[error] docs directory not found: {docs_dir}")
        sys.exit(1)

    all_docs: list[Document] = []

    for ext, loader_cls in LOADER_MAP.items():
        files = list(docs_dir.rglob(f"*{ext}"))
        if not files:
            continue
        print(f"  Loading {len(files)} {ext} file(s) …")
        for fp in files:
            try:
                loader = loader_cls(str(fp))
                docs = loader.load()
                for doc in docs:
                    doc.metadata.setdefault("source", str(fp.relative_to(docs_dir)))
                all_docs.extend(docs)
            except Exception as exc:
                print(f"  [warn] Could not load {fp.name}: {exc}")

    print(f"Loaded {len(all_docs)} document(s) total.")
    return all_docs


def split_documents(documents: list[Document], chunk_size=1000, chunk_overlap=150) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunk(s)  (chunk_size={chunk_size}, overlap={chunk_overlap}).")
    return chunks


def ingest(docs_dir: Path, clear: bool = False) -> None:
    print(f"\n{'='*50}")
    print(f"  Docs dir   : {docs_dir}")
    print(f"  Chroma path: {CHROMA_PATH}")
    print(f"  Collection : {CHROMA_COLLECTION}")
    print(f"{'='*50}\n")

    documents = load_documents(docs_dir)
    if not documents:
        print("No documents found — nothing to ingest.")
        return

    chunks = split_documents(documents)

    print("\nConnecting to ChromaDB …")
    embedding_fn = new_embedding_function()
    db = ChromaDB(path=CHROMA_PATH, collection=CHROMA_COLLECTION, embedding_function=embedding_fn)

    if clear:
        print("Clearing existing collection …")
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        client.delete_collection(CHROMA_COLLECTION)
        db = ChromaDB(path=CHROMA_PATH, collection=CHROMA_COLLECTION, embedding_function=embedding_fn)

    print(f"Embedding and storing {len(chunks)} chunk(s) … (this may take a moment)")
    db.add_documents(chunks)
    print("\nDone. Documents are now in the vector store.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest documents into ChromaDB.")
    parser.add_argument("--docs", type=Path, default=ROOT / "docs", help="Docs folder (default: ./docs)")
    parser.add_argument("--clear", action="store_true", help="Wipe collection before ingesting.")
    args = parser.parse_args()
    ingest(docs_dir=args.docs.resolve(), clear=args.clear)