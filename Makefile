# ------------------------------
# Makefile for Dataset Generator
# ------------------------------

VENV := venv
PYTHON := python3
CLI := src.cli

DOMAIN ?= expense
OUT_DIR ?= training-jsons
CONFIG ?= config.yaml

.PHONY: help install generate generate-all shell format clean clean-venv clean-output test lint

# Default target - show help
help:
	@echo "Dataset Generator - Makefile Targets"
	@echo "====================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install          Create venv and install dependencies"
	@echo ""
	@echo "Dataset Generation:"
	@echo "  make generate         Generate dataset for DOMAIN (default: expense)"
	@echo "  make generate-all     Generate datasets for all domains in $(CONFIG)"
	@echo ""
	@echo "Development:"
	@echo "  make shell            Enter virtual environment shell"
	@echo "  make format           Format JSON files with jq"
	@echo "  make lint             Run code quality checks (black, ruff, mypy)"
	@echo "  make test             Run tests (if implemented)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean-venv       Remove virtual environment"
	@echo "  make clean-output     Remove generated JSON files"
	@echo "  make clean            Clean everything (venv + output)"
	@echo ""
	@echo "Variables:"
	@echo "  DOMAIN=$(DOMAIN)          Domain to generate (use with 'make generate')"
	@echo "  OUT_DIR=$(OUT_DIR)   Output directory for JSON files"
	@echo "  CONFIG=$(CONFIG)       Configuration file"
	@echo ""
	@echo "Examples:"
	@echo "  make generate DOMAIN=expense"
	@echo "  make generate-all"
	@echo "  make clean && make generate-all"
	@echo ""

# Create virtual environment
$(VENV)/bin/activate:
	@echo ">>> Creating virtual environment: $(VENV)"
	$(PYTHON) -m venv $(VENV)
	@echo ">>> Virtual environment created."

# Install dependencies
install: $(VENV)/bin/activate
	@echo ">>> Installing dependencies..."
	@if [ -f requirements.txt ]; then \
		$(VENV)/bin/pip install -r requirements.txt; \
	else \
		$(VENV)/bin/pip install pyyaml; \
	fi
	@echo ">>> Installation complete."

# Generate dataset for one domain
generate: install
	@echo ">>> Generating dataset for domain=$(DOMAIN)"
	$(VENV)/bin/$(PYTHON) -m $(CLI) --config $(CONFIG) --domain $(DOMAIN) --out-dir $(OUT_DIR)/$(DOMAIN)
	@echo ">>> Done: $(OUT_DIR)/$(DOMAIN)"

# Generate dataset for all domains
generate-all: install
	@echo ">>> Reading domains from $(CONFIG)..."
	@domains=$$($(VENV)/bin/$(PYTHON) -c 'import yaml, sys; data=yaml.safe_load(open("$(CONFIG)")); print(" ".join([d["id"] for d in data.get("domains", [])]))'); \
	for dom in $$domains; do \
		echo ">>> Generating datasets for $$dom"; \
		$(VENV)/bin/$(PYTHON) -m $(CLI) --config $(CONFIG) --domain $$dom --out-dir $(OUT_DIR)/$$dom; \
	done; \
	echo ">>> All domains completed."

# Drop into venv shell
shell: install
	@echo ">>> Entering virtual environment"
	@$(VENV)/bin/bash || $(VENV)/bin/zsh

# Format JSON files
format:
	@echo ">>> Formatting JSON files"
	@if command -v jq >/dev/null 2>&1; then \
		find $(OUT_DIR) -type f -name "*.json" -exec bash -c 'jq . "$$1" > "$$1.tmp" && mv "$$1.tmp" "$$1"' _ {} \; ; \
		echo ">>> Formatting complete"; \
	else \
		echo ">>> Warning: jq not found. Install with: apt-get install jq / brew install jq"; \
		exit 1; \
	fi

# Run code quality checks
lint: install
	@echo ">>> Running code quality checks..."
	@echo ">>> Running black (code formatting check)"
	-$(VENV)/bin/black --check src/
	@echo ">>> Running ruff (linting)"
	-$(VENV)/bin/ruff check src/
	@echo ">>> Running mypy (type checking)"
	-$(VENV)/bin/mypy src/
	@echo ">>> Lint checks complete"

# Run tests
test: install
	@echo ">>> Running tests..."
	@if [ -d tests ]; then \
		$(VENV)/bin/pytest tests/ -v; \
	else \
		echo ">>> No tests directory found. Create tests/ directory and add test files."; \
	fi

# Clean virtual environment
clean-venv:
	rm -rf $(VENV)

# Clean output directory
clean-output:
	rm -rf $(OUT_DIR)

# Clean everything
clean: clean-venv clean-output
	@echo ">>> Cleanup complete"
