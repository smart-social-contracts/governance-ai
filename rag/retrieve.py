"""Retrieve relevant content from the vector store."""

from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from config import EMBEDDING_MODEL, OPENAI_API_KEY, TOP_K, VECTORSTORE_PATH


def get_vectorstore(persist_dir: Path = VECTORSTORE_PATH) -> Chroma:
    """Load an existing Chroma vector store."""
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
    )

    return Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embeddings,
        collection_name="paper_content",
    )


def retrieve(query: str, top_k: int = TOP_K, persist_dir: Path = VECTORSTORE_PATH) -> list[dict]:
    """Retrieve the most relevant chunks for a query.

    Returns a list of dicts with 'content', 'metadata', and 'score' keys.
    """
    vectorstore = get_vectorstore(persist_dir)

    results = vectorstore.similarity_search_with_relevance_scores(query, k=top_k)

    return [
        {
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": score,
        }
        for doc, score in results
    ]


def format_context(results: list[dict]) -> str:
    """Format retrieved results into a context string for the LLM."""
    if not results:
        return "No relevant content found in the paper."

    sections = []
    for i, result in enumerate(results, 1):
        source = result["metadata"].get("source", "unknown")
        score = result["score"]
        content = result["content"]
        sections.append(
            f"--- Source {i}: {source} (relevance: {score:.2f}) ---\n{content}"
        )

    return "\n\n".join(sections)
