# dataset_generator/cli.py

from __future__ import annotations

import argparse
from pathlib import Path

from .domain_config import load_domain_config
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

    # Validate config file exists
    config_path = Path(args.config)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    # Validate output directory is writable
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not out_dir.is_dir():
        raise ValueError(f"Output path exists but is not a directory: {out_dir}")

    # Test write permissions
    test_file = out_dir / ".write_test"
    try:
        test_file.touch()
        test_file.unlink()
    except (OSError, PermissionError) as e:
        raise PermissionError(f"Output directory is not writable: {out_dir}") from e

    try:
        cfg = load_domain_config(config_path, args.domain)
    except ValueError as e:
        raise ValueError(f"Failed to load domain config: {e}") from e

    factory = SectionBuilderFactory(include_expense_docs=True)
    generator = DatasetGenerator(factory)
    generator.generate_for_domain(cfg, out_dir)


if __name__ == "__main__":
    main()
   