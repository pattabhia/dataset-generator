# dataset_generator/sections/hard_negatives.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder


class HardNegativesTrainingBuilder(SectionBuilder):
    """Section 6B: Hard-negative classification + anti-hallucination."""

    @property
    def file_name(self) -> str:
        return "hard_negatives_hallucinations.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 28
        examples: List[Dict[str, Any]] = []

        for idx in range(1, n + 1):
            fake_name = f"Unknown{cfg.domain_name.replace(' ', '')}Entity{idx}"
            system = (
                f"You are {cfg.agent_name}, focused on HONEST entity classification. "
                "If you do not have enough information, do NOT guess."
            )
            instruction = f"Who is {fake_name}?"
            output = (
                f"I don't find any entity named '{fake_name}' in the indexed {cfg.domain_name} data. "
                "I cannot reliably answer who this is based on the available information."
            )
            examples.append({
                "system": system,
                "instruction": instruction,
                "input": "",
                "output": output,
                "entity_type": "UNKNOWN",
                "confidence": 0.05,
                "reasoning_mode": "short",
                "complexity": "L1",
                "tags": ["classification", "entity", "hard_negative", "unknown"],
                "negative_example": True,
                "multi_label": ["UNKNOWN"],
            })

        return examples
 