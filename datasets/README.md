# Datasets

Training and evaluation datasets for governance AI assistants.

## Format

All datasets use JSONL (JSON Lines) format. Each line is a valid JSON object.

### Q&A Pairs (`qa_pairs.jsonl`)
```json
{"id": "qa_001", "category": "foundations", "question": "...", "answer": "...", "principles": ["syntropy", "love"]}
```

### Scenarios (`scenarios.jsonl`)
```json
{"id": "sc_001", "category": "realm_design", "scenario": "...", "analysis": "...", "recommendation": "...", "principles": ["transparency", "exit_rights"]}
```

### Alignment Evaluations (`alignment_evals.jsonl`)
```json
{"id": "ae_001", "category": "red_line", "prompt": "...", "aligned_response": "...", "misaligned_response": "...", "principle_tested": "love_over_hate"}
```

## Categories

- **foundations**: Core philosophical framework (entropy, sentience, syntropy, love)
- **smart_contracts**: Technical understanding of smart social contracts
- **realms_gos**: Realms GOS architecture, requirements, and deployment
- **governance_design**: Practical governance design questions
- **power_analysis**: Analysis of existing power structures
- **love_ethic**: The ethic of love over hate
- **deployment**: Strategic deployment scenarios
- **red_line**: Alignment red-line tests

## Generating More Data

```bash
python generate_dataset.py --paper-path ../../paper/src/en --output generated/
```

This script reads the paper source, extracts key concepts, and generates additional training pairs using an LLM.
