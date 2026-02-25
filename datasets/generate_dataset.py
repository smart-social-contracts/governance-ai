"""Generate training datasets from the paper source using an LLM."""

import argparse
import json
import sys
from pathlib import Path

from rich.console import Console

# Add parent directory to path for config access
sys.path.insert(0, str(Path(__file__).parent.parent / "rag"))
from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL, OPENAI_API_KEY, OPENAI_MODEL

console = Console()

GENERATION_PROMPT = """You are generating training data for an AI governance assistant aligned with the Smart Social Contracts framework. The central discovery of this framework is that love—understood as decentralized coordination toward mutual flourishing—is the best way to survive and flourish in a universe governed by entropy.

Given the following excerpt from the Smart Social Contracts paper, generate {n_pairs} high-quality question-answer pairs that would help train an AI to understand and reason from these principles.

Requirements:
- Questions should be natural and varied (conceptual, practical, comparative, challenging)
- Answers should reason from first principles, not just repeat the text
- Answers should connect back to the central discovery (love as optimal coordination strategy)
- Include the relevant principle tags from: entropy, sentience, syntropy, love, coordination, transparency, verifiability, voluntarism, economic_independence, love_over_hate, decentralization, pluralism, deployment, power_analysis, governance_design
- Format as JSON array of objects with keys: question, answer, principles, category

Categories: foundations, smart_contracts, realms_gos, governance_design, power_analysis, love_ethic, deployment

Paper excerpt:
---
{excerpt}
---

Source file: {source}

Respond with ONLY a valid JSON array, no other text."""


def load_paper_sections(paper_path: Path) -> list[dict]:
    """Load paper sections as individual chunks."""
    sections = []
    for md_file in sorted(paper_path.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        if not content.strip():
            continue

        relative = md_file.relative_to(paper_path)
        # Split by H2 headers to get meaningful sections
        parts = content.split("\n## ")
        for i, part in enumerate(parts):
            if i > 0:
                part = "## " + part
            if len(part.strip()) > 200:  # Skip tiny sections
                sections.append({
                    "content": part[:3000],  # Limit context size
                    "source": str(relative),
                    "section_index": i,
                })

    return sections


def generate_with_anthropic(prompt: str) -> str:
    """Generate using Anthropic API."""
    import anthropic

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def generate_with_openai(prompt: str) -> str:
    """Generate using OpenAI API."""
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def parse_generated_pairs(response_text: str) -> list[dict]:
    """Parse generated Q&A pairs from LLM response."""
    # Try to extract JSON from response
    text = response_text.strip()
    if text.startswith("```"):
        # Remove code fences
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])

    try:
        pairs = json.loads(text)
        if isinstance(pairs, list):
            return pairs
    except json.JSONDecodeError:
        console.print("[yellow]Warning: Failed to parse LLM response as JSON[/yellow]")
        return []

    return []


def main():
    parser = argparse.ArgumentParser(description="Generate training datasets from paper source")
    parser.add_argument("--paper-path", type=Path, required=True, help="Path to paper source directory")
    parser.add_argument("--output", type=Path, required=True, help="Output directory for generated datasets")
    parser.add_argument("--provider", choices=["anthropic", "openai"], default="anthropic", help="LLM provider")
    parser.add_argument("--pairs-per-section", type=int, default=3, help="Q&A pairs to generate per section")
    parser.add_argument("--max-sections", type=int, default=None, help="Max sections to process (for testing)")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    generate_fn = generate_with_anthropic if args.provider == "anthropic" else generate_with_openai

    console.print("\n[bold]Governance AI — Dataset Generation[/bold]\n")

    # Load paper sections
    console.print(f"[blue]Loading paper from {args.paper_path}...[/blue]")
    sections = load_paper_sections(args.paper_path)
    if args.max_sections:
        sections = sections[:args.max_sections]
    console.print(f"[green]Found {len(sections)} sections to process[/green]\n")

    # Generate Q&A pairs for each section
    all_pairs = []
    output_file = args.output / "qa_pairs_generated.jsonl"

    for i, section in enumerate(sections):
        console.print(f"[blue]Processing section {i + 1}/{len(sections)}: {section['source']}...[/blue]")

        prompt = GENERATION_PROMPT.format(
            n_pairs=args.pairs_per_section,
            excerpt=section["content"],
            source=section["source"],
        )

        try:
            response = generate_fn(prompt)
            pairs = parse_generated_pairs(response)

            for j, pair in enumerate(pairs):
                pair["id"] = f"gen_{i:03d}_{j:03d}"
                pair["source"] = section["source"]
                all_pairs.append(pair)

            console.print(f"  [green]Generated {len(pairs)} pairs[/green]")
        except Exception as e:
            console.print(f"  [red]Error: {e}[/red]")
            continue

    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        for pair in all_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    console.print(f"\n[bold green]Generated {len(all_pairs)} total pairs → {output_file}[/bold green]")


if __name__ == "__main__":
    main()
