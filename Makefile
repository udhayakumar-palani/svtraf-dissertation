.PHONY: help install run verify clean lint test all

help:
	@echo "SVTRAF Dissertation — Common Tasks"
	@echo "===================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install          Install dependencies"
	@echo "  make setup            Complete setup (install + verify)"
	@echo ""
	@echo "Execution:"
	@echo "  make run              Execute all 5 notebooks"
	@echo "  make verify           Verify outputs & data integrity"
	@echo ""
	@echo "Development:"
	@echo "  make lint             Run linters (if available)"
	@echo "  make test             Run verification tests"
	@echo "  make clean            Remove generated outputs"
	@echo ""
	@echo "Full Workflow:"
	@echo "  make all              Install → Run → Verify (complete reproducibility)"
	@echo ""

install:
	@echo "Installing dependencies from requirements.txt..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

run:
	@echo "Executing all 5 notebooks (reproducible with seed=42)..."
	bash run_notebooks.sh
	@echo "✅ Notebooks executed"

verify:
	@echo "Verifying framework outputs and data integrity..."
	python3 verify_results.py --verbose
	@echo "✅ Verification complete"

lint:
	@echo "Linting notebooks (if nbqa available)..."
	-which nbqa && nbqa black --line-length=100 svtraf-dissertation/notebooks/*.ipynb || echo "ℹ nbqa not installed; skipping"

test:
	@echo "Running verification tests..."
	python3 verify_results.py

clean:
	@echo "Cleaning generated outputs..."
	rm -f svtraf-dissertation/notebooks/svtraf_scored.csv
	rm -f svtraf-dissertation/notebooks/svtraf_dataset.csv
	rm -f svtraf-dissertation/notebooks/table_validation_results.csv
	rm -rf svtraf-dissertation/FEW/data/*.csv
	rm -rf svtraf-dissertation/FEW/tables/*.csv
	find . -name ".ipynb_checkpoints" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned"

all: install run verify
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ Complete reproducibility pipeline executed!"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "Generated artifacts in:"
	@echo "  📊 FEW/data/         — Scored datasets"
	@echo "  📈 FEW/tables/       — Statistical results"
	@echo "  🖼️  FEW/figures/     — Visualizations (ready for thesis)"
	@echo ""
	@echo "Documentation:"
	@echo "  📝 README.md                    — Project overview"
	@echo "  📋 GETTING_STARTED.md           — Setup guide"
	@echo "  📚 svtraf-dissertation/docs/    — Research documentation"
	@echo ""

.DEFAULT_GOAL := help
