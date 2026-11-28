"""Unit tests for the OpenClone Engineering Lifecycle & Independent Verification System."""
import unittest
from pathlib import Path

from src.openclone.lifecycle.engine import LifecycleEngine
from src.openclone.lifecycle.schema import (
    ProjectType,
    ItemStatus,
    Priority,
    Applicability,
    VerificationOutcome,
)

ROOT = Path(__file__).resolve().parents[1]


class LifecycleVerificationTests(unittest.TestCase):
    def setUp(self):
        self.engine = LifecycleEngine(project_id="test-proj", repo_root=ROOT)

    def test_dynamic_generation_web_saas(self):
        items = self.engine.generate_checklist(
            project_type=ProjectType.WEB_SAAS,
            features=["auth", "billing", "dashboard"],
            has_ai=False,
        )
        self.assertGreater(len(items), 30)
        # Verify SaaS pack extra tasks are present
        saas_pack_items = [it for it in items.values() if "Multi-Tenant" in it.title]
        self.assertGreaterEqual(len(saas_pack_items), 1)
        # Phase 13 (AI) must be NOT_APPLICABLE because has_ai=False
        phase_13 = items.get("PHASE_13_AI_INTELLIGENCE")
        self.assertIsNotNone(phase_13)
        self.assertEqual(phase_13.applicability, Applicability.NOT_APPLICABLE)

    def test_dynamic_generation_static_website(self):
        items = self.engine.generate_checklist(
            project_type=ProjectType.STATIC_WEBSITE,
            features=["blog", "portfolio"],
            has_ai=False,
        )
        # Backend and database phases must be NOT_APPLICABLE
        backend = items.get("PHASE_09_BACKEND")
        database = items.get("PHASE_10_DATABASE")
        self.assertEqual(backend.applicability, Applicability.NOT_APPLICABLE)
        self.assertEqual(database.applicability, Applicability.NOT_APPLICABLE)
        self.assertIn("Static marketing", backend.applicability_reason)

    def test_dynamic_generation_ai_platform(self):
        items = self.engine.generate_checklist(
            project_type=ProjectType.AI_AGENT_PLATFORM,
            features=["chat", "rag"],
        )
        phase_13 = items.get("PHASE_13_AI_INTELLIGENCE")
        self.assertEqual(phase_13.applicability, Applicability.REQUIRED)

    def test_forbidden_verified_transition_without_evidence(self):
        self.engine.generate_checklist(project_type=ProjectType.WEB_SAAS)
        task_id = "PHASE_01_DISCOVERY_TASK_01"
        with self.assertRaises(ValueError) as ctx:
            self.engine.transition_item(item_id=task_id, target_status=ItemStatus.VERIFIED)
        self.assertIn("without evidence", str(ctx.exception))

    def test_independent_verification_with_valid_and_invalid_evidence(self):
        self.engine.generate_checklist(project_type=ProjectType.WEB_SAAS)
        task_id = "PHASE_01_DISCOVERY_TASK_01"

        # Case 1: Non-existent file path as evidence -> Verification must fail and record defect
        self.engine.attach_evidence(
            item_id=task_id,
            evidence_type="code_diff",
            ref="non_existent_file_xyz_123.py",
            description="Fake implementation",
        )
        outcome, msg = self.engine.run_independent_verification(item_id=task_id)
        self.assertEqual(outcome, VerificationOutcome.FAIL)
        self.assertEqual(self.engine.items[task_id].status, ItemStatus.FAILED)
        self.assertGreaterEqual(len(self.engine.items[task_id].defects), 1)

        # Case 2: Valid existing file path -> Verification passes
        self.engine.items[task_id].evidence_refs.clear()
        self.engine.attach_evidence(
            item_id=task_id,
            evidence_type="code_diff",
            ref="README.md",
            description="Verified problem statement in README",
        )
        outcome, msg = self.engine.run_independent_verification(item_id=task_id)
        self.assertEqual(outcome, VerificationOutcome.PASS)
        self.assertEqual(self.engine.items[task_id].status, ItemStatus.VERIFIED)

    def test_quality_gate_evaluation(self):
        self.engine.generate_checklist(project_type=ProjectType.WEB_SAAS)
        gate = self.engine.evaluate_quality_gate(phase_id="PHASE_01_DISCOVERY")
        # Initially blocked because tasks are NOT_STARTED
        self.assertEqual(gate.status, "BLOCKED")
        self.assertGreater(len(gate.blockers), 0)

        # Verify all mandatory tasks in Phase 01
        for t_id in gate.mandatory_item_ids:
            self.engine.attach_evidence(
                item_id=t_id,
                evidence_type="code_diff",
                ref="README.md",
                description="Evidence",
            )
            self.engine.run_independent_verification(item_id=t_id)

        # Re-evaluate gate -> should pass
        gate = self.engine.evaluate_quality_gate(phase_id="PHASE_01_DISCOVERY")
        self.assertEqual(gate.status, "PASSED")
        self.assertEqual(len(gate.blockers), 0)

    def test_progress_calculation(self):
        self.engine.generate_checklist(project_type=ProjectType.WEB_SAAS)
        p = self.engine.calculate_progress()
        self.assertEqual(p["implementation_progress_pct"], 0.0)
        self.assertEqual(p["verified_progress_pct"], 0.0)

        # Attach evidence to one task
        task_id = "PHASE_01_DISCOVERY_TASK_01"
        self.engine.attach_evidence(
            item_id=task_id,
            evidence_type="code_diff",
            ref="README.md",
            description="Doc evidence",
        )
        p2 = self.engine.calculate_progress()
        self.assertGreater(p2["implementation_progress_pct"], 0.0)
        self.assertEqual(p2["verified_progress_pct"], 0.0)

        # Verify it
        self.engine.run_independent_verification(item_id=task_id)
        p3 = self.engine.calculate_progress()
        self.assertGreater(p3["verified_progress_pct"], 0.0)

    def test_ide_handoff_and_report_ingestion(self):
        self.engine.generate_checklist(project_type=ProjectType.WEB_SAAS)
        task_id = "PHASE_01_DISCOVERY_TASK_01"

        # Generate handoff package
        pkg = self.engine.generate_ide_handoff_package(task_id=task_id)
        self.assertIn("Task Handoff Package", pkg)
        self.assertIn(task_id, pkg)

        # Ingest empty report -> must reject
        success, err = self.engine.ingest_ide_completion_report({"task_id": task_id})
        self.assertFalse(success)
        self.assertIn("Dishonest or empty", err)

        # Ingest valid report -> moves to VERIFICATION_PENDING, not VERIFIED
        success, msg = self.engine.ingest_ide_completion_report({
            "task_id": task_id,
            "status": "IMPLEMENTED",
            "changed_files": ["README.md"],
            "test_command": "python tools/validate_repository.py",
            "test_result": "PASS",
        })
        self.assertTrue(success)
        self.assertEqual(self.engine.items[task_id].status, ItemStatus.VERIFICATION_PENDING)


if __name__ == "__main__":
    unittest.main()
