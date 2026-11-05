"""Unit tests for the Quantum at Work enterprise feasibility harness."""

import unittest

from examples.combinatorial_triage import (
    AllocationTask,
    CryptoAssetInventory,
    WorkloadSpec,
    build_conflict_qubo,
    demo_scenario,
    evaluate_release_gate,
    solve_classical_greedy,
    solve_qubo_exact,
    triage_workload,
)


class TestCombinatorialTriage(unittest.TestCase):
    def test_triage_routes_coupled_workload_to_hybrid_qubo(self) -> None:
        spec = WorkloadSpec(
            name="pit_to_port_Blending",
            decision_variables=64,
            coupling_density=0.42,
            hard_constraints=18,
            sla_budget_ms=2000,
            telemetry_completeness=0.95,
        )
        decision = triage_workload(spec)
        self.assertEqual(decision.route, "HYBRID_QUBO_CANDIDATE")
        self.assertTrue(decision.requires_classical_baseline)

    def test_triage_blocks_dirty_telemetry_and_tight_sla(self) -> None:
        dirty = WorkloadSpec(
            name="unclean_erp_feed",
            decision_variables=50,
            coupling_density=0.5,
            hard_constraints=10,
            sla_budget_ms=1000,
            telemetry_completeness=0.70,
        )
        self.assertEqual(triage_workload(dirty).route, "HOLD_DATA_HYGIENE")

        tight_sla = WorkloadSpec(
            name="hft_order_router",
            decision_variables=50,
            coupling_density=0.5,
            hard_constraints=10,
            sla_budget_ms=12,
            telemetry_completeness=0.99,
        )
        self.assertEqual(
            triage_workload(tight_sla).route, "CLASSICAL_DETERMINISTIC_FAST_PATH"
        )

    def test_qubo_outperforms_greedy_on_coupled_conflicts(self) -> None:
        triage, greedy_res, qubo_res, gate = demo_scenario()
        self.assertEqual(triage.route, "HYBRID_QUBO_CANDIDATE")
        self.assertEqual(greedy_res.selected_tasks, ("T1_FEEDER_EXPRESS", "T4_BUNKER_BARGE"))
        self.assertEqual(greedy_res.objective_value, 20.0)
        self.assertEqual(qubo_res.selected_tasks, ("T2_ULCV_NORTH", "T3_ULCV_SOUTH"))
        self.assertEqual(qubo_res.objective_value, 23.0)
        self.assertTrue(gate.approved_for_pilot)
        self.assertEqual(gate.uplift_bps, 1500.0)

    def test_release_gate_rejects_sla_breach(self) -> None:
        _, greedy_res, qubo_res, _ = demo_scenario()
        gate = evaluate_release_gate(
            classical=greedy_res,
            candidate=qubo_res,
            latency_ms=2400,
            sla_budget_ms=1500,
        )
        self.assertFalse(gate.approved_for_pilot)
        self.assertIn("latency_2400ms_exceeds_sla_1500ms", gate.failed_checks)

    def test_mosca_cryptographic_exposure(self) -> None:
        legacy_Archive = CryptoAssetInventory(
            system_name="long_lived_trade_finance_ledger",
            public_key_primitive="RSA-2048",
            confidentiality_shelf_life_years=12,
            migration_lead_time_years=3,
            estimated_crqc_horizon_years=10,
        )
        self.assertEqual(legacy_Archive.mosca_exposure_years, 5)
        self.assertTrue(legacy_Archive.requires_immediate_pqc_remediation)


if __name__ == "__main__":
    unittest.main()
