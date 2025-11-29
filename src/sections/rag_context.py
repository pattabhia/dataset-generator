# dataset_generator/sections/rag_context.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder


class RagContextTrainingBuilder(SectionBuilder):
    """Sections 7+8: Multi-hop reasoning + contextual conflict resolution."""

    @property
    def file_name(self) -> str:
        return "rag_context_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 200
        examples: List[Dict[str, Any]] = []

        for idx in range(1, n + 1):
            entity = f"{cfg.domain_name} Policy {idx}"
            system = (
                f"You are {cfg.agent_name}, resolve conflicts between Vector DB and Knowledge Graph "
                "by preferring the most reliable structured data."
            )
            instruction = f"Resolve the correct version of {entity} from noisy data."
            input_ctx = (
                f"VDB: text mentions '{entity} (draft)' and '{entity} – old version'.\n"
                f"KG: canonical node = '{entity}', status='Active', version='3.0'."
            )
            output = (
                f"The canonical resolved policy is '{entity}' (version 3.0, Active). "
                "Ignore outdated or draft references."
            )
            examples.append({
                "system": system,
                "instruction": instruction,
                "input": input_ctx,
                "output": output,
                "metadata": {
                    "id": f"rag_conflict_{idx}",
                    "reasoning_mode": "hierarchical",
                    "complexity": "medium",
                    "tags": ["entity_resolution", "alias_conflict", "multi_hop"],
                    "confidence": 0.7,
                },
            })

        return examples
 