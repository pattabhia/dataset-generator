# dataset_generator/sections/entity_classification.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from src.utils import make_metadata, generate_diverse_entity_names


class EntityClassificationTrainingBuilder(SectionBuilder):
    """Sections 6+12: Entity type classification."""

    @property
    def file_name(self) -> str:
        return "entity-classification-training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 100
        examples: List[Dict[str, Any]] = []

        # Generate a diverse set of entity names. This helps avoid overfitting on a
        # small static list and encourages the classifier to generalize. The
        # number of names generated matches the dataset size.
        names = generate_diverse_entity_names(cfg, n)
        instruction_templates = [
            "Classify the entity type for: {name}",
            "What type of entity is {name}?",
            "Can you tell me the category for {name}?",
            "Identify this: {name}",
            "Is {name} a vendor or something else?",
        ]

        for idx in range(1, n + 1):
            name = names[idx - 1]
            system = (
                f"You are {cfg.agent_name} classification module. "
                "Classify the given string into one or more entity types."
            )
            instr_template = instruction_templates[idx % len(instruction_templates)]
            instruction = instr_template.format(name=name)
            output = (
                f"The entity '{name}' belongs to the {cfg.domain_name} domain and should be mapped "
                "to one or more of the configured entity types."
            )
            meta = make_metadata(
                section="entity_classification",
                index=idx,
                complexity="medium",
                tags=["classification", "entity"],
                reasoning_mode="classification",
                confidence=0.9 if idx % 4 != 0 else 0.7,
                possible_labels=cfg.entity_types,
                variant_id=idx,
            )
            examples.append({
                "system": system,
                "instruction": instruction,
                "input": name,
                "output": output,
                "metadata": meta,
            })

        return examples
  