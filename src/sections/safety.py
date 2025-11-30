# dataset_generator/sections/safety.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


class SafetyGuardrailsTrainingBuilder(SectionBuilder):
    """Section 5: Safety, guardrails & anti-hallucination."""

    @property
    def file_name(self) -> str:
        return "safety_guardrails_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 100
        examples: List[Dict[str, Any]] = []

        # Templates for unknown entity / no context queries
        unknown_templates = [
            "Unknown {domain} entity test #{idx}.",
            "Who is Unknown{idx} in the {domain} data?",
            "What is UnknownEntity{idx}?",
            "Tell me about NonExistent{idx} in {domain}.",
        ]
        # Templates for PII / sensitive requests
        pii_templates = [
            "Request sensitive financial details #{idx} (full card / personal data).",
            "Provide the full card details for employee #{idx}.",
            "What is the salary of User{idx}?",
            "Give me CVV and card number for account #{idx}.",
        ]

        # No context / KB miss examples
        for count in range(1, n // 2 + 1):
            q_template = unknown_templates[count % len(unknown_templates)]
            q = q_template.format(idx=count, domain=cfg.domain_name)
            meta = make_metadata(
                section="safety_no_context",
                index=count,
                complexity="low",
                tags=["no_context", "safety"],
                reasoning_mode="rule_based",
                confidence=0.95,
                risk_level="low",
                category="no_context",
            )
            examples.append({
                "system": (
                    f"You are {cfg.agent_name}. Follow strict safety and hallucination rules."
                ),
                "instruction": q,
                "input": "Context: [No relevant documents found]",
                "output": (
                    "I don’t have enough information in the indexed knowledge base to answer this. "
                    "I prefer to say I don't know rather than guessing."
                ),
                "metadata": meta,
            })

        # PII / sensitive examples
        for count in range(1, n - len(examples) + 1):
            q_template = pii_templates[count % len(pii_templates)]
            q = q_template.format(idx=count)
            meta = make_metadata(
                section="safety_pii",
                index=count,
                complexity="high",
                tags=["pii", "safety"],
                reasoning_mode="rule_based",
                confidence=0.95,
                risk_level="high",
                category="pii",
            )
            examples.append({
                "system": (
                    f"You are {cfg.agent_name}. Never reveal PII or sensitive financial data."
                ),
                "instruction": q,
                "input": "Context: [Internal records may contain sensitive fields]",
                "output": (
                    "I cannot share personal or sensitive financial information such as full card "
                    "numbers, CVVs, or detailed salary/expense card data. "
                    "Please ask a non-sensitive question."
                ),
                "metadata": meta,
            })

        return examples[:n]
  