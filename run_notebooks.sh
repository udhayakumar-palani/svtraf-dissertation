#!/bin/bash
# SVTRAF Dissertation — Execute all 5 notebooks in sequence
# Validates reproducibility and generates outputs
# Usage: bash run_notebooks.sh

set -e  # Exit on first error

NOTEBOOK_DIR="svtraf-dissertation/notebooks"
NOTEBOOKS=(
    "Notebook_1_Framework_Definition.ipynb"
    "Notebook_2_Dataset_Preparation.ipynb"
    "Notebook_3_Scoring_Implementation.ipynb"
    "Notebook_4_Statistical_Validation.ipynb"
    "Notebook_5_Framework_Comparison.ipynb"
)

echo "=========================================="
echo "SVTRAF Dissertation — Notebook Execution"
echo "=========================================="
echo ""

# Check if notebooks exist
for nb in "${NOTEBOOKS[@]}"; do
    if [ ! -f "$NOTEBOOK_DIR/$nb" ]; then
        echo "❌ Error: $NOTEBOOK_DIR/$nb not found"
        exit 1
    fi
done

# Check if Jupyter is installed
if ! command -v jupyter &> /dev/null; then
    echo "❌ Error: Jupyter not found. Install with: pip install -r requirements.txt"
    exit 1
fi

# Execute each notebook
for i in "${!NOTEBOOKS[@]}"; do
    nb="${NOTEBOOKS[$i]}"
    num=$((i + 1))
    
    echo "[${num}/5] Running: $nb"
    echo "---"
    
    start_time=$(date +%s)
    
    # Execute notebook and save output
    jupyter nbconvert \
        --to notebook \
        --execute \
        --ExecutePreprocessor.timeout=600 \
        --output-dir="$NOTEBOOK_DIR" \
        "$NOTEBOOK_DIR/$nb" 2>&1 || {
            echo ""
            echo "❌ Notebook execution failed: $nb"
            exit 1
        }
    
    end_time=$(date +%s)
    runtime=$((end_time - start_time))
    
    echo "✅ Completed in ${runtime}s"
    echo ""
done

echo "=========================================="
echo "✅ All notebooks executed successfully!"
echo "=========================================="
echo ""
echo "📊 Generated outputs:"
echo "   - Updated notebooks with execution results"
echo "   - Check 'svtraf-dissertation/results/' for figures"
echo ""
echo "🔍 To validate results, open any notebook in Jupyter:"
echo "   jupyter notebook svtraf-dissertation/notebooks/"
echo ""
