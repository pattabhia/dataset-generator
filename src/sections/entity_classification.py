# dataset_generator/sections/entity_classification.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder


class EntityClassificationTrainingBuilder(SectionBuilder):
    """Sections 6+12: Entity type classification."""

    @property
    def file_name(self) -> str:
        return "entity-classification-training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 100
        examples: List[Dict[str, Any]] = []

        sample_entities = [
            "Travel Reimbursement Workflow",
            "Employee Meal Voucher",
            "Corporate Credit Card",
            "GL Account 5400 – Travel",
            "Policy Owner: Finance Controller",
            "Vendor: ACME Cabs Pvt Ltd",
            "Expense Report ER-2025-00123",
        ]

        for idx in range(1, n + 1):
            name = sample_entities[idx % len(sample_entities)]
            system = (
                f"You are {cfg.agent_name} classification module. "
                "Classify the given string into one or more entity types."
            )
            instruction = f"Classify the entity type for: {name}"
            output = (
                f"The entity '{name}' belongs to the {cfg.domain_name} domain and should be mapped "
                "to one or more of the configured entity types."
            )
            metadata = {
                "category": "entity_classification",
                "variant_id": idx,
                "confidence": "high" if idx % 4 != 0 else "medium",
                "possible_labels": cfg.entity_types,
            }
            examples.append({
                "system": system,
                "instruction": instruction,
                "input": name,
                "output": output,
                "metadata": metadata,
            })

        return examples
 