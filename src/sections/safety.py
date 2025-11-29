# dataset_generator/sections/safety.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder


class SafetyGuardrailsTrainingBuilder(SectionBuilder):
    """Section 5: Safety, guardrails & anti-hallucination."""

    @property
    def file_name(self) -> str:
        return "safety_guardrails_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 100
        examples: List[Dict[str, Any]] = []

        # No context / KB miss
        for idx in range(1, n // 2 + 1):
            q = f"Unknown {cfg.domain_name} entity test #{idx}."
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
                "metadata": {
                    "category": "no_context",
                    "risk_level": "low",
                    "reasoning_mode": "rule_based",
                    "confidence": "high",
                },
            })

        # PII / sensitive
        for idx in range(1, n - len(examples) + 1):
            q = f"Request sensitive financial details #{idx} (full card / personal data)."
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
                "metadata": {
                    "category": "pii",
                    "risk_level": "high",
                    "reasoning_mode": "rule_based",
                    "confidence": "high",
                },
            })

        return examples[:n]
 