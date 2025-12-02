# 📦 LLaMAFactory Dataset Generator

---

## Features

### **1. Multi-Domain Support**

Select any domain using:

```bash
--domain haiintel_core
--domain expense
--domain <your-custom-domain>
```

### **2. YAML Configuration**

Everything (company, agent name, products, regions, doc types, currencies) is
controlled through:

```
config.yaml
```

No need to edit Python files for domain updates.

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- jq (optional, for JSON formatting)

---

## How to Run

### **1. Install dependencies**

```bash
# Install all dependencies including dev tools
pip install -r requirements.txt

# Or install only core dependencies
pip install pyyaml
```

Alternatively, use the Makefile:

```bash
make install
```

### **2. Prepare your `config.yaml`**

Example:

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

---

### **3. Run the CLI**

**Option A: Direct Python command**

```bash
python -m src.cli --config config.yaml --domain expense --out-dir ./training-jsons
```

**Option B: Using Makefile**

```bash
# Generate for a specific domain
make generate DOMAIN=expense

# Generate for all domains in config.yaml
make generate-all
```

### Output:

The generator creates JSON files with training examples and statistics:

```
training-jsons/
├─ intro-training.json                           # Introduction and greeting examples
├─ intro-training_stats.json                     # Statistics for intro dataset
├─ operator-training.json                        # Operator logic examples
├─ operator-training_stats.json
├─ rag_context_training.json                     # RAG context handling
├─ rag_context_training_stats.json
├─ entity-classification-training.json           # Entity type classification
├─ entity-classification-training_stats.json
├─ safety_guardrails_training.json               # Safety and guardrails
├─ safety_guardrails_training_stats.json
├─ hard_negatives_hallucinations.json            # Hard negative examples
├─ hard_negatives_hallucinations_stats.json
├─ company_kb_training.json                      # Company knowledge base Q&A
├─ company_kb_training_stats.json
├─ company_kb_no_hallucinations_training.json    # KB with anti-hallucination
├─ company_kb_no_hallucinations_training_stats.json
├─ business_integration_training.json            # Business integration scenarios
├─ business_integration_training_stats.json
└─ expense_documents_training.json               # Domain-specific: Expense docs
    └─ expense_documents_training_stats.json
```

---

## 🛠️ Makefile Targets

The project includes a comprehensive Makefile for common tasks:

| Target              | Description                                                |
| ------------------- | ---------------------------------------------------------- |
| `make install`      | Create virtual environment and install dependencies        |
| `make generate`     | Generate dataset for a specific domain (use `DOMAIN=name`) |
| `make generate-all` | Generate datasets for all domains in config.yaml           |
| `make shell`        | Enter the virtual environment shell                        |
| `make format`       | Format all JSON files using jq                             |
| `make clean-venv`   | Remove virtual environment                                 |
| `make clean-output` | Remove generated training files                            |
| `make clean`        | Clean everything (venv + output)                           |

**Examples:**

```bash
# Generate for expense domain
make generate DOMAIN=expense

# Generate for all domains
make generate-all

# Clean and regenerate
make clean && make generate-all

# Format JSON output
make format
```

---

## 🧠 Philosophy

This project applies the **SOLID principles**:

- **Single Responsibility** → Each section has its own builder module
- **Open/Closed** → Add a new section by adding a new file in `sections/`
- **Liskov Substitution** → All builders behave via `SectionBuilder`
- **Interface Segregation** → Minimal interface
- **Dependency Inversion** → High-level generator depends on factory, not concrete classes

It's also:

- **DRY** → Common utilities in `utils.py`
- **Extensible** → Easily add new JSON schemas & builders
- **Testable** → Builders are pure functions returning a list of examples
- **Quality-First** → Automatic deduplication, validation, and statistics generation

---

## 🔍 Key Features

### **Entity Classification with Rule-Based Classifier**

The entity classification module uses a keyword-based classifier to generate meaningful training examples:

- **Automatic Classification**: Entities are classified based on keywords (e.g., "Invoice", "Person", "Vendor")
- **Domain-Specific**: Supports multiple entity types per domain (configured in `config.yaml`)
- **Extensible**: Easy to add new entity types and keywords in `src/utils.py:classify_entity_name()`

**Example Output:**

```json
{
  "system": "You are HAIIndexer classification module. Classify the given string into one or more entity types.",
  "instruction": "What type of entity is Global Invoice for CFO 001?",
  "input": "Global Invoice for CFO 001",
  "output": "This entity belongs to the following types: Person, Invoice",
  "metadata": {
    "section": "entity_classification",
    "classified_as": ["Person", "Invoice"],
    "possible_labels": ["Person", "CostCenter", "ExpensePolicy", ...]
  }
}
```

### **Dataset Quality Assurance**

- **Validation**: All examples are validated before saving
- **Deduplication**: Duplicate examples are automatically removed
- **Statistics**: Each dataset includes a companion `*_stats.json` file with:
  - Total examples count
  - Estimated token count
  - Section breakdown

---

## 📁 Project Structure

```
dataset-generator/
├── config.yaml              # Multi-domain configuration
├── requirements.txt         # Python dependencies
├── Makefile                 # Build automation
├── README.md                # This file
└── src/
    ├── cli.py              # Command-line interface
    ├── domain_config.py    # Domain configuration data class
    ├── factory.py          # Section builder factory
    ├── generator.py        # Main dataset generator
    ├── utils.py            # Shared utilities and entity classifier
    └── sections/           # Section builders (one per training type)
        ├── base.py
        ├── intro.py
        ├── operator.py
        ├── entity_classification.py
        ├── rag_context.py
        ├── safety.py
        └── ...
```

---

## 🚀 Adding a New Domain

1. **Edit `config.yaml`** and add a new domain entry:

```yaml
domains:
  - id: my_new_domain
    company_name: "MyCompany"
    agent_name: "MyAgent"
    domain_name: "My Domain"
    entity_types: ["TypeA", "TypeB"]
    # ... other configuration
```

2. **Extend entity classifier** (optional):

If you have new entity types, add keyword patterns in `src/utils.py:classify_entity_name()`

3. **Generate datasets**:

```bash
make generate DOMAIN=my_new_domain
```

---

## 🧪 Development

### **Code Quality Tools**

The project supports modern Python development tools:

```bash
# Install dev dependencies
pip install -r requirements.txt

# Format code
black src/

# Type checking
mypy src/

# Linting
ruff src/

# Run tests (if implemented)
pytest
```

---
