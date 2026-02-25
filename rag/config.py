"""Configuration for the RAG pipeline."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PAPER_PATH = Path(os.getenv("PAPER_PATH", str(PROJECT_ROOT / ".." / "paper" / "src" / "en")))
VECTORSTORE_PATH = Path(os.getenv("VECTORSTORE_PATH", str(PROJECT_ROOT / "data" / "vectorstore")))
PROMPTS_PATH = PROJECT_ROOT / "prompts"

# Embedding
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# LLM
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Retrieval
TOP_K = int(os.getenv("TOP_K", "5"))
