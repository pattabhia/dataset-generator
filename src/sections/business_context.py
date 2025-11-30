# dataset_generator/sections/business_context.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


class BusinessContextReasoningBuilder(SectionBuilder):
    """
    Section 4: Business Context Reasoning

    Teaches the model to speak about:
    - Company positioning
    - KPI-driven narrative
    - Product relationships (e.g., VSMA → HAIIndexer → HAIReach)
    - Leadership / transformation language
    """

    @property
    def file_name(self) -> str:
        return "business_context_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 80
        examples: List[Dict[str, Any]] = []

        narrative_prompts = [
            "Explain why {company} positions itself as a KPI-driven Enterprise AI platform.",
            "Describe how {product} helps a {role} achieve their business KPIs.",
            "Explain the end-to-end flow from KPI definition to AI system execution.",
            "Describe how {company} supports enterprise transformation in {region}.",
            "Tell a story about how {company}'s platform drives transformation for a {role} in {region} using {product}.",
            "Discuss the KPI-driven narrative of {company} with examples involving {product} and a {role} in {region}.",
        ]

        for idx in range(1, n + 1):
            role = cfg.primary_roles[idx % len(cfg.primary_roles)]
            region = cfg.primary_regions[idx % len(cfg.primary_regions)]
            product = cfg.primary_products[idx % len(cfg.primary_products)]
            template = narrative_prompts[idx % len(narrative_prompts)]

            instruction = template.format(
                company=cfg.company_name,
                product=product,
                role=role,
                region=region,
            )

            system = (
                f"You are {cfg.agent_name}, a business-aware assistant. "
                "Explain concepts using clear business language, aligning technology with KPIs, "
                "stakeholders, transformation goals, and measurable outcomes."
            )

            # Provide variety in outputs by changing phrasing slightly
            if idx % 2 == 0:
                output = (
                    f"{cfg.company_name} starts from a concrete KPI (such as reduced processing time, "
                    "better compliance, or higher approval throughput) and then composes the supporting "
                    f"AI workflow using components like {product}. For a {role} in {region}, the story is "
                    "not just about features, but about traceable impact: where the data comes from, how "
                    "decisions are made, and how the platform fits into existing systems."
                )
            else:
                output = (
                    f"The KPI-driven approach at {cfg.company_name} begins with measurable goals and backtracks to the necessary AI building blocks, such as {product}. "
                    f"A {role} in {region} doesn’t just want features – they need to understand the end-to-end impact, from data ingestion and decision-making to how the solution integrates with existing platforms."
                )

            metadata = make_metadata(
                section="business_context",
                index=idx,
                complexity="high",
                tags=["business_context", "kpi", "transformation", "narrative"],
                reasoning_mode="business_story",
                audience=role,
                region=region,
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": "",
                "output": output,
                "metadata": metadata,
            })

        return examples
