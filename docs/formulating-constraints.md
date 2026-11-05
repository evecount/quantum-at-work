---
title: Formulating constraints & penalties
hero: assets/3-FormulatingConstraints.svg
hero_alt: "Chapter 03: Formulating Constraints & Penalties. Translate operational rules into inspectable QUBO matrices."
---

# 03 · Formulating constraints & penalties

**A quantum or digital annealer does not read business rules; it minimizes an energy landscape.**

To evaluate a combinatorial problem on a quantum annealer, gate-model QAOA circuit, or Ising-inspired solver, we express binary decisions $x_i \in \{0, 1\}$ as a **Quadratic Unconstrained Binary Optimization (QUBO)** objective:

$$H(x) = \sum_{i} Q_{ii} x_i + \sum_{i < j} Q_{ij} x_i x_j$$

where:

- **Linear diagonal terms ($Q_{ii} = -v_i$)** reward selecting high-value tasks, and
- **Quadratic off-diagonal terms ($Q_{ij} > 0$)** penalize pairs of tasks that violate mutual exclusion or exceed shared resource capacity.

## Calibrating penalty weights

If penalty weights (`conflict_penalty` or `capacity_penalty`) are set too low, the solver will happily violate hard operational constraints to chase higher rewards. If set too high, the energy landscape flattens out and numerical precision degrades.

```python
from examples.combinatorial_triage import (
    AllocationTask,
    build_conflict_qubo,
    solve_qubo_exact,
)

tasks = [
    AllocationTask("T1_FEEDER_EXPRESS", value=16.0, resource_cost=5, conflicts_with=("T2_ULCV_NORTH", "T3_ULCV_SOUTH")),
    AllocationTask("T2_ULCV_NORTH", value=12.0, resource_cost=4, conflicts_with=("T1_FEEDER_EXPRESS",)),
    AllocationTask("T3_ULCV_SOUTH", value=11.0, resource_cost=4, conflicts_with=("T1_FEEDER_EXPRESS",)),
    AllocationTask("T4_BUNKER_BARGE", value=4.0, resource_cost=3, conflicts_with=()),
]

q_matrix = build_conflict_qubo(tasks, max_capacity=8, conflict_penalty=25.0, capacity_penalty=8.0)
assert q_matrix[(0, 0)] == -16.0
assert q_matrix[(0, 1)] > 0.0  # Conflict + capacity coupling between T1 and T2

best = solve_qubo_exact(tasks, max_capacity=8)
assert best.selected_tasks == ("T2_ULCV_NORTH", "T3_ULCV_SOUTH")
assert best.objective_value == 23.0
print("Global optimum:", best)
```

By accounting for the off-diagonal coupling terms $Q_{01}$ and $Q_{02}$ simultaneously, the QUBO formulation bypasses the greedy decoy (`T1`) and selects `("T2_ULCV_NORTH", "T3_ULCV_SOUTH")` for a verified objective of `23.0`.

!!! example "Try with your AI coding assistant"
    Ask your assistant: *"Inspect `build_conflict_qubo` in `examples/combinatorial_triage.py`. What happens to the minimum-energy state if `conflict_penalty` is reduced from `25.0` to `1.0`? Why must `evaluate_qubo_bitstring` still verify hard feasibility independently?"*

## Checkpoint

Never trust raw solver energy alone. Your harness must always decode the binary bitstring back into domain objects and verify `feasible == True` against hard operational rules before accepting a solution.
