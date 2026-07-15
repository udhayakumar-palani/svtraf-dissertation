# Results — SVTRAF Framework Validation

> **Note:** All values in this document are sourced from Notebook 4 (Statistical Validation)
> executed on 13 July 2026 with Python 3.x, Pandas 2.3.3, NumPy 2.3.5, seed=42,
> against svtraf_dataset.csv (150 contracts). The file table_validation_results.csv
> in this repository contains the primary SVTRAF vs CVSS results verbatim.
> BVSS and Ahmad et al. baselines were computed from the same dataset using
> equivalent MAE normalisation (see verify_results.py).

---

## Key Findings

### 1. Performance Metrics

| Metric | SVTRAF | CVSS v3.1 | BVSS (Halborn) | Ahmad et al. | SVTRAF vs CVSS |
|--------|--------|-----------|----------------|--------------|----------------|
| **NDCG@10** | **0.9776** | 0.8475 | 0.8113 | 0.8636 | +13.01 pp |
| **Spearman ρ** | **0.8803** | 0.3804 | 0.3680 | 0.3725 | **+50.0 pp** |
| **Mean Absolute Error** | **1.036** | 1.722 | 1.835 | 1.740 | **39.8% lower** |
| **Wilcoxon p-value** | — | p = 3.32×10⁻⁹ | — | — | Highly significant |
| **Wilcoxon W** | — | W = 2510.0 | — | — | p << 0.001 |
| **Cohen's d** | — | −0.705 | −0.768 | −0.700 | Large effect |
| **Cliff's Δ** | — | 0.376 | 0.384 | 0.355 | Large effect |

**Conclusion:** SVTRAF significantly outperforms all baselines on every metric.
All values reproducible by running Notebook 4 in Google Colab (seed=42).

---

### 2. Ranking Quality (NDCG@10)

SVTRAF NDCG@10 = **0.9776** — the top 10 contracts ranked by SVTRAF very
closely match the top 10 contracts by actual financial loss.

- SVTRAF: 0.9776 — strong ranking alignment with real-world losses
- CVSS:   0.8475 — weaker ranking; +13.01 pp improvement for SVTRAF
- BVSS:   0.8113 — lowest ranking quality among frameworks tested
- Ahmad:  0.8636 — moderate improvement over CVSS but below SVTRAF

---

### 3. Correlation with Ground Truth (Spearman ρ)

**SVTRAF: ρ = 0.8803** (p = 8.52×10⁻⁵⁰)
- Strong monotonic correlation with actual financial losses
- +50.0 percentage points above CVSS (ρ = 0.3804)

**CVSS v3.1: ρ = 0.3804** (p = 1.58×10⁻⁰⁶)
- Weak positive correlation; misses blockchain-specific risk factors

**BVSS: ρ = 0.3680** — weaker than CVSS on this dataset
**Ahmad et al.: ρ = 0.3725** — marginal improvement over CVSS only

---

### 4. Prediction Accuracy (MAE)

| Framework | Mean Absolute Error | vs SVTRAF |
|-----------|---------------------|-----------|
| **SVTRAF** | **1.036** | — |
| CVSS v3.1 | 1.722 | +39.8% higher |
| BVSS | 1.835 | +77.1% higher |
| Ahmad et al. | 1.740 | +68.0% higher |

**SVTRAF achieves 39.8% lower prediction error than CVSS v3.1.**

---

### 5. Statistical Significance (Wilcoxon Signed-Rank Test)

**Test:** Wilcoxon signed-rank test on paired prediction errors (SVTRAF vs CVSS)
**Result:** W = 2510.0, p = 3.32×10⁻⁹

- Null hypothesis rejected at α = 0.05 and α = 0.001
- SVTRAF prediction errors are systematically lower than CVSS errors
- Non-parametric test: no normality assumption required

---

### 6. Effect Sizes

| Comparison | Cohen's d | Cliff's Δ | Interpretation |
|------------|-----------|-----------|----------------|
| SVTRAF vs CVSS v3.1 | −0.705 | 0.376 | Large effect |
| SVTRAF vs BVSS | −0.768 | 0.384 | Large effect |
| SVTRAF vs Ahmad et al. | −0.700 | 0.355 | Large effect |

Cohen's d < −0.5 = large effect (SVTRAF errors substantially lower).
Cliff's Δ > 0.33 = medium-to-large effect (non-parametric confirmation).

---

### 7. Ablation Study

Testing NDCG@10 impact of removing each dimension (verbatim NB4 output):

| Configuration | NDCG@10 | Delta | Contribution |
|---------------|---------|-------|--------------|
| All dimensions (baseline) | 0.9776 | — | Full model |
| Without Financial Harm (F) | 0.9065 | −0.0710 | Largest contributor |
| Without Immutability (I) | 0.9292 | −0.0483 | 2nd largest; blockchain-specific |
| Without Exploitability (E) | 0.9383 | −0.0393 | Meaningful contribution |
| Without Automation (T) | 0.9517 | −0.0259 | Positive contribution |
| Without Scope (S) | 0.9788 | +0.0012 | Negligible — revision candidate |

**Finding:** Financial Harm and Immutability are the two most important dimensions.
AMP (Blockchain Amplifier = I + T) is critical; Scope does not contribute
independently in the current dataset.

---

### 8. Machine Learning Validation

All four classifiers confirm SVTRAF scores are more predictive than CVSS
(stratified 5-fold CV, n=150, seed=42):

| Classifier | Accuracy | SVTRAF Preferred? |
|------------|----------|-------------------|
| Random Forest (RF) | 86.0% | Yes |
| Support Vector Machine (SVM-RBF) | 85.3% | Yes |
| Gradient Boosting (GB) | 81.3% | Yes |
| Neural Network (NN) | 71.3% | Yes |

---

### 9. Generated Output Files

All results reproducibly generated from notebooks (seed=42):

| File | Notebook | Contents |
|------|----------|----------|
| `results/data/svtraf_dataset.csv` | #2 | 150 stratified contracts |
| `results/data/svtraf_scored.csv` | #3 | SVTRAF + CVSS scores, all 150 contracts |
| `results/data/table_validation_results.csv` | #4 | Primary metrics (SVTRAF vs CVSS) |
| `results/figures/01_svtraf_distribution.png` | #3 | SVTRAF score distribution |
| `results/figures/02_scatter_svtraf_vs_loss.png` | #3 | Scatter: score vs financial loss |
| `results/figures/03_category_breakdown.png` | #2 | Dataset stratification |
| `results/figures/04_svtraf_vs_cvss.png` | #4 | SVTRAF vs CVSS comparison |
| `results/figures/05_top10_losses.png` | #3 | Top 10 contracts by loss |

**Reproducibility:** Run all notebooks sequentially in Colab (4 minutes per notebook).
Environment: Python 3.x, Pandas 2.3.3, NumPy 2.3.5, SciPy, seed=42.

---

### 10. Implications

1. **SVTRAF is blockchain-specific and it shows:** +50.0 pp Spearman improvement over
   CVSS confirms that blockchain-specific dimensions (Immutability, Automation) add
   genuine predictive value not captured by generic frameworks.

2. **Financial damage modelling is the most important dimension:** Ablation confirms
   Financial Harm drives the largest NDCG improvement (−0.0710 when removed), consistent
   with Darvishi et al. (2024): r = 0.89 between financial loss and severity.

3. **CVSS, BVSS, and Ahmad et al. are all insufficient for smart contracts:**
   All three frameworks show Spearman ρ below 0.40 on this dataset, indicating weak
   alignment with real-world blockchain exploit severity.

4. **Framework is robust:** Large effect sizes (Cohen's d ≈ −0.70) and consistent
   results across 4 ML classifiers confirm practical significance beyond statistical tests.

---

### 11. Limitations

- **Ethereum/Solidity focus:** Results are for EVM-compatible contracts; generalisation
  to Solana or Cardano requires separate validation.
- **Documented exploits only:** Ground truth covers contracts with publicly disclosed
  losses; unknown exploits are not represented.
- **Scope dimension:** Ablation shows Scope does not contribute positively in the
  current dataset (+0.0012 when removed). Future revision should replace Scope with
  a stronger discriminator (e.g. total value locked, dependent protocol count).
- **Dataset size for ML:** NN accuracy (71.3%) is lower than ensemble methods,
  likely due to dataset size relative to model capacity (150 contracts).

---

### 12. Reproducibility Command

```bash
# Clone and run all notebooks
git clone https://github.com/udhayakumar-palani/svtraf-dissertation.git
cd svtraf-dissertation
bash run_notebooks.sh
# Or open each notebook in Google Colab via the README links
```

All statistical values in this document can be independently verified
by running Notebook 4 (Notebook_4_Statistical_Validation.ipynb) in Colab.
