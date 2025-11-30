# 📦 LLaMAFactory Dataset Generator

## _Modular · SOLID · DRY · Extensible · Multi-Domain Dataset Builder for SFT/Reward Training_

---

## 🚀 Features

## **1. Multi-Domain Support**

Select any domain using:

```bash
--domain haiintel_core
--domain expense
--domain <your-custom-domain>
```

## **2. YAML Configuration**

Everything (company, agent name, products, regions, doc types, currencies) is
controlled through:

```
config.yaml
```

No need to edit Python files for domain updates.

---

## ⚙️ How to Run

## **1. Install dependencies**

```bash
pip install pyyaml
```

## **2. Prepare your `config.yaml`**

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

## **3. Run the CLI**

```bash
python -m dataset_generator.cli   --config config.yaml   --domain expense   --out-dir ./training-jsons
```

## Output:

```
training-jsons/
├─ intro-training.json
├─ operator-training.json
├─ rag_context_training.json
├─ entity-classification-training.json
├─ safety_guardrails_training.json
├─ hard_negatives_hallucinations.json
├─ company_kb_training.json
├─ company_kb_no_hallucinations_training.json
├─ business_integration_training.json
└─ expense_documents_training.json
```

---

## 🧠 Philosophy

This project applies the **SOLID principles**:

- **Single Responsibility** → Each section has its own builder module
- **Open/Closed** → Add a new section by adding a new file in `sections/`
- **Liskov Substitution** → All builders behave via `SectionBuilder`
- **Interface Segregation** → Minimal interface
- **Dependency Inversion** → High-level generator depends on factory, not concrete classes

It’s also:

- **DRY** → Common utilities in `utils.py`
- **Extensible** → Easily add new JSON schemas & builders
- **Testable** → Builders are pure functions returning a list of examples

---

## Makefile Usage

1. Create venv + install deps + generate datasets
   (all in one command)

```
make generate
```

This does:

- Create venv (if not exists)
- Install dependencies
- Run dataset generator
- Output JSON to training-jsons/

**2. Generate for a different domain**

```
make generate domain=expense
```

**3. Open venv and run CLI**

```
make shell
```

This drops you inside the venv without needing:

```
source venv/bin/activate
```

**4. Clean ALL**

```
make clean
```

**5. Format generated JSON files using jq**

```
make format
```

(Requires jq installed: brew install jq)
