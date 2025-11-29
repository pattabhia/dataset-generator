# dataset_generator/cli.py

from __future__ import annotations

import argparse
from pathlib import Path

from src.domain_config import load_domain_config
from .factory import SectionBuilderFactory
from .generator import DatasetGenerator


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate LLaMAFactory SFT datasets from YAML config."
    )
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    parser.add_argument("--domain", required=True, help="Domain id from config.yaml")
    parser.add_argument("--out-dir", required=True, help="Output directory for JSON files")
    args = parser.parse_args()

    cfg = load_domain_config(Path(args.config), args.domain)
    factory = SectionBuilderFactory(include_expense_docs=True)
    generator = DatasetGenerator(factory)
    generator.generate_for_domain(cfg, Path(args.out_dir))


if __name__ == "__main__":
    main()
   