# dataset_generator/factory.py

from __future__ import annotations

from typing import List

from .domain_config import DomainConfig
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
)


class SectionBuilderFactory:
    """
    Decides which SectionBuilder implementations to use for a given domain.
    (Dependency Inversion: high-level code depends on this abstraction.)
    """

    def __init__(self, include_expense_docs: bool = True) -> None:
        self._include_expense_docs = include_expense_docs

    def create_builders(self, cfg: DomainConfig) -> List[SectionBuilder]:
        builders: List[SectionBuilder] = [
            IntroTrainingBuilder(cfg),
            OperatorTrainingBuilder(cfg),
            RagContextTrainingBuilder(cfg),
            EntityClassificationTrainingBuilder(cfg),
            SafetyGuardrailsTrainingBuilder(cfg),
            HardNegativesTrainingBuilder(cfg),
            CompanyKBTrainingBuilder(cfg),
            CompanyKBNoHallucinationsTrainingBuilder(cfg),
            BusinessIntegrationTrainingBuilder(cfg),
        ]

        if self._include_expense_docs and (
            cfg.expense_doc_types is not None or "expense" in cfg.domain_name.lower()
        ):
            builders.append(ExpenseDocumentsTrainingBuilder(cfg))

        return builders
  