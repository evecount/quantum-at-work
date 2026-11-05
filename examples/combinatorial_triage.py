"""Deterministic Python feasibility harness for Quantum at Work.

Separates problem specification, classical baseline benchmarking, QUBO penalty
calibration, latency envelope checks, and release-gate governance without
requiring external cloud credentials or vendor hardware tokens.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import Dict, List, Sequence, Tuple


@dataclass(frozen=True)
class WorkloadSpec:
    """Operational workload specification before choosing a solver."""

    name: str
    decision_variables: int
    coupling_density: float
    hard_constraints: int
    sla_budget_ms: int
    telemetry_completeness: float = 1.0
    is_linear_relaxable: bool = False


@dataclass(frozen=True)
class TriageDecision:
    """Result of routing an enterprise workload across solver classes."""

    workload: str
    route: str
    rationale: str
    requires_classical_baseline: bool = True


def triage_workload(spec: WorkloadSpec) -> TriageDecision:
    """Route an operational workload based on structure, telemetry, and SLA."""
    if spec.telemetry_completeness < 0.85:
        return TriageDecision(
            workload=spec.name,
            route="HOLD_DATA_HYGIENE",
            rationale="Telemetry completeness below 85% minimum threshold; fix data pipeline first.",
            requires_classical_baseline=False,
        )

    if spec.sla_budget_ms < 50:
        return TriageDecision(
            workload=spec.name,
            route="CLASSICAL_DETERMINISTIC_FAST_PATH",
            rationale="Sub-50ms SLA precludes remote hybrid queue round-trips; use compiled classical heuristics.",
        )

    if spec.is_linear_relaxable or spec.coupling_density < 0.15:
        return TriageDecision(
            workload=spec.name,
            route="CLASSICAL_MIP_OR_GREEDY",
            rationale="Low quadratic coupling density; modern linear/MIP solvers remain optimal.",
        )

    if spec.decision_variables >= 24 and spec.coupling_density >= 0.25:
        return TriageDecision(
            workload=spec.name,
            route="HYBRID_QUBO_CANDIDATE",
            rationale="High quadratic coupling density with bounded SLA window; eligible for hybrid QUBO vs. classical metaheuristic benchmark.",
        )

    return TriageDecision(
        workload=spec.name,
        route="CLASSICAL_METAHEURISTIC",
        rationale="Moderate scale; benchmark simulated annealing and tabu search before hybrid escalation.",
    )


@dataclass(frozen=True)
class AllocationTask:
    """Discrete operational slot (e.g., vessel berth, pit haulage dispatch, or liquidity tranche)."""

    task_id: str
    value: float
    resource_cost: int
    conflicts_with: Tuple[str, ...] = ()


@dataclass(frozen=True)
class BenchmarkResult:
    """Comparison record between a classical baseline and a QUBO candidate."""

    method: str
    selected_tasks: Tuple[str, ...]
    objective_value: float
    total_cost: int
    feasible: bool
    energy: float = 0.0


def solve_classical_greedy(
    tasks: Sequence[AllocationTask], max_capacity: int
) -> BenchmarkResult:
    """Deterministic greedy baseline ordered by value-to-cost efficiency."""
    ranked = sorted(
        tasks,
        key=lambda t: (t.value / max(t.resource_cost, 1), t.value),
        reverse=True,
    )
    chosen: List[AllocationTask] = []
    chosen_ids: set[str] = set()
    used_capacity = 0

    for task in ranked:
        if used_capacity + task.resource_cost > max_capacity:
            continue
        if any(c in chosen_ids for c in task.conflicts_with):
            continue
        if any(task.task_id in existing.conflicts_with for existing in chosen):
            continue
        chosen.append(task)
        chosen_ids.add(task.task_id)
        used_capacity += task.resource_cost

    total_val = round(sum(t.value for t in chosen), 4)
    ordered_ids = tuple(t.task_id for t in tasks if t.task_id in chosen_ids)
    return BenchmarkResult(
        method="classical_greedy",
        selected_tasks=ordered_ids,
        objective_value=total_val,
        total_cost=used_capacity,
        feasible=True,
        energy=-total_val,
    )


def build_conflict_qubo(
    tasks: Sequence[AllocationTask],
    max_capacity: int,
    conflict_penalty: float = 25.0,
    capacity_penalty: float = 8.0,
) -> Dict[Tuple[int, int], float]:
    """Construct an inspectable upper-triangular QUBO dictionary Q[(i, j)].

    Minimizes H(x) = -sum_i v_i x_i + conflict_penalty * sum_{(i,j) in E} x_i x_j
    plus a soft quadratic overload penalty when total cost exceeds max_capacity.
    """
    q_matrix: Dict[Tuple[int, int], float] = {}
    n = len(tasks)
    id_to_idx = {t.task_id: idx for idx, t in enumerate(tasks)}

    # Linear reward terms (-value_i)
    for i, task in enumerate(tasks):
        q_matrix[(i, i)] = q_matrix.get((i, i), 0.0) - float(task.value)

    # Pairwise conflict penalties
    seen_pairs: set[Tuple[int, int]] = set()
    for i, task in enumerate(tasks):
        for other_id in task.conflicts_with:
            if other_id in id_to_idx:
                j = id_to_idx[other_id]
                pair = (min(i, j), max(i, j))
                if pair[0] != pair[1] and pair not in seen_pairs:
                    seen_pairs.add(pair)
                    q_matrix[pair] = q_matrix.get(pair, 0.0) + float(conflict_penalty)

    # Pairwise resource contention bias scaled by relative capacity share
    for i in range(n):
        for j in range(i + 1, n):
            combined = tasks[i].resource_cost + tasks[j].resource_cost
            if combined > max_capacity:
                q_matrix[(i, j)] = q_matrix.get((i, j), 0.0) + float(capacity_penalty)

    return q_matrix


def evaluate_qubo_bitstring(
    bitstring: Sequence[int],
    tasks: Sequence[AllocationTask],
    max_capacity: int,
    q_matrix: Dict[Tuple[int, int], float],
) -> BenchmarkResult:
    """Evaluate a binary assignment vector against both the QUBO matrix and hard operational rules."""
    energy = 0.0
    for (i, j), weight in q_matrix.items():
        if bitstring[i] and bitstring[j]:
            energy += weight

    chosen = [tasks[i] for i, bit in enumerate(bitstring) if bit == 1]
    chosen_ids = {t.task_id for t in chosen}
    total_cost = sum(t.resource_cost for t in chosen)
    total_value = round(sum(t.value for t in chosen), 4)

    has_conflict = any(
        (other in chosen_ids)
        for t in chosen
        for other in t.conflicts_with
    )
    feasible = (total_cost <= max_capacity) and (not has_conflict)

    return BenchmarkResult(
        method="qubo_exact_scan",
        selected_tasks=tuple(t.task_id for t in chosen),
        objective_value=total_value if feasible else 0.0,
        total_cost=total_cost,
        feasible=feasible,
        energy=round(energy, 4),
    )


def solve_qubo_exact(
    tasks: Sequence[AllocationTask],
    max_capacity: int,
    conflict_penalty: float = 25.0,
    capacity_penalty: float = 8.0,
) -> BenchmarkResult:
    """Reference solver for small-N pedagogical verification (exhaustively scans 2^N states)."""
    q_matrix = build_conflict_qubo(
        tasks,
        max_capacity=max_capacity,
        conflict_penalty=conflict_penalty,
        capacity_penalty=capacity_penalty,
    )
    best_result: BenchmarkResult | None = None
    for bits in product((0, 1), repeat=len(tasks)):
        candidate = evaluate_qubo_bitstring(bits, tasks, max_capacity, q_matrix)
        if not candidate.feasible:
            continue
        if (
            best_result is None
            or candidate.objective_value > best_result.objective_value
            or (
                candidate.objective_value == best_result.objective_value
                and candidate.total_cost < best_result.total_cost
            )
        ):
            best_result = candidate

    assert best_result is not None
    return best_result


@dataclass(frozen=True)
class CryptoAssetInventory:
    """Inventory item for Post-Quantum Cryptography (PQC) vs. optimization governance."""

    system_name: str
    public_key_primitive: str
    confidentiality_shelf_life_years: int
    migration_lead_time_years: int
    estimated_crqc_horizon_years: int = 10

    @property
    def mosca_exposure_years(self) -> int:
        """Mosca inequality margin: (X + Y) - Z. Positive values indicate urgent harvest-now risk."""
        return (
            self.confidentiality_shelf_life_years + self.migration_lead_time_years
        ) - self.estimated_crqc_horizon_years

    @property
    def requires_immediate_pqc_remediation(self) -> bool:
        return self.mosca_exposure_years > 0


@dataclass(frozen=True)
class ReleaseGateDecision:
    """Governance verdict for deploying a hybrid optimization workflow."""

    approved_for_pilot: bool
    uplift_bps: float
    summary: str
    failed_checks: Tuple[str, ...] = field(default_factory=tuple)


def evaluate_release_gate(
    classical: BenchmarkResult,
    candidate: BenchmarkResult,
    latency_ms: int,
    sla_budget_ms: int,
    min_uplift_bps: float = 150.0,
) -> ReleaseGateDecision:
    """Enforce Eve Count's 'Evidence Before Advantage' pilot release gate."""
    failures: List[str] = []

    if not candidate.feasible:
        failures.append("candidate_violates_hard_constraints")

    if latency_ms > sla_budget_ms:
        failures.append(f"latency_{latency_ms}ms_exceeds_sla_{sla_budget_ms}ms")

    if classical.objective_value <= 0:
        uplift_bps = 0.0
    else:
        uplift_bps = round(
            ((candidate.objective_value - classical.objective_value) / classical.objective_value)
            * 10000.0,
            1,
        )

    if uplift_bps < min_uplift_bps:
        failures.append(
            f"uplift_{uplift_bps}bps_below_threshold_{min_uplift_bps}bps"
        )

    approved = len(failures) == 0
    summary = (
        f"APPROVED: +{uplift_bps} bps verified uplift over classical baseline within {latency_ms}ms SLA."
        if approved
        else f"HOLD: Retain classical baseline ({', '.join(failures)})."
    )
    return ReleaseGateDecision(
        approved_for_pilot=approved,
        uplift_bps=uplift_bps,
        summary=summary,
        failed_checks=tuple(failures),
    )


def demo_scenario() -> Tuple[TriageDecision, BenchmarkResult, BenchmarkResult, ReleaseGateDecision]:
    """Run the standard end-to-end maritime berth & crane allocation demonstration."""
    spec = WorkloadSpec(
        name="terminal_berth_crane_window",
        decision_variables=48,
        coupling_density=0.38,
        hard_constraints=14,
        sla_budget_ms=1500,
        telemetry_completeness=0.96,
    )
    triage = triage_workload(spec)

    # Notice how T1 ("high efficiency decoy") conflicts with both T2 and T3.
    # Greedy takes T1 (value 14, cost 5) + T4 (value 6, cost 3) = 20.0.
    # Exact QUBO skips T1 and takes T2 (value 12, cost 4) + T3 (value 11, cost 4) = 23.0 (+1500 bps uplift!).
    tasks = [
        AllocationTask("T1_FEEDER_EXPRESS", value=16.0, resource_cost=5, conflicts_with=("T2_ULCV_NORTH", "T3_ULCV_SOUTH")),
        AllocationTask("T2_ULCV_NORTH", value=12.0, resource_cost=4, conflicts_with=("T1_FEEDER_EXPRESS",)),
        AllocationTask("T3_ULCV_SOUTH", value=11.0, resource_cost=4, conflicts_with=("T1_FEEDER_EXPRESS",)),
        AllocationTask("T4_BUNKER_BARGE", value=4.0, resource_cost=3, conflicts_with=()),
    ]
    greedy_res = solve_classical_greedy(tasks, max_capacity=8)
    qubo_res = solve_qubo_exact(tasks, max_capacity=8)
    gate = evaluate_release_gate(
        classical=greedy_res,
        candidate=qubo_res,
        latency_ms=420,
        sla_budget_ms=spec.sla_budget_ms,
        min_uplift_bps=150.0,
    )
    return triage, greedy_res, qubo_res, gate


if __name__ == "__main__":
    triage, greedy_res, qubo_res, gate = demo_scenario()
    print(f"[1] Triage Route      : {triage.route} ({triage.rationale})")
    print(f"[2] Classical Greedy  : tasks={greedy_res.selected_tasks} value={greedy_res.objective_value}")
    print(f"[3] Coupled QUBO Best : tasks={qubo_res.selected_tasks} value={qubo_res.objective_value}")
    print(f"[4] Release Gate      : {gate.summary}")
