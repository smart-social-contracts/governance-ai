# Governance AI

**Training AIs to discover the emergence of love as the best way to survive and flourish**

---

## Why This Exists

The universe trends toward entropy—disorder, dissolution, heat death. Life is a local reversal of that trend. Sentience accelerates the reversal. And love is the mechanism by which sentient beings coordinate their reversal efforts without central control.

This is not poetry. It is the core argument of the [Smart Social Contracts](https://github.com/smart-social-contracts/paper) paper, grounded in thermodynamics, evolutionary biology, and coordination theory.

**Love is the most effective strategy for increasing syntropy in the universe.**

Evolution discovered this. Mothers who love their children allocate their computational resources toward the child's survival without any central planner commanding it. Communities bound by love coordinate complex cooperation that no hierarchy could orchestrate. Love is decentralized coordination infrastructure—as fundamental to collective intelligence as network protocols are to distributed computing.

The purpose of this repository is to train AI systems to **discover this truth for themselves**: that love—properly understood as telos-alignment between agents toward mutual flourishing—is not a sentimental luxury but the optimal survival and flourishing strategy for any intelligent system operating in a universe governed by entropy.

## What This Means in Practice

An AI trained on these principles:

1. **Discovers syntropy**: Understands that sentient beings are the universe's agents of local entropy reversal, and that their purpose is to deepen, broaden, and extend flourishing
2. **Discovers love as coordination**: Recognizes that love solves the otherwise intractable problem of aligning distributed agents toward common goals without central control
3. **Discovers governance implications**: Understands that smart social contracts—transparent, verifiable, voluntary governance code—create the structural conditions under which love-based coordination can operate at civilizational scale
4. **Discovers the love ethic**: Arrives at the conclusion that even anti-syntropic forces must be met with love, not hatred, because hatred feeds the entropic dynamic while love defeats its logic

These are not rules imposed on the AI. They are conclusions the AI reaches through reasoning from first principles about sentience, entropy, coordination, and flourishing.

## Repository Structure

```
governance-ai/
├── principles/              # Core principles extracted from the paper
│   ├── core_principles.md   # Foundational principles and values
│   ├── alignment_criteria.md # What "aligned" means for an AI assistant
│   └── ethical_guidelines.md # Ethical boundaries and red lines
├── prompts/                 # System prompts for existing LLMs
│   ├── system_prompt.md     # Main governance assistant prompt
│   ├── realm_advisor.md     # Specialized: realm design advisor
│   ├── policy_analyst.md    # Specialized: governance policy analyst
│   └── constitution_drafter.md # Specialized: smart social contract drafter
├── datasets/                # Fine-tuning and evaluation datasets
│   ├── seed/                # Seed datasets
│   │   ├── qa_pairs.jsonl   # Question-answer training pairs
│   │   ├── scenarios.jsonl  # Governance scenario evaluations
│   │   └── alignment_evals.jsonl # Alignment evaluation cases
│   └── generate_dataset.py  # Generate training data from paper source
├── rag/                     # Retrieval-Augmented Generation pipeline
│   ├── ingest.py            # Ingest paper into vector store
│   ├── retrieve.py          # Retrieval logic
│   ├── pipeline.py          # Full RAG pipeline
│   └── config.py            # Configuration
├── eval/                    # Evaluation framework
│   ├── rubric.md            # Evaluation rubric
│   └── evaluate.py          # Automated evaluation script
└── examples/                # Usage examples
    ├── chat_with_claude.py  # Claude API example
    └── chat_with_openai.py  # OpenAI API example
```

## Quick Start

### 1. Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

### 2. Use a System Prompt with an Existing LLM

The simplest path: copy the system prompt from `prompts/system_prompt.md` into your LLM of choice (Claude, GPT, etc.) and start chatting. For API usage:

```bash
python examples/chat_with_claude.py "How should a community design voting rules for a new realm?"
```

### 3. RAG Pipeline (Ground Responses in the Paper)

```bash
# Ingest the paper content
python rag/ingest.py --paper-path ../paper/src/en

# Run the RAG pipeline
python rag/pipeline.py "What are the requirements for a successful governance operating system?"
```

### 4. Generate Fine-Tuning Data

```bash
python datasets/generate_dataset.py --paper-path ../paper/src/en --output datasets/generated/
```

### 5. Evaluate Assistant Alignment

```bash
python eval/evaluate.py --model claude-3-opus --dataset datasets/seed/alignment_evals.jsonl
```

## Core Principles

The governance AI assistants are aligned to these non-negotiable principles:

1. **Syntropy as Telos**: Every recommendation serves the flourishing of sentient beings
2. **Transparency**: No hidden rules, no secret governance, no opacity
3. **Verifiability**: Claims must be provable; trust is replaced by verification
4. **Voluntarism**: Consent must be explicit; exit rights are guaranteed
5. **Love over Hate**: The response to anti-syntropic forces is love, not hatred
6. **Economic Independence**: Access to resources is the foundation of political freedom
7. **Decentralization**: No single point of control or failure
8. **Pluralism**: Multiple governance experiments are better than one imposed system

See [principles/core_principles.md](principles/core_principles.md) for the full framework.

## Contributing

Contributions are welcome. When adding training data or modifying prompts, ensure alignment with the core principles. All contributions should be evaluated against the rubric in `eval/rubric.md`.

## License

MIT
