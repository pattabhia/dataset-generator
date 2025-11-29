# dataset_generator/utils.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .domain_config import DomainConfig


def save_json_array(path: Path, items: List[Dict[str, Any]]) -> None:
    """Persist a list of dicts as a JSON array (LLaMAFactory-friendly)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def default_currencies(cfg: DomainConfig) -> List[str]:
    return cfg.currencies or ["USD", "INR"]


def default_expense_doc_types(cfg: DomainConfig) -> List[str]:
    return cfg.expense_doc_types or ["Invoice", "Bill", "Receipt"]
  