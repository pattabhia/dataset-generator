# dataset_generator/sections/operator.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder


class OperatorTrainingBuilder(SectionBuilder):
    """Section 3: Operator selection (Vector DB / KG / Hybrid)."""

    @property
    def file_name(self) -> str:
        return "operator-training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 100
        examples: List[Dict[str, Any]] = []

        scenarios = [
            ("vdb_only", "VDB", ["KG"], {"vdb": 0.8, "kg": 0.1, "graph": 0.05, "web": 0.05}),
            ("kg_only", "KG", ["VDB"], {"vdb": 0.1, "kg": 0.8, "graph": 0.05, "web": 0.05}),
            ("hybrid", "VDB+KG", [], {"vdb": 0.5, "kg": 0.4, "graph": 0.1, "web": 0.0}),
        ]

        for idx in range(1, n + 1):
            scenario_key, primary, secondary, scores = scenarios[idx % len(scenarios)]
            role = cfg.primary_roles[idx % len(cfg.primary_roles)]
            product = cfg.primary_products[idx % len(cfg.primary_products)]

            instruction = f"As a {role}, summarize how {product} is used (sample {idx})."
            input_ctx = (
                "Vector DB context:\n"
                f"- Snippet: description of {product} usage in {cfg.domain_name}\n\n"
                "Knowledge Graph context:\n"
                "- Entities: [Product, Capability, Integration]\n"
            )
            output = (
                f"{product} is used as an intelligence layer for {cfg.domain_name}, based on "
                "the available context."
            )

            examples.append({
                "system": (
                    f"You are {cfg.agent_name}, an AI retrieval router. Decide whether to use "
                    "VDB, KG, both, or safe fallback."
                ),
                "instruction": instruction,
                "input": input_ctx,
                "output": output,
                "metadata": {
                    "section": "operator_decision_logic",
                    "index": idx,
                    "complexity": "medium" if scenario_key != "hybrid" else "high",
                    "scenario": scenario_key,
                    "tags": ["operator_selection", "rag_router", cfg.agent_name.lower()],
                    "reasoning_mode": "chain_of_thought",
                    "confidence": 0.8,
                    "question_wrapper": (
                        "Choose the best operators and answer grounded on context."
                    )
                },
                "operator_decision": {
                    "primary_operator": primary,
                    "secondary_operators": secondary,
                    "reasoning_steps": [
                        "Inspect vector search results for rich unstructured context.",
                        "Inspect knowledge graph entities for structured relationships.",
                        "Pick the operator (or combination) that gives the most grounded answer."
                    ],
                    "operator_scores": scores
                }
            })

        return examples
  