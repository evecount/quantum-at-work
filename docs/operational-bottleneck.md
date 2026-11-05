---
title: Start with an operational bottleneck
hero: assets/1-OperationalBottleneck.svg
hero_alt: "Chapter 01: Start with an Operational Bottleneck. Separate coupled combinatorial constraints from linear workloads."
---

# 01 · Start with an operational bottleneck

**Quantum advantage never begins with a qubit count; it begins with a coupled operational constraint.**

Most enterprise quantum proofs-of-concept fail in their first week because teams pick a familiar analytics or reporting workflow, wrap it in a quantum SDK, and discover that standard SQL, linear programming, or gradient boosted trees already solve it orders of magnitude faster.

## Identify coupled combinatorial structure

Where do hybrid quantum-classical formulations actually earn their keep? Look for **discrete operational bottlenecks** where choosing one option changes the feasibility or cost of many other options simultaneously:

- **Maritime & Fleet Operations:** Assigning vessels to berth windows and quay cranes where draft limits, tidal windows, and yard congestion couple every assignment.
- **Mining & Bulk Resources:** Pit-to-port ore blending and haulage scheduling under non-linear grade penalty thresholds.
- **Financial & Treasury Operations:** Intraday collateral allocation and multi-lateral netting under discrete bucket haircuts.

In our harness, we represent a candidate workload using `WorkloadSpec` before selecting any solver:

```python
from examples.combinatorial_triage import WorkloadSpec, triage_workload

spec = WorkloadSpec(
    name="terminal_berth_crane_window",
    decision_variables=48,
    coupling_density=0.38,
    hard_constraints=14,
    sla_budget_ms=1500,
    telemetry_completeness=0.96,
)
decision = triage_workload(spec)
assert decision.route == "HYBRID_QUBO_CANDIDATE"
print(decision)
```

Notice what `triage_workload` checks:

1. **Telemetry completeness (`0.96`):** Are at least 85% of the required constraint inputs clean and available at decision time?
2. **SLA budget (`1500` ms):** Does the operational window allow a hybrid solver round-trip?
3. **Coupling density (`0.38`):** Are the discrete variables densely coupled, or can the problem be relaxed into independent linear sub-problems?

!!! example "Try with your AI coding assistant"
    Paste the snippet above into your assistant and ask: *"Inspect `WorkloadSpec` in `examples/combinatorial_triage.py`. Propose three real operational workloads from our industry—one that routes to `CLASSICAL_MIP_OR_GREEDY`, one that routes to `CLASSICAL_DETERMINISTIC_FAST_PATH`, and one that qualifies as `HYBRID_QUBO_CANDIDATE`."*

## Checkpoint

Before advancing to mathematical formulation, your team should document:

- One named operational decision bottleneck with discrete choices,
- Why choices are mutually coupled (why greedy local picks create downstream conflicts), and
- The decision window SLA in milliseconds or minutes.
