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
        # Increased from 80 to 120 to account for deduplication
        n = 120
        examples: List[Dict[str, Any]] = []

        narrative_prompts = [
            "Explain why {company} positions itself as a KPI-driven Enterprise AI platform.",
            "Describe how {product} helps a {role} achieve their business KPIs.",
            "Explain the end-to-end flow from KPI definition to AI system execution.",
            "Describe how {company} supports enterprise transformation in {region}.",
            "Tell a story about how {company}'s platform drives transformation for a {role} in {region} using {product}.",
            "Discuss the KPI-driven narrative of {company} with examples involving {product} and a {role} in {region}.",
            "How does {company} align {product} with measurable outcomes for a {role} in {region}?",
            "What makes {company}'s approach to {product} uniquely KPI-focused for {role}s in {region}?",
            "Outline the business value proposition of {product} from {company} for a {role} in {region}.",
            "Describe {company}'s methodology for connecting {product} capabilities to business metrics.",
            "How would a {role} in {region} measure ROI from implementing {product} with {company}?",
            "Explain {company}'s framework for translating business goals into {product} configurations.",
            "What KPI improvements should a {role} in {region} expect from {company}'s {product}?",
            "How does {company} ensure {product} delivers tangible business value for {role}s in {region}?",
            "Describe the transformation journey {company} offers to a {role} in {region} using {product}.",
            "What differentiates {company}'s KPI-first approach with {product} for {role}s in {region}?",
            "Explain how {company} measures success for {product} implementations with {role}s in {region}.",
            "How does {company} map {product} features to specific KPIs for a {role} in {region}?",
            "What business outcomes does {company} promise a {role} in {region} when deploying {product}?",
            "Describe {company}'s value creation model for {product} targeting {role}s in {region}.",
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

            # Provide variety in outputs
            output_templates = [
                (
                    f"{cfg.company_name} starts from a concrete KPI (such as reduced processing time, "
                    "better compliance, or higher approval throughput) and then composes the supporting "
                    f"AI workflow using components like {product}. For a {role} in {region}, the story is "
                    "not just about features, but about traceable impact: where the data comes from, how "
                    "decisions are made, and how the platform fits into existing systems."
                ),
                (
                    f"The KPI-driven approach at {cfg.company_name} begins with measurable goals and backtracks to the necessary AI building blocks, such as {product}. "
                    f"A {role} in {region} doesn't just want features – they need to understand the end-to-end impact, from data ingestion and decision-making to how the solution integrates with existing platforms."
                ),
                (
                    f"At {cfg.company_name}, every deployment of {product} begins with defining success metrics. "
                    f"For {role}s in {region}, this means identifying KPIs like cost reduction, faster turnaround, or improved accuracy, "
                    "then architecting the AI solution to directly address those metrics with measurable outcomes."
                ),
                (
                    f"{cfg.company_name} differentiates itself by anchoring {product} implementations to business KPIs. "
                    f"When working with a {role} in {region}, we first establish what success looks like numerically, "
                    "then design the data flows, model training, and integration points to optimize for those specific targets."
                ),
                (
                    f"The value proposition of {product} from {cfg.company_name} centers on measurable business outcomes. "
                    f"A {role} in {region} can expect to see improvements in efficiency, accuracy, and compliance, "
                    "all tied back to specific KPIs established during the initial planning phase."
                ),
                (
                    f"For {role}s in {region}, {cfg.company_name}'s methodology with {product} follows a KPI-first pattern: "
                    "define the business objective, identify the metrics that matter, design the AI architecture to optimize those metrics, "
                    "and continuously monitor performance against targets."
                ),
                (
                    f"{cfg.company_name} positions {product} as a transformation enabler for {role}s in {region}. "
                    "Rather than deploying technology for its own sake, we focus on business outcomes—faster processing, better decisions, "
                    "enhanced compliance—and configure the platform to deliver those results."
                ),
                (
                    f"When implementing {product} with {cfg.company_name}, {role}s in {region} experience a structured approach: "
                    "KPI identification, baseline measurement, solution design, iterative deployment, and continuous optimization. "
                    "Each phase is anchored to measurable business impact."
                ),
                (
                    f"The transformation journey with {cfg.company_name} and {product} for a {role} in {region} emphasizes ROI. "
                    "We start by quantifying current state performance, define target KPIs, implement the AI solution incrementally, "
                    "and track improvements against those baselines."
                ),
                (
                    f"{cfg.company_name}'s framework for {product} ensures that {role}s in {region} can connect technical capabilities "
                    "to business value. Every feature is mapped to KPIs like processing time, error rates, or compliance scores, "
                    "providing transparency into how technology drives business outcomes."
                ),
            ]
            output = output_templates[idx % len(output_templates)]

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
