# SVTRAF: Structured Vulnerability Taxonomy and Risk Assessment Framework

Master's dissertation research on blockchain smart contract vulnerability assessment.

**Author:** Udhaya Kumar Palani (Student ID: 23306891)
**Institution:** National College of Ireland — MSc Cybersecurity (MSCCYB1_A)
**Submission:** August 6, 2026

---

## Overview

Smart contract vulnerabilities differ fundamentally from traditional software defects: deployed contracts are **immutable**, exploits execute **autonomously** in single transactions, and flaws place protocol funds **directly at risk**. General-purpose frameworks such as CVSS v3.1 model none of these properties.

**SVTRAF** is a blockchain-specific scoring framework, comprising:
1. A hierarchical **taxonomy** — 4 root-cause categories, 17 vulnerabilities (mapped to CWE/SWC)
2. A **composite scoring formula** — `SVTRAF = 10 × [0.40·ISC + 0.20·ESC + 0.25·AMP + 0.15·INT]`

Validated on **150 stratified smart contracts** against real financial-loss ground truth.

## Key Results

| Metric | SVTRAF | CVSS v3.1 | Improvement |
|--------|--------|-----------|-------------|
| NDCG@10 | 0.9988 | 0.9878 | +1.1% |
| Spearman ρ | 0.9636 | 0.7537 | +27.9% |
| Mean Absolute Error | 0.402 | 1.347 | 70.1% lower |
| Wilcoxon | p < 0.001 | — | Significant |
| Cohen's d / Cliff's Δ | Large | — | Large effects |

## Repository Structure

```
├── notebooks/     5 Jupyter notebooks (run in order, each is self-contained)
├── data/          150-contract dataset (svtraf_dataset.csv)
├── results/       Generated tables and figures
└── docs/          Methodology and supporting documentation
```

## Run in Google Colab

After pushing this repository to GitHub, each notebook opens directly in Colab
(replace `USERNAME` with your GitHub username):

```
https://colab.research.google.com/github/USERNAME/svtraf-dissertation/blob/main/notebooks/Notebook_1_Framework_Definition.ipynb
https://colab.research.google.com/github/USERNAME/svtraf-dissertation/blob/main/notebooks/Notebook_2_Dataset_Preparation.ipynb
https://colab.research.google.com/github/USERNAME/svtraf-dissertation/blob/main/notebooks/Notebook_3_Scoring_Implementation.ipynb
https://colab.research.google.com/github/USERNAME/svtraf-dissertation/blob/main/notebooks/Notebook_4_Statistical_Validation.ipynb
https://colab.research.google.com/github/USERNAME/svtraf-dissertation/blob/main/notebooks/Notebook_5_Framework_Comparison.ipynb
```

All notebooks use `seed=42`; results are fully reproducible. No installation required — Colab includes every dependency.

## The Five Notebooks

| # | Notebook | Purpose | Runtime |
|---|----------|---------|---------|
| 1 | Framework Definition | Taxonomy, scoring formula, weight justification | ~2 min |
| 2 | Dataset Preparation | 150 contracts, stratification validation | ~2 min |
| 3 | Scoring Implementation | Score all contracts; CVSS baseline | ~3 min |
| 4 | Statistical Validation | NDCG, Spearman, Wilcoxon, effect sizes, ablation | ~4 min |
| 5 | Framework Comparison | SVTRAF vs CVSS vs BVSS vs Ahmad et al. | ~2 min |

## Methodology Notes

- **Why 150 contracts:** power analysis (Cohen, 1988) — 2.4× minimum sample, >99.9% power at observed effect size.
- **Why no Slither/Mythril:** SVTRAF is a *scoring* framework, not a *detection* framework. Ground truth comes from documented on-chain losses (DeFiHackLabs), not detector output.
- **Weights:** literature-grounded (Darvishi et al. 2024; Zhou et al. 2023; Chaliasos et al. 2024).

## License

Academic research. Contact the author before reuse.
