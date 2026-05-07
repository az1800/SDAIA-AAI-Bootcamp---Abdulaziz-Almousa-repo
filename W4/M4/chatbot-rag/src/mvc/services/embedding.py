"""Factory that returns a LangChain Embeddings object.

Uses FastEmbed by default — runs on onnxruntime, no torch required.
Supported providers:
  - "fastembed" (default) — local, free, no GPU needed
  - "openai"              — requires OPENAI_API_KEY in .env
"""

from langchain_core.embeddings import Embeddings


def new_embedding_function() -> Embeddings:
    from mvc.config import EMBEDDING_PROVIDER, EMBEDDING_MODEL, OPENAI_API_KEY

    if EMBEDDING_PROVIDER == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=OPENAI_API_KEY)

    # Default: FastEmbed (onnxruntime-based, no torch needed)
    from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
    return FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)