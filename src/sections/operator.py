# dataset_generator/sections/operator.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


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
        n = cfg.operator_samples
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
            ("vdb_medium", "VDB", ["KG"], {"vdb": 0.7, "kg": 0.15, "graph": 0.1, "web": 0.05}),
            ("kg_medium", "KG", ["VDB", "Graph"], {"vdb": 0.15, "kg": 0.7, "graph": 0.1, "web": 0.05}),
            ("graph_high", "Graph", ["KG"], {"vdb": 0.1, "kg": 0.2, "graph": 0.65, "web": 0.05}),
            ("hybrid_vdb_heavy", "VDB+KG", [], {"vdb": 0.6, "kg": 0.3, "graph": 0.08, "web": 0.02}),
            ("hybrid_kg_heavy", "VDB+KG", [], {"vdb": 0.3, "kg": 0.6, "graph": 0.08, "web": 0.02}),
            ("vdb_with_web", "VDB", ["Web"], {"vdb": 0.65, "kg": 0.1, "graph": 0.05, "web": 0.2}),
            ("kg_with_web", "KG", ["Web"], {"vdb": 0.1, "kg": 0.65, "graph": 0.05, "web": 0.2}),
            ("multi_operator", "VDB+KG", ["Graph"], {"vdb": 0.35, "kg": 0.35, "graph": 0.25, "web": 0.05}),
            ("vdb_uncertain", "VDB", ["KG"], {"vdb": 0.5, "kg": 0.3, "graph": 0.15, "web": 0.05}),
            ("kg_uncertain", "KG", ["VDB"], {"vdb": 0.3, "kg": 0.5, "graph": 0.15, "web": 0.05}),
            ("graph_medium", "Graph", ["VDB", "KG"], {"vdb": 0.15, "kg": 0.2, "graph": 0.55, "web": 0.1}),
            ("balanced_all", "VDB+KG", ["Graph"], {"vdb": 0.33, "kg": 0.33, "graph": 0.27, "web": 0.07}),
            ("vdb_very_high", "VDB", [], {"vdb": 0.95, "kg": 0.02, "graph": 0.02, "web": 0.01}),
            ("kg_very_high", "KG", [], {"vdb": 0.02, "kg": 0.95, "graph": 0.02, "web": 0.01}),
            ("graph_very_high", "Graph", [], {"vdb": 0.05, "kg": 0.05, "graph": 0.85, "web": 0.05}),
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
            "From a {role} perspective, what value does {product} provide in {domain}?",
            "How would you explain {product} to a {role} working in {domain}?",
            "Detail the primary function of {product} for {role}s in {domain}.",
            "What specific {domain} capabilities does {product} enable for a {role}?",
            "As someone in the {role} role, how do you leverage {product} in {domain}?",
            "Explain to a new {role} how {product} fits into {domain} workflows.",
            "What are the key benefits of {product} for a {role} managing {domain}?",
            "Describe {product}'s integration with {domain} systems from a {role}'s viewpoint.",
            "How does {product} transform {domain} operations for a {role}?",
            "What makes {product} essential for {role}s in {domain} environments?",
            "Outline how a {role} would utilize {product} in daily {domain} tasks.",
            "From your experience as a {role}, how does {product} support {domain}?",
            "What core {domain} problems does {product} solve for a {role}?",
            "Describe the relationship between {product} and {domain} from a {role}'s angle.",
            "How would a {role} best take advantage of {product} in {domain} scenarios?",
        ]

        output_templates = [
            "{product} acts as an intelligence layer for {domain}, drawing on vector search and knowledge graphs to provide answers.",
            "According to the available context, {product} sits between unstructured data and structured knowledge to support {domain} tasks.",
            "The tool {product} integrates vector DB and KG to deliver grounded insights for {domain}.",
            "From the given context, {product} serves as a retrieval and reasoning engine for {domain}.",
            "{product} functions as a unified intelligence platform, combining vector embeddings and graph relationships to power {domain} decisions.",
            "Based on available data, {product} bridges the gap between raw information and actionable {domain} intelligence.",
            "The system {product} orchestrates multiple data sources through vector and graph technologies to enhance {domain} outcomes.",
            "{product} operates as the core reasoning layer, leveraging both unstructured search and structured knowledge for {domain}.",
            "In our {domain} context, {product} synthesizes vector-based retrieval with graph-based reasoning to deliver comprehensive answers.",
            "{product} provides an AI-powered backbone for {domain}, merging semantic search with relational knowledge.",
            "As documented, {product} enables intelligent {domain} workflows by unifying vector databases and knowledge graphs.",
            "The platform {product} empowers {domain} through hybrid retrieval mechanisms spanning both vector and graph modalities.",
            "{product} serves as the decision support infrastructure for {domain}, combining embedding-based search with entity relationships.",
            "Within {domain}, {product} acts as a smart aggregation layer that pulls from vectors and knowledge graphs simultaneously.",
            "According to our setup, {product} delivers {domain} insights by routing queries through vector stores and graph databases.",
            "{product} creates a connected intelligence ecosystem for {domain}, linking unstructured content with structured entities.",
            "The architecture of {product} supports {domain} by orchestrating parallel searches across vector and graph backends.",
            "{product} enhances {domain} capabilities through intelligent blending of semantic similarity and knowledge graph traversal.",
            "For {domain} use cases, {product} provides a robust retrieval framework backed by both vector embeddings and entity graphs.",
            "{product} transforms {domain} information access by harmonizing vector search results with graph-derived relationships.",
        ]

        for idx in range(n):
            # Use different prime multipliers for each dimension to create better distribution
            # and avoid repeating patterns that cause deduplication
            scenario_key, primary, secondary, scores = scenarios[idx % len(scenarios)]
            role = cfg.primary_roles[(idx * 7) % len(cfg.primary_roles)]
            product = cfg.primary_products[(idx * 11) % len(cfg.primary_products)]

            instr_template = instruction_templates[(idx * 3) % len(instruction_templates)]
            instruction = instr_template.format(role=role, product=product, domain=cfg.domain_name)

            # Multiple input context templates for variety
            input_ctx_templates = [
                (
                    "Vector DB context:\n"
                    f"- Snippet: description of {product} usage in {cfg.domain_name}\n\n"
                    "Knowledge Graph context:\n"
                    "- Entities: [Product, Capability, Integration]\n"
                ),
                (
                    "Available context:\n"
                    f"- VDB: Retrieved documents about {product} in {cfg.domain_name}\n"
                    "- KG: Entity relationships and product metadata\n"
                ),
                (
                    f"Context from {product}:\n"
                    "- Vector search results: Medium relevance snippets\n"
                    f"- Graph entities: [Product, Feature, {cfg.domain_name}]\n"
                ),
                (
                    "Indexed information:\n"
                    f"- Unstructured docs on {product} usage\n"
                    f"- Structured entities linking {product} to {cfg.domain_name} workflows\n"
                ),
                (
                    "Retrieval sources:\n"
                    f"- Vector DB: {product} documentation and examples\n"
                    "- Knowledge Graph: Product-capability-integration relationships\n"
                ),
                (
                    "System context:\n"
                    f"- Semantic search: Found {product} references in {cfg.domain_name} data\n"
                    "- Entity graph: Connected product nodes with capability attributes\n"
                ),
                (
                    f"Data available for {product}:\n"
                    "- Text embeddings from vector store\n"
                    f"- Relationship graph showing {cfg.domain_name} connections\n"
                ),
                (
                    "Query results:\n"
                    f"- VDB returned: Description snippets for {product}\n"
                    f"- KG returned: Entity nodes [Product, Integration, {cfg.domain_name}]\n"
                ),
                (
                    f"Combined context on {product}:\n"
                    "- Vector results with 0.75 confidence\n"
                    "- Graph paths showing capability relationships\n"
                ),
                (
                    "Retrieved data:\n"
                    f"- Embedding-based search: {product} documentation\n"
                    f"- Graph traversal: Links to {cfg.domain_name} entities\n"
                ),
            ]
            input_ctx = input_ctx_templates[(idx * 5) % len(input_ctx_templates)]

            out_template = output_templates[(idx * 13) % len(output_templates)]
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
  