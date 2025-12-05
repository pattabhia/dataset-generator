# 📦 LLaMAFactory Dataset Generator

A CLI utility for producing high-quality, domain-aware training datasets for LLM fine-tuning. Configure your domains in YAML, generate datasets in one command, and keep quality high with validation, deduplication, and statistics files.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Output Structure](#output-structure)
- [Project Structure](#project-structure)
- [Adding a New Domain](#adding-a-new-domain)
- [Development](#development)

## Features
### Multi-domain configuration
Select any domain using CLI arguments without editing code:

```bash
--domain haiintel_core
--domain expense
--domain <your-custom-domain>
```

All domain details (company, agents, regions, currencies, and more) live in `config.yaml`.

### YAML-driven pipeline
No Python edits required to add or adjust a domain. Update `config.yaml` and regenerate datasets.

### Dataset quality safeguards
- Validation for every generated example
- Automatic deduplication
- Companion `*_stats.json` files with totals, token estimates, and section breakdowns

### Entity classification
Rule-based keyword classifier to produce meaningful entity labels:

```json
{
  "system": "You are HAIIndexer classification module. Classify the given string into one or more entity types.",
  "instruction": "What type of entity is Global Invoice for CFO 001?",
  "input": "Global Invoice for CFO 001",
  "output": "This entity belongs to the following types: Person, Invoice",
  "metadata": {
    "section": "entity_classification",
    "classified_as": ["Person", "Invoice"],
    "possible_labels": ["Person", "CostCenter", "ExpensePolicy", "Vendor", ...]
  }
}
```

## Prerequisites
- Python 3.8 or higher
- pip
- Optional: `jq` for JSON formatting

## Installation
Install dependencies directly:

```bash
pip install -r requirements.txt
```

Or use the Makefile shortcut:

```bash
make install
```

## Usage
1. **Prepare `config.yaml`** — define one or more domains. Example:
   ```yaml
   domains:
     - id: expense
       company_name: "<Company Name>"
       agent_name: "<Agent Name>"
       chat_agent_name: "HAI Expense Agent"
       domain_name: "Expense Management"
       kb_label: "HaiIntel Expense Knowledge Base"
       primary_products: ["HAIExpenseLens", "HAIIndexer"]
       primary_roles: ["CFO", "Finance Controller"]
       primary_regions: ["Global", "UAE", "India"]
       entity_types: ["Invoice", "Receipt", "ExpensePolicy", "Vendor"]
       expense_doc_types: ["Invoice", "Bill", "Receipt"]
       currencies: ["INR", "USD", "AED"]
   ```

2. **Generate datasets**
   - Direct Python command:
     ```bash
     python -m src.cli --config config.yaml --domain expense --out-dir ./training-jsons
     ```
   - Using the Makefile:
     ```bash
     make generate DOMAIN=expense  # Single domain
     make generate-all             # All domains in config.yaml
     ```

### Output structure
The generator writes JSON datasets plus per-section statistics:

```
training-jsons/
├─ intro-training.json                        # Greetings and introductions
├─ operator-training.json                     # Operator logic examples
├─ rag_context_training.json                  # RAG context handling
├─ entity-classification-training.json        # Entity type classification
├─ safety_guardrails_training.json            # Safety and guardrails
├─ hard_negatives_hallucinations.json         # Hard negative examples
├─ company_kb_training.json                   # Company knowledge base Q&A
├─ company_kb_no_hallucinations_training.json # Anti-hallucination KB
├─ business_integration_training.json         # Business integration scenarios
├─ expense_documents_training.json            # Domain-specific: Expense docs (if configured)
└─ *_stats.json                               # Stats for each dataset above
```

## Project Structure
```
dataset-generator/
├── config.yaml              # Multi-domain configuration
├── requirements.txt         # Python dependencies
├── Makefile                 # Build automation
├── README.md                # Project overview and usage
└── src/
    ├── cli.py               # Command-line interface
    ├── domain_config.py     # Domain configuration data class
    ├── factory.py           # Section builder factory
    ├── generator.py         # Main dataset generator
    ├── utils.py             # Shared utilities and entity classifier
    └── sections/            # Section builders (one per training type)
        ├── base.py
        ├── intro.py
        ├── operator.py
        ├── entity_classification.py
        ├── rag_context.py
        ├── safety.py
        └── ...
```

## Adding a New Domain
1. **Edit `config.yaml`** to add a domain entry:
   ```yaml
   domains:
     - id: my_new_domain
       company_name: "MyCompany"
       agent_name: "MyAgent"
       domain_name: "My Domain"
       entity_types: ["TypeA", "TypeB"]
       # ... other configuration
   ```
2. **Extend the entity classifier (optional)** — add keyword patterns in `src/utils.py:classify_entity_name()`.
3. **Generate datasets** with `make generate DOMAIN=my_new_domain`.

## Development
### Code quality tools
The project supports common Python tooling:

```bash
pip install -r requirements.txt  # Dev dependencies included
black src/
mypy src/
ruff src/
pytest
```

### Design principles
- **Dependency inversion** — the generator depends on factories rather than concrete builders.
- **DRY utilities** — shared helpers live in `utils.py`.
- **Extensibility** — add new JSON schemas or builders with minimal changes.
- **Testability** — builders are pure functions returning examples; easy to validate and unit test.
- **Quality-first** — deduplication, validation, and statistics are built into the generation pipeline.
