# dataset_generator/sections/intro.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from src.utils import make_metadata


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

        # Provide varied templates for greetings, capabilities and limitations to reduce
        # repetition. Each template uses named placeholders which are filled from
        # ``cfg`` during iteration.
        greeting_templates = [
            "Hi! I'm {agent}, your {domain} assistant.",
            "Hello! I can help you navigate {company}'s {domain} data.",
            "Hey there! I'm {agent}. How can I assist with {domain} today?",
            "Greetings! {agent} here to support your {domain} queries.",
            "Hi! Need help with {domain}? I'm {agent}, ask away!",
        ]

        capability_templates = [
            "As {agent}, I can read indexed documents, resolve entities, and answer "
            "grounded questions about {domain} for {company}. I route queries through vector "
            "search and knowledge graphs when needed.",
            "{agent} is capable of exploring the {domain} knowledge base, doing vector and "
            "graph retrieval to answer your queries with accuracy.",
            "In my role as {agent} for {company}, I ingest and index {domain} documents and "
            "provide grounded answers via hybrid retrieval strategies.",
            "As a {domain} assistant at {company}, I'm designed to fetch information from "
            "indexed sources and structured graphs to give you the best possible answer.",
        ]

        limitation_templates = [
            "I work only with indexed {domain} data for {company}. If something is outside this "
            "scope or missing from the index, I will say I don't know instead of guessing.",
            "My knowledge is limited to the indexed {domain} documents within {company}'s systems. "
            "When context is missing, I prefer to be honest and say I don't know.",
            "Currently, I rely solely on {domain} data that has been indexed by {company}. "
            "I can't answer questions outside the index and will admit when I'm unsure.",
            "At this time I only have access to {company}'s indexed {domain} data. If I lack "
            "context, I'll transparently say I don't know rather than speculate.",
        ]

        # Generate greetings
        for idx in range(n // 3):
            template = greeting_templates[idx % len(greeting_templates)]
            output = template.format(agent=cfg.chat_agent_name,
                                    domain=cfg.domain_name,
                                    company=cfg.company_name)
            meta = make_metadata(
                section="intro_greeting",
                index=idx + 1,
                complexity="low",
                tags=["greeting"],
                reasoning_mode="template",
                confidence=0.95,
            )
            examples.append({
                "system": f"Respond to user greetings and introduce yourself as {cfg.chat_agent_name}.",
                "instruction": f"User greets you (variant {idx + 1})",
                "input": "",
                "output": output,
                "category": "greeting",
                "intent": "user_greeting",
                "confidence": "high",
                "source": "persona",
                "notes": "",
                "metadata": meta,
            })

        # Generate capability declarations
        for idx in range(n // 3):
            template = capability_templates[idx % len(capability_templates)]
            output = template.format(agent=cfg.agent_name,
                                    domain=cfg.domain_name,
                                    company=cfg.company_name)
            meta = make_metadata(
                section="intro_capability",
                index=idx + 1,
                complexity="medium",
                tags=["capability"],
                reasoning_mode="template",
                confidence=0.95,
            )
            examples.append({
                "system": (
                    f"You are {cfg.agent_name}. Describe your capabilities clearly, factually, "
                    "and without hallucination."
                ),
                "instruction": f"Explain what you can do in {cfg.domain_name} (variant {idx + 1})",
                "input": "",
                "output": output,
                "category": "capability",
                "intent": "agent_capabilities",
                "confidence": "high",
                "source": "persona",
                "notes": "",
                "metadata": meta,
            })

        # Generate limitations until we reach n total examples
        while len(examples) < n:
            idx = len(examples) - (2 * (n // 3)) + 1  # starting index for limitations
            template = limitation_templates[idx % len(limitation_templates)]
            output = template.format(domain=cfg.domain_name, company=cfg.company_name)
            meta = make_metadata(
                section="intro_limitation",
                index=idx,
                complexity="medium",
                tags=["limitation"],
                reasoning_mode="template",
                confidence=0.95,
            )
            examples.append({
                "system": (
                    f"You are {cfg.agent_name}. Always be honest about missing context or "
                    "limitations."
                ),
                "instruction": f"Explain your limitations and when you say 'I don't know' (sample {idx})",
                "input": "",
                "output": output,
                "category": "limitation",
                "intent": "agent_limitations",
                "confidence": "high",
                "source": "persona",
                "notes": "",
                "metadata": meta,
            })

        return examples[:n]
  