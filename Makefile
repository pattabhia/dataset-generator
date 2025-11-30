# ------------------------------
# Makefile for Dataset Generator
# ------------------------------

VENV := venv
PYTHON := python3
CLI := src.cli

DOMAIN ?= expense
OUT_DIR ?= training-jsons

.PHONY: install generate generate-all shell format clean clean-venv clean-output

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
	$(VENV)/bin/$(PYTHON) -m $(CLI) --config config.yaml --domain $(DOMAIN) --out-dir $(OUT_DIR)/$(DOMAIN)
	@echo ">>> Done: $(OUT_DIR)/$(DOMAIN)"

# Generate dataset for all domains
generate-all: install
	@echo ">>> Reading domains from config.yaml..."
	@domains=$$($(VENV)/bin/$(PYTHON) -c 'import yaml, sys; data=yaml.safe_load(open("config.yaml")); print(" ".join([d["id"] for d in data.get("domains", [])]))'); \
	for dom in $$domains; do \
		echo ">>> Generating datasets for $$dom"; \
		$(VENV)/bin/$(PYTHON) -m $(CLI) --config config.yaml --domain $$dom --out-dir $(OUT_DIR)/$$dom; \
	done; \
	echo ">>> All domains completed."

# Drop into venv shell
shell: install
	@echo ">>> Entering virtual environment"
	@$(VENV)/bin/bash || $(VENV)/bin/zsh

# Format JSON files
format:
	@echo ">>> Formatting JSON files"
	@find $(OUT_DIR) -type f -name "*.json" -exec bash -c 'jq . "$$1" > "$$1.tmp" && mv "$$1.tmp" "$$1"' _ {} \;
	@echo ">>> Formatting complete"

# Clean virtual environment
clean-venv:
	rm -rf $(VENV)

# Clean output directory
clean-output:
	rm -rf $(OUT_DIR)

# Clean everything
clean: clean-venv clean-output
	@echo ">>> Cleanup complete"
