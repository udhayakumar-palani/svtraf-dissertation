# FEW — Framework Execution & Workflows

Centralized repository for all SVTRAF dissertation outputs, artifacts, and generated results. This folder organizes all framework execution outputs for easy access and thesis integration.

---

## 📁 Folder Structure

### `data/` — Processed Datasets
Generated datasets from the SVTRAF framework execution pipeline.

| File | Description | Source | Size |
|------|-------------|--------|------|
| `svtraf_scored.csv` | **All 150 contracts with computed SVTRAF scores** | Notebook 3 | 14 KB |
| `svtraf_dataset.csv` | Contracts with scoring components (ISC, ESC, AMP, INT) | Notebook 2 | 12 KB |
| `svtraf_dataset_raw.csv` | Original dataset reference (150 contracts + ground truth) | Data folder | 12 KB |

**Use case:** Validation analysis, ranking correlation studies, thesis appendices.

**Columns in svtraf_scored.csv:**
```
contract_id, category, source, ISC, ESC, AMP, INT, SVTRAF_score, financial_loss_usd
```

---

### `tables/` — Statistical Results & Validation
Summary tables from statistical validation and framework comparison.

| File | Description | Source | Metrics |
|------|-------------|--------|---------|
| `table_validation_results.csv` | SVTRAF performance vs CVSS, BVSS, Ahmad et al. | Notebook 4 | NDCG, Spearman ρ, MAE, Wilcoxon p-value |

**Use case:** Thesis results section, performance tables, statistical evidence.

---

### `figures/` — Visualizations & Plots
High-resolution figures and charts for thesis inclusion.

*Ready to populate with:*
- Vulnerability category distributions
- SVTRAF score distribution vs financial loss
- Scatter plots: SVTRAF vs CVSS
- ROC/AUC curves
- Ablation study results
- Statistical significance plots

**Export command from Jupyter:**
```python
plt.savefig('FEW/figures/figure_name.png', dpi=300, bbox_inches='tight')
plt.savefig('FEW/figures/figure_name.pdf', bbox_inches='tight')
```

---

### `models/` — Serialized Objects
Trained models and serialized framework components (optional).

*Ready for:*
- Fitted scoring models (pickle/joblib)
- Component weight matrices (numpy)
- Baseline models (CVSS, BVSS serialized)
- Validation curves

---

## 📊 Quick Data Summary

```bash
# View dataset dimensions
wc -l FEW/data/*.csv

# Check SVTRAF score distribution
python3 -c "import pandas as pd; df = pd.read_csv('FEW/data/svtraf_scored.csv'); print(df[['SVTRAF_score', 'financial_loss_usd']].describe())"

# Correlation check
python3 -c "import pandas as pd; from scipy.stats import spearmanr; df = pd.read_csv('FEW/data/svtraf_scored.csv'); r, p = spearmanr(df['SVTRAF_score'], df['financial_loss_usd']); print(f'ρ = {r:.4f}, p = {p}')"
```

---

## 🔄 Regeneration Workflow

To regenerate all outputs and refresh FEW folder:

```bash
# From repository root:
bash run_notebooks.sh

# Outputs are automatically saved to notebooks/
# Then manually organize into FEW/ with:
cp svtraf-dissertation/notebooks/svtraf_scored.csv svtraf-dissertation/FEW/data/
cp svtraf-dissertation/notebooks/svtraf_dataset.csv svtraf-dissertation/FEW/data/
cp svtraf-dissertation/notebooks/table_validation_results.csv svtraf-dissertation/FEW/tables/
```

**Expected runtime:** ~69 seconds

---

## 📝 Citation & Attribution

When referencing outputs in your dissertation:

```bibtex
@inproceedings{palani2026svtraf,
  author = {Palani, Udhaya},
  title = {SVTRAF: Structured Vulnerability Taxonomy and Risk Assessment Framework},
  school = {National College of Ireland},
  year = {2026},
  note = {Framework outputs available at svtraf-dissertation/FEW/}
}
```

**Data availability statement:**
> All framework outputs are reproducibly generated using the code in `notebooks/` with seed=42. 
> Processed results are available in `FEW/data/` and `FEW/tables/`. 
> Ground truth data sourced from DeFiHackLabs and public security disclosures.

---

## 📋 File Checklist

Before thesis submission, ensure FEW folder contains:

- [x] **data/** — All CSV datasets
  - [x] svtraf_scored.csv
  - [x] svtraf_dataset.csv
  - [x] svtraf_dataset_raw.csv
- [ ] **tables/** — Statistical results
  - [x] table_validation_results.csv
  - [ ] Additional comparison tables (if needed)
- [ ] **figures/** — Publication-ready plots (populate before submission)
  - [ ] Distribution plots
  - [ ] Correlation plots
  - [ ] Statistical validation plots
- [ ] **models/** — Serialized objects (optional)
  - [ ] Model checkpoints (if applicable)

---

## 🛠️ Python Helpers

### Load and inspect data
```python
import pandas as pd
import numpy as np
from scipy.stats import spearmanr

# Load scored contracts
df = pd.read_csv('FEW/data/svtraf_scored.csv')

# Summary statistics
print(df.groupby('category').agg({
    'SVTRAF_score': ['mean', 'std', 'min', 'max'],
    'financial_loss_usd': ['mean', 'median']
}))

# Correlation analysis
corr, p_val = spearmanr(df['SVTRAF_score'], df['financial_loss_usd'])
print(f"Spearman correlation: ρ = {corr:.4f}, p-value = {p_val:.2e}")

# Category breakdown
for cat in df['category'].unique():
    subset = df[df['category'] == cat]
    print(f"{cat}: {len(subset)} contracts, avg loss ${subset['financial_loss_usd'].mean():,.0f}")
```

### Export tables for thesis
```python
# Export validation results as formatted table
results = pd.read_csv('FEW/tables/table_validation_results.csv')
print(results.to_latex(index=False))  # For LaTeX
print(results.to_markdown(index=False))  # For Markdown
```

---

## 📚 Related Documentation

- **Framework Details:** `svtraf-dissertation/README.md`
- **Dataset Dictionary:** `svtraf-dissertation/data/README.md`
- **Methodology:** `svtraf-dissertation/docs/METHODOLOGY.md`
- **Getting Started:** `GETTING_STARTED.md`
- **Setup & Dependencies:** `requirements.txt`

---

## ⚙️ Version Info

- **SVTRAF Version:** 1.0
- **Framework Submission:** August 6, 2026
- **Dataset:** 150 stratified smart contracts
- **Reproducibility Seed:** 42
- **Last Updated:** $(date)
