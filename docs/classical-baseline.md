---
title: The classical baseline first
hero: assets/2-ClassicalBaseline.svg
hero_alt: "Chapter 02: The Classical Baseline First. Every defensible quantum roadmap begins by bounding classical solvers."
---

# 02 · The classical baseline first

**If you haven't benchmarked a well-tuned classical heuristic, you cannot measure quantum value.**

A recurring antipattern in vendor-led pilots is comparing a tuned quantum-inspired or hybrid solver against a strawman brute-force script. At Eve Count, our first rule of governance is **Evidence Before Advantage**: every candidate formulation must be benchmarked against a deterministic classical baseline on the exact same constraint set.

## How greedy heuristics get trapped by coupling

Consider four discrete allocation requests competing for `max_capacity = 8` units of berth/crane capacity:

- `T1_FEEDER_EXPRESS` yields value `16.0` at cost `5` (highest value-per-unit ratio `3.20`), but **conflicts** with both `T2_ULCV_NORTH` and `T3_ULCV_SOUTH`.
- `T2_ULCV_NORTH` (`value=12.0, cost=4`) and `T3_ULCV_SOUTH` (`value=11.0, cost=4`) do not conflict with each other and together yield `23.0` within the exact capacity of `8`.

Let's run the deterministic classical greedy baseline:

```python
from examples.combinatorial_triage import AllocationTask, solve_classical_greedy

tasks = [
    AllocationTask("T1_FEEDER_EXPRESS", value=16.0, resource_cost=5, conflicts_with=("T2_ULCV_NORTH", "T3_ULCV_SOUTH")),
    AllocationTask("T2_ULCV_NORTH", value=12.0, resource_cost=4, conflicts_with=("T1_FEEDER_EXPRESS",)),
    AllocationTask("T3_ULCV_SOUTH", value=11.0, resource_cost=4, conflicts_with=("T1_FEEDER_EXPRESS",)),
    AllocationTask("T4_BUNKER_BARGE", value=4.0, resource_cost=3, conflicts_with=()),
]

baseline = solve_classical_greedy(tasks, max_capacity=8)
assert baseline.selected_tasks == ("T1_FEEDER_EXPRESS", "T4_BUNKER_BARGE")
assert baseline.objective_value == 20.0
print(baseline)
```

Because `solve_classical_greedy` ranks tasks locally by efficiency (`16.0 / 5 = 3.2`), it locks in `T1_FEEDER_EXPRESS` first, blocking both `T2` and `T3` and leaving the schedule stuck at `20.0` instead of the global optimum `23.0` (a **1,500 basis-point optimality gap**).

!!! example "Try with your AI coding assistant"
    Ask your assistant: *"Write a short unit test showing when `solve_classical_greedy` achieves the exact global optimum (when `conflicts_with` is empty) versus when pairwise conflicts create a local-minimum trap."*

## Checkpoint

You should have a deterministic classical baseline (`solve_classical_greedy`, MIP, or simulated annealing) that runs in milliseconds, produces a feasible schedule, and establishes the **floor objective value** that any advanced solver must beat.
