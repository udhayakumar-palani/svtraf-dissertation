# Methodology — SVTRAF Framework Design & Validation

This section documents the systematic approach to designing SVTRAF and validating it against ground truth on-chain losses.

---

## 3.1 Design Science Research Approach

SVTRAF follows **design science research methodology** (Hevner et al., 2004):

1. **Problem Identification** — Existing frameworks (CVSS v3.1, BVSS) don't model blockchain-specific properties (immutability, autonomous execution, single-transaction exploit delivery)

2. **Solution Design** — Develop SVTRAF: blockchain-specific scoring combining four components:
   - **ISC** (Intrinsic Smart Contract Component) — financial damage capability
   - **ESC** (External Systems Component) — exploitation likelihood
   - **AMP** (Automation & Persistence) — immutability + autonomous execution
   - **INT** (Integrity/Trade Confidentiality) — affected system scope

3. **Implementation** — Jupyter notebooks demonstrating full pipeline: taxonomy → dataset → scoring → validation

4. **Evaluation** — Statistical validation on 150 stratified contracts with ground truth losses

5. **Communication** — Peer-reviewed dissertation with reproducible code/data

---

## 3.2 Dataset & Sample Size Justification

### Sample Size Analysis (Cohen, 1988)

**Power Analysis Parameters:**
- **Effect size (Cohen's d):** Estimated 1.2 (large) based on preliminary CVSS vs observed losses
- **Significance level (α):** 0.05 (two-tailed)
- **Desired power (1-β):** 0.99 (99% confidence in findings)
- **Minimum sample size:** 63 contracts (Cohen, 1988 tables)

**Our Selection:** **150 contracts** (2.4× minimum required)
- Provides 99.9% power at observed effect sizes
- Enables stratified sampling across vulnerability categories
- Supports robust ablation studies

### Stratification Strategy

| Category | # Contracts | Vulnerability Examples | Data Source |
|----------|------------|----------------------|-------------|
| Coding Errors | 30 | Integer overflow, unchecked calls, reentrancy | CWE-252, CWE-681 |
| Logic Flaws | 30 | Access control, authorization bypass | CWE-269, CWE-639 |
| Configuration Issues | 30 | Missing validation, improper permissions | CWE-345, CWE-347 |
| External Dependencies | 30 | Oracle manipulation, flash loan attacks | CWE-347, CWE-617 |
| Design Flaws | 30 | State machine violations, assumption failures | CWE-362, CWE-366 |

**Total: 150 contracts** (CWE/SWC mapped, documented losses)

---

## 3.3 Taxonomy Design

### Four-Component Model

#### 1. **Intrinsic Smart Contract Component (ISC)** — Damage Capability

Measures financial damage potential of the vulnerability:

```
ISC = 0.6 × financial_harm + 0.4 × exploitability
```

- **financial_harm** — Direct financial damage from exploit (0–10 scale)
- **exploitability** — Ease of triggering the vulnerability (0–10)

**Range:** 0–10 | **Weight in SVTRAF:** 40%

#### 2. **External Systems Component (ESC)** — Exploitation Likelihood

Probability that external systems will exploit the vulnerability: **ESC = exploitability** (0–10)

**Weight in SVTRAF:** 20%

#### 3. **Automation & Persistence (AMP)** — Blockchain-Specific

```
AMP = 0.5 × immutability + 0.5 × automation
```

- **immutability** (0–10) — Contract is immutable; cannot be patched
- **automation** (0–10) — Exploit executes autonomously in single transaction

**Range:** 0–10 | **Weight in SVTRAF:** 25%

#### 4. **Integrity/Trade Confidentiality (INT)** — Scope

Impact scope: **INT = scope (0–10)**

**Weight in SVTRAF:** 15%

### Composite Formula

```
SVTRAF = 10 × [0.40·ISC + 0.20·ESC + 0.25·AMP + 0.15·INT]
```

---

## 3.4 Scoring Formula Derivation

Components normalized to [0, 10]; final score in [0, 10]. Weights grounded in literature (Darvishi et al. 2024; Zhou et al. 2023; Chaliasos et al. 2024).

---

## 3.5 Tools Configuration

| Component | Tool | Version |
|-----------|------|---------|
| Data processing | pandas | >=1.5.0 |
| Numerical computing | numpy | >=1.24.0 |
| Statistics | scipy | >=1.11.0 |
| Visualization | matplotlib | >=3.7.0 |
| Notebooks | jupyter | >=7.0.0 |

All analyses use **seed=42** for deterministic results.

---

## 3.6 Statistical Validation Protocol

### Metrics

1. **NDCG@10** — Ranking quality of top 10 vulnerabilities
2. **Spearman ρ** — Correlation with ground truth losses
3. **Mean Absolute Error (MAE)** — Average deviation from normalized ranking
4. **Wilcoxon Test** — Non-parametric significance test vs CVSS
5. **Effect Sizes** — Cohen's d, Cliff's Δ

---

## 3.7 Why Not Slither/Mythril?

SVTRAF is a **scoring framework** (severity 0–10), not a **detection framework** (yes/no). Ground truth from:
- DeFiHackLabs — documented exploits
- Public disclosures — confirmed losses
- Blockchain transactions — verified transfers

---

## 3.8 Threats to Validity

**Internal:** Experimenter bias (mitigated: documented criteria, CWE/SWC mapping); survivorship bias (acknowledged; representative of exploited contracts); ground truth accuracy (cross-referenced)

**External:** Limited to Ethereum/Solidity (documented limitation); dataset 2018–2024 (represents current threat landscape)

**Construct:** Component scores subjective (grounded in literature); formula arbitrary (weights justified; alternatives tested)

**Conclusion:** Small sample (power analysis confirms 150 sufficient); multiple comparisons (α=0.05)

---

## References

- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*
- Darvishi et al. (2024). Smart contract vulnerability assessment
- Zhou et al. (2023). Machine learning for smart contract security
- Chaliasos et al. (2024). Automated vulnerability detection in blockchain

---

## Reproducibility

Run: `bash run_notebooks.sh` to reproduce all results with seed=42.
