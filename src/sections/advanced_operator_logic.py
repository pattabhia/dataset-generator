# dataset_generator/sections/advanced_operator_logic.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder


class AdvancedOperatorDecisionBuilder(SectionBuilder):
    """
    Section 13: Advanced Operator Decision Logic

    Teaches:
    - Hybrid routing with scores
    - Risk scoring
    - Fallback operators
    - CoT suppression flags
    """

    @property
    def file_name(self) -> str:
        return "advanced_operator_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 80
        examples: List[Dict[str, Any]] = []

        scenarios = [
            {
                "key": "hybrid_low_risk",
                "primary": "VDB+KG",
                "secondary": [],
                "scores": {"vdb": 0.55, "kg": 0.4, "graph": 0.05, "web": 0.0},
                "risk_score": 0.1,
                "fallback": None,
                "cot_suppressed": True,
            },
            {
                "key": "kg_high_risk_fallback_web",
                "primary": "KG",
                "secondary": ["VDB"],
                "scores": {"vdb": 0.2, "kg": 0.7, "graph": 0.1, "web": 0.3},
                "risk_score": 0.6,
                "fallback": "WEB_SEARCH",
                "cot_suppressed": False,
            },
            {
                "key": "vdb_low_confidence_fallback_kg",
                "primary": "VDB",
                "secondary": ["KG"],
                "scores": {"vdb": 0.45, "kg": 0.4, "graph": 0.15, "web": 0.0},
                "risk_score": 0.4,
                "fallback": "KG",
                "cot_suppressed": True,
            },
        ]

        for idx in range(1, n + 1):
            scenario = scenarios[idx % len(scenarios)]
            product = cfg.primary_products[idx % len(cfg.primary_products)]

            system = (
                f"You are {cfg.agent_name}, an advanced retrieval router. "
                "Decide which operators (VDB, KG, Graph, Web) to use, compute scores, "
                "risk, and fallback, and decide whether to suppress chain-of-thought "
                "in the final user-facing answer."
            )

            instruction = (
                f"Decide routing for a complex {cfg.domain_name} question about {product}. "
                "Return operator decisions, scores, risk, fallback, and CoT suppression flag."
            )

            input_ctx = (
                "Signals:\n"
                "- VDB: relevant snippets with medium confidence\n"
                "- KG: strong structural relationships but partial coverage\n"
                "- Graph: some entity paths\n"
                "- Web: optional external reference\n"
            )

            operator_decision = {
                "primary_operator": scenario["primary"],
                "secondary_operators": scenario["secondary"],
                "operator_scores": scenario["scores"],
                "risk_score": scenario["risk_score"],
                "fallback_operator": scenario["fallback"],
                "suppress_chain_of_thought": scenario["cot_suppressed"],
                "explanation": (
                    "Select operators that maximize groundedness while minimizing hallucination "
                    "risk and cost. Use fallback when risk exceeds acceptable thresholds."
                ),
            }

            metadata = {
                "section": "advanced_operator_logic",
                "index": idx,
                "complexity": "high",
                "tags": ["operator_selection", "advanced", "risk", "fallback"],
                "reasoning_mode": "router_decision",
            }

            output = operator_decision

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": input_ctx,
                "output": output,
                "metadata": metadata,
            })

        return examples
