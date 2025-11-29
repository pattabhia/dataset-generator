# dataset_generator/domain_config.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml


@dataclass(frozen=True)
class DomainConfig:
    id: str
    company_name: str
    agent_name: str
    chat_agent_name: str
    domain_name: str
    kb_label: str
    primary_products: List[str]
    primary_roles: List[str]
    primary_regions: List[str]
    entity_types: List[str]
    expense_doc_types: Optional[List[str]] = None
    currencies: Optional[List[str]] = None


def load_domain_config(config_path: Path, domain_id: str) -> DomainConfig:
    """Infrastructure concern: read YAML and map to DomainConfig."""
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    domains = data.get("domains", [])
    for d in domains:
        if d.get("id") == domain_id:
            return DomainConfig(
                id=d["id"],
                company_name=d["company_name"],
                agent_name=d["agent_name"],
                chat_agent_name=d["chat_agent_name"],
                domain_name=d["domain_name"],
                kb_label=d["kb_label"],
                primary_products=d["primary_products"],
                primary_roles=d["primary_roles"],
                primary_regions=d["primary_regions"],
                entity_types=d["entity_types"],
                expense_doc_types=d.get("expense_doc_types"),
                currencies=d.get("currencies"),
            )

    raise ValueError(f"Domain id '{domain_id}' not found in {config_path}")
  