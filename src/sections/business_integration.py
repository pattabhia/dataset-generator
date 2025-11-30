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
        n = cfg.business_integration_samples
        examples: List[Dict[str, Any]] = []

        # Generate all combinations, then cycle through them to reach n samples
        base_combinations = list(itertools.product(cfg.primary_roles, cfg.primary_regions, cfg.primary_products))

        for idx in range(1, n + 1):
            # Cycle through combinations if n exceeds the number of unique combinations
            role, region, product = base_combinations[(idx - 1) % len(base_combinations)]
            # Vary system prompts for diversity
            system_templates = [
                f"You are {cfg.agent_name}, part of {cfg.company_name}'s intelligence-first platform. Explain how the platform fits into existing enterprise systems without inventing client-specific data.",
                f"You are {cfg.agent_name}, an integration specialist from {cfg.company_name}. Describe system integration approaches without making assumptions about specific client environments.",
                f"You are {cfg.agent_name}, {cfg.company_name}'s platform advisor. Outline how our solutions complement existing enterprise infrastructure.",
                f"You are {cfg.agent_name} from {cfg.company_name}. Guide users on integrating our platform with their current systems using general best practices.",
            ]
            system = system_templates[idx % len(system_templates)]

            # Vary instruction phrasing for better diversity
            instruction_templates = [
                f"As a {role} in {region}, describe how {product} would plug into our existing systems during a {cfg.domain_name} pilot.",
                f"For a pilot in {cfg.domain_name}, how do you see {product} integrating with the current stack as the {role} in {region}?",
                f"From your perspective as {role} in {region}, outline the integration pattern of {product} with ERP/CRM/HR systems for a {cfg.domain_name} initiative.",
                f"How would {product} fit into our enterprise architecture for {cfg.domain_name} if you're a {role} in {region}?",
                f"Explain the integration approach for {product} in a {cfg.domain_name} context from a {role}'s viewpoint in {region}.",
                f"As a {role} based in {region}, what's the integration strategy for {product} within our {cfg.domain_name} ecosystem?",
                f"Describe how a {role} in {region} would architect {product} integration for {cfg.domain_name}.",
                f"From the {role} perspective in {region}, how does {product} connect with existing {cfg.domain_name} infrastructure?",
            ]
            instruction = instruction_templates[idx % len(instruction_templates)]

            # Provide varied input context templates to avoid repetition
            input_variants = [
                f"Current landscape:\n- Primary systems: ERP, CRM, HR, and a legacy expense tool\n- Pain points: duplicated data, manual approvals, poor observability\n- Target: introduce {product} as an intelligence layer for {cfg.domain_name}\n",
                f"Existing stack:\n- Core platforms: ERP, CRM, HRIS, expense management\n- Challenges: data silos, manual approvals, lack of visibility\n- Goal: overlay {product} to unify and enrich the {cfg.domain_name} process\n",
                f"System inventory:\n- Enterprise apps: ERP, CRM, HRIS, document management\n- Issues: fragmented data, slow workflows, limited insights\n- Objective: deploy {product} to streamline {cfg.domain_name} operations\n",
                f"Technology landscape:\n- Core systems: Financial ERP, CRM platform, HR system\n- Gaps: poor data integration, manual processes, weak analytics\n- Goal: integrate {product} for intelligent {cfg.domain_name} automation\n",
                f"Current environment:\n- Main platforms: ERP (financial), CRM (sales), HRIS (people)\n- Pain points: disconnected systems, repetitive manual work, no unified view\n- Target: {product} as a unifying layer for {cfg.domain_name}\n",
            ]
            input_ctx = input_variants[idx % len(input_variants)]

            # Varied but consistent output pattern
            output_variants = [
                f"{product} would sit as an intelligence layer on top of your existing systems, indexing documents and events, then exposing APIs and agents for workflows such as approvals, anomaly detection, and policy checks.",
                f"By deploying {product} you overlay an indexing and reasoning layer across ERP, CRM and expense systems. It ingests documents and events, builds relationships and surfaces insights via APIs and assistants for approval, anomaly detection and policy compliance.",
                f"{product} integrates with your current ERP, CRM, and HRIS by connecting via APIs and webhooks, extracting key events and documents, then providing intelligent search, automation, and decision support for {cfg.domain_name} workflows.",
                f"The {product} platform serves as a middleware intelligence layer, consuming data from ERP, CRM, and HR systems through standard integrations, then delivering enriched insights, automated workflows, and smart agents for {cfg.domain_name} use cases.",
                f"Implementing {product} means establishing connectors to your ERP, CRM, and HRIS, ingesting relevant data streams, and exposing augmented capabilities like semantic search, process automation, and intelligent assistants tailored to {cfg.domain_name}.",
                f"{product} functions as an integration hub that pulls from existing enterprise systems (ERP, CRM, HR), indexes and enriches the data, then offers enhanced services including smart routing, predictive analytics, and conversational interfaces for {cfg.domain_name}.",
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
  