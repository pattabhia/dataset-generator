# dataset_generator/sections/hard_negatives.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata  # standardized metadata helper


class HardNegativesTrainingBuilder(SectionBuilder):
    """Section 6B: Hard-negative classification + anti-hallucination."""

    @property
    def file_name(self) -> str:
        return "hard_negatives_hallucinations.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 28
        examples: List[Dict[str, Any]] = []

        # Provide variation in question phrasing and responses to avoid overfitting
        question_templates = [
            "Who is {name}?",
            "Can you tell me who {name} is?",
            "Identify {name}.",
            "What do you know about {name}?",
        ]
        output_templates = [
            "I don't find any entity named '{name}' in the indexed {domain} data. "
            "I cannot reliably answer who this is based on the available information.",
            "There are no records for '{name}' in our {domain} data set. I prefer to say I don't know rather than guess.",
            "I couldn't locate any entity called '{name}' in the {domain} index, so I'm unable to provide details.",
        ]

        for idx in range(1, n + 1):
            fake_name = f"Unknown{cfg.domain_name.replace(' ', '')}Entity{idx}"
            system = (
                f"You are {cfg.agent_name}, focused on HONEST entity classification. "
                "If you do not have enough information, do NOT guess."
            )
            # Choose a question and response template based on index for variation
            q_template = question_templates[idx % len(question_templates)]
            o_template = output_templates[idx % len(output_templates)]
            instruction = q_template.format(name=fake_name)
            output = o_template.format(name=fake_name, domain=cfg.domain_name)

            # Build standardized metadata; mark this as a negative/hard negative example
            metadata = make_metadata(
                section="hard_negatives",
                index=idx,
                complexity="low",
                tags=["classification", "hard_negative", "unknown_entity"],
                reasoning_mode="unknown_entity",
                confidence=0.05,
                is_negative_example=True,
                entity_type="UNKNOWN",
                multi_label=["UNKNOWN"],
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": "",
                "output": output,
                "metadata": metadata,
            })

        return examples
  