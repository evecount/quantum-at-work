---
title: Companion home
hero: assets/0-QuantumAtWork.svg
hero_alt: "Quantum at Work — Open Session & Enterprise Cohort Companion by Eve Count Quantum Systems. Evidence Before Advantage."
---

# Quantum at Work: Where Enterprises Can Actually Use Quantum Today

<p class="workshop-eyebrow">Eve Count Quantum Systems · Gwen Yi &amp; Benjamin Lim · 10 December 2026 Open Session &amp; Enterprise Cohorts</p>

<p class="workshop-lead">Quantum readiness is an engineering and mathematical discipline, not a hardware procurement exercise. Separate coupled combinatorial bottlenecks from linear workloads, establish an honest classical baseline, and require measurable operational evidence before committing capital.</p>

[Start Chapter 01](operational-bottleneck.md){ .md-button .md-button--primary }
[Explore the 8 Chapters](#choose-your-chapter){ .md-button }
[10 Dec Open Session & Cohorts](https://evecount.com/work/events){ .md-button }

## Welcome

This technical companion turns the core methodology from **Quantum at Work** into an inspectable, hands-on engineering walkthrough. You can follow the eight chapters alongside the **10 December 2026 Open Session** or work through the exercises with your architecture and operations teams during our **2-Day Corporate Intensive**.

The running example models a **constrained enterprise allocation and scheduling bottleneck** (applicable to berth and crane scheduling, pit-to-port blending, fleet routing, and intraday liquidity allocation). A deterministic Python harness—not vendor marketing claims—decides whether a workload belongs on a classical solver, a classical metaheuristic, or a hybrid QUBO formulation. No paid quantum cloud account, API key, or proprietary SDK is required to run the exercises.

## Get ready

Use **Python 3.10+** and any modern code editor (VS Code, Cursor, or Google Antigravity) to run the exercises.

To run the companion harness locally, clone the [quantum-at-work repository](https://github.com/evecount/quantum-at-work) and execute:

```bash
python -m examples.combinatorial_triage
```

Every chapter includes a runnable Python verification snippet, an AI-assisted architecture prompt, and an **observable governance checkpoint**.

!!! tip "Designed for two speeds"
    **Executive & Architecture Track (25–45 mins):** Follow the architectural plates, decision boundaries, and governance checkpoints across the eight chapters.  
    **Hands-on Engineering Track (60–90 mins):** Run the Python snippets, inspect [`examples/combinatorial_triage.py`](https://github.com/evecount/quantum-at-work/blob/main/examples/combinatorial_triage.py), and test the penalty calibration and SLA gate boundaries on your own operational constraints.

## The Evidence-Before-Advantage Loop

**Specify → Baseline → Formulate → Triage → Benchmark → Govern.**

Quantum and hybrid solvers can unlock measurable basis-point improvements on tightly coupled discrete problems, but enterprise owners remain accountable for data hygiene, SLA latency envelopes, and classical parity benchmarks. A vendor demo without a tuned classical baseline is never sufficient evidence for production deployment.

## Choose your chapter

<div class="workshop-grid">
  <a class="workshop-card" href="operational-bottleneck/">
    <img src="assets/1-OperationalBottleneck.svg" alt="" width="916" height="516" loading="lazy">
    <strong>01 · Start with an operational bottleneck</strong>
    <span>Separate coupled combinatorial constraints from linear workloads before touching a solver.</span>
  </a>
  <a class="workshop-card" href="classical-baseline/">
    <img src="assets/2-ClassicalBaseline.svg" alt="" width="916" height="516" loading="lazy">
    <strong>02 · The classical baseline first</strong>
    <span>Bound greedy, MIP, and metaheuristic performance before claiming quantum uplift.</span>
  </a>
  <a class="workshop-card" href="formulating-constraints/">
    <img src="assets/3-FormulatingConstraints.svg" alt="" width="916" height="516" loading="lazy">
    <strong>03 · Formulating constraints &amp; penalties</strong>
    <span>Translate operational rules into inspectable QUBO matrices and calibrated penalty weights.</span>
  </a>
  <a class="workshop-card" href="hybrid-qubo-triage/">
    <img src="assets/4-HybridQuboTriage.svg" alt="" width="916" height="516" loading="lazy">
    <strong>04 · Classical-to-quantum triage</strong>
    <span>Route sub-problems dynamically between deterministic classical heuristics and hybrid solvers.</span>
  </a>
  <a class="workshop-card" href="latency-and-data-boundaries/">
    <img src="assets/5-LatencyAndData.svg" alt="" width="916" height="516" loading="lazy">
    <strong>05 · Data, latency &amp; SLA boundaries</strong>
    <span>Why real-time SLA timers and incomplete ERP telemetry invalidate naive PoCs.</span>
  </a>
  <a class="workshop-card" href="cryptographic-exposure/">
    <img src="assets/6-CryptographicExposure.svg" alt="" width="916" height="516" loading="lazy">
    <strong>06 · Cryptographic exposure vs. optimization</strong>
    <span>Separate near-term combinatorial optimization value from Post-Quantum Cryptography (PQC) timelines.</span>
  </a>
  <a class="workshop-card" href="benchmarking-without-hype/">
    <img src="assets/7-BenchmarkingWithoutHype.svg" alt="" width="916" height="516" loading="lazy">
    <strong>07 · Benchmarking without vendor hype</strong>
    <span>Evaluate solver families across scaling behaviour, feasibility rates, and cost per basis point.</span>
  </a>
  <a class="workshop-card" href="enterprise-capability/">
    <img src="assets/8-EnterpriseCapability.svg" alt="" width="916" height="516" loading="lazy">
    <strong>08 · Repeatable enterprise capability</strong>
    <span>Move from executive briefings to a 2-Day Corporate Intensive and 90-day Feasibility Diagnostic.</span>
  </a>
  <a class="workshop-card" href="resources/">
    <strong>Continue learning · Cohorts &amp; Briefings</strong>
    <span>Open Session registration (10 Dec 2026), Corporate Intensive syllabus, and diagnostic intake.</span>
  </a>
</div>
