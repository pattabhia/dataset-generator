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
        builders: List[SectionBuilder] = [
            IntroTrainingBuilder(cfg),                         # 1 + 2
            OperatorTrainingBuilder(cfg),                      # 3
            BusinessContextReasoningBuilder(cfg),              # 4
            SafetyGuardrailsTrainingBuilder(cfg),              # 5
            EntityClassificationTrainingBuilder(cfg),          # 6
            HardNegativesTrainingBuilder(cfg),                 # 6B
            RagContextTrainingBuilder(cfg),                    # 7 + 8
            ResumeIntelligenceTrainingBuilder(cfg),            # 9
            EntityReasoningDepthTrainingBuilder(cfg),          # 10
            CompanyKBTrainingBuilder(cfg),                     # 11
            CompanyKBNoHallucinationsTrainingBuilder(cfg),     # 11B
            AdvancedEntityClassificationTrainingBuilder(cfg),  # 12
            AdvancedOperatorDecisionBuilder(cfg),              # 13
            BusinessIntegrationTrainingBuilder(cfg),           # 14
        ]

        if self._include_expense_docs and (
            cfg.expense_doc_types is not None or "expense" in cfg.domain_name.lower()
        ):
            builders.append(ExpenseDocumentsTrainingBuilder(cfg))

        return builders
