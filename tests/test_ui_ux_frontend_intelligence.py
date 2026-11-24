"""Exhaustive test suite for OpenClone UI/UX and Frontend Engineering Intelligence.
Covers foundation, 5 specialist skills, 17 scenario classifications, dependency
resolution, application states, and regression protection.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from src.openclone.skills.engine import (
    ApplicationState,
    ApplicationStateManager,
    ProjectArchetype,
    ProjectArchetypeClassifier,
    Skill,
    SkillMaturity,
    SkillRegistry,
    SkillReportGenerator,
    SkillSelector,
    SkillStatus,
)
from src.openclone.frontend import (
    FrontendQualityGate,
    ComponentState,
    evaluate_component_states,
    ResponsiveMatrixAuditor,
    ViewportCategory,
    AccessibilityAuditor,
    WCAGRule,
    FrontendSecurityAuditor,
    PerformanceBudgetAuditor,
    DesignTokenManager,
    TokenHierarchy,
    FrontendLifecycleWorkflow,
    WorkflowPhase,
)


class TestSkillFoundation(unittest.TestCase):
    """Foundation tests for discovery, paths, manifests, loading, and precedence."""

    def setUp(self):
        self.registry = SkillRegistry(root=ROOT)
        self.selector = SkillSelector(registry=self.registry)

    def test_discovery_all_12_skills(self):
        skills = self.registry.list_all()
        self.assertGreaterEqual(len(skills), 12)
        expected_ids = {
            "saas-security-baseline",
            "ux-pro",
            "taste-skill",
            "design-system-engineering",
            "responsive-engineering",
            "strix-pentest-adapter",
            "accessibility-engineering",
            "frontend-engineering",
            "typography-standards",
            "backend-architecture",
            "ai-context-engineering",
            "motion-design",
        }
        actual_ids = {s.id for s in skills}
        self.assertTrue(expected_ids.issubset(actual_ids))

    def test_all_paths_resolve_on_disk(self):
        errors = self.registry.validate_all()
        self.assertEqual(errors, [], f"Expected 0 path resolution errors, found: {errors}")

    def test_skill_loading_and_manifest_parsing(self):
        for s in self.registry.list_all():
            loaded = self.registry.load(s.id)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.skill_id, s.id)
            self.assertTrue(loaded.resolved_path.exists())
            self.assertGreater(len(loaded.body), 50)
            self.assertIn(loaded.maturity, [SkillMaturity.L3_LOADABLE, SkillMaturity.L5_VERIFIED])

    def test_missing_skill_handling(self):
        self.assertIsNone(self.registry.get("non-existent-skill"))
        with self.assertRaises(KeyError):
            self.registry.load("non-existent-skill")

    def test_skill_maturity_tracking(self):
        for s in self.registry.list_all():
            self.assertIn(
                s.maturity,
                [SkillMaturity.L0_NOT_IMPLEMENTED, SkillMaturity.L1_DEFINED, SkillMaturity.L2_REGISTERED,
                 SkillMaturity.L3_LOADABLE, SkillMaturity.L4_EXECUTABLE, SkillMaturity.L5_VERIFIED],
            )
            self.assertEqual(s.maturity, SkillMaturity.L5_VERIFIED)

    def test_dependency_resolution(self):
        # frontend-engineering has dependencies: [responsive-engineering, accessibility-engineering]
        res = self.selector.select("Implement Next.js component state and routing")
        selected_ids = [s.id for s in res["selected_skills"]]
        self.assertIn("frontend-engineering", selected_ids)
        self.assertIn("responsive-engineering", selected_ids)
        self.assertIn("accessibility-engineering", selected_ids)
        self.assertTrue(len(res["dependencies_resolved"]) >= 1)

    def test_strict_precedence_ordering(self):
        res = self.selector.select("Build SaaS analytics command center with auth, components, responsive layout, and charts")
        selected_ids = [s.id for s in res["selected_skills"]]
        # Security (5) < UX Pro (8) < Taste Skill (10) < Design System (12) < Responsive (14) < A11y (16) < Frontend (18)
        self.assertLess(selected_ids.index("saas-security-baseline"), selected_ids.index("ux-pro"))
        self.assertLess(selected_ids.index("ux-pro"), selected_ids.index("taste-skill"))
        self.assertLess(selected_ids.index("taste-skill"), selected_ids.index("design-system-engineering"))
        self.assertLess(selected_ids.index("design-system-engineering"), selected_ids.index("responsive-engineering"))
        self.assertLess(selected_ids.index("responsive-engineering"), selected_ids.index("accessibility-engineering"))
        self.assertLess(selected_ids.index("accessibility-engineering"), selected_ids.index("frontend-engineering"))


class TestSpecialistSkillsDefinitions(unittest.TestCase):
    """Tests confirming all 5 new specialist skills have complete contracts."""

    def setUp(self):
        self.registry = SkillRegistry(root=ROOT)

    def test_ux_pro_skill_contract(self):
        skill = self.registry.get("ux-pro")
        self.assertIsNotNone(skill)
        self.assertEqual(skill.category, "ux")
        self.assertEqual(skill.precedence, 8)
        self.assertTrue(len(skill.required_actions) >= 4)
        self.assertTrue(len(skill.pre_build_gates) >= 2)
        self.assertTrue(len(skill.finish_gates) >= 2)

    def test_design_system_engineering_contract(self):
        skill = self.registry.get("design-system-engineering")
        self.assertIsNotNone(skill)
        self.assertEqual(skill.category, "design")
        self.assertEqual(skill.precedence, 12)
        self.assertTrue(any("token" in a.lower() for a in skill.required_actions))
        self.assertTrue(any("variant" in g.lower() for g in skill.finish_gates))

    def test_responsive_engineering_contract(self):
        skill = self.registry.get("responsive-engineering")
        self.assertIsNotNone(skill)
        self.assertEqual(skill.category, "frontend")
        self.assertEqual(skill.precedence, 14)
        self.assertTrue(any("44" in a for a in skill.required_actions))
        self.assertTrue(any("overflow" in g.lower() for g in skill.finish_gates))

    def test_accessibility_engineering_contract(self):
        skill = self.registry.get("accessibility-engineering")
        self.assertIsNotNone(skill)
        self.assertEqual(skill.category, "accessibility")
        self.assertEqual(skill.precedence, 16)
        self.assertTrue(any("wcag" in a.lower() for a in skill.required_actions))
        self.assertTrue(any("keyboard" in g.lower() for g in skill.finish_gates))

    def test_frontend_engineering_contract(self):
        skill = self.registry.get("frontend-engineering")
        self.assertIsNotNone(skill)
        self.assertEqual(skill.category, "frontend")
        self.assertEqual(skill.precedence, 18)
        self.assertIn("responsive-engineering", skill.dependencies)
        self.assertIn("accessibility-engineering", skill.dependencies)


class TestProjectArchetypesAndStates(unittest.TestCase):
    """Tests archetype classification and mandatory application states."""

    def test_archetype_classification(self):
        self.assertIn(ProjectArchetype.SAAS, ProjectArchetypeClassifier.classify("Build modern SaaS subscription platform"))
        self.assertIn(ProjectArchetype.LANDING_PAGE, ProjectArchetypeClassifier.classify("Create high-converting landing page"))
        self.assertIn(ProjectArchetype.ADMIN_DASHBOARD, ProjectArchetypeClassifier.classify("Internal admin console with metrics"))
        self.assertIn(ProjectArchetype.ECOMMERCE, ProjectArchetypeClassifier.classify("E-commerce storefront with shopping cart"))
        self.assertIn(ProjectArchetype.MOBILE_APPLICATION, ProjectArchetypeClassifier.classify("Mobile app for iOS and Android"))

    def test_mandatory_application_states_coverage(self):
        states = ApplicationStateManager.get_recommended_states(ProjectArchetype.SAAS, feature="User project list and creation form")
        self.assertIn(ApplicationState.INITIAL, states)
        self.assertIn(ApplicationState.LOADING, states)
        self.assertIn(ApplicationState.SUCCESS, states)
        self.assertIn(ApplicationState.EMPTY, states)
        self.assertIn(ApplicationState.ERROR, states)
        self.assertIn(ApplicationState.SUBMITTING, states)
        self.assertIn(ApplicationState.VALIDATION_ERROR, states)
        self.assertIn(ApplicationState.UNAUTHORIZED, states)
        self.assertIn(ApplicationState.SESSION_EXPIRED, states)


class TestAll17Scenarios(unittest.TestCase):
    """Tests skill selection accuracy across all 17 mandatory scenarios."""

    def setUp(self):
        self.registry = SkillRegistry(root=ROOT)
        self.selector = SkillSelector(registry=self.registry)

    # 1. Responsive SaaS landing page
    def test_scenario_01_responsive_saas_landing_page(self):
        res = self.selector.select("Build a responsive SaaS landing page with hero entrance and conversion CTA")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("taste-skill", ids)
        self.assertIn("responsive-engineering", ids)
        self.assertIn("ux-pro", ids)

    # 2. SaaS admin dashboard
    def test_scenario_02_saas_admin_dashboard(self):
        res = self.selector.select("Build a SaaS admin dashboard with user management and metric cards")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("ux-pro", ids)
        self.assertIn("design-system-engineering", ids)
        self.assertIn("responsive-engineering", ids)
        self.assertIn("saas-security-baseline", ids)

    # 3. Complex analytics dashboard
    def test_scenario_03_analytics_dashboard(self):
        res = self.selector.select("Build an analytics dashboard with interactive charts, telemetry, and date filters")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("ux-pro", ids)
        self.assertIn("design-system-engineering", ids)
        self.assertIn("frontend-engineering", ids)

    # 4. E-commerce storefront
    def test_scenario_04_ecommerce_storefront(self):
        res = self.selector.select("Build an e-commerce shop storefront with products grid and checkout cart")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("ux-pro", ids)
        self.assertIn("frontend-engineering", ids)
        self.assertIn("responsive-engineering", ids)

    # 5. Mobile-first PWA
    def test_scenario_05_mobile_first_pwa(self):
        res = self.selector.select("Build a mobile-first PWA with offline caching and touch drawer navigation")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("responsive-engineering", ids)
        self.assertIn("accessibility-engineering", ids)

    # 6. Flutter application
    def test_scenario_06_flutter_application(self):
        res = self.selector.select("Create a cross-platform Flutter mobile app with local SQLite cache")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("responsive-engineering", ids)
        self.assertIn("ux-pro", ids)

    # 7. Enterprise ERP interface
    def test_scenario_07_enterprise_erp_interface(self):
        res = self.selector.select("Develop enterprise ERP workflows with multi-step transaction approval forms and RBAC")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("saas-security-baseline", ids)
        self.assertIn("ux-pro", ids)
        self.assertIn("frontend-engineering", ids)

    # 8. Authentication and onboarding flow
    def test_scenario_08_auth_onboarding_flow(self):
        res = self.selector.select("Design a multi-step user onboarding flow with authentication and account setup")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("ux-pro", ids)
        self.assertIn("saas-security-baseline", ids)

    # 9. Accessible form
    def test_scenario_09_accessible_form(self):
        res = self.selector.select("Implement an accessible registration form with WCAG contrast, aria live regions, and screen reader labels")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("accessibility-engineering", ids)
        self.assertIn("frontend-engineering", ids)

    # 10. Responsive data table
    def test_scenario_10_responsive_data_table(self):
        res = self.selector.select("Create a responsive data table with mobile card breakdown, horizontal touch scrolling, and pagination")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("responsive-engineering", ids)
        self.assertIn("design-system-engineering", ids)

    # 11. Component library creation
    def test_scenario_11_component_library_creation(self):
        res = self.selector.select("Build a reusable UI component library with primitives, variants, and state contracts")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("design-system-engineering", ids)
        self.assertIn("frontend-engineering", ids)

    # 12. Design system implementation
    def test_scenario_12_design_system_implementation(self):
        res = self.selector.select("Define semantic design tokens for color palette, dark mode theme, typography scale, and spacing tokens")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("design-system-engineering", ids)
        self.assertIn("typography-standards", ids)

    # 13. Accessibility remediation
    def test_scenario_13_accessibility_remediation(self):
        res = self.selector.select("Fix accessibility violations: modal focus trapping, color contrast, and missing aria landmarks")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("accessibility-engineering", ids)

    # 14. Frontend performance optimization
    def test_scenario_14_frontend_performance_optimization(self):
        res = self.selector.select("Optimize React client-side rendering performance, code splitting, and reduce layout thrashing")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("frontend-engineering", ids)

    # 15. Existing application redesign
    def test_scenario_15_existing_application_redesign(self):
        res = self.selector.select("Redesign existing web app interface to remove AI slop and establish modern visual hierarchy")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("taste-skill", ids)
        self.assertIn("ux-pro", ids)

    # 16. Minor CSS bug fix (Micro-fix)
    def test_scenario_16_minor_css_bug_fix(self):
        res = self.selector.select("Fix mobile overflow issue on header navigation bar")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("responsive-engineering", ids)

    # 17. Backend-only task with no frontend requirement
    def test_scenario_17_backend_only_task(self):
        res = self.selector.select("Design PostgreSQL database schema migrations and Redis cache invalidation (backend-only, no-ui)")
        ids = [s.id for s in res["selected_skills"]]
        self.assertIn("backend-architecture", ids)
        self.assertNotIn("taste-skill", ids)
        self.assertNotIn("ux-pro", ids)
        self.assertNotIn("frontend-engineering", ids)
        self.assertNotIn("responsive-engineering", ids)


class TestReportingAndLedger(unittest.TestCase):
    """Tests markdown reporting and traceable execution ledger outputs."""

    def setUp(self):
        self.registry = SkillRegistry(root=ROOT)
        self.selector = SkillSelector(registry=self.registry)

    def test_selection_report_generation(self):
        res = self.selector.select("Build SaaS command center with responsive charts and dark mode")
        report = SkillReportGenerator.generate_selection_report("TASK-DASH-01", res)
        self.assertIn("# SKILL_SELECTION_REPORT — Task TASK-DASH-01", report)
        self.assertIn("Selected Skills", report)
        self.assertIn("Skipped Skills", report)
        self.assertIn("Precedence Ordered", report)

    def test_application_report_generation(self):
        records = [
            {
                "skill_id": "ux-pro",
                "reason": "Map user journeys",
                "source": "framework/skills/ux-pro/SKILL.md",
                "actions_completed": "Mapped primary and error recovery flows",
                "evidence": "Usability inspection pass",
                "status": SkillStatus.APPLIED,
            },
            {
                "skill_id": "responsive-engineering",
                "reason": "11-tier matrix verification",
                "source": "framework/skills/responsive-engineering/SKILL.md",
                "actions_completed": "Verified 320px to 1440px+ without horizontal overflow",
                "evidence": "Zero scrollWidth overflow verified",
                "status": SkillStatus.APPLIED,
            },
        ]
        report = SkillReportGenerator.generate_application_report("TASK-DASH-01", records)
        self.assertIn("# SKILL_APPLICATION_REPORT — Task TASK-DASH-01", report)
        self.assertIn("`ux-pro`", report)
        self.assertIn("`responsive-engineering`", report)
        self.assertIn("`APPLIED`", report)

    def test_lifecycle_governance_report_generation(self):
        res = self.selector.select("Build SaaS admin dashboard")
        states = ApplicationStateManager.get_recommended_states(ProjectArchetype.SAAS)
        report = SkillReportGenerator.generate_lifecycle_report("PULSE SaaS", [ProjectArchetype.SAAS], res, states)
        self.assertIn("# LIFECYCLE_GOVERNANCE_REPORT — PULSE SaaS", report)
        self.assertIn("Mandatory Application States Coverage", report)
        self.assertIn("Pre-Build and Finish Quality Gates", report)
        self.assertIn("`LOADING`", report)
        self.assertIn("`EMPTY`", report)
        self.assertIn("`ERROR`", report)


class TestFrontendRuntimeIntelligence(unittest.TestCase):
    """Verifies deterministic Python modules for quality gates, responsive, a11y, security, performance, and tokens."""

    def test_frontend_quality_gates_and_scorecard(self):
        gate_engine = FrontendQualityGate()
        # All 15 gates passed
        criteria = {f"GATE-{i:02d}": True for i in range(1, 16)}
        scorecard = gate_engine.evaluate_all(criteria)
        self.assertEqual(scorecard.total_gates, 15)
        self.assertEqual(scorecard.passed_gates, 15)
        self.assertEqual(scorecard.failed_gates, 0)
        self.assertEqual(scorecard.compliance_score, 100.0)
        self.assertEqual(scorecard.verdict, "PRODUCTION_READY")

    def test_component_states_evaluation(self):
        # Interactive button with core 5 states
        button_states = {
            ComponentState.DEFAULT,
            ComponentState.HOVER,
            ComponentState.FOCUS,
            ComponentState.ACTIVE,
            ComponentState.DISABLED,
        }
        res = evaluate_component_states(button_states)
        self.assertTrue(res["is_core_complete"])
        self.assertFalse(res["is_full_lifecycle"])
        self.assertEqual(len(res["missing_core_states"]), 0)

        # Full lifecycle component (with loading, empty, error, success)
        data_table_states = button_states.union({
            ComponentState.LOADING,
            ComponentState.SUCCESS,
            ComponentState.ERROR,
            ComponentState.EMPTY,
            ComponentState.SELECTED,
        })
        res_full = evaluate_component_states(data_table_states)
        self.assertTrue(res_full["is_core_complete"])
        self.assertTrue(res_full["is_full_lifecycle"])
        self.assertEqual(res_full["coverage_ratio"], 1.0)

    def test_responsive_matrix_auditor(self):
        auditor = ResponsiveMatrixAuditor()
        # Default all passing
        audit_res = auditor.evaluate_matrix()
        self.assertTrue(audit_res.is_fully_responsive)
        self.assertEqual(audit_res.passed_viewports, len(ViewportCategory))

        # Viewport with horizontal overflow failure
        obs = {
            ViewportCategory.SMALL_MOBILE: {"has_overflow": True, "min_touch_px": 32, "usable": False, "nav_ok": True}
        }
        failing_res = auditor.evaluate_matrix(obs)
        self.assertFalse(failing_res.is_fully_responsive)
        self.assertEqual(failing_res.failed_viewports, 1)

    def test_accessibility_auditor_wcag(self):
        auditor = AccessibilityAuditor()
        # Clean audit
        res = auditor.run_audit()
        self.assertTrue(res.is_wcag_aa_compliant)
        self.assertEqual(res.score, 100.0)

        # Audit with contrast and keyboard traps
        res_flaws = auditor.run_audit({
            WCAGRule.CONTRAST_MINIMUM: ["Header subtitle contrast is 2.8:1, requires 4.5:1"],
            WCAGRule.NO_KEYBOARD_TRAP: ["Focus trap in newsletter dialog fails on Escape key"],
        })
        self.assertFalse(res_flaws.is_wcag_aa_compliant)
        self.assertEqual(res_flaws.failed_rules, 2)
        self.assertLess(res_flaws.score, 100.0)

    def test_frontend_security_auditor(self):
        auditor = FrontendSecurityAuditor()
        # Insecure snippet with exposed token
        insecure_code = """
        const apiKey = "api_key = 'abcdef1234567890abcdef1234567890'";
        const db = process.env.DATABASE_URL;
        """
        findings = auditor.audit_code_snippet(insecure_code, "insecure_client.tsx")
        self.assertGreaterEqual(len(findings), 2)
        audit_res = auditor.evaluate(findings)
        self.assertFalse(audit_res.is_secure)
        self.assertGreater(audit_res.critical_count, 0)

        # CSP check
        csp_findings = auditor.audit_csp_policy("script-src 'self' 'unsafe-eval' 'unsafe-inline'")
        self.assertEqual(len(csp_findings), 2)

    def test_performance_budget_auditor(self):
        auditor = PerformanceBudgetAuditor()
        # Optimal performance
        res = auditor.audit_vitals(lcp=1.8, inp=90.0, cls=0.04, bundle_kb=150.0)
        self.assertTrue(res.all_metrics_passed)
        self.assertEqual(res.score, 100.0)

        # Exceeding budget
        res_slow = auditor.audit_vitals(lcp=3.6, inp=350.0, cls=0.22, bundle_kb=450.0)
        self.assertFalse(res_slow.all_metrics_passed)
        self.assertEqual(res_slow.failed_metrics, 4)

    def test_design_token_manager_hierarchy(self):
        dtm = DesignTokenManager()
        dtm.register_primitive("color.slate.900", "#0f172a", "Deep neutral surface")
        dtm.register_semantic("color.surface.canvas", "color.slate.900", description="App canvas")
        dtm.register_component_token("card.surface", "color.surface.canvas", description="Card background")

        audit = dtm.validate_architecture()
        self.assertTrue(audit["is_valid"])
        self.assertEqual(audit["primitive_count"], 1)
        self.assertEqual(audit["semantic_count"], 1)
        self.assertEqual(audit["component_count"], 1)

    def test_frontend_lifecycle_workflow_18_stages(self):
        workflow = FrontendLifecycleWorkflow("PROJ-SAAS-001")
        # Full happy path
        res = workflow.execute_lifecycle(
            project_type="SaaS Application",
            requirements=["Multi-tenant workspace", "Responsive data table", "WCAG 2.2 AA"],
            has_human_approval=True,
        )
        self.assertTrue(res.is_success)
        self.assertEqual(res.completed_phases, 18)
        self.assertEqual(res.verdict, "VERIFIED_DELIVERY")

        # Stopped at human approval gate
        res_blocked = workflow.execute_lifecycle(
            project_type="SaaS Application",
            requirements=["Admin dashboard"],
            has_human_approval=False,
        )
        self.assertFalse(res_blocked.is_success)
        self.assertIn("HALTED_AT", res_blocked.verdict)


if __name__ == "__main__":
    unittest.main()
