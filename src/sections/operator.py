# dataset_generator/sections/operator.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from src.utils import make_metadata


def validate_operator_scores(scores: Dict[str, float], tolerance: float = 0.01) -> None:
    """Validate that operator scores sum to approximately 1.0.

    Parameters
    ----------
    scores : Dict[str, float]
        Dictionary mapping operator names to their confidence scores.
    tolerance : float, optional
        Acceptable deviation from 1.0, by default 0.01.

    Raises
    ------
    ValueError
        If the sum of scores deviates from 1.0 by more than tolerance.
    """
    total = sum(scores.values())
    if abs(total - 1.0) > tolerance:
        raise ValueError(
            f"Operator scores must sum to ~1.0 (tolerance: {tolerance}). "
            f"Got {total:.4f} from scores: {scores}"
        )


class OperatorTrainingBuilder(SectionBuilder):
    """Section 3: Operator selection (Vector DB / KG / Hybrid)."""

    @property
    def file_name(self) -> str:
        return "operator-training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 100
        examples: List[Dict[str, Any]] = []

        # A richer set of routing scenarios to provide the model with more varied
        # decision patterns. Each tuple contains a key, primary operator, list of
        # secondary operators and a score distribution. Low confidence and
        # fallback scenarios are included implicitly by advanced_operator_logic.py.
        # Note: All operator scores must sum to approximately 1.0.
        scenarios = [
            ("vdb_high", "VDB", ["KG"], {"vdb": 0.9, "kg": 0.05, "graph": 0.03, "web": 0.02}),
            ("kg_high", "KG", ["VDB"], {"vdb": 0.05, "kg": 0.9, "graph": 0.03, "web": 0.02}),
            ("graph_only", "Graph", ["VDB"], {"vdb": 0.2, "kg": 0.2, "graph": 0.5, "web": 0.1}),
            ("hybrid_balanced", "VDB+KG", [], {"vdb": 0.45, "kg": 0.45, "graph": 0.1, "web": 0.0}),
            ("low_confidence", "VDB", ["KG", "Graph"], {"vdb": 0.3, "kg": 0.3, "graph": 0.3, "web": 0.1}),
        ]

        # Validate all scenario scores sum to ~1.0
        for scenario_key, _, _, scores in scenarios:
            validate_operator_scores(scores)

        # Instruction templates to reduce repetition
        instruction_templates = [
            "As a {role}, explain the role of {product} in {domain}.",
            "What does {product} do for {role} in {domain} processes?",
            "Describe how {role}s use {product} in {domain}.",
            "Summarize how {product} is used by a {role} in {domain}.",
            "In two sentences, describe {product}'s purpose for a {role} in {domain}.",
        ]

        output_templates = [
            "{product} acts as an intelligence layer for {domain}, drawing on vector search and knowledge graphs to provide answers.",
            "According to the available context, {product} sits between unstructured data and structured knowledge to support {domain} tasks.",
            "The tool {product} integrates vector DB and KG to deliver grounded insights for {domain}.",
            "From the given context, {product} serves as a retrieval and reasoning engine for {domain}.",
        ]

        for idx in range(n):
            scenario_key, primary, secondary, scores = scenarios[idx % len(scenarios)]
            role = cfg.primary_roles[idx % len(cfg.primary_roles)]
            product = cfg.primary_products[idx % len(cfg.primary_products)]

            instr_template = instruction_templates[idx % len(instruction_templates)]
            instruction = instr_template.format(role=role, product=product, domain=cfg.domain_name)

            input_ctx = (
                "Vector DB context:\n"
                f"- Snippet: description of {product} usage in {cfg.domain_name}\n\n"
                "Knowledge Graph context:\n"
                "- Entities: [Product, Capability, Integration]\n"
            )

            out_template = output_templates[idx % len(output_templates)]
            output = out_template.format(product=product, domain=cfg.domain_name)

            # Determine complexity based on scenario
            complexity = "high" if scenario_key in {"low_confidence", "graph_only"} else "medium"

            meta = make_metadata(
                section="operator_decision_logic",
                index=idx + 1,
                complexity=complexity,
                tags=["operator_selection", "rag_router", cfg.agent_name.lower()],
                reasoning_mode="chain_of_thought",
                confidence=0.8,
                scenario=scenario_key,
                question_wrapper="Choose the best operators and answer grounded on context."
            )

            examples.append({
                "system": (
                    f"You are {cfg.agent_name}, an AI retrieval router. Decide whether to use "
                    "VDB, KG, both, or safe fallback."
                ),
                "instruction": instruction,
                "input": input_ctx,
                "output": output,
                "metadata": meta,
                "operator_decision": {
                    "primary_operator": primary,
                    "secondary_operators": secondary,
                    "reasoning_steps": [
                        "Inspect vector search results for rich unstructured context.",
                        "Inspect knowledge graph entities for structured relationships.",
                        "Pick the operator (or combination) that gives the most grounded answer."
                    ],
                    "operator_scores": scores,
                }
            })

        return examples
  