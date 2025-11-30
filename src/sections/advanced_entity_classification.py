# dataset_generator/sections/advanced_entity_classification.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


class AdvancedEntityClassificationTrainingBuilder(SectionBuilder):
    """
    Section 12: Advanced Entity Classification

    - Multi-label classification
    - Overlapping categories (e.g., Vendor + ServiceProvider)
    - Confidence per label
    """

    @property
    def file_name(self) -> str:
        return "advanced_entity_classification_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 100
        examples: List[Dict[str, Any]] = []

        sample_entities = [
            ("ACME Cabs Pvt Ltd", ["Vendor", "ServiceProvider"]),
            ("Corporate Travel Policy 2025", ["ExpensePolicy", "Document"]),
            ("GL Account 5400 – Travel", ["GLAccount", "CostCenter"]),
            ("ACME Software FZ-LLC", ["Vendor", "TechnologyPartner"]),
            ("ACME Logistics LLC", ["Vendor", "Logistics"]),
            ("Project Phoenix 2024", ["Project", "ExpensePolicy"]),
            ("Vendor: Beta Travel Inc", ["Vendor", "ServiceProvider"]),
        ]

        possible_labels = sorted(
            {label for _, labels in sample_entities for label in labels}
        )

        for idx in range(1, n + 1):
            raw_name, labels = sample_entities[idx % len(sample_entities)]

            system = (
                f"You are {cfg.agent_name} advanced classification module. "
                "Classify the entity into one or more labels, and assign a confidence "
                "score per label. If a label does not apply, its confidence should be low."
            )
            instruction = f"Classify the entity with multi-label output: {raw_name}"

            # Assign high confidence to correct labels and low to others. The values
            # alternate slightly with the index to introduce minor variation.
            label_confidences = {
                label: (0.85 if label in labels else 0.05 + 0.01 * (idx % 5))
                for label in possible_labels
            }

            output = {
                "entity": raw_name,
                "multi_label": True,
                "predicted_labels": labels,
                "label_confidences": label_confidences,
            }

            meta = make_metadata(
                section="advanced_entity_classification",
                index=idx,
                complexity="medium",
                tags=["classification", "multi_label", "advanced"],
                reasoning_mode="classification",
                confidence=0.8,
                possible_labels=possible_labels,
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": raw_name,
                "output": output,
                "metadata": meta,
            })

        return examples
