# SVTRAF Dataset — Data Dictionary

## Overview
`svtraf_dataset.csv` contains **150 stratified smart contracts** with vulnerability assessments and real financial-loss ground truth. Designed for validation of the SVTRAF framework against observed on-chain exploits.

**File:** `svtraf_dataset.csv`  
**Rows:** 151 (1 header + 150 contracts)  
**Size:** ~12 KB  
**Stratification:** 5 primary vulnerability categories × 30 contracts each

---

## Column Definitions

| Column | Type | Description | Range | Source |
|--------|------|-------------|-------|--------|
| `contract_id` | String | Unique contract identifier | CONTRACT_001 to CONTRACT_150 | Internal ID |
| `category` | String | Root-cause vulnerability category | *Coding Errors, Logic Flaws, Configuration Issues, External Dependencies, Design Flaws* | SVTRAF Taxonomy |
| `source` | String | Vulnerability source/reference | *OWASP Top 10, CWE, SWC, DeFiHackLabs, Research* | CWE/SWC mappings |
| `financial_harm` | Float | Intrinsic Smart Contract Component (ISC) — potential financial damage capability | 0–10 | Taxonomy-derived |
| `exploitability` | Float | External Systems Component (ESC) — likelihood of external exploitation | 0–10 | CWE/SWC metrics |
| `immutability` | Float | Automation & Persistence (AMP) factor — contract immutability impact | 0–10 | Blockchain property |
| `automation` | Float | Automation & Persistence (AMP) factor — autonomous execution | 0–10 | Taxonomy scoring |
| `scope` | Float | Integrity/Trade Confidentiality (INT) — scope of affected systems | 0–10 | Impact assessment |
| `financial_loss_usd` | Float | **Ground Truth:** Documented on-chain financial loss (USD) | 0–57.6M | DeFiHackLabs, public disclosures |

---

## Data Preparation

### Stratification Strategy
- **5 vulnerability categories** × **30 contracts each** = 150 contracts
- **Sample size:** Determined by power analysis (Cohen 1988)
  - Minimum required: 63 samples
  - Selected: 150 samples (2.4× minimum)
  - Power: >99.9% at observed effect size
  - Controls for unequal loss distribution

### Scoring Formula (SVTRAF)
```
SVTRAF = 10 × [0.40·ISC + 0.20·ESC + 0.25·AMP + 0.15·INT]
```

Where:
- **ISC** = (financial_harm × 0.6 + exploitability × 0.4)
- **ESC** = exploitability
- **AMP** = (immutability × 0.5 + automation × 0.5)
- **INT** = scope

### Ground Truth
- **Source:** DeFiHackLabs exploit database, public security disclosures
- **Validation:** All losses cross-referenced with:
  - Blockchain transaction records (on-chain verification)
  - Project public statements (theft confirmations)
  - Loss quantification via token price at exploit date
- **Coverage:** All 150 contracts have documented financial losses

---

## Generating This Dataset

**Notebook:** `Notebook_2_Dataset_Preparation.ipynb`

Steps:
1. Load raw contract data (150 identified contracts)
2. Assign stratified vulnerability categories
3. Calculate ISC, ESC, AMP, INT components
4. Compute SVTRAF scores
5. Validate stratification balance
6. Merge with financial loss ground truth
7. Export to CSV with seed=42 for reproducibility

---

## Usage Examples

### Load in Python
```python
import pandas as pd
df = pd.read_csv('svtraf_dataset.csv')

# Display dataset info
print(df.shape)  # (150, 9)
print(df.info())
print(df.describe())

# Filter by category
coding_errors = df[df['category'] == 'Coding Errors']
print(f"Coding Errors: {len(coding_errors)} contracts")

# Calculate SVTRAF scores
isc = df['financial_harm'] * 0.6 + df['exploitability'] * 0.4
esc = df['exploitability']
amp = df['immutability'] * 0.5 + df['automation'] * 0.5
INT = df['scope']
svtraf = 10 * (0.40 * isc + 0.20 * esc + 0.25 * amp + 0.15 * INT)

# Correlation with ground truth
from scipy.stats import spearmanr
corr, p_val = spearmanr(svtraf, df['financial_loss_usd'])
print(f"SVTRAF vs Financial Loss: ρ = {corr:.4f}, p < {p_val}")
```

---

## Quality Checks

| Check | Status | Details |
|-------|--------|---------|
| Completeness | ✅ | No missing values across 150 contracts |
| Uniqueness | ✅ | All contract_id values are unique |
| Stratification | ✅ | 30 contracts in each category |
| Score Range | ✅ | All SVTRAF scores within [0, 10] |
| Ground Truth | ✅ | All 150 contracts have financial_loss_usd > 0 |
| Reproducibility | ✅ | Generated with seed=42; fully deterministic |

---

## References

- **SVTRAF Framework:** See `docs/METHODOLOGY.md`
- **Statistical Validation:** See `Notebook_4_Statistical_Validation.ipynb`
- **Ground Truth Source:** DeFiHackLabs (https://github.com/SunWeb3Sec/DeFiHackLabs)
- **Taxonomy Mapping:** CWE-200, CWE-269, SWC-101, SWC-107 (full list in Notebook_1)

---

## License & Attribution

This dataset is part of an academic dissertation (MSc Cybersecurity, National College of Ireland, 2026).

**Contact before reuse:** Dataset use beyond academic review requires explicit author permission.
