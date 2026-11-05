---
title: Data, latency & SLA boundaries
hero: assets/5-LatencyAndData.svg
hero_alt: "Chapter 05: Data, Latency & Integration Boundaries. Why real-time SLA budgets and dirty ERP telemetry kill naive PoCs."
---

# 05 · Data, latency & SLA boundaries

**A 10-millisecond solver runtime is useless if network serialization, queue wait, and embedding take 4 seconds inside a 200-millisecond SLA.**

When evaluating quantum or hybrid workflows for enterprise production, wall-clock **End-to-End Time-to-Solution (E2E TTS)** is the only latency metric that matters:

$$\text{E2E TTS} = t_{\text{ingest}} + t_{\text{formulate}} + t_{\text{network}} + t_{\text{queue}} + t_{\text{embed/compile}} + t_{\text{sample}} + t_{\text{validate}}$$

## Guarding against dirty telemetry and SLA breaches

In `examples/combinatorial_triage.py`, two explicit guardrails protect production pipelines before any solver is invoked:

1. **Telemetry Hygiene Gate (`telemetry_completeness >= 0.85`):** If ERP or sensor feeds are missing arrival times, capacities, or conflict edges, optimizing a Hallucinated QUBO matrix simply produces high-precision nonsense.
2. **SLA Fast-Path Gate (`sla_budget_ms >= 50`):** Sub-50ms operational loops (such as high-frequency order routing or real-time safety interlocks) cannot tolerate cloud queue round-trips.

```python
from examples.combinatorial_triage import WorkloadSpec, triage_workload

dirty_erp_feed = WorkloadSpec(
    name="incomplete_manifest_sync",
    decision_variables=80,
    coupling_density=0.45,
    hard_constraints=22,
    sla_budget_ms=2000,
    telemetry_completeness=0.72,
)

sub_50ms_loop = WorkloadSpec(
    name="intraday_execution_router",
    decision_variables=60,
    coupling_density=0.35,
    hard_constraints=12,
    sla_budget_ms=15,
    telemetry_completeness=0.99,
)

assert triage_workload(dirty_erp_feed).route == "HOLD_DATA_HYGIENE"
assert triage_workload(sub_50ms_loop).route == "CLASSICAL_DETERMINISTIC_FAST_PATH"
```

!!! example "Try with your AI coding assistant"
    Ask your assistant: *"Break down the latency budget for a 1,500ms dispatch window into concrete allocations for data snapshot extraction, QUBO matrix assembly, solver execution, and post-validation."*

## Checkpoint

Document both the **minimum data completeness threshold** and the **maximum wall-clock SLA budget** for your candidate workload before signing any solver pilot agreement.
