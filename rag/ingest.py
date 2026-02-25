"""Ingest paper content into a vector store for RAG retrieval."""

import argparse
import sys
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from rich.console import Console

from config import CHUNK_OVERLAP, CHUNK_SIZE, EMBEDDING_MODEL, OPENAI_API_KEY, PAPER_PATH, VECTORSTORE_PATH

console = Console()


def load_paper_documents(paper_path: Path) -> list[dict]:
    """Load all markdown files from the paper source directory."""
    documents = []
    md_files = sorted(paper_path.rglob("*.md"))

    if not md_files:
        console.print(f"[red]No markdown files found in {paper_path}[/red]")
        sys.exit(1)

    for md_file in md_files:
        relative_path = md_file.relative_to(paper_path)
        content = md_file.read_text(encoding="utf-8")
        if content.strip():
            documents.append({
                "content": content,
                "metadata": {
                    "source": str(relative_path),
                    "filename": md_file.name,
                    "section": relative_path.parent.name or "root",
                },
            })
            console.print(f"  [dim]Loaded {relative_path}[/dim]")

    return documents


def chunk_documents(documents: list[dict], chunk_size: int, chunk_overlap: int) -> tuple[list[str], list[dict]]:
    """Split documents into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", " ", ""],
    )

    all_texts = []
    all_metadatas = []

    for doc in documents:
        chunks = splitter.split_text(doc["content"])
        for i, chunk in enumerate(chunks):
            all_texts.append(chunk)
            all_metadatas.append({
                **doc["metadata"],
                "chunk_index": i,
                "chunk_total": len(chunks),
            })

    return all_texts, all_metadatas


def create_vectorstore(texts: list[str], metadatas: list[dict], persist_dir: Path) -> Chroma:
    """Create and persist a Chroma vector store."""
    persist_dir.mkdir(parents=True, exist_ok=True)

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
    )

    vectorstore = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        embedding=embeddings,
        persist_directory=str(persist_dir),
        collection_name="paper_content",
    )

    return vectorstore


def main():
    parser = argparse.ArgumentParser(description="Ingest paper content into vector store")
    parser.add_argument("--paper-path", type=Path, default=PAPER_PATH, help="Path to paper source directory")
    parser.add_argument("--output", type=Path, default=VECTORSTORE_PATH, help="Path to vector store output")
    parser.add_argument("--chunk-size", type=int, default=CHUNK_SIZE, help="Chunk size for splitting")
    parser.add_argument("--chunk-overlap", type=int, default=CHUNK_OVERLAP, help="Chunk overlap for splitting")
    args = parser.parse_args()

    console.print("\n[bold]Governance AI — Paper Ingestion[/bold]\n")

    # Load documents
    console.print(f"[blue]Loading documents from {args.paper_path}...[/blue]")
    documents = load_paper_documents(args.paper_path)
    console.print(f"[green]Loaded {len(documents)} documents[/green]\n")

    # Chunk documents
    console.print(f"[blue]Chunking documents (size={args.chunk_size}, overlap={args.chunk_overlap})...[/blue]")
    texts, metadatas = chunk_documents(documents, args.chunk_size, args.chunk_overlap)
    console.print(f"[green]Created {len(texts)} chunks[/green]\n")

    # Create vector store
    console.print(f"[blue]Creating vector store at {args.output}...[/blue]")
    vectorstore = create_vectorstore(texts, metadatas, args.output)
    console.print(f"[green]Vector store created with {vectorstore._collection.count()} embeddings[/green]\n")

    console.print("[bold green]Ingestion complete![/bold green]")


if __name__ == "__main__":
    main()
