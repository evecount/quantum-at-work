---
title: Classical-to-quantum triage
hero: assets/4-HybridQuboTriage.svg
hero_alt: "Chapter 04: Classical-to-Quantum Triage. Route sub-problems dynamically between classical heuristics and hybrid QUBO solvers."
---

# 04 · Classical-to-quantum triage

**Production systems are hybrid by architecture: classical code owns pre-processing, decomposition, and fallback.**

Even when a workload contains a tightly coupled combinatorial core, 80% of the surrounding pipeline—data ingestion, constraint pruning, variable freezing, and post-solution validation—remains strictly classical.

## Dynamic workload routing

Rather than hard-wiring an application to a single solver, an enterprise harness inspects problem structure at runtime and routes each sub-problem to the appropriate tier:

| Coupling Density | Variables ($N$) | SLA Window | Recommended Route |
| :--- | :--- | :--- | :--- |
| `< 0.15` or Linear | Any | Any | `CLASSICAL_MIP_OR_GREEDY` |
| Any | Any | `< 50 ms` | `CLASSICAL_DETERMINISTIC_FAST_PATH` |
| `0.15 – 0.24` | `< 24` | `>= 50 ms` | `CLASSICAL_METAHEURISTIC` |
| `>= 0.25` | `>= 24` | `>= 50 ms` | `HYBRID_QUBO_CANDIDATE` |

Let's verify how the triage router distinguishes a linear-relaxable warehouse replenishment task from a densely coupled pit-to-port blending schedule:

```python
from examples.combinatorial_triage import WorkloadSpec, triage_workload

linear_job = WorkloadSpec(
    name="standard_inventory_replenishment",
    decision_variables=200,
    coupling_density=0.04,
    hard_constraints=20,
    sla_budget_ms=5000,
    is_linear_relaxable=True,
)

coupled_job = WorkloadSpec(
    name="pit_to_port_ore_blending",
    decision_variables=64,
    coupling_density=0.41,
    hard_constraints=18,
    sla_budget_ms=3000,
)

assert triage_workload(linear_job).route == "CLASSICAL_MIP_OR_GREEDY"
assert triage_workload(coupled_job).route == "HYBRID_QUBO_CANDIDATE"
```

!!! example "Try with your AI coding assistant"
    Ask your assistant: *"Design a decomposition step that freezes variables with zero conflicts before building the QUBO matrix, reducing the effective variable count sent to the solver."*

## Checkpoint

Your architecture diagram must show a **deterministic classical fallback** alongside any hybrid solver call so that if a remote queue times out or returns an infeasible sample, operations continue uninterrupted using the classical baseline.
