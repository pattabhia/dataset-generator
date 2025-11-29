# dataset_generator/sections/business_integration.py

from __future__ import annotations

import itertools
from typing import Any, Dict, List

from .base import SectionBuilder


class BusinessIntegrationTrainingBuilder(SectionBuilder):
    """Sections 4+14: Business context + integration scenarios."""

    @property
    def file_name(self) -> str:
        return "business_integration_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 100
        examples: List[Dict[str, Any]] = []

        for idx, (role, region, product) in enumerate(
            itertools.islice(
                itertools.product(cfg.primary_roles, cfg.primary_regions, cfg.primary_products),
                n
            ),
            start=1
        ):
            system = (
                f"You are {cfg.agent_name}, part of {cfg.company_name}'s intelligence-first platform. "
                "Explain how the platform fits into existing enterprise systems without inventing "
                "client-specific data."
            )
            instruction = (
                f"As a {role} in {region}, how would {product} integrate with our existing systems "
                f"if we start with a pilot in {cfg.domain_name}?"
            )
            input_ctx = (
                "Current landscape:\n"
                "- Primary systems: ERP, CRM, HR, and a legacy expense tool\n"
                "- Pain points: duplicated data, manual approvals, poor observability\n"
                f"- Target: introduce {product} as an intelligence layer for {cfg.domain_name}\n"
            )
            output = (
                f"{product} would sit as an intelligence layer on top of your existing systems, "
                "indexing documents and events, then exposing APIs and agents for workflows such as "
                "approvals, anomaly detection, and policy checks."
            )
            metadata = {
                "section": "integration_business_context",
                "scenario_type": "integration_pattern",
                "complexity": "high",
                "tags": ["integration", product, cfg.company_name, role, region],
                "reasoning_mode": "business_architecture",
                "negative_example": False,
                "operator_hint": "vector+graph",
            }
            examples.append({
                "system": system,
                "instruction": instruction,
                "input": input_ctx,
                "output": output,
                "metadata": metadata,
            })

        return examples
  