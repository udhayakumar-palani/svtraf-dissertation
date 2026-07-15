# Research Background — Smart Contract Vulnerabilities & Frameworks

## Context: Why Blockchain Vulnerabilities Differ

### Traditional Software vs Smart Contracts

| Aspect | Traditional Software | Smart Contracts |
|--------|---------------------|-----------------|
| **Deployment** | Patches available; can fix bugs | **Immutable; cannot be changed** |
| **Execution** | Runs on controlled infrastructure | Executes on decentralized network |
| **Exploit delivery** | Multi-step attacks, coordination needed | **Single transaction; autonomous** |
| **Financial impact** | Data breach, downtime | **Direct loss of funds** |
| **Threat model** | Malicious users; systems operators control | Malicious contract state; users act rationally |

**Implication:** Generic vulnerability frameworks (CVSS, OWASP) don't capture blockchain-specific properties.

---

## Existing Frameworks & Limitations

### CVSS v3.1 (Common Vulnerability Scoring System)

**Designed for:** General-purpose software, networks, firmware

**Components:**
- Attack Vector (AV) — network, adjacent, local
- Attack Complexity (AC) — low, high
- Privileges Required (PR) — none, low, high
- User Interaction (UI) — none, required
- Scope (S) — unchanged, changed
- Confidentiality/Integrity/Availability (CIA) — none, low, high

**Problem:** No component for:
- ✗ Contract immutability
- ✗ Autonomous transaction execution
- ✗ Financial damage magnitude
- ✗ Direct loss causality

**Result:** CVSS ρ = 0.7537 vs actual blockchain losses (27.9% worse than SVTRAF)

---

### BVSS (Blockchain Vulnerability Scoring System)

**Designed for:** Blockchain and cryptocurrency ecosystems

**Additions over CVSS:**
- Affected users percentage
- Economic impact layer
- Consensus mechanism impact

**Limitations:**
- Still borrows heavily from CVSS structure
- Doesn't fully separate blockchain concerns
- No empirical validation on ground truth losses
- ρ = 0.6284 on our dataset (lowest performer)

---

### Ahmad et al. (2023) — ML-Based Smart Contract Risk Assessment

**Approach:** Train ML model on historical exploits to predict severity

**Strengths:**
- Data-driven
- Learns non-linear relationships

**Limitations:**
- Black-box; hard to interpret
- Requires labeled training data
- Doesn't generalize to novel vulnerability types
- ρ = 0.6891 on our dataset

---

## Blockchain Vulnerability Landscape

### Top Categories by Financial Loss (DeFiHackLabs)

| Category | Avg Loss | Example | CWE/SWC |
|----------|----------|---------|---------|
| **Reentrancy** | $32M | TheDAO (2016) | CWE-362 |
| **Oracle Manipulation** | $28M | Euler Finance (2023) | CWE-347 |
| **Access Control** | $18M | bZx (2019) | CWE-269 |
| **Flash Loans** | $15M | Pancake Bunny (2021) | CWE-617 |
| **Integer Overflow** | $12M | Beauty Chain (2018) | CWE-190 |

### Attack Characteristics

1. **Autonomous Execution** — Attacker calls contract; exploit runs automatically
2. **Immutability** — Once deployed, contract can't be patched; vulnerability persists indefinitely
3. **Single Transaction** — Entire attack succeeds or fails in one atomic block
4. **Direct Fund Loss** — Unlike traditional software, exploit immediately transfers funds

---

## CWE/SWC Mapping

### CWE (Common Weakness Enumeration)

**Mapping SVTRAF categories to CWE IDs:**

| SVTRAF Category | CWE IDs | Examples |
|-----------------|---------|----------|
| Coding Errors | CWE-252, CWE-681, CWE-190 | Unchecked arithmetic, reentrancy |
| Logic Flaws | CWE-269, CWE-639, CWE-362 | Access control, concurrency |
| Configuration Issues | CWE-345, CWE-347, CWE-665 | Missing validation, default permissions |
| External Dependencies | CWE-617, CWE-347, CWE-943 | Oracle attacks, external calls |
| Design Flaws | CWE-362, CWE-366, CWE-697 | Race conditions, state violations |

### SWC (Smart Contract Weakness Classification)

SWC Registry maintains Solidity-specific IDs:
- **SWC-101:** Reentrancy
- **SWC-103:** Floating Pragma
- **SWC-104:** Unchecked Call Return Value
- **SWC-107:** Reentrancy (Solidity-specific variant)

---

## Related Work

### Academic Research

1. **Darvishi et al. (2024)** — "Comprehensive Smart Contract Vulnerability Assessment"
   - Proposes taxonomy of 100+ vulnerabilities
   - Validates on 500 contracts
   - Highlights immutability as key blockchain property

2. **Zhou et al. (2023)** — "Machine Learning for Smart Contract Security"
   - Tests ML models on vulnerability detection
   - Concludes human-designed frameworks more interpretable for scoring

3. **Chaliasos et al. (2024)** — "Automated Vulnerability Detection in Blockchain Systems"
   - Focuses on detection (yes/no) rather than scoring
   - Notes need for severity assessment frameworks

### Industry Standards

1. **OpenZeppelin Security Standard** — Best practices for contract auditing
2. **Trail of Bits Audit Guide** — Methodology for manual vulnerability review
3. **Certora Formal Verification** — Proof-based contract validation

---

## Why a New Framework?

### Design Gap

No existing framework combines:
1. **Blockchain-specific modeling** (immutability, autonomy)
2. **Financial damage quantification** (ISC component)
3. **Empirical validation** against ground truth losses (Spearman ρ comparison)
4. **Interpretability** (transparent formula vs black-box ML)

### SVTRAF Addresses This

- ✅ Explicit modeling of immutability + autonomous execution (AMP)
- ✅ Financial harm as primary component (ISC weights 40%)
- ✅ Validated on 150 contracts with documented losses
- ✅ Transparent scoring formula (interpretable, auditable)
- ✅ 27.9% better correlation than CVSS on blockchain data

---

## Data Sources

### DeFiHackLabs

**GitHub:** https://github.com/SunWeb3Sec/DeFiHackLabs

**Coverage:** >200 documented DeFi exploits with:
- Transaction hashes
- Loss amounts (USD)
- Exploit code
- Root cause analysis

**Used for:** Ground truth validation (150 contracts selected from this database)

### Public Disclosures

- Protocol official statements
- Security company reports (Chainalysis, CertiK, Trail of Bits)
- Blockchain transaction records (Etherscan)
- Token price feeds (CoinGecko, CoinMarketCap)

### Ground Truth Quantification

**Process:**
1. Identify smart contract involved in exploit
2. Extract transaction from blockchain
3. Determine token transferred + amount
4. Lookup token price at exploit date
5. Calculate USD loss = amount × price

**Example:** Euler Finance Oracle Attack (2023)
- Token transferred: ~$196M in various tokens
- Blockchain: Ethereum mainnet
- USD loss: ~$196M
- SVTRAF score: 9.6 (high financial impact, high exploitability)

---

## Assumptions & Constraints

### Scope

- **EVM-compatible chains:** Ethereum, Polygon, Avalanche (framework generalizable)
- **Smart contract layer:** Protocol-level vulnerabilities out of scope
- **Documented exploits:** Covers contracts where losses were publicly disclosed
- **2018–2024:** Dataset represents 6-year threat landscape

### Limitations

1. **Survivorship bias** — Only exploited contracts included; undetected vulnerabilities not captured
2. **Ethereum-centric** — Solidity syntax; may not apply to other languages
3. **Historical data** — Threat landscape evolves; today's rankings may differ
4. **Stratification** — Equal category distribution doesn't reflect real-world proportions

---

## Future Work

1. **Extend to other blockchains** — StarkNet (Cairo), Near Protocol, Cosmos
2. **Predictive validation** — Test SVTRAF on newly disclosed exploits
3. **ML integration** — Combine SVTRAF formula with anomaly detection
4. **Dynamic scoring** — Adjust weights as threat landscape evolves
5. **Formal verification integration** — Combine with Coq/Isabelle proofs

---

## References

- **DeFiHackLabs:** https://github.com/SunWeb3Sec/DeFiHackLabs
- **CVSS v3.1 Spec:** https://www.first.org/cvss/v3.1/specification-document
- **Ethereum Yellow Paper:** Buterin, V. (2014)
- **Smart Contract Weaknesses:** https://swcregistry.io/

---

## Related Documentation

- **METHODOLOGY.md** — Framework design details
- **RESULTS.md** — Validation results & metrics
- **README.md** — Project overview
