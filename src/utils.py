# dataset_generator/utils.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .domain_config import DomainConfig


# -----------------------------------------------------------------------------
# Utility helpers for metadata, validation, deduplication and statistics
#
# The original generator code produced a number of ad‑hoc metadata formats and
# repetitive examples. To improve the quality of the datasets and ease
# downstream analysis we provide a set of helpers here:
#
# * ``make_metadata`` builds a standard metadata dict with common keys. You
#   should call this in every section builder instead of constructing
#   ``metadata`` by hand. Additional fields can be passed via kwargs.
# * ``validate_example`` checks that each example contains required keys and
#   non-empty outputs. Invalid examples are dropped silently before saving.
# * ``deduplicate_examples`` removes duplicate examples based on the
#   instruction and a prefix of the output. This helps prevent over‑fitting on
#   repeated templates.
# * ``compute_stats`` returns a summary of the dataset for transparency.
# * ``save_json_array`` now deduplicates, validates and saves both the data and
#   a sidecar ``*_stats.json`` file with high level statistics.

def make_metadata(section: str, index: int, complexity: str, tags: List[str],
                  reasoning_mode: str, confidence: float = 1.0,
                  is_negative_example: bool = False, **kwargs: Any) -> Dict[str, Any]:
    """Create a standardized metadata dictionary.

    Parameters
    ----------
    section: str
        Identifier for the training section (e.g. "intro", "operator", etc.).
    index: int
        Sequential index of the example within the section.
    complexity: str
        Complexity tier for curriculum learning ("low", "medium", "high").
    tags: list of str
        Arbitrary tags to classify the example (e.g. ["greeting", "capability"]).
    reasoning_mode: str
        High level mode used for reasoning (e.g. "template", "chain_of_thought").
    confidence: float, optional
        Confidence level of the example (0.0–1.0). Defaults to 1.0.
    is_negative_example: bool, optional
        Whether the example represents a negative/hard negative case.
    **kwargs: Any
        Extra metadata fields are merged into the result.

    Returns
    -------
    dict
        A metadata dictionary ready to be attached to a training example.
    """
    meta: Dict[str, Any] = {
        "section": section,
        "index": index,
        "complexity": complexity,
        "tags": tags,
        "reasoning_mode": reasoning_mode,
        "confidence": confidence,
        "is_negative_example": is_negative_example,
    }
    meta.update(kwargs)
    return meta


def validate_example(example: Dict[str, Any]) -> bool:
    """Validate a single training example.

    An example is considered valid if it contains at least a ``system`` key and
    a non-empty ``output``. If ``instruction`` is present it must be non-empty
    as well. For examples where ``output`` is a dict or list, the structure
    must not be empty.

    Parameters
    ----------
    example: dict
        The example to validate.

    Returns
    -------
    bool
        True if the example passes validation, False otherwise.
    """
    # Check mandatory keys
    if "system" not in example or "output" not in example:
        return False
    # Check instruction if provided
    instr = example.get("instruction")
    if instr is not None and isinstance(instr, str) and not instr.strip():
        return False
    # Validate output
    out = example["output"]
    if isinstance(out, str):
        if not out.strip():
            return False
    elif isinstance(out, dict):
        if not out:
            return False
    elif isinstance(out, list):
        # For multi-turn dialogues output may be a list of messages
        if not out:
            return False
        # ensure at least one message has content
        if not any(isinstance(m, dict) and m.get("content", "").strip() for m in out):
            return False
    else:
        # Unknown output type – reject
        return False
    return True


def deduplicate_examples(examples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate examples based on instruction and output prefix.

    This function hashes each example by its instruction (empty string if not
    provided) and the first 100 characters of the output (stringified). Only
    the first occurrence of a hash is kept.

    Parameters
    ----------
    examples: list of dicts
        The list of examples to deduplicate.

    Returns
    -------
    list of dicts
        A new list with duplicates removed.
    """
    seen: set = set()
    unique_examples: List[Dict[str, Any]] = []
    for ex in examples:
        key = (ex.get("instruction", ""), str(ex.get("output"))[:100])
        if key not in seen:
            seen.add(key)
            unique_examples.append(ex)
    return unique_examples


def compute_stats(examples: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute basic statistics for a dataset.

    Calculates the number of examples, an approximate token count and the
    distinct sections present. The token count is a rough estimate based on
    splitting text into words and applying a multiplier to account for
    sub-word tokenization.

    Parameters
    ----------
    examples: list of dicts
        The dataset for which to compute stats.

    Returns
    -------
    dict
        A dictionary with keys ``total_examples``, ``estimated_tokens`` and
        ``sections``.
    """
    total_tokens: int = 0
    sections: set = set()
    for ex in examples:
        # Count tokens in output
        out = ex.get("output")
        if isinstance(out, str):
            total_tokens += int(len(out.split()) * 1.3)
        elif isinstance(out, dict):
            total_tokens += int(len(json.dumps(out).split()) * 1.3)
        elif isinstance(out, list):
            # Flatten list of messages for token estimation
            contents = []
            for m in out:
                if isinstance(m, dict):
                    contents.append(m.get("content", ""))
                else:
                    contents.append(str(m))
            total_tokens += int(len(" ".join(contents).split()) * 1.3)
        # Collect sections from metadata if available
        meta = ex.get("metadata", {})
        sec = meta.get("section")
        if sec:
            sections.add(sec)
    return {
        "total_examples": len(examples),
        "estimated_tokens": total_tokens,
        "sections": sorted(list(sections)),
    }


def save_json_array(path: Path, items: List[Dict[str, Any]]) -> None:
    """Persist a list of dicts as a JSON array and sidecar stats file.

    This function performs deduplication and validation on the provided items
    before writing them to ``path``. It also computes simple statistics and
    writes them to a ``*_stats.json`` file alongside the dataset. If the
    directory does not exist it will be created.

    Parameters
    ----------
    path: Path
        Destination file path for the JSON dataset.
    items: list of dicts
        The raw examples to be cleaned and saved.
    """
    # Filter out invalid examples and remove duplicates
    cleaned = deduplicate_examples([ex for ex in items if validate_example(ex)])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    # Write stats
    stats = compute_stats(cleaned)
    stats_path = path.parent / f"{path.stem}_stats.json"
    with stats_path.open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def default_currencies(cfg: DomainConfig) -> List[str]:
    return cfg.currencies or ["USD", "INR"]


def default_expense_doc_types(cfg: DomainConfig) -> List[str]:
    return cfg.expense_doc_types or ["Invoice", "Bill", "Receipt"]


def classify_entity_name(name: str, entity_types: List[str]) -> List[str]:
    """Classify an entity name into one or more entity types based on keywords.

    This function uses keyword matching to determine which entity types apply
    to a given entity name. It's designed to work with domain-specific entity
    types and provides rule-based classification for training data generation.

    Parameters
    ----------
    name: str
        The entity name to classify.
    entity_types: list of str
        Available entity types for the domain (from config).

    Returns
    -------
    list of str
        A list of matching entity types. Returns ["Unknown"] if no match found.
    """
    n = name.lower()
    labels = []

    # Person keywords
    person_keywords = ["mr ", "ms ", "mrs ", "dr ", "prof ", "ceo", "cto", "cio",
                      "cfo", "person", "manager", "director", "head of", "controller",
                      "lead", "auditor", "architect", "engineer"]
    if any(keyword in n for keyword in person_keywords):
        if "Person" in entity_types:
            labels.append("Person")

    # Cost Center keywords
    if any(x in n for x in ["cost center", "costcenter", "cc-", "department"]):
        if "CostCenter" in entity_types:
            labels.append("CostCenter")

    # Expense Policy keywords
    if any(x in n for x in ["policy", "travel policy", "reimbursement", "meal policy",
                           "expense policy", "guideline"]):
        if "ExpensePolicy" in entity_types:
            labels.append("ExpensePolicy")

    # Expense Report keywords
    if any(x in n for x in ["expense report", "expense claim", "reimbursement report"]):
        if "ExpenseReport" in entity_types:
            labels.append("ExpenseReport")

    # Vendor keywords
    if any(x in n for x in ["vendor", "supplier", "merchant"]):
        if "Vendor" in entity_types:
            labels.append("Vendor")

    # GL Account keywords
    if any(x in n for x in ["gl account", "glaccount", "general ledger", "account code"]):
        if "GLAccount" in entity_types:
            labels.append("GLAccount")

    # Invoice keywords
    if "invoice" in n:
        if "Invoice" in entity_types:
            labels.append("Invoice")

    # Receipt keywords
    if "receipt" in n:
        if "Receipt" in entity_types:
            labels.append("Receipt")

    # Card Transaction keywords
    if any(x in n for x in ["credit card", "card transaction", "debit card",
                           "cardtransaction", "card payment"]):
        if "CardTransaction" in entity_types:
            labels.append("CardTransaction")

    # Project keywords
    if any(x in n for x in ["project", "initiative", "program"]):
        if "Project" in entity_types:
            labels.append("Project")

    # Skill keywords
    if any(x in n for x in ["skill", "competency", "expertise", "capability"]):
        if "Skill" in entity_types:
            labels.append("Skill")

    # Organization keywords
    if any(x in n for x in ["organization", "organisation", "company", "enterprise",
                           "corporation", "firm"]):
        if "Organization" in entity_types:
            labels.append("Organization")

    # Product keywords
    if any(x in n for x in ["product", "solution", "platform", "tool", "system"]):
        if "Product" in entity_types:
            labels.append("Product")

    # Architecture Pattern keywords
    if any(x in n for x in ["architecture", "pattern", "design pattern", "framework"]):
        if "ArchitecturePattern" in entity_types:
            labels.append("ArchitecturePattern")

    return labels if labels else ["Unknown"]


def generate_diverse_entity_names(cfg: DomainConfig, n: int) -> List[str]:
    """Generate a diverse list of entity-like names for classification tasks.

    This helper creates pseudo entity names by combining regions, entity types,
    roles and simple numeric identifiers. It ensures that a reasonable variety
    of names are produced to avoid overfitting on a small static set. If
    ``cfg`` provides specific ``entity_types`` they will be used; otherwise a
    fallback set of generic financial domain entities is applied. The number of
    names returned will be at least ``n``; if the Cartesian product of the
    components yields more than needed, the list will be truncated.

    Parameters
    ----------
    cfg: DomainConfig
        The domain configuration used to derive region and role names.
    n: int
        The minimum number of unique names to generate.

    Returns
    -------
    list of str
        A list of unique entity names suitable for training examples.
    """
    regions = cfg.primary_regions or ["Global"]
    roles = cfg.primary_roles or ["User"]
    # Use provided entity types if available; otherwise fallback
    base_entities = cfg.entity_types or [
        "Expense Report", "Expense Policy", "Workflow", "Voucher", "Card Transaction",
        "Invoice", "Receipt", "Vendor", "GL Account"
    ]
    names: List[str] = []
    counter = 1
    # Cartesian combination of regions, base entities and roles
    for region in regions:
        for ent in base_entities:
            for role in roles:
                # e.g. "India Expense Policy for Finance Controller 001"
                name = f"{region} {ent} for {role} {counter:03d}"
                names.append(name)
                counter += 1
                if len(names) >= n:
                    return names
    # If still not enough, append numeric suffixes
    while len(names) < n:
        name = f"{regions[0]} {base_entities[0]} {counter:03d}"
        names.append(name)
        counter += 1
    return names
   