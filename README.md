# Quantum at Work — Enterprise Feasibility Companion

**Where Enterprises Can Actually Use Quantum Today · Evidence Before Advantage**

[![Build and publish Quantum at Work companion](https://github.com/evecount/quantum-at-work/actions/workflows/pages.yml/badge.svg)](https://github.com/evecount/quantum-at-work/actions/workflows/pages.yml)

Live companion site: **[https://evecount.github.io/quantum-at-work/](https://evecount.github.io/quantum-at-work/)**  
Practice & Cohort Portal: **[https://evecount.com/work](https://evecount.com/work)**

---

## About This Repository

This repository is the hands-on technical and executive companion for **Eve Count Quantum Systems' Open Session** and **2-Day Corporate Intensive Cohorts**, led by **Gwen Yi** and **Benjamin Lim**.

Rather than starting with hardware hype or vendor-locked SDKs, this companion walks enterprise technology leaders, operations architects, and quantitative engineers through an **inspectable, eight-stage feasibility discipline**:

1. **01 · Start with an operational bottleneck** (`operational-bottleneck.md`)
2. **02 · The classical baseline first** (`classical-baseline.md`)
3. **03 · Formulating constraints & penalties** (`formulating-constraints.md`)
4. **04 · Classical-to-quantum triage** (`hybrid-qubo-triage.md`)
5. **05 · Data, latency & SLA boundaries** (`latency-and-data-boundaries.md`)
6. **06 · Cryptographic exposure vs. optimization** (`cryptographic-exposure.md`)
7. **07 · Benchmarking without vendor hype** (`benchmarking-without-hype.md`)
8. **08 · Repeatable enterprise capability** (`enterprise-capability.md`)

## Quick Start (Zero Credentials Required)

Every code snippet in this companion uses Python's standard library so your team can inspect and test the feasibility harness immediately—without cloud billing accounts, hardware tokens, or proprietary solver licenses.

```bash
# Run the end-to-end combinatorial triage & QUBO vs. classical benchmark demo
python -m examples.combinatorial_triage

# Run the verification test suite
python -m unittest discover -s tests -v
```

## Build the Companion Site Locally

```bash
python -m pip install -r requirements.txt
python -m mkdocs serve
```

---

© 2026 [Eve Count Quantum Systems](https://evecount.com/work) · Independent Advisory · *Evidence Before Advantage*
