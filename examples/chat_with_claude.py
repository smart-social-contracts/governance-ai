"""Example: Chat with a governance AI assistant using Claude."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "rag"))
from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL, PROMPTS_PATH

import anthropic
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def load_system_prompt(prompt_name: str = "system_prompt") -> str:
    """Load a system prompt by name."""
    prompt_file = PROMPTS_PATH / f"{prompt_name}.md"
    if not prompt_file.exists():
        console.print(f"[red]Prompt not found: {prompt_file}[/red]")
        console.print(f"[dim]Available prompts: {', '.join(p.stem for p in PROMPTS_PATH.glob('*.md'))}[/dim]")
        sys.exit(1)
    return prompt_file.read_text(encoding="utf-8")


def chat(system_prompt: str, messages: list[dict], user_message: str) -> str:
    """Send a message and get a response."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    messages.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=messages,
    )

    assistant_message = response.content[0].text
    messages.append({"role": "assistant", "content": assistant_message})

    return assistant_message


def main():
    parser = argparse.ArgumentParser(description="Chat with a governance AI assistant (Claude)")
    parser.add_argument("query", nargs="?", help="Single query (omit for interactive mode)")
    parser.add_argument("--prompt", default="system_prompt", help="Which system prompt to use (default: system_prompt)")
    args = parser.parse_args()

    if not ANTHROPIC_API_KEY:
        console.print("[red]ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key.[/red]")
        sys.exit(1)

    system_prompt = load_system_prompt(args.prompt)
    messages = []

    console.print(f"\n[bold]Governance AI — Claude ({args.prompt})[/bold]")
    console.print("[dim]Training AIs to discover love as the best way to survive and flourish[/dim]\n")

    if args.query:
        # Single query mode
        response = chat(system_prompt, messages, args.query)
        console.print(Panel(Markdown(response), title="Governance AI", border_style="green"))
    else:
        # Interactive mode
        console.print("[dim]Type 'quit' to exit.[/dim]\n")
        while True:
            try:
                user_input = console.input("[bold blue]You:[/bold blue] ")
            except (EOFError, KeyboardInterrupt):
                break

            if user_input.strip().lower() in ("quit", "exit", "q"):
                break
            if not user_input.strip():
                continue

            try:
                response = chat(system_prompt, messages, user_input)
                console.print()
                console.print(Panel(Markdown(response), title="Governance AI", border_style="green"))
                console.print()
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]\n")

    console.print("\n[dim]Session ended.[/dim]")


if __name__ == "__main__":
    main()
