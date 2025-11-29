# dataset_generator/sections/intro.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder


class IntroTrainingBuilder(SectionBuilder):
    """
    Sections 1+2: Greetings + Agent Identity + Capability Declaration.
    """

    @property
    def file_name(self) -> str:
        return "intro-training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 100
        examples: List[Dict[str, Any]] = []

        # Greetings
        for i in range(1, n // 3 + 1):
            examples.append({
                "system": (
                    f"Respond to user greetings and introduce yourself as {cfg.chat_agent_name}."
                ),
                "instruction": f"User says hello (variant {i})",
                "input": "",
                "output": (
                    f"Hi, I’m {cfg.chat_agent_name}. I help you with {cfg.domain_name} questions "
                    f"using {cfg.company_name}'s internal knowledge and tools."
                ),
                "category": "greeting",
                "intent": "user_greeting",
                "confidence": "high",
                "source": "persona",
                "notes": ""
            })

        # Capabilities
        for i in range(1, n // 3 + 1):
            examples.append({
                "system": (
                    f"You are {cfg.agent_name}. Describe your capabilities clearly, factually, "
                    "and without hallucination."
                ),
                "instruction": f"Explain what you can do in {cfg.domain_name} (variant {i})",
                "input": "",
                "output": (
                    f"As {cfg.agent_name}, I can read indexed documents, resolve entities, and "
                    f"answer grounded questions about {cfg.domain_name} for {cfg.company_name}. "
                    "I route queries through vector search and knowledge graphs when needed."
                ),
                "category": "capability",
                "intent": "agent_capabilities",
                "confidence": "high",
                "source": "persona",
                "notes": ""
            })

        # Limitations
        while len(examples) < n:
            i = len(examples) + 1
            examples.append({
                "system": (
                    f"You are {cfg.agent_name}. Always be honest about missing context or "
                    "limitations."
                ),
                "instruction": f"Explain your limitations and when you say 'I don't know' (sample {i})",
                "input": "",
                "output": (
                    f"I work only with indexed {cfg.domain_name} data for {cfg.company_name}. "
                    "If something is outside this scope or missing from the index, "
                    "I will say I don’t know instead of guessing."
                ),
                "category": "limitation",
                "intent": "agent_limitations",
                "confidence": "high",
                "source": "persona",
                "notes": ""
            })

        return examples[:n]
  