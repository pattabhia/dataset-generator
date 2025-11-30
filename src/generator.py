# dataset_generator/generator.py

from __future__ import annotations

from pathlib import Path

from .domain_config import DomainConfig
from .factory import SectionBuilderFactory
from .utils import save_json_array


class DatasetGenerator:
    """Coordinates building and writing all dataset sections for a domain."""

    def __init__(self, builder_factory: SectionBuilderFactory) -> None:
        self._builder_factory = builder_factory

    def generate_for_domain(self, cfg: DomainConfig, out_dir: Path) -> None:
        out_dir = out_dir.resolve()
        builders = self._builder_factory.create_builders(cfg)

        for builder in builders:
            examples = builder.build_examples()
            path = out_dir / builder.file_name
            save_json_array(path, examples)
            print(f"Wrote {len(examples):4d} examples -> {path}")
   