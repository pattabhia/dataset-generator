# dataset_generator/sections/entity_reasoning_depth.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


class EntityReasoningDepthTrainingBuilder(SectionBuilder):
    """
    Section 10: Entity Reasoning Depth

    Teaches the model to:
    - Take ONE entity (product, policy, person, project)
    - Explain it across multiple dimensions (timeline, responsibilities, risks, KPIs)
    - Provide deeper, layered reasoning
    """

    @property
    def file_name(self) -> str:
        return "entity_reasoning_depth_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 80
        examples: List[Dict[str, Any]] = []

        for idx in range(1, n + 1):
            product = cfg.primary_products[idx % len(cfg.primary_products)]
            system = (
                f"You are {cfg.agent_name}, specialized in deep entity reasoning. "
                "When asked about an entity, provide a structured, multi-paragraph analysis: "
                "purpose, components, lifecycle, risks, and KPI impact."
            )
            instruction = f"Explain the role of {product} in depth."

            # Provide a variation of multi-paragraph explanation every other example
            if idx % 2 == 0:
                output = (
                    f"{product} is a core component in {cfg.company_name}'s {cfg.domain_name} stack.\n\n"
                    "1. **Purpose**\n"
                    f"- Acts as the intelligence or indexing layer for {cfg.domain_name}.\n"
                    "- Normalizes data from multiple systems and exposes it consistently.\n\n"
                    "2. **Key Responsibilities**\n"
                    "- Ingest data from upstream systems.\n"
                    "- Build and maintain entity relationships.\n"
                    "- Provide consistent APIs for downstream consumers.\n\n"
                    "3. **Lifecycle**\n"
                    "- Initial configuration and schema mapping.\n"
                    "- Continuous ingestion and re-indexing.\n"
                    "- Monitoring, drift detection, and policy updates.\n\n"
                    "4. **Risks & Controls**\n"
                    "- Data quality issues → mitigated via validation and observability.\n"
                    "- Schema evolution → controlled via versioning and migration plans.\n\n"
                    "5. **KPI Impact**\n"
                    "- Reduces manual analysis effort.\n"
                    "- Improves time-to-answer for key business questions.\n"
                    "- Enables better governance and compliance reporting."
                )
            else:
                output = (
                    f"Within {cfg.company_name}'s {cfg.domain_name} stack, {product} serves as the nexus for indexing and reasoning.\n\n"
                    "**Purpose**: It consolidates disparate data sources and offers a consistent view across systems.\n\n"
                    "**Responsibilities**: Beyond ingestion, it models relationships, maintains schemas and exposes them via APIs.\n\n"
                    "**Lifecycle**: From initial setup through continuous ingestion and periodic re-indexing, it remains a live component that adapts to schema changes.\n\n"
                    "**Risks**: Poor data quality or schema drift are mitigated with robust validation and controlled versioning.\n\n"
                    "**KPI Impact**: By automating data aggregation and reasoning, it shortens analysis time, improves compliance reporting and reduces manual work."
                )

            metadata = make_metadata(
                section="entity_reasoning_depth",
                index=idx,
                complexity="high",
                tags=["entity_reasoning", "deep_explanation", "kpi"],
                reasoning_mode="multi_paragraph",
                entity=product,
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": "",
                "output": output,
                "metadata": metadata,
            })

        return examples
