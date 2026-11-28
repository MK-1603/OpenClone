"""Unit & Integration Tests for OpenClone Universal Engineering Intelligence System.

Verifies:
- Complete 155 Engineering Disciplines Registry and coverage.
- Canonical Engineering Domains and Subdomains.
- Engineering Knowledge Catalogue & Decision Intelligence Trade-Offs.
- Engineering Domain Aliases & Bridge (Folders, EIS Sectors, Classifier Signatures).
- Dynamic Engineering Domain Activation Engine.
- Hardened Phase 0 Boundary on OpenClonePlannerAgent (execute=True fails closed).
"""
from __future__ import annotations

import unittest
from pathlib import Path

from src.openclone.engineering.taxonomy import EngineeringDomain, EngineeringDomainRegistry
from src.openclone.engineering.disciplines import EngineeringDisciplineRegistry
from src.openclone.engineering.aliases import EngineeringDomainBridge
from src.openclone.engineering.knowledge import EngineeringKnowledgeCatalogue, ConceptType
from src.openclone.engineering.activation import DynamicDomainActivationEngine, ActivationLevel
from src.openclone.planning.agent import OpenClonePlannerAgent


class TestUniversalEngineeringIntelligence(unittest.TestCase):

    def setUp(self):
        self.domain_reg = EngineeringDomainRegistry()
        self.disc_reg = EngineeringDisciplineRegistry()
        self.catalog = EngineeringKnowledgeCatalogue()
        self.activation_engine = DynamicDomainActivationEngine()
        self.planner = OpenClonePlannerAgent()

    # 1. 155 Disciplines Verification
    def test_complete_discipline_catalogue_count(self):
        disciplines = self.disc_reg.list_disciplines()
        self.assertEqual(len(disciplines), 155)

        # Check coverage of key groups
        req_discs = self.disc_reg.list_disciplines(EngineeringDomain.DOMAIN_02_REQUIREMENTS)
        self.assertGreaterEqual(len(req_discs), 8)

        arch_discs = self.disc_reg.list_disciplines(EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE)
        self.assertGreaterEqual(len(arch_discs), 8)

        ai_discs = self.disc_reg.list_disciplines(EngineeringDomain.DOMAIN_11_AI)
        self.assertGreaterEqual(len(ai_discs), 15)

        sec_discs = self.disc_reg.list_disciplines(EngineeringDomain.DOMAIN_12_SECURITY)
        self.assertGreaterEqual(len(sec_discs), 8)

    # 2. Bridge & Aliases Verification
    def test_domain_bridge_aliases(self):
        # 31 Framework folders resolution
        self.assertEqual(
            EngineeringDomainBridge.resolve_folder("08-SOFTWARE-ARCHITECTURE"),
            EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE,
        )
        self.assertEqual(
            EngineeringDomainBridge.resolve_folder("14-SECURITY-AND-PRIVACY"),
            EngineeringDomain.DOMAIN_12_SECURITY,
        )
        self.assertEqual(
            EngineeringDomainBridge.resolve_folder("00-GOVERNANCE"),
            EngineeringDomain.DOMAIN_23_GOVERNANCE,
        )

        # 17 EIS sectors resolution
        self.assertEqual(
            EngineeringDomainBridge.resolve_eis_sector("EIS-04"),
            EngineeringDomain.DOMAIN_09_SOFTWARE_ARCHITECTURE,
        )
        self.assertEqual(
            EngineeringDomainBridge.resolve_eis_sector("EIS-11"),
            EngineeringDomain.DOMAIN_12_SECURITY,
        )

        # Classifier signature resolution
        web_doms = EngineeringDomainBridge.resolve_classifier_family("web_engineering")
        self.assertIn(EngineeringDomain.DOMAIN_05_FRONTEND, web_doms)

    # 3. Knowledge Catalog & Decision Intelligence
    def test_knowledge_catalog_and_decisions(self):
        microservices = self.catalog.get_concept("concept.arch.microservices")
        self.assertIsNotNone(microservices)
        self.assertEqual(microservices.concept_type, ConceptType.ARCHITECTURE_STYLE)

        dec = microservices.decision_record
        self.assertIsNotNone(dec)
        self.assertIn("Modular Monolith", [self.catalog.get_concept(a).name for a in dec.alternatives if self.catalog.get_concept(a)])
        self.assertGreaterEqual(len(dec.applicable_when), 1)
        self.assertGreaterEqual(len(dec.avoid_when), 1)

    # 4. Dynamic Domain Activation
    def test_dynamic_domain_activation_scenarios(self):
        # Scenario A: AI Agent Platform
        ai_report = self.activation_engine.activate_domains_for_project(
            prompt="Build an autonomous AI agent swarm with RAG and vector database",
            project_name="AIAgentSwarm",
        )
        self.assertIn(EngineeringDomain.DOMAIN_11_AI, ai_report.primary_domains)
        self.assertIn(EngineeringDomain.DOMAIN_08_DATABASE, ai_report.primary_domains)
        self.assertIn(EngineeringDomain.DOMAIN_13_MOBILE, ai_report.inactive_domains)

        # Scenario B: Mobile Fintech
        fintech_report = self.activation_engine.activate_domains_for_project(
            prompt="Develop an iOS and Android mobile app for payments with Stripe and HIPAA compliance",
            project_name="FintechMobile",
        )
        self.assertIn(EngineeringDomain.DOMAIN_13_MOBILE, fintech_report.primary_domains)
        self.assertIn(EngineeringDomain.DOMAIN_12_SECURITY, fintech_report.primary_domains)
        self.assertIn(EngineeringDomain.DOMAIN_23_GOVERNANCE, fintech_report.primary_domains)

    # 5. Phase 0 Execution Boundary Hardening (execute=True fails closed)
    def test_phase0_execution_boundary_fails_closed(self):
        # 1. Direct plan_project terminates at planning with answers provided to bypass clarification
        answers = {"q1": "Static HTML/CSS website", "q2": "Individual developer", "q3": "GitHub Pages"}
        plan_res = self.planner.plan_project(
            prompt="Build a simple portfolio website",
            project_name="Portfolio",
            answers=answers,
        )
        self.assertEqual(plan_res["status"], "COMPLETED")
        self.assertEqual(plan_res["phase"], "PHASE_0_PLANNING_LOCKED")
        self.assertFalse(plan_res["executed"])

        # 2. plan_and_execute with execute=True fails closed
        exec_res = self.planner.plan_and_execute(
            prompt="Build a SaaS backend",
            project_name="SaaSBackend",
            answers=answers,
            execute=True,
        )
        self.assertFalse(exec_res["executed"])
        self.assertIsNotNone(exec_res.get("execution"))
        self.assertEqual(exec_res["execution"]["status"], "REJECTED_PHASE_0_BOUNDARY")


if __name__ == "__main__":
    unittest.main()
