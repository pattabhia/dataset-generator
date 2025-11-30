# dataset_generator/sections/rag_context.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


class RagContextTrainingBuilder(SectionBuilder):
    """Sections 7+8: Multi-hop reasoning + contextual conflict resolution."""

    @property
    def file_name(self) -> str:
        return "rag_context_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = cfg.rag_context_samples
        examples: List[Dict[str, Any]] = []

        # Define varied input and output templates for conflict resolution tasks.
        input_templates = [
            "VDB: possible match score=0.{score}; KG entity variants=['{entity} v1', '{entity} (draft)', '{entity} – final?']",
            "VDB: text mentions '{entity} (draft)' and '{entity} – old version'; KG: canonical node = '{entity}', status='Active', version='3.0'.",
            "Vector DB results show references to '{entity}' in outdated contexts; KG indicates '{entity}' is current with version 3.",
            "VDB mentions multiple aliases for '{entity}', some deprecated; KG marks '{entity}' as canonical version 3.0 (Active).",
        ]
        output_templates = [
            "The canonical resolved entity is '{entity}'. Provide a cleaned, conflict-free interpretation using KG as the source of truth.",
            "According to the KG, the final policy is '{entity}' version 3.0 (Active); ignore earlier drafts.",
            "Resolve to '{entity}' based on KG; disregard any outdated or draft mentions.",
            "'{entity}' (version 3.0, Active) is the canonical policy. Ignore versions labelled draft or old.",
        ]

        for idx in range(1, n + 1):
            entity = f"{cfg.domain_name} Policy {idx}"
            system = (
                f"You are {cfg.agent_name}, resolve conflicts between Vector DB and Knowledge Graph "
                "by preferring the most reliable structured data."
            )
            instruction = f"Resolve the correct version of {entity} from noisy data."
            inp_template = input_templates[idx % len(input_templates)]
            input_ctx = inp_template.format(entity=entity, score=7 + (idx % 3))
            out_template = output_templates[idx % len(output_templates)]
            output = out_template.format(entity=entity)

            meta = make_metadata(
                section="rag_context",
                index=idx,
                complexity="medium",
                tags=["entity_resolution", "alias_conflict", "multi_hop"],
                reasoning_mode="hierarchical",
                confidence=0.7,
                id=f"rag_conflict_{idx}"
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": input_ctx,
                "output": output,
                "metadata": meta,
            })

        return examples
  