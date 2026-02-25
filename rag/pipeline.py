"""Full RAG pipeline: retrieve paper context + generate response."""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL, OPENAI_API_KEY, OPENAI_MODEL, PROMPTS_PATH
from retrieve import format_context, retrieve

console = Console()


def load_system_prompt() -> str:
    """Load the main system prompt."""
    prompt_file = PROMPTS_PATH / "system_prompt.md"
    if not prompt_file.exists():
        console.print(f"[red]System prompt not found at {prompt_file}[/red]")
        sys.exit(1)
    return prompt_file.read_text(encoding="utf-8")


def build_rag_prompt(query: str, context: str, system_prompt: str) -> tuple[str, str]:
    """Build the system and user messages for the RAG query."""
    system = system_prompt + "\n\n## Grounding Context\n\nThe following excerpts from the Smart Social Contracts paper are relevant to the user's question. Use them to ground your response in the paper's specific arguments and terminology. Cite the source sections when relevant.\n\n" + context

    return system, query


def query_anthropic(system: str, user_message: str) -> str:
    """Query the Anthropic API."""
    import anthropic

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


def query_openai(system: str, user_message: str) -> str:
    """Query the OpenAI API."""
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=4096,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content


def main():
    parser = argparse.ArgumentParser(description="Query the governance AI with RAG grounding")
    parser.add_argument("query", nargs="?", help="The question to ask")
    parser.add_argument("--provider", choices=["anthropic", "openai"], default="anthropic", help="LLM provider")
    parser.add_argument("--top-k", type=int, default=5, help="Number of context chunks to retrieve")
    parser.add_argument("--interactive", action="store_true", help="Interactive chat mode")
    args = parser.parse_args()

    console.print("\n[bold]Governance AI — RAG Pipeline[/bold]\n")

    system_prompt = load_system_prompt()

    query_fn = query_anthropic if args.provider == "anthropic" else query_openai

    if args.interactive:
        console.print("[dim]Interactive mode. Type 'quit' to exit.[/dim]\n")
        while True:
            try:
                query = console.input("[bold blue]You:[/bold blue] ")
            except (EOFError, KeyboardInterrupt):
                break
            if query.strip().lower() in ("quit", "exit", "q"):
                break
            if not query.strip():
                continue

            # Retrieve context
            results = retrieve(query, top_k=args.top_k)
            context = format_context(results)

            # Build prompt and query
            system, user_message = build_rag_prompt(query, context, system_prompt)
            try:
                response = query_fn(system, user_message)
                console.print()
                console.print(Panel(Markdown(response), title="Governance AI", border_style="green"))
                console.print()
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]\n")
    else:
        if not args.query:
            console.print("[red]Please provide a query or use --interactive mode[/red]")
            sys.exit(1)

        # Retrieve context
        console.print(f"[blue]Retrieving context for:[/blue] {args.query}\n")
        results = retrieve(args.query, top_k=args.top_k)
        context = format_context(results)

        console.print(f"[dim]Retrieved {len(results)} relevant chunks[/dim]\n")

        # Build prompt and query
        system, user_message = build_rag_prompt(args.query, context, system_prompt)

        console.print(f"[blue]Querying {args.provider}...[/blue]\n")
        try:
            response = query_fn(system, user_message)
            console.print(Panel(Markdown(response), title="Governance AI", border_style="green"))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)


if __name__ == "__main__":
    main()
