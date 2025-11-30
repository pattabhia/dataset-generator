# dataset_generator/sections/advanced_operator_logic.py

from __future__ import annotations

import json
from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


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
        # Increased from 80 to 120 to account for deduplication
        n = 120
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
            {
                "key": "graph_high_risk",
                "primary": "Graph",
                "secondary": ["KG", "VDB"],
                "scores": {"vdb": 0.15, "kg": 0.25, "graph": 0.5, "web": 0.1},
                "risk_score": 0.7,
                "fallback": "WEB_SEARCH",
                "cot_suppressed": False,
            },
            {
                "key": "vdb_high_confidence",
                "primary": "VDB",
                "secondary": [],
                "scores": {"vdb": 0.85, "kg": 0.1, "graph": 0.05, "web": 0.0},
                "risk_score": 0.15,
                "fallback": None,
                "cot_suppressed": True,
            },
            {
                "key": "kg_medium_risk",
                "primary": "KG",
                "secondary": ["Graph"],
                "scores": {"vdb": 0.1, "kg": 0.65, "graph": 0.2, "web": 0.05},
                "risk_score": 0.35,
                "fallback": "Graph",
                "cot_suppressed": False,
            },
            {
                "key": "graph_medium_confidence",
                "primary": "Graph",
                "secondary": ["VDB"],
                "scores": {"vdb": 0.25, "kg": 0.15, "graph": 0.55, "web": 0.05},
                "risk_score": 0.3,
                "fallback": "VDB",
                "cot_suppressed": True,
            },
            {
                "key": "hybrid_balanced_medium_risk",
                "primary": "VDB+KG",
                "secondary": ["Graph"],
                "scores": {"vdb": 0.45, "kg": 0.4, "graph": 0.15, "web": 0.0},
                "risk_score": 0.25,
                "fallback": "Graph",
                "cot_suppressed": False,
            },
            {
                "key": "vdb_uncertain_fallback_hybrid",
                "primary": "VDB",
                "secondary": ["KG", "Graph"],
                "scores": {"vdb": 0.5, "kg": 0.3, "graph": 0.15, "web": 0.05},
                "risk_score": 0.5,
                "fallback": "VDB+KG",
                "cot_suppressed": False,
            },
            {
                "key": "kg_low_risk_no_fallback",
                "primary": "KG",
                "secondary": [],
                "scores": {"vdb": 0.05, "kg": 0.9, "graph": 0.05, "web": 0.0},
                "risk_score": 0.1,
                "fallback": None,
                "cot_suppressed": True,
            },
            {
                "key": "multi_operator_balanced",
                "primary": "VDB+KG",
                "secondary": ["Graph", "Web"],
                "scores": {"vdb": 0.35, "kg": 0.35, "graph": 0.2, "web": 0.1},
                "risk_score": 0.45,
                "fallback": "WEB_SEARCH",
                "cot_suppressed": False,
            },
            {
                "key": "graph_low_risk",
                "primary": "Graph",
                "secondary": [],
                "scores": {"vdb": 0.1, "kg": 0.1, "graph": 0.75, "web": 0.05},
                "risk_score": 0.2,
                "fallback": None,
                "cot_suppressed": True,
            },
            {
                "key": "vdb_medium_with_web_fallback",
                "primary": "VDB",
                "secondary": ["Web"],
                "scores": {"vdb": 0.6, "kg": 0.15, "graph": 0.1, "web": 0.15},
                "risk_score": 0.4,
                "fallback": "WEB_SEARCH",
                "cot_suppressed": False,
            },
            {
                "key": "hybrid_vdb_heavy_low_risk",
                "primary": "VDB+KG",
                "secondary": [],
                "scores": {"vdb": 0.65, "kg": 0.3, "graph": 0.05, "web": 0.0},
                "risk_score": 0.15,
                "fallback": None,
                "cot_suppressed": True,
            },
            {
                "key": "kg_with_graph_fallback",
                "primary": "KG",
                "secondary": ["Graph", "VDB"],
                "scores": {"vdb": 0.2, "kg": 0.55, "graph": 0.2, "web": 0.05},
                "risk_score": 0.35,
                "fallback": "Graph",
                "cot_suppressed": False,
            },
            {
                "key": "graph_uncertain_high_risk",
                "primary": "Graph",
                "secondary": ["VDB", "KG", "Web"],
                "scores": {"vdb": 0.2, "kg": 0.2, "graph": 0.45, "web": 0.15},
                "risk_score": 0.65,
                "fallback": "WEB_SEARCH",
                "cot_suppressed": False,
            },
        ]

        for idx in range(1, n + 1):
            scenario = scenarios[idx % len(scenarios)]
            product = cfg.primary_products[idx % len(cfg.primary_products)]

            system_templates = [
                (
                    f"You are {cfg.agent_name}, an advanced retrieval router. "
                    "Decide which operators (VDB, KG, Graph, Web) to use, compute scores, "
                    "risk, and fallback, and decide whether to suppress chain-of-thought "
                    "in the final user-facing answer."
                ),
                (
                    f"You are {cfg.agent_name}, a sophisticated routing engine. "
                    "Analyze available data sources (vector DB, knowledge graph, graph DB, web search), "
                    "assign confidence scores, assess risk, determine fallback strategies, "
                    "and control chain-of-thought visibility."
                ),
                (
                    f"You are {cfg.agent_name}, specialized in multi-source retrieval optimization. "
                    "Evaluate VDB, KG, Graph, and Web signals to select optimal operators, "
                    "calculate risk metrics, plan fallback paths, and manage CoT suppression."
                ),
                (
                    f"You are {cfg.agent_name}, an intelligent query router. "
                    "Process retrieval signals from multiple backends, score each operator's suitability, "
                    "quantify hallucination risk, define fallback options, and determine reasoning transparency."
                ),
            ]
            system = system_templates[idx % len(system_templates)]

            instruction_templates = [
                f"Decide routing for a complex {cfg.domain_name} question about {product}. Return operator decisions, scores, risk, fallback, and CoT suppression flag.",
                f"Analyze retrieval signals for a {cfg.domain_name} query regarding {product}. Provide operator selection, confidence scores, risk assessment, and fallback plan.",
                f"Route a {cfg.domain_name} question about {product} by selecting operators, computing scores, evaluating risk, and determining CoT suppression.",
                f"For a {product}-related {cfg.domain_name} query, choose the best operators, assign scores, calculate risk, specify fallback, and control reasoning visibility.",
                f"Process a {cfg.domain_name} question on {product}: select primary/secondary operators, score each, assess risk, define fallback, decide on CoT.",
                f"Evaluate routing options for {product} in {cfg.domain_name}: operator choice, scoring, risk quantification, fallback strategy, CoT management.",
                f"Make an operator decision for {product} in {cfg.domain_name}: determine VDB/KG/Graph/Web usage, scores, risk, fallback, and suppression.",
                f"Route {cfg.domain_name} query about {product}: pick operators, calculate confidence, measure risk, set fallback, control chain-of-thought.",
            ]
            instruction = instruction_templates[idx % len(instruction_templates)]

            input_ctx_templates = [
                (
                    "Signals:\n"
                    "- VDB: relevant snippets with medium confidence\n"
                    "- KG: strong structural relationships but partial coverage\n"
                    "- Graph: some entity paths\n"
                    "- Web: optional external reference\n"
                ),
                (
                    "Available retrieval results:\n"
                    "- Vector DB: moderate relevance, partial matches\n"
                    "- Knowledge Graph: solid entity connections, incomplete data\n"
                    "- Graph DB: limited relationship paths\n"
                    "- Web Search: supplementary information available\n"
                ),
                (
                    "Data sources:\n"
                    "- VDB: text embeddings with 0.6-0.7 similarity\n"
                    "- KG: well-defined entity relationships\n"
                    "- Graph: sparse connectivity\n"
                    "- Web: fallback option for gaps\n"
                ),
                (
                    "Retrieval context:\n"
                    "- Vector search: moderate confidence snippets\n"
                    "- Entity graph: strong schema but missing some nodes\n"
                    "- Path traversal: few relevant paths found\n"
                    "- External search: backup available\n"
                ),
                (
                    "Query signals:\n"
                    "- Semantic search: medium-quality matches\n"
                    "- Structured knowledge: good relationships, limited coverage\n"
                    "- Graph queries: partial results\n"
                    "- Web fallback: ready if needed\n"
                ),
            ]
            input_ctx = input_ctx_templates[idx % len(input_ctx_templates)]

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

            meta = make_metadata(
                section="advanced_operator_logic",
                index=idx,
                complexity="high",
                tags=["operator_selection", "advanced", "risk", "fallback"],
                reasoning_mode="router_decision",
                confidence=0.75,
                scenario=scenario["key"],
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": input_ctx,
                "output": json.dumps(operator_decision, ensure_ascii=False),
                "metadata": meta,
            })

        return examples
