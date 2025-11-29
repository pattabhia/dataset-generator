# dataset_generator/sections/base.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.domain_config import DomainConfig


class SectionBuilder(ABC):
    """Abstract base for all dataset section builders (LSP + SRP)."""

    def __init__(self, config: DomainConfig) -> None:
        self._config = config

    @property
    def config(self) -> DomainConfig:
        return self._config

    @property
    @abstractmethod
    def file_name(self) -> str:
        """Name of the output JSON file for this section."""
        raise NotImplementedError

    @abstractmethod
    def build_examples(self) -> List[Dict[str, Any]]:
        """Return list of training examples for this section."""
        raise NotImplementedError
  