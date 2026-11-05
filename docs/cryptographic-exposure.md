---
title: Cryptographic exposure vs. optimization
hero: assets/6-CryptographicExposure.svg
hero_alt: "Chapter 06: Cryptographic Exposure vs. Optimization. Separate near-term combinatorial optimization from Post-Quantum Cryptography migration."
---

# 06 · Cryptographic exposure vs. optimization

**Boards frequently conflate two completely separate quantum tracks: near-term combinatorial optimization and Post-Quantum Cryptography (PQC) defense.**

A well-governed enterprise separates these tracks immediately:

- **Track A — Combinatorial Optimization & Simulation (Value Creation):** Optional, ROI-driven, governed by basis-point uplift over classical baselines.
- **Track B — Cryptographic Exposure & PQC Migration (Risk Mitigation):** Mandatory compliance and security hygiene driven by **Mosca's Inequality** ($X + Y > Z$):

$$X \text{ (confidentiality shelf-life)} + Y \text{ (migration lead-time)} > Z \text{ (years until cryptanalytically relevant quantum capability)}$$

If $X + Y > Z$, encrypted traffic intercepted today (**Harvest Now, Decrypt Later**) will still be sensitive when legacy RSA/ECC keys become vulnerable.

## Quantifying Mosca exposure in code

```python
from examples.combinatorial_triage import CryptoAssetInventory

swift_archive = CryptoAssetInventory(
    system_name="cross_border_trade_finance_archive",
    public_key_primitive="RSA-2048",
    confidentiality_shelf_life_years=10,
    migration_lead_time_years=4,
    estimated_crqc_horizon_years=10,
)

ephemeral_session = CryptoAssetInventory(
    system_name="internal_Telemetry_webhook",
    public_key_primitive="ECDSA-P256",
    confidentiality_shelf_life_years=1,
    migration_lead_time_years=1,
    estimated_crqc_horizon_years=10,
)

assert swift_archive.mosca_exposure_years == 4
assert swift_archive.requires_immediate_pqc_remediation is True
assert ephemeral_session.requires_immediate_pqc_remediation is False
```

!!! example "Try with your AI coding assistant"
    Ask your assistant: *"Generate a 5-row `CryptoAssetInventory` audit table for a regional bank or maritime logistics operator, ranking systems by `mosca_exposure_years`."*

## Checkpoint

Keep your **PQC security roadmap** (owned by CISO / Infrastructure) and your **Combinatorial Optimization roadmap** (owned by Operations / Quantitative Engineering) in separate governance charters so neither stalls or confuses the other.
