# dataset_generator/sections/business_integration.py

from __future__ import annotations

import itertools
from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


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
            # System prompt remains consistent
            system = (
                f"You are {cfg.agent_name}, part of {cfg.company_name}'s intelligence-first platform. "
                "Explain how the platform fits into existing enterprise systems without inventing "
                "client-specific data."
            )
            # Vary instruction phrasing for better diversity
            if idx % 3 == 0:
                instruction = (
                    f"As a {role} in {region}, describe how {product} would plug into our existing systems "
                    f"during a {cfg.domain_name} pilot."
                )
            elif idx % 3 == 1:
                instruction = (
                    f"For a pilot in {cfg.domain_name}, how do you see {product} integrating with the current stack "
                    f"as the {role} in {region}?"
                )
            else:
                instruction = (
                    f"From your perspective as {role} in {region}, outline the integration pattern of {product} "
                    f"with ERP/CRM/HR systems for a {cfg.domain_name} initiative."
                )

            # Provide varied input context templates to avoid repetition
            input_variants = [
                (
                    "Current landscape:\n"
                    "- Primary systems: ERP, CRM, HR, and a legacy expense tool\n"
                    "- Pain points: duplicated data, manual approvals, poor observability\n"
                    f"- Target: introduce {product} as an intelligence layer for {cfg.domain_name}\n"
                ),
                (
                    "Existing stack:\n"
                    "- Core platforms: ERP, CRM, HRIS, expense management\n"
                    "- Challenges: data silos, manual approvals, lack of visibility\n"
                    f"- Goal: overlay {product} to unify and enrich the {cfg.domain_name} process\n"
                ),
            ]
            input_ctx = input_variants[idx % len(input_variants)]

            # Varied but consistent output pattern
            output_variants = [
                (
                    f"{product} would sit as an intelligence layer on top of your existing systems, "
                    "indexing documents and events, then exposing APIs and agents for workflows such as "
                    "approvals, anomaly detection, and policy checks."
                ),
                (
                    f"By deploying {product} you overlay an indexing and reasoning layer across ERP, CRM and expense systems. "
                    "It ingests documents and events, builds relationships and surfaces insights via APIs and assistants "
                    "for approval, anomaly detection and policy compliance."
                ),
            ]
            output = output_variants[idx % len(output_variants)]

            metadata = make_metadata(
                section="business_integration",
                index=idx,
                complexity="high",
                tags=["integration", product, cfg.company_name, role, region],
                reasoning_mode="business_architecture",
                operator_hint="vector+graph",
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": input_ctx,
                "output": output,
                "metadata": metadata,
            })

        return examples
  