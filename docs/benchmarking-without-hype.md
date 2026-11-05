---
title: Benchmarking without vendor hype
hero: assets/7-BenchmarkingWithoutHype.svg
hero_alt: "Chapter 07: Benchmarking Without Vendor Hype. Hardware-agnostic evaluation across scaling, feasibility, and basis-point uplift."
---

# 07 · Benchmarking without vendor hype

**Never let a solver vendor grade their own homework.**

When evaluating any quantum, quantum-inspired, or hybrid optimization platform, Eve Count enforces a **hardware-agnostic release gate** (`evaluate_release_gate`). A candidate solver is only approved for pilot progression if it simultaneously satisfies three non-negotiable criteria:

1. **100% Hard-Constraint Feasibility:** Zero unpenalized constraint violations on out-of-sample operational snapshots.
2. **End-to-End SLA Compliance:** Total wall-clock latency (including network, compilation/embedding, and post-processing) within `sla_budget_ms`.
3. **Material Basis-Point Uplift:** Verified improvement over the tuned classical baseline exceeding `min_uplift_bps` (e.g., `+150 bps` or `+1.5%` net objective gain).

## Running the automated release gate

```python
from examples.combinatorial_triage import demo_scenario, evaluate_release_gate

triage, greedy_res, qubo_res, gate = demo_scenario()
assert gate.approved_for_pilot is True
assert gate.uplift_bps == 1500.0
print(gate.summary)

# Now simulate a solver that takes 2,400ms on a 1,500ms operational SLA:
rejected_gate = evaluate_release_gate(
    classical=greedy_res,
    candidate=qubo_res,
    latency_ms=2400,
    sla_budget_ms=1500,
    min_uplift_bps=150.0,
)
assert rejected_gate.approved_for_pilot is False
assert "latency_2400ms_exceeds_sla_1500ms" in rejected_gate.failed_checks
print(rejected_gate.summary)
```

!!! example "Try with your AI coding assistant"
    Ask your assistant: *"Extend `evaluate_release_gate` to also compute the annual dollar value of `uplift_bps` given an enterprise's annual throughput volume and compare it against annual solver licensing cost."*

## Checkpoint

You now have an automated, vendor-neutral release gate in Python that turns subjective PoC presentations into an objective **Approve / Hold** engineering decision.
