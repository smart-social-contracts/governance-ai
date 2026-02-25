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

## Quick Start: Build the Ollama Model

The primary output of this repo is an **Ollama model** you can run locally or serve to [geister](https://github.com/smart-social-contracts/geister) (the AI governance assistant platform).

```bash
# 1. Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# 2. Build the governance-ai model
cd ollama
./build.sh

# 3. Run it
ollama run governance-ai
```

That's it. You now have a governance AI that reasons from first principles about entropy, syntropy, and love-as-coordination.

### Use in Geister

```bash
# As the default model
export DEFAULT_LLM_MODEL=governance-ai

# Or per-agent
python persona_agent.py --model governance-ai --agent-id my_agent --persona compliant

# Or via the CLI
geister ask "What is syntropy?" --model governance-ai
```

A ready-made geister persona file is included at `ollama/geister-persona.yaml` — copy it to `geister/prompts/personas/` to add a Governance persona.

### Choose a Base Model

```bash
./build.sh              # llama3.1:8b (default — best balance)
./build.sh mistral      # mistral:7b (good alternative)
./build.sh --list       # see all options
```

Edit the `FROM` line in any `Modelfile` to use a different base.

---

## Repository Structure

```
governance-ai/
├── ollama/                  # ★ PRIMARY OUTPUT: Ollama model
│   ├── Modelfile            # Main Modelfile (llama3.1:8b base)
│   ├── Modelfile.mistral    # Mistral variant
│   ├── build.sh             # One-command model builder
│   └── geister-persona.yaml # Ready-made geister persona
├── principles/              # Core principles extracted from the paper
│   ├── core_principles.md   # Foundational principles and values
│   ├── alignment_criteria.md # What "aligned" means for an AI assistant
│   └── ethical_guidelines.md # Ethical boundaries and red lines
├── prompts/                 # System prompts (source for Modelfile)
│   ├── system_prompt.md     # Main governance assistant prompt
│   ├── realm_advisor.md     # Specialized: realm design advisor
│   ├── policy_analyst.md    # Specialized: governance policy analyst
│   └── constitution_drafter.md # Specialized: codex drafter
├── datasets/                # Training and evaluation datasets
│   ├── seed/                # Seed datasets
│   │   ├── qa_pairs.jsonl   # Question-answer training pairs
│   │   ├── scenarios.jsonl  # Governance scenario evaluations
│   │   └── alignment_evals.jsonl # Alignment evaluation cases
│   └── generate_dataset.py  # Generate more data from paper source
├── rag/                     # RAG pipeline (optional, for paper-grounded responses)
│   ├── ingest.py            # Ingest paper into vector store
│   ├── retrieve.py          # Retrieval logic
│   ├── pipeline.py          # Full RAG pipeline
│   └── config.py            # Configuration
├── eval/                    # Evaluation framework
│   ├── rubric.md            # Alignment evaluation rubric
│   └── evaluate.py          # Automated evaluation script
└── examples/                # API usage examples
    ├── chat_with_claude.py  # Claude API example
    └── chat_with_openai.py  # OpenAI API example
```

## Advanced Usage

### RAG Pipeline (Ground Responses in the Paper)

```bash
pip install -r requirements.txt
cp .env.example .env  # Add your API keys

python rag/ingest.py --paper-path ../paper/src/en
python rag/pipeline.py --interactive
```

### Generate More Training Data

```bash
python datasets/generate_dataset.py --paper-path ../paper/src/en --output datasets/generated/
```

### Evaluate Alignment

```bash
python eval/evaluate.py --dataset datasets/seed/alignment_evals.jsonl --provider anthropic
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
