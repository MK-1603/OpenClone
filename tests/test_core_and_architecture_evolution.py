"""Unit and Integration Tests for OpenClone Core & Architecture Evolution.

Verifies:
- OpenCloneCore lifecycle, event bus, and subsystem health
- ModuleManager lifecycle (DISCOVERED -> VALIDATED -> ACTIVE) and rollback
- UnifiedCapabilityRegistry discovery, domain indexing, and risk tiers
- DependencyGraphAnalyzer cycle detection and topological ordering
- 23 Canonical Engineering Domains and project type resolution
- EngineeringRoleRegistry workforce mapping and task matching
- EngineeringSkillRegistry and TechnologyCatalogRegistry
- WorkflowEngine 10-stage lifecycle and state persistence
- STRIDEThreatModeler planning threat matrices
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.openclone.core.system import OpenCloneCore, SystemState, SystemEvent
from src.openclone.core.modules import ModuleManager, ModuleState, ModuleMetadata
from src.openclone.core.capabilities import UnifiedCapabilityRegistry, CoreCapability
from src.openclone.core.dependencies import DependencyGraphAnalyzer, DependencyType
from src.openclone.engineering.taxonomy import EngineeringDomain, EngineeringDomainRegistry
from src.openclone.engineering.roles import EngineeringRoleRegistry
from src.openclone.engineering.skills import EngineeringSkillRegistry
from src.openclone.engineering.technologies import TechnologyCatalogRegistry, TechnologyCategory
from src.openclone.engineering.graph import KnowledgeGraphEngine
from src.openclone.workflow.engine import WorkflowEngine, WorkflowStage, StageStatus
from src.openclone.security.threat_model import STRIDEThreatModeler, ThreatCategory, ThreatSeverity


class TestCoreArchitectureEvolution(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace_root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    # 1. Core System Tests
    def test_core_system_lifecycle_and_event_bus(self):
        core = OpenCloneCore(self.workspace_root)
        self.assertEqual(core.state, SystemState.BOOTSTRAP)

        events_received = []
        core.event_bus.subscribe("test:event", lambda e: events_received.append(e))
        core.event_bus.publish(SystemEvent("test:event", "test_unit", {"foo": "bar"}))

        self.assertEqual(len(events_received), 1)
        self.assertEqual(events_received[0].payload["foo"], "bar")

        core.transition_state(SystemState.READY, "Initialization complete")
        self.assertEqual(core.state, SystemState.READY)

        health = core.health_check()
        self.assertEqual(health["status"], "HEALTHY")

    # 2. Module Management Engine Tests
    def test_module_manager_lifecycle_and_rollback(self):
        mm = ModuleManager(self.workspace_root)
        modules = mm.list_modules()
        self.assertGreaterEqual(len(modules), 10)

        # Register dynamic test module
        test_meta = ModuleMetadata(
            module_id="test.module.dynamic",
            name="Dynamic Test Module",
            dependencies=["openclone.core"],
        )
        mm.modules["test.module.dynamic"] = test_meta

        self.assertTrue(mm.validate_module("test.module.dynamic"))
        self.assertEqual(test_meta.state, ModuleState.VALIDATED)

        mm.rollback_module("test.module.dynamic")
        self.assertEqual(test_meta.state, ModuleState.ROLLED_BACK)

    # 3. Unified Capability Management Tests
    def test_unified_capability_registry(self):
        caps = UnifiedCapabilityRegistry()
        all_caps = caps.list_capabilities()
        self.assertGreaterEqual(len(all_caps), 8)

        # Match capabilities
        matched = caps.match_capabilities(["reverse", "ast"])
        self.assertTrue(any("reverse" in c.capability_id for c in matched))

    # 4. Dependency Graph Analyzer Tests
    def test_dependency_graph_analyzer_cycles_and_order(self):
        analyzer = DependencyGraphAnalyzer()
        analyzer.add_node("A", dependencies=["B"])
        analyzer.add_node("B", dependencies=["C"])
        analyzer.add_node("C", dependencies=[])

        cycles = analyzer.detect_cycles()
        self.assertEqual(len(cycles), 0)

        order = analyzer.topological_order()
        self.assertEqual(order, ["C", "B", "A"])

        # Test cycle detection
        analyzer.add_node("C", dependencies=["A"])
        cycles = analyzer.detect_cycles()
        self.assertGreaterEqual(len(cycles), 1)

    # 5. 23 Canonical Engineering Domains Tests
    def test_engineering_domains_taxonomy(self):
        dom_reg = EngineeringDomainRegistry()
        self.assertEqual(len(dom_reg.domains), 23)

        # Check resolution for SaaS
        saas_doms = dom_reg.resolve_domains_for_project_type("Multi-Tenant AI SaaS")
        self.assertIn(EngineeringDomain.DOMAIN_01_PRODUCT, saas_doms)
        self.assertIn(EngineeringDomain.DOMAIN_06_BACKEND, saas_doms)
        self.assertIn(EngineeringDomain.DOMAIN_08_DATABASE, saas_doms)
        self.assertIn(EngineeringDomain.DOMAIN_11_AI, saas_doms)
        self.assertIn(EngineeringDomain.DOMAIN_12_SECURITY, saas_doms)
        self.assertIn(EngineeringDomain.DOMAIN_23_GOVERNANCE, saas_doms)

    # 6. Workforce Role & Skill Registry Tests
    def test_engineering_role_and_skill_registries(self):
        role_reg = EngineeringRoleRegistry()
        self.assertGreaterEqual(len(role_reg.roles), 70)

        # Verify task matching
        worker_for_ui = role_reg.match_role_for_task("Implement Tailwind Navigation UI")
        self.assertEqual(worker_for_ui, "frontend-engineer")

        worker_for_db = role_reg.match_role_for_task("Create PostgreSQL Database Schema")
        self.assertEqual(worker_for_db, "database-engineer")

        worker_for_sec = role_reg.match_role_for_task("STRIDE Threat Vector Analysis")
        self.assertEqual(worker_for_sec, "security-engineer")

        skill_reg = EngineeringSkillRegistry()
        skills = skill_reg.list_skills()
        self.assertGreaterEqual(len(skills), 5)

    # 7. Technology Catalog Tests
    def test_technology_catalog_registry(self):
        tech_reg = TechnologyCatalogRegistry()
        items = tech_reg.list_technologies()
        self.assertGreaterEqual(len(items), 5)

        pg = tech_reg.get_technology("tech.db.postgresql")
        self.assertIsNotNone(pg)
        self.assertEqual(pg.category, TechnologyCategory.DATABASE)
        self.assertIn("Row-Level Security (RLS)", pg.strengths)

    # 8. Relational Graph Traversals
    def test_relational_knowledge_graph(self):
        kg = KnowledgeGraphEngine()
        pkg = kg.recommend_engineering_package("AI SaaS Platform")
        self.assertEqual(pkg["project_type"], "AI SaaS Platform")
        self.assertGreaterEqual(pkg["active_domain_count"], 10)
        self.assertIn("principal-architect", pkg["recommended_roles"])

    # 9. 10-Stage Workflow Engine Tests
    def test_workflow_engine_lifecycle_and_persistence(self):
        wf = WorkflowEngine(self.workspace_root, workflow_id="wf-test-01")
        self.assertEqual(wf.current_stage, WorkflowStage.REQUEST)

        wf.advance_stage(WorkflowStage.REQUEST, StageStatus.COMPLETED, {"prompt": "Build service"})
        wf.advance_stage(WorkflowStage.UNDERSTANDING, StageStatus.COMPLETED, {"intent": "feature"})

        summary = wf.get_progress_summary()
        self.assertEqual(summary["completed_stages"], 2)
        self.assertFalse(summary["is_complete"])

        # Test state reload
        wf2 = WorkflowEngine(self.workspace_root, workflow_id="wf-test-01")
        loaded = wf2.load_state()
        self.assertTrue(loaded)
        self.assertEqual(wf2.current_stage, WorkflowStage.UNDERSTANDING)
        self.assertEqual(wf2.checkpoints[WorkflowStage.REQUEST].status, StageStatus.COMPLETED)

    # 10. STRIDE Threat Modeler Tests
    def test_stride_threat_modeler(self):
        threat_report = STRIDEThreatModeler.evaluate(
            project_name="FinTechApp",
            architecture_pattern="Modular Monolith",
            has_auth=True,
            is_multi_tenant=True,
        )
        self.assertGreaterEqual(threat_report["total_threats"], 6)
        categories = {t["category"] for t in threat_report["threats"]}
        self.assertIn(ThreatCategory.SPOOFING.value, categories)
        self.assertIn(ThreatCategory.TAMPERING.value, categories)
        self.assertIn(ThreatCategory.ELEVATION_OF_PRIVILEGE.value, categories)


if __name__ == "__main__":
    unittest.main()
