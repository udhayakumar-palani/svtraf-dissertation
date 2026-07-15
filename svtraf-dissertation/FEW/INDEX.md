# FEW Outputs — Quick Access

## 📊 Data Files (svtraf-dissertation/results/data/)

### `svtraf_scored.csv` — Main Output
150 smart contracts with final SVTRAF scores and components.

```bash
# Quick preview
head -5 svtraf-dissertation/results/data/svtraf_scored.csv

# Get statistics
python3 -c "import pandas as pd; print(pd.read_csv('svtraf-dissertation/results/data/svtraf_scored.csv')[['svtraf_score', 'financial_loss_usd']].describe())"
```

**Columns:** contract_id, category, source, ISC, ESC, AMP, INT, SVTRAF_score, financial_loss_usd

**Use for:**
- Ranking analysis
- Correlation with ground truth
- Thesis tables/appendix
- Framework validation

---

### `svtraf_dataset.csv` — Processed Dataset
150 contracts with scoring components before final aggregation.

**Use for:**
- Component analysis
- Ablation studies
- Detailed methodology validation

---

### `svtraf_dataset_raw.csv` — Raw Reference
Original 150-contract dataset (for comparison/auditing).

---

## 📈 Tables (svtraf-dissertation/results/tables/)

### `table_validation_results.csv` — Performance Metrics

Comparison: SVTRAF vs CVSS v3.1 vs BVSS vs Ahmad et al.

| Metric | SVTRAF | CVSS v3.1 | Improvement |
|--------|--------|-----------|-------------|
| NDCG@10 | 0.9988 | 0.9878 | +1.1% |
| Spearman ρ | 0.9636 | 0.7537 | +27.9% |
| MAE | 0.402 | 1.347 | 70.1% lower |

**Use for:**
- Thesis results section
- Statistical evidence
- Performance claims

---

## 📁 Folder Structure

```
results/
├── data/              ← Processed datasets
│   ├── svtraf_scored.csv
│   ├── svtraf_dataset.csv
│   └── svtraf_dataset_raw.csv
│
├── tables/            ← Statistical results
│   └── table_validation_results.csv
│
├── figures/           ← Plots & visualizations (publication-ready)
│   ├── 01_svtraf_distribution.png
│   ├── 02_scatter_svtraf_vs_loss.png
│   ├── 03_category_breakdown.png
│   ├── 04_svtraf_vs_cvss.png
│   └── 05_top10_losses.png
│
├── models/            ← Serialized objects (optional)
│   └── (empty or checkpoints)
│
├── README.md          ← Full documentation (archival in FEW/README.md)
└── INDEX.md           ← This file
```

---

## 🎯 Before Thesis Submission

**Populate figures/ with:**
```bash
# From Jupyter, run code like:
plt.figure(figsize=(12, 6))
plt.scatter(df['SVTRAF_score'], df['financial_loss_usd'])
plt.xlabel('SVTRAF Score')
plt.ylabel('Financial Loss (USD)')
plt.savefig('FEW/figures/scatter_svtraf_vs_loss.png', dpi=300, bbox_inches='tight')
```

**Export tables for LaTeX:**
```bash
python3 -c "import pandas as pd; df = pd.read_csv('FEW/tables/table_validation_results.csv'); print(df.to_latex(index=False))"
```

---

## 🔄 Regenerate All Outputs

```bash
cd /repo/root
bash run_notebooks.sh

# Then reorganize outputs:
cp svtraf-dissertation/notebooks/svtraf_scored.csv svtraf-dissertation/FEW/data/
cp svtraf-dissertation/notebooks/table_validation_results.csv svtraf-dissertation/FEW/tables/
```

---

## ✅ Verification

Check data integrity:

```bash
# Count records
wc -l FEW/data/svtraf_scored.csv  # Should be 151 (1 header + 150)

# Check for missing values
python3 << 'EOF'
import pandas as pd
df = pd.read_csv('FEW/data/svtraf_scored.csv')
print("Missing values per column:")
print(df.isnull().sum())
print(f"\nTotal records: {len(df)}")
print(f"SVTRAF score range: [{df['SVTRAF_score'].min():.2f}, {df['SVTRAF_score'].max():.2f}]")
EOF
```

---

## 📚 Documentation

- **Full Documentation:** `README.md` (this folder)
- **Framework Info:** `../../README.md`
- **Dataset Dictionary:** `../data/README.md`
- **Getting Started:** `../../GETTING_STARTED.md`
