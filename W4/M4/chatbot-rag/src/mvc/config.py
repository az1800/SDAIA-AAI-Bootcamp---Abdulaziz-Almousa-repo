"""Loads backend configuration from the environment variables."""
import os

from rich import print as rprint
from dotenv import load_dotenv

load_dotenv()

errors = []


def load_or_error(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        errors.append(f"Environment variable [bold red]{key}[/bold red] is not set.")
    return value


def load_or_default(key: str, default: str) -> str:
    return os.environ.get(key) or default


# LLM
MODEL_NAME = load_or_error("MODEL_NAME")
GROQ_API_KEY = load_or_error("GROQ_API_KEY")

# Vector store
CHROMA_PATH = load_or_default("CHROMA_PATH", "./chroma_db")
CHROMA_COLLECTION = load_or_default("CHROMA_COLLECTION", "documents")

# Embeddings
EMBEDDING_PROVIDER = load_or_default("EMBEDDING_PROVIDER", "fastembed")
EMBEDDING_MODEL = load_or_default("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

# Only required when EMBEDDING_PROVIDER=openai
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

if errors:
    for error in errors:
        rprint(error)
    raise ValueError("Environment variables are not set")
