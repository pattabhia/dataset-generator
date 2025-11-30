# dataset_generator/factory.py

from __future__ import annotations

from typing import List

from src.domain_config import DomainConfig
from .sections import (
    SectionBuilder,
    IntroTrainingBuilder,
    OperatorTrainingBuilder,
    RagContextTrainingBuilder,
    EntityClassificationTrainingBuilder,
    SafetyGuardrailsTrainingBuilder,
    HardNegativesTrainingBuilder,
    CompanyKBTrainingBuilder,
    CompanyKBNoHallucinationsTrainingBuilder,
    BusinessIntegrationTrainingBuilder,
    ExpenseDocumentsTrainingBuilder,
    BusinessContextReasoningBuilder,
    ResumeIntelligenceTrainingBuilder,
    EntityReasoningDepthTrainingBuilder,
    AdvancedEntityClassificationTrainingBuilder,
    AdvancedOperatorDecisionBuilder,
)


class SectionBuilderFactory:
    """
    Decides which SectionBuilder implementations to use for a given domain.
    """

    def __init__(self, include_expense_docs: bool = True) -> None:
        self._include_expense_docs = include_expense_docs

    def create_builders(self, cfg: DomainConfig) -> List[SectionBuilder]:
        """Assemble a list of section builders for a given domain.

        This method instantiates all of the core training section builders. Some
        builders are gated based on the domain configuration. For example,
        resume intelligence is only added for domains explicitly related to
        resumes or talent, and expense-specific sections (expense docs and
        multi-turn dialogues) are only added when the domain is about
        expense management.

        Parameters
        ----------
        cfg: DomainConfig
            The domain configuration object.

        Returns
        -------
        list of SectionBuilder
            An ordered list of instantiated section builders.
        """
        builders: List[SectionBuilder] = []

        # Always include core sections
        builders.extend([
            IntroTrainingBuilder(cfg),                        # Sections 1 + 2
            OperatorTrainingBuilder(cfg),                    # Section 3
            BusinessContextReasoningBuilder(cfg),            # Section 4
            SafetyGuardrailsTrainingBuilder(cfg),            # Section 5
            EntityClassificationTrainingBuilder(cfg),        # Section 6
            HardNegativesTrainingBuilder(cfg),               # Section 6B
            RagContextTrainingBuilder(cfg),                  # Sections 7 + 8
            EntityReasoningDepthTrainingBuilder(cfg),        # Section 10
            CompanyKBTrainingBuilder(cfg),                   # Section 11 (positive)
            CompanyKBNoHallucinationsTrainingBuilder(cfg),   # Section 11B (negative)
            AdvancedEntityClassificationTrainingBuilder(cfg),# Section 12
            AdvancedOperatorDecisionBuilder(cfg),            # Section 13
            BusinessIntegrationTrainingBuilder(cfg),         # Section 14
        ])

        # Conditionally include resume intelligence only for domains that
        # explicitly deal with resumes or talent management. We use a simple
        # heuristic: check if the domain name or ID contains keywords like
        # "resume", "cv", or "talent". This prevents unrelated domains such
        # as expense management from producing resume examples.
        resume_keywords = ["resume", "cv", "talent", "recruit", "career"]
        domain_str = f"{cfg.id} {cfg.domain_name}".lower()
        if any(kw in domain_str for kw in resume_keywords):
            builders.append(ResumeIntelligenceTrainingBuilder(cfg))

        # Add expense-specific sections when the domain covers expense management.
        # This includes both the expense document extraction and the multi‑turn
        # dialogue examples. We trigger these when a domain has expense_doc_types
        # defined or the domain name explicitly mentions "expense".
        is_expense = (
            cfg.expense_doc_types is not None or "expense" in cfg.domain_name.lower()
        )
        if self._include_expense_docs and is_expense:
            builders.append(ExpenseDocumentsTrainingBuilder(cfg))
            # Import the dialogue builder lazily to avoid circular dependencies. Note
            # that dialogue_expense lives in the sections subpackage.
            from .sections.dialogue_expense import DialogueExpenseTrainingBuilder  # type: ignore
            builders.append(DialogueExpenseTrainingBuilder(cfg))

        return builders
