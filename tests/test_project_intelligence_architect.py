import json
import tempfile
import unittest
from pathlib import Path

from src.openclone.intelligence.project_intelligence import (
    AIExecutionGuidance,
    DocumentAuthorityTier,
    EvidenceType,
    PIAMode,
    ProjectIntelligenceArchitect,
    SolutionStatus,
)
from src.openclone.intelligence.generator import ProjectPackageGenerator
from src.openclone.runtime.workforce import topo, load_workers


class TestProjectIntelligenceArchitectRole(unittest.TestCase):
    def setUp(self):
        self.pia = ProjectIntelligenceArchitect()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_pia_mode_normalization(self):
        self.assertEqual(PIAMode.from_string("PIA-NEW"), PIAMode.NEW)
        self.assertEqual(PIAMode.from_string("new"), PIAMode.NEW)
        self.assertEqual(PIAMode.from_string("PIA-DEFINED"), PIAMode.DEFINED)
        self.assertEqual(PIAMode.from_string("defined"), PIAMode.DEFINED)
        self.assertEqual(PIAMode.from_string("PIA-EVOLUTION"), PIAMode.EVOLUTION)
        self.assertEqual(PIAMode.from_string("evolution"), PIAMode.EVOLUTION)
        # Test backward-compatible alias
        self.assertEqual(PIAMode.from_string("PIA-EXISTING"), PIAMode.EVOLUTION)
        self.assertEqual(PIAMode.from_string("existing"), PIAMode.EVOLUTION)

        with self.assertRaises(ValueError):
            PIAMode.from_string("UNKNOWN-MODE")

    def test_pia_new_execution_four_sets(self):
        prompt = "Build a real-time collaborative task management SaaS platform with FastAPI and PostgreSQL."
        guidance = AIExecutionGuidance(
            doc_provider="google",
            doc_model_id="gemini-2.5-pro",
            impl_provider="anthropic",
            impl_model_id="claude-3-7-sonnet",
        )

        out_dir = self.base / "new_project"
        res = self.pia.execute_new(prompt, project_name="TaskManager", ai_guidance=guidance, output_dir=out_dir)

        self.assertEqual(res["mode"], "PIA-NEW")
        self.assertEqual(res["project_name"], "TaskManager")

        # ---------------------------------------------------------------------
        # SET A — FEATURE INTELLIGENCE
        # ---------------------------------------------------------------------
        self.assertIn("set_a_features", res)
        set_a = res["set_a_features"]
        self.assertIn("primary_archetype", set_a)
        self.assertEqual(set_a["primary_archetype"]["evidence_type"], EvidenceType.PROMPT_EXTRACTED.value)
        self.assertTrue(len(set_a["features"]) >= 3)
        feat_ids = [f["feature_id"] for f in set_a["features"]]
        self.assertIn("FEAT-001", feat_ids)
        self.assertIn("FEAT-002", feat_ids)
        categories = {f["category"] for f in set_a["features"]}
        self.assertIn("essential", categories)
        self.assertIn("advanced", categories)
        self.assertTrue(len(set_a["user_expectations"]) >= 1)
        self.assertTrue(len(set_a["competitor_capabilities"]) >= 1)

        # ---------------------------------------------------------------------
        # SET B — GAP & PROBLEM INTELLIGENCE
        # ---------------------------------------------------------------------
        self.assertIn("set_b_gaps_problems", res)
        set_b = res["set_b_gaps_problems"]
        self.assertTrue(set_b["total_gaps"] + set_b["total_problems"] >= 1)
        # Verify Set B items use GAP-xxx / PROB-xxx
        b_ids = [item["item_id"] for item in set_b["gaps_and_problems"]]
        self.assertTrue(any(bid.startswith("GAP-") or bid.startswith("PROB-") for bid in b_ids))
        # Ensure Set B is NOT Target Architecture
        for item in set_b["gaps_and_problems"]:
            self.assertIn(item["category"], [
                "scalability_problem", "security_weakness", "technical_limitation",
                "functional_gap", "architecture_debt", "product_weakness", "performance_issue"
            ])
            self.assertIn(item["evidence_type"], [
                EvidenceType.STATIC_INSPECTION.value,
                EvidenceType.AUTOMATED_SCAN.value,
                EvidenceType.ARCHITECTURE_DEBT.value,
            ])
            self.assertTrue(item.get("verified", False))

        # ---------------------------------------------------------------------
        # SET C — SOLUTION INTELLIGENCE (NEW)
        # ---------------------------------------------------------------------
        self.assertIn("set_c_solutions", res)
        set_c = res["set_c_solutions"]
        self.assertTrue(set_c["total_solutions"] >= 2)
        self.assertTrue(set_c["recommended_count"] >= 1)
        sol_list = set_c["solutions"]
        sol_ids = [s["solution_id"] for s in sol_list]
        self.assertIn("SOL-001", sol_ids)

        for sol in sol_list:
            self.assertTrue(sol["solution_id"].startswith("SOL-"))
            # Problem-to-solution traceability: target_id must reference Set B GAP/PROB or PROACTIVE_IMPROVEMENT
            self.assertTrue(
                sol["target_id"].startswith("GAP-") or
                sol["target_id"].startswith("PROB-") or
                sol["target_id"] == "PROACTIVE_IMPROVEMENT"
            )
            self.assertTrue(len(sol["problem_description"]) > 5)
            self.assertTrue(len(sol["proposed_solution"]) > 5)
            self.assertTrue(len(sol["expected_outcome"]) > 5)
            self.assertTrue(len(sol["business_user_value"]) > 5)
            self.assertIn(sol["complexity"], ["LOW", "MEDIUM", "HIGH"])
            self.assertIn(sol["status"], [
                SolutionStatus.PROPOSED.value,
                SolutionStatus.RECOMMENDED.value,
                SolutionStatus.ALTERNATIVE.value,
                SolutionStatus.APPROVED.value,
                SolutionStatus.REJECTED.value,
            ])
            self.assertTrue(len(sol["acceptance_criteria"]) >= 1)
            self.assertTrue(any(ac.startswith("AC-") for ac in sol["acceptance_criteria"]))

        # Verify proactive improvement exists
        proactive_solutions = [s for s in sol_list if s["target_id"] == "PROACTIVE_IMPROVEMENT"]
        self.assertTrue(len(proactive_solutions) >= 1)

        # ---------------------------------------------------------------------
        # SET D — FINAL PRODUCT INTELLIGENCE (CONSOLIDATION)
        # ---------------------------------------------------------------------
        self.assertIn("set_d_final_blueprint", res)
        set_d = res["set_d_final_blueprint"]
        self.assertEqual(len(set_d["feature_catalogue"]), len(set_a["features"]))
        self.assertEqual(len(set_d["gaps_and_problems"]), len(set_b["gaps_and_problems"]))
        self.assertEqual(len(set_d["solutions"]), len(set_c["solutions"]))
        self.assertTrue(set_d["traceability_verified"])
        self.assertTrue(len(set_d["traceability_matrix"]) >= 1)

        # Verify Generated Markdown Artifacts
        artifacts = res["artifacts"]
        self.assertIn("PROJECT.md", artifacts)
        self.assertIn("Project-Requirement.md", artifacts)
        self.assertIn("Features-List.md", artifacts)
        self.assertIn("Gaps-And-Problems.md", artifacts)
        self.assertIn("Solution-Blueprint.md", artifacts)
        self.assertIn("Tech-Stack.md", artifacts)
        self.assertIn("Decision-Log.md", artifacts)
        self.assertIn("Project-Details.md", artifacts)

        # Verify AI Metadata frontmatter in PROJECT.md
        self.assertIn("openclone_profile:", artifacts["PROJECT.md"])
        self.assertIn("gemini-2.5-pro", artifacts["PROJECT.md"])
        self.assertIn("claude-3-7-sonnet", artifacts["PROJECT.md"])

        # Verify written files on disk
        self.assertTrue((out_dir / "PROJECT.md").exists())
        self.assertTrue((out_dir / "Gaps-And-Problems.md").exists())
        self.assertTrue((out_dir / "Solution-Blueprint.md").exists())
        self.assertTrue((out_dir / "Project-Requirement.md").exists())
        self.assertTrue((out_dir / "Tech-Stack.md").exists())

        # Verify Two-Gate Phase Milestone Plan
        phase_plan = res["phase_plan"]
        self.assertTrue(len(phase_plan) >= 4)
        task_ids = [t["task_id"] for t in phase_plan]
        self.assertIn("PHASE-01-START", task_ids)
        self.assertIn("PHASE-01-COMPLETION", task_ids)
        self.assertIn("PHASE-02-START", task_ids)
        self.assertIn("PHASE-02-COMPLETION", task_ids)

        # Verify topological sort passes without circular dependencies
        ordered_ids = topo(phase_plan)
        self.assertEqual(len(ordered_ids), len(phase_plan))
        self.assertLess(ordered_ids.index("PHASE-01-START"), ordered_ids.index("TASK-01-01"))
        self.assertLess(ordered_ids.index("TASK-01-01"), ordered_ids.index("PHASE-01-COMPLETION"))
        self.assertLess(ordered_ids.index("PHASE-01-COMPLETION"), ordered_ids.index("PHASE-02-START"))

    def test_pia_defined_execution_with_four_sets(self):
        docs = {
            "PROJECT.md": "# Project\nDatabase: SQLite for embedded storage.",
            "Tech-Stack.md": "# Technologies\nDatabase: PostgreSQL cloud instance.",
        }

        res = self.pia.execute_defined(docs, project_name="ConflictApp")
        self.assertEqual(res["mode"], "PIA-DEFINED")
        self.assertIn("set_a_features", res)
        self.assertIn("set_b_gaps_problems", res)
        self.assertIn("set_c_solutions", res)
        self.assertIn("set_d_final_blueprint", res)

        conflicts = res["conflicts_detected"]
        self.assertTrue(len(conflicts) > 0)
        self.assertEqual(conflicts[0]["winner_doc"], "PROJECT.md (Tier 1)")
        self.assertEqual(conflicts[0]["loser_doc"], "Tech-Stack.md (Tier 4)")

        # Verify Gap in Set B for the conflict
        b_items = res["set_b_gaps_problems"]["gaps_and_problems"]
        self.assertTrue(any("GAP-CONF" in item["item_id"] for item in b_items))

        # Verify explicit ADR recorded in Decision-Log.md
        decision_log = res["harmonized_artifacts"]["Decision-Log.md"]
        self.assertIn("ADR-CONFLICT-001", decision_log)
        self.assertIn("Primary Database Selection", decision_log)

    def test_pia_evolution_execution_with_four_sets(self):
        # Create a mock codebase
        code_dir = self.base / "mock_repo"
        code_dir.mkdir()
        src_dir = code_dir / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text(
            "def handle(x):\n"
            "    if x > 10:\n"
            "        for i in range(x):\n"
            "            if i % 2 == 0:\n"
            "                print(i)\n",
            encoding="utf-8"
        )
        (src_dir / "utils.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")

        res = self.pia.execute_evolution(code_dir, project_name="LegacyApp")
        self.assertEqual(res["mode"], "PIA-EVOLUTION")
        self.assertEqual(res["files_analyzed"], 2)
        self.assertTrue(res["total_loc"] > 5)

        # Verify all four sets exist
        self.assertIn("set_a_features", res)
        self.assertIn("set_b_gaps_problems", res)
        self.assertIn("set_c_solutions", res)
        self.assertIn("set_d_final_blueprint", res)
        self.assertIn("evolution_plan", res)

        # Verify Set B contains verified static inspection findings
        b_items = res["set_b_gaps_problems"]["gaps_and_problems"]
        self.assertTrue(any(item["item_id"] == "PROB-001" for item in b_items))
        self.assertTrue(all(item["verified"] is True for item in b_items))

        # Verify Set C provides solutions for the code problems
        c_solutions = res["set_c_solutions"]["solutions"]
        self.assertTrue(any(s["target_id"] == "PROB-001" for s in c_solutions))

    def test_workforce_role_registration(self):
        worker_path = Path(__file__).resolve().parents[1] / "src" / "openclone" / "workforce" / "registry" / "workers" / "project-intelligence-architect.json"
        self.assertTrue(worker_path.exists())
        pia_worker = json.loads(worker_path.read_text(encoding="utf-8"))
        self.assertEqual(pia_worker["worker_id"], "project-intelligence-architect")
        self.assertEqual(pia_worker["team"], "architecture")
        self.assertIn("project_intelligence_architect", pia_worker["capabilities"])
        self.assertIn("observe", pia_worker["allowed_actions"])
        self.assertIn("analyze", pia_worker["allowed_actions"])
        self.assertIn("propose", pia_worker["allowed_actions"])
        self.assertIn("plan", pia_worker["allowed_actions"])
        self.assertIn("production_deploy", pia_worker["denied_actions"])
        self.assertIn("self_approve", pia_worker["denied_actions"])

    def test_generator_backward_compatibility(self):
        gen = ProjectPackageGenerator()
        pkg = gen.generate("Create an analytics dashboard in React with a Python FastAPI backend.", project_name="Analytics")

        # Must maintain existing return structure
        self.assertIn("profile", pkg)
        self.assertIn("technologies", pkg)
        self.assertIn("routing", pkg)
        self.assertIn("artifacts", pkg)

        artifacts = pkg["artifacts"]
        # Must retain all legacy keys
        self.assertIn("PROJECT.md", artifacts)
        self.assertIn("BUILD_PROMPT.md", artifacts)
        self.assertIn("AGENT_INSTRUCTIONS.md", artifacts)
        self.assertIn("IMPLEMENTATION_PLAN.md", artifacts)
        self.assertIn("ACCEPTANCE_MATRIX.md", artifacts)
        self.assertIn("SECURITY_PLAN.md", artifacts)
        self.assertIn("PROJECT-PROFILE.yaml", artifacts)
        self.assertIn(".env.example", artifacts)

        # Must also provide modular Set D keys including Set B and Set C specifications
        self.assertIn("Project-Requirement.md", artifacts)
        self.assertIn("Features-List.md", artifacts)
        self.assertIn("Gaps-And-Problems.md", artifacts)
        self.assertIn("Solution-Blueprint.md", artifacts)
        self.assertIn("Tech-Stack.md", artifacts)
        self.assertIn("Decision-Log.md", artifacts)
        self.assertIn("Project-Details.md", artifacts)

    def test_stage_1_system_design_and_diagrams_integration(self):
        """Verify Stage 1 wiring: CapacityEstimator, C4 diagrams, and ADR-003 in Set D."""
        prompt = "Enterprise multi-tenant banking platform with high availability, 50,000 DAU, and strict audit requirements."
        res = self.pia.execute_new(prompt, project_name="EnterpriseBank")

        artifacts = res["artifacts"]
        self.assertIn("System-Architecture.md", artifacts)
        sys_arch = artifacts["System-Architecture.md"]

        # 1. C4 Context & Container Diagrams (Mermaid syntax)
        self.assertIn("```mermaid", sys_arch)
        self.assertIn("C4 Context Diagram", sys_arch)
        self.assertIn("System Boundary: EnterpriseBank", sys_arch)

        # 2. Capacity & Sizing Projections (CapacityEstimator calculations)
        self.assertIn("# System Capacity & Sizing Estimation Report", sys_arch)
        self.assertIn("Daily Active Users", sys_arch)
        self.assertIn("Peak Overall RPS", sys_arch)

        # 3. Decision-Log ADR-003 (SystemDesignDecisionEngine)
        dec_log = artifacts["Decision-Log.md"]
        self.assertIn("ADR-003: Architectural Pattern Selection", dec_log)

        # 4. Set D blueprint metadata
        set_d = res["set_d_final_blueprint"]
        self.assertIn("architecture_recommendation", set_d)
        self.assertIn("capacity_report", set_d)
        self.assertIsNotNone(set_d["architecture_recommendation"]["primary_pattern"])

    def test_stage_1_omis_memory_gated_by_human_authorization(self):
        """Verify Stage 1: OMIS persistence occurs ONLY with explicit human approval and signed record."""
        p_def = {"project_id": "test_proj_001", "project_name": "SecureProject"}

        # Attempt without human authorization -> MUST BE SKIPPED
        skipped = self.pia.sync_to_memory(p_def, self.base, human_approved=False, approval_digest=None)
        self.assertEqual(skipped["status"], "SKIPPED")
        self.assertFalse(skipped["persisted"])

        # Attempt with human authorization but missing approval record -> MUST BE DENIED (no self-authorization)
        denied_no_record = self.pia.sync_to_memory(p_def, self.base, human_approved=True, approval_digest="a" * 64)
        self.assertEqual(denied_no_record["status"], "DENIED")
        self.assertFalse(denied_no_record["persisted"])
        self.assertIn("authentic signed approval record", denied_no_record["reason"])

    # -------------------------------------------------------------------------
    # DEFECT REMEDIATION VERIFICATION TESTS
    # -------------------------------------------------------------------------
    def test_defect_1_capacity_estimator_zero_invention_rule(self):
        """Defect 1: Verify missing workload parameters yield NOT_ESTIMATED without silent DAU injection."""
        from src.openclone.system_design.capacity import UnestimatedCapacityReport, ComprehensiveCapacityReport

        # 1. Missing workload parameters -> MUST produce UnestimatedCapacityReport (NOT_ESTIMATED)
        res_unestimated = self.pia.execute_new(
            "Build an internal admin dashboard for managing catalog items.",
            project_name="InternalCatalog",
        )
        set_c_unest = res_unestimated["set_c_solutions"]
        cap_report_unest = set_c_unest["capacity_report"]
        self.assertIsInstance(cap_report_unest, UnestimatedCapacityReport)
        self.assertEqual(cap_report_unest.status, "NOT_ESTIMATED")
        self.assertIn("NOT_ESTIMATED", set_c_unest["capacity_markdown"])
        self.assertIn("Missing Inputs Required for Quantitative Sizing", set_c_unest["capacity_markdown"])

        # Verify artifacts in Set D reflect NOT_ESTIMATED status
        sys_arch = res_unestimated["artifacts"]["System-Architecture.md"]
        self.assertIn("NOT_ESTIMATED", sys_arch)

        # 2. Explicit workload parameters in prompt -> MUST produce calculated ComprehensiveCapacityReport
        res_explicit = self.pia.execute_new(
            "Build a high-traffic payment processing service sustaining 50,000 DAU and 1,200 RPS.",
            project_name="PaymentService",
        )
        set_c_exp = res_explicit["set_c_solutions"]
        cap_report_exp = set_c_exp["capacity_report"]
        self.assertIsInstance(cap_report_exp, ComprehensiveCapacityReport)
        self.assertEqual(cap_report_exp.traffic.daily_active_users, 50_000)
        self.assertIn("System Capacity & Sizing Estimation Report", set_c_exp["capacity_markdown"])

        # 3. Explicitly requested hypothetical assumptions -> MUST contain clear unconfirmed warning banner
        res_hypo = self.pia.execute_new(
            "Build a photo sharing mobile app. Please provide hypothetical capacity estimate assumptions.",
            project_name="PhotoShare",
        )
        set_c_hypo = res_hypo["set_c_solutions"]
        self.assertIn("Hypothetical Baseline Assumption — Unconfirmed", set_c_hypo["capacity_markdown"])
        self.assertIn("MUST NOT be treated as confirmed user requirements", set_c_hypo["capacity_markdown"])

    def test_defect_2_omis_cryptographic_approval_verification_and_replay_prevention(self):
        """Defect 2: Verify IntegrationGateway policy enforcement, expiration, signature, and cross-instance persistent replay defense."""
        import hashlib
        import time
        from openclone.integrations.gateway import (
            ApprovalRecord,
            AuthContext,
            IntegrationGateway,
            PolicyVerdict,
        )

        nonce_db = self.base / ".openclone" / "test_gateway_nonces.sqlite3"
        gw1 = IntegrationGateway(repo_root=Path(self.base), nonce_db_path=nonce_db)
        p_def = {"project_id": "proj_gov_002", "project_name": "GovernanceProject"}
        exec_args = {
            "project_id": "proj_gov_002",
            "project_name": "GovernanceProject",
            "workspace_path": str(self.base),
        }
        digest = "c" * 64

        # 1. Deny when approval record is expired
        expired_approval = ApprovalRecord(
            approval_id="app-expired-01",
            approver_id="human-lead",
            capability_id="openclone_sync_memory",
            project_id="proj_gov_002",
            payload_digest=digest,
            nonce="nonce-expired-01",
            expires_at=time.time() - 100.0,  # Expired
            signature="mock_sig",
        )
        denied_expired = self.pia.sync_to_memory(
            p_def,
            self.base,
            human_approved=True,
            approval_digest=digest,
            approval_record=expired_approval,
            gateway=gw1,
        )
        self.assertEqual(denied_expired["status"], "DENIED")
        self.assertFalse(denied_expired["persisted"])
        self.assertIn("expired", denied_expired["reason"].lower())

        # 2. Deny when signature is invalid / fabricated
        fake_approval = ApprovalRecord(
            approval_id="app-fake-01",
            approver_id="human-lead",
            capability_id="openclone_sync_memory",
            project_id="proj_gov_002",
            payload_digest=digest,
            nonce="nonce-fake-01",
            expires_at=time.time() + 600.0,
            signature="totally_fabricated_signature_12345",
        )
        denied_sig = self.pia.sync_to_memory(
            p_def,
            self.base,
            human_approved=True,
            approval_digest=digest,
            approval_record=fake_approval,
            gateway=gw1,
        )
        self.assertEqual(denied_sig["status"], "DENIED")
        self.assertFalse(denied_sig["persisted"])
        self.assertIn("signature", denied_sig["reason"].lower())

        # 3. Deny when payload is modified (payload digest mismatch)
        now_ts = time.time()
        exp_ts = now_ts + 600.0
        nonce_tamper = "nonce-tamper-01"
        clean_args = {k: v for k, v in exec_args.items() if k not in ("approval_record", "approval_digest")}
        valid_payload_digest = hashlib.sha256(json.dumps(clean_args, sort_keys=True).encode()).hexdigest()
        import hmac as _hmac
        tampered_sig_base = f"app-tamper-01:human-lead:proj_gov_002:openclone_sync_memory:wrong_digest:{nonce_tamper}:{exp_ts}"
        tampered_sig = _hmac.new(gw1.signing_secret, tampered_sig_base.encode("utf-8"), hashlib.sha256).hexdigest()
        tampered_approval = ApprovalRecord(
            approval_id="app-tamper-01",
            approver_id="human-lead",
            capability_id="openclone_sync_memory",
            project_id="proj_gov_002",
            payload_digest="wrong_digest",
            nonce=nonce_tamper,
            expires_at=exp_ts,
            signature=tampered_sig,
        )
        denied_tamper = self.pia.sync_to_memory(
            p_def,
            self.base,
            human_approved=True,
            approval_digest=digest,
            approval_record=tampered_approval,
            gateway=gw1,
        )
        self.assertEqual(denied_tamper["status"], "DENIED")
        self.assertFalse(denied_tamper["persisted"])
        self.assertIn("payload digest mismatch", denied_tamper["reason"].lower())

        # 4. Deny when caller lacks required scope
        auth_no_scope = AuthContext(
            user_id="human-lead",
            project_id="proj_gov_002",
            scopes={"evidence:read"},  # Missing projects:write & evidence:write
            is_human=True,
        )
        valid_scope_sig_base = f"app-scope-01:human-lead:proj_gov_002:openclone_sync_memory:{valid_payload_digest}:nonce-scope-01:{exp_ts}"
        valid_scope_sig = _hmac.new(gw1.signing_secret, valid_scope_sig_base.encode("utf-8"), hashlib.sha256).hexdigest()
        approval_for_scope = ApprovalRecord(
            approval_id="app-scope-01",
            approver_id="human-lead",
            capability_id="openclone_sync_memory",
            project_id="proj_gov_002",
            payload_digest=valid_payload_digest,
            nonce="nonce-scope-01",
            expires_at=exp_ts,
            signature=valid_scope_sig,
        )
        denied_scope = self.pia.sync_to_memory(
            p_def,
            self.base,
            human_approved=True,
            approval_digest=digest,
            approval_record=approval_for_scope,
            auth_context=auth_no_scope,
            gateway=gw1,
        )
        self.assertEqual(denied_scope["status"], "DENIED")
        self.assertFalse(denied_scope["persisted"])
        self.assertIn("scope", denied_scope["reason"].lower())

        # 5. Deny when caller is non-human (agent)
        auth_agent = AuthContext(
            user_id="agent-worker",
            project_id="proj_gov_002",
            scopes={"projects:write", "evidence:write"},
            is_human=False,
            client_type="agent_runtime",
        )
        valid_agent_sig_base = f"app-agent-01:agent-worker:proj_gov_002:openclone_sync_memory:{valid_payload_digest}:nonce-agent-01:{exp_ts}"
        valid_agent_sig = _hmac.new(gw1.signing_secret, valid_agent_sig_base.encode("utf-8"), hashlib.sha256).hexdigest()
        approval_for_agent = ApprovalRecord(
            approval_id="app-agent-01",
            approver_id="agent-worker",
            capability_id="openclone_sync_memory",
            project_id="proj_gov_002",
            payload_digest=valid_payload_digest,
            nonce="nonce-agent-01",
            expires_at=exp_ts,
            signature=valid_agent_sig,
        )
        denied_nonhuman = self.pia.sync_to_memory(
            p_def,
            self.base,
            human_approved=True,
            approval_digest=digest,
            approval_record=approval_for_agent,
            auth_context=auth_agent,
            gateway=gw1,
        )
        self.assertEqual(denied_nonhuman["status"], "DENIED")
        self.assertFalse(denied_nonhuman["persisted"])
        self.assertIn("non-human", denied_nonhuman["reason"].lower())

        # 6. Valid signed approval -> PERSISTED
        nonce_val = "nonce-single-use-01"
        valid_sig_base = f"app-valid-01:human-lead:proj_gov_002:openclone_sync_memory:{valid_payload_digest}:{nonce_val}:{exp_ts}"
        import hmac as _hmac
        valid_sig = _hmac.new(gw1.signing_secret, valid_sig_base.encode("utf-8"), hashlib.sha256).hexdigest()
        valid_approval = ApprovalRecord(
            approval_id="app-valid-01",
            approver_id="human-lead",
            capability_id="openclone_sync_memory",
            project_id="proj_gov_002",
            payload_digest=valid_payload_digest,
            nonce=nonce_val,
            expires_at=exp_ts,
            signature=valid_sig,
        )
        persisted_first = self.pia.sync_to_memory(
            p_def,
            self.base,
            human_approved=True,
            approval_digest=digest,
            approval_record=valid_approval,
            gateway=gw1,
        )
        self.assertEqual(persisted_first["status"], "PERSISTED")
        self.assertTrue(persisted_first["persisted"])

        # 7. Replay attempt on same gateway instance -> MUST BE REJECTED
        denied_replay = self.pia.sync_to_memory(
            p_def,
            self.base,
            human_approved=True,
            approval_digest=digest,
            approval_record=valid_approval,
            gateway=gw1,
        )
        self.assertEqual(denied_replay["status"], "DENIED")
        self.assertFalse(denied_replay["persisted"])
        self.assertIn("replay", denied_replay["reason"].lower())

        # 8. Replay attempt across a NEW gateway instance -> MUST BE REJECTED via SQLite persistent store
        gw2 = IntegrationGateway(repo_root=Path(self.base), nonce_db_path=nonce_db, signing_secret=gw1.signing_secret)
        denied_cross_instance = self.pia.sync_to_memory(
            p_def,
            self.base,
            human_approved=True,
            approval_digest=digest,
            approval_record=valid_approval,
            gateway=gw2,
        )
        self.assertEqual(denied_cross_instance["status"], "DENIED")
        self.assertFalse(denied_cross_instance["persisted"])
        self.assertIn("replay", denied_cross_instance["reason"].lower())

        # 9. Concurrent duplicate nonce consumption -> at most one request succeeds
        import concurrent.futures
        nonce_conc = "nonce-concurrent-999"
        conc_sig_base = f"app-conc-01:human-lead:proj_gov_002:openclone_sync_memory:{valid_payload_digest}:{nonce_conc}:{exp_ts}"
        conc_sig = _hmac.new(gw1.signing_secret, conc_sig_base.encode("utf-8"), hashlib.sha256).hexdigest()
        conc_approval = ApprovalRecord(
            approval_id="app-conc-01",
            approver_id="human-lead",
            capability_id="openclone_sync_memory",
            project_id="proj_gov_002",
            payload_digest=valid_payload_digest,
            nonce=nonce_conc,
            expires_at=exp_ts,
            signature=conc_sig,
        )

        def _attempt_sync():
            return self.pia.sync_to_memory(
                p_def,
                self.base,
                human_approved=True,
                approval_digest=digest,
                approval_record=conc_approval,
                gateway=gw1,
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(_attempt_sync) for _ in range(4)]
            results = [f.result() for f in futures]

        print("\nDEBUG CONC RESULTS:", results)
        persisted_count = sum(1 for r in results if r["status"] == "PERSISTED")
        denied_count = sum(1 for r in results if r["status"] == "DENIED")
        self.assertEqual(persisted_count, 1)
        self.assertEqual(denied_count, 3)

    def test_defect_3_dynamic_c4_architecture_generation(self):
        """Defect 3: Verify dynamic C4 diagrams reflect technology decisions across all 9 required scenarios."""
        from src.openclone.intelligence.technology import TechnologyDecision

        # Scenario 1: Static Portfolio with no backend or database
        res_static = self.pia.execute_new(
            "Build a responsive personal portfolio static website.",
            project_name="StaticPortfolio",
        )
        sys_static = res_static["artifacts"]["System-Architecture.md"]
        self.assertIn("Browser Client", sys_static)
        self.assertIn("Static Web Host", sys_static)
        self.assertNotIn("Primary Database", sys_static)
        self.assertNotIn("Backend Core API", sys_static)

        # Scenario 2: Standard web application using PostgreSQL
        res_pg = self.pia.execute_new(
            "Build an enterprise CRM SaaS portal with relational PostgreSQL database.",
            project_name="CRMPlatform",
        )
        sys_pg = res_pg["artifacts"]["System-Architecture.md"]
        self.assertIn("PostgreSQL", sys_pg)
        self.assertIn("Frontend Application", sys_pg)
        self.assertIn("Backend Core API", sys_pg)

        # Scenario 3: Standard web application using MongoDB instead of PostgreSQL
        # Pass explicit technology decision for MongoDB
        custom_decisions_mongo = [
            TechnologyDecision(
                category="Frontend Framework",
                selected_technology="Vue.js 3",
                version="3.4.x",
                license="MIT",
                selection_rationale="Reactive UI",
                alternatives_evaluated=[],
                compatibility_evidence="",
                cost_assumptions="",
                required_env_vars=[],
                known_limitations=[],
            ),
            TechnologyDecision(
                category="Backend API Service",
                selected_technology="Go Gin",
                version="1.9.x",
                license="MIT",
                selection_rationale="High throughput REST",
                alternatives_evaluated=[],
                compatibility_evidence="",
                cost_assumptions="",
                required_env_vars=[],
                known_limitations=[],
            ),
            TechnologyDecision(
                category="Database & Persistence",
                selected_technology="MongoDB",
                version="7.0.x",
                license="SSPL",
                selection_rationale="Document store",
                alternatives_evaluated=[],
                compatibility_evidence="",
                cost_assumptions="",
                required_env_vars=[],
                known_limitations=[],
            ),
        ]
        u, ext, containers_mongo = self.pia._build_dynamic_c4_containers(
            self.pia.classifier.classify_text("Build a web portal with MongoDB", project_name="MongoApp"),
            custom_decisions_mongo,
        )
        tech_names = [c["technology"] for c in containers_mongo]
        self.assertIn("MongoDB", tech_names)
        self.assertNotIn("PostgreSQL", tech_names)
        self.assertIn("Vue.js 3", tech_names)
        self.assertIn("Go Gin", tech_names)

        # Scenario 4: AI platform using a selected vector database (e.g. Qdrant)
        custom_decisions_ai_vector = [
            TechnologyDecision(
                category="AI / LLM Orchestration",
                selected_technology="OpenClone MIE",
                version="2.0.0",
                license="MIT",
                selection_rationale="Model router",
                alternatives_evaluated=[],
                compatibility_evidence="",
                cost_assumptions="",
                required_env_vars=[],
                known_limitations=[],
            ),
            TechnologyDecision(
                category="Vector Database",
                selected_technology="Qdrant Vector DB",
                version="1.8.x",
                license="Apache-2.0",
                selection_rationale="High-speed vector index",
                alternatives_evaluated=[],
                compatibility_evidence="",
                cost_assumptions="",
                required_env_vars=[],
                known_limitations=[],
            ),
        ]
        profile_ai = self.pia.classifier.classify_text("Autonomous AI agent system", project_name="AIAgent")
        u_ai, ext_ai, containers_ai_vec = self.pia._build_dynamic_c4_containers(profile_ai, custom_decisions_ai_vector)
        ai_techs = [c["technology"] for c in containers_ai_vec]
        self.assertIn("Qdrant Vector DB", ai_techs)

        # Scenario 5: AI platform without a selected vector database (marked as unconfirmed / missing)
        custom_decisions_ai_no_vec = [
            TechnologyDecision(
                category="AI / LLM Orchestration",
                selected_technology="OpenClone MIE",
                version="2.0.0",
                license="MIT",
                selection_rationale="Model router",
                alternatives_evaluated=[],
                compatibility_evidence="",
                cost_assumptions="",
                required_env_vars=[],
                known_limitations=[],
            ),
        ]
        u_ai5, ext_ai5, containers_ai_no_vec = self.pia._build_dynamic_c4_containers(profile_ai, custom_decisions_ai_no_vec)
        # Vector store should NOT be invented if no decision and not in conditional profiles
        v_stores = [c for c in containers_ai_no_vec if c["id"] == "vector_memory_store"]
        if v_stores:
            self.assertIn("Unresolved", v_stores[0]["technology"])
        else:
            self.assertEqual(len(v_stores), 0)

        # Scenario 6: IoT platform with a selected event broker (RabbitMQ instead of Kafka)
        custom_decisions_iot_rabbit = [
            TechnologyDecision(
                category="Event Broker",
                selected_technology="RabbitMQ Streams",
                version="3.13.x",
                license="MPL-2.0",
                selection_rationale="Lightweight event stream broker",
                alternatives_evaluated=[],
                compatibility_evidence="",
                cost_assumptions="",
                required_env_vars=[],
                known_limitations=[],
            ),
            TechnologyDecision(
                category="Database",
                selected_technology="TimescaleDB",
                version="2.14.x",
                license="Apache-2.0",
                selection_rationale="Time-series extension",
                alternatives_evaluated=[],
                compatibility_evidence="",
                cost_assumptions="",
                required_env_vars=[],
                known_limitations=[],
            ),
        ]
        profile_iot = self.pia.classifier.classify_text("IoT streaming telemetry pipeline", project_name="IoTRabbit")
        u_iot, ext_iot, containers_iot = self.pia._build_dynamic_c4_containers(profile_iot, custom_decisions_iot_rabbit)
        iot_techs = [c["technology"] for c in containers_iot]
        self.assertIn("RabbitMQ Streams", iot_techs)
        self.assertNotIn("Apache Kafka", iot_techs)
        self.assertIn("TimescaleDB", iot_techs)

        # Scenario 7: CLI application without a browser frontend
        profile_cli = self.pia.classifier.classify_text("Command-line tool for git operations", project_name="GitCLI")
        u_cli, ext_cli, containers_cli = self.pia._build_dynamic_c4_containers(profile_cli, [])
        cli_ids = [c["id"] for c in containers_cli]
        self.assertIn("cli_engine", cli_ids)
        self.assertNotIn("frontend_app", cli_ids)
        self.assertNotIn("browser_client", cli_ids)
        # Verify CLI engine does not invent Python
        cli_tech = next(c["technology"] for c in containers_cli if c["id"] == "cli_engine")
        self.assertIn("Unresolved", cli_tech)
        self.assertNotIn("embedded_storage", cli_ids)

        # CLI application with explicit Rust decision
        cli_decisions_rust = [
            TechnologyDecision(
                category="CLI Runtime",
                selected_technology="Rust / Cargo",
                version="1.76.x",
                license="MIT",
                selection_rationale="Fast native CLI binary",
                alternatives_evaluated=[],
                compatibility_evidence="",
                cost_assumptions="",
                required_env_vars=[],
                known_limitations=[],
            ),
            TechnologyDecision(
                category="Persistence & Storage",
                selected_technology="RocksDB",
                version="8.10.x",
                license="Apache-2.0",
                selection_rationale="Embedded key-value store",
                alternatives_evaluated=[],
                compatibility_evidence="",
                cost_assumptions="",
                required_env_vars=[],
                known_limitations=[],
            ),
        ]
        _, _, containers_rust_cli = self.pia._build_dynamic_c4_containers(profile_cli, cli_decisions_rust)
        self.assertEqual(next(c["technology"] for c in containers_rust_cli if c["id"] == "cli_engine"), "Rust / Cargo")
        self.assertEqual(next(c["technology"] for c in containers_rust_cli if c["id"] == "embedded_storage"), "RocksDB")

        # Scenario 8: Embedded application without an external database
        profile_emb = self.pia.classifier.classify_text("Embedded firmware controller", project_name="FirmwareCore")
        profile_emb.delivery_targets = ["embedded_hardware"]
        u_emb, ext_emb, containers_emb = self.pia._build_dynamic_c4_containers(profile_emb, [])
        emb_ids = [c["id"] for c in containers_emb]
        self.assertNotIn("primary_db", emb_ids)
        self.assertNotIn("frontend_app", emb_ids)

        # Embedded application with explicit Flash ROM storage decision
        emb_decisions_flash = [
            TechnologyDecision(
                category="Embedded Storage",
                selected_technology="Flash ROM / EEPROM",
                version="1.0.x",
                license="Proprietary",
                selection_rationale="Onboard non-volatile memory",
                alternatives_evaluated=[],
                compatibility_evidence="",
                cost_assumptions="",
                required_env_vars=[],
                known_limitations=[],
            ),
        ]
        _, _, containers_flash_emb = self.pia._build_dynamic_c4_containers(profile_emb, emb_decisions_flash)
        self.assertEqual(next(c["technology"] for c in containers_flash_emb if c["id"] == "embedded_storage"), "Flash ROM / EEPROM")

        # Scenario 9: Application with incomplete technology decisions (marked unresolved)
        profile_web_incomplete = self.pia.classifier.classify_text("General web app", project_name="IncompleteApp")
        u_inc, ext_inc, containers_inc = self.pia._build_dynamic_c4_containers(profile_web_incomplete, [])
        # Missing decisions should be explicitly tagged as [Unresolved: Missing ... Decision]
        be_container = next(c for c in containers_inc if c["id"] == "backend_api")
        self.assertIn("Unresolved", be_container["technology"])

    def test_production_signing_key_fail_closed_and_issuance_security(self):
        """Verify production missing-key fail-closed behavior, concurrency, and approval issuance gates."""
        import concurrent.futures
        import os
        import tempfile
        import time
        from openclone.integrations.gateway import AuthContext, IntegrationGateway, PolicyVerdict

        orig_env = os.environ.get("OPENCLONE_ENV")
        orig_sec = os.environ.get("OPENCLONE_SIGNING_SECRET")

        try:
            # 1. Production Mode: Missing key fails closed
            os.environ["OPENCLONE_ENV"] = "production"
            if "OPENCLONE_SIGNING_SECRET" in os.environ:
                del os.environ["OPENCLONE_SIGNING_SECRET"]

            temp_prod = Path(tempfile.mkdtemp())
            gw_prod = IntegrationGateway(repo_root=temp_prod, nonce_db_path=temp_prod / "nonces.sqlite3")
            self.assertIsNone(gw_prod.signing_secret)

            auth_human = AuthContext(
                user_id="lead-architect",
                project_id="proj_prod_001",
                scopes={"projects:write", "evidence:write"},
                is_human=True,
            )

            # create_approval_record fails closed
            with self.assertRaises(PermissionError) as cm_create:
                gw_prod.create_approval_record(auth_human, "openclone_sync_memory", {"project_id": "proj_prod_001"})
            self.assertIn("Signing secret not configured", str(cm_create.exception))

            valid_rec = {
                "capability_id": "openclone_sync_memory",
                "project_id": "proj_prod_001",
                "expires_at": time.time() + 3600,
                "signature": "mock",
            }

            # evaluate_policy fails closed
            decision = gw_prod.evaluate_policy(
                auth_human,
                "openclone_sync_memory",
                {"project_id": "proj_prod_001", "approval_record": valid_rec},
            )
            self.assertEqual(decision.verdict, PolicyVerdict.DENIED)
            self.assertIn("Signing secret not configured", decision.reason)

            # execute fails closed
            with self.assertRaises(PermissionError) as cm_exec:
                gw_prod.execute(
                    auth_human,
                    "openclone_sync_memory",
                    {"project_id": "proj_prod_001", "approval_record": valid_rec},
                )
            self.assertIn("Signing secret not configured", str(cm_exec.exception))

            # 2. Development Mode: Auto-creates key file with permissions
            os.environ["OPENCLONE_ENV"] = "development"
            temp_dev = Path(tempfile.mkdtemp())
            gw_dev = IntegrationGateway(repo_root=temp_dev, nonce_db_path=temp_dev / "nonces.sqlite3")
            self.assertIsNotNone(gw_dev.signing_secret)
            secret_file = temp_dev / ".openclone" / ".signing_secret"
            self.assertTrue(secret_file.exists())
            self.assertTrue(gw_dev._verify_secret_file_permissions(secret_file))

            # 3. Concurrent gateway initialization race-condition avoidance
            temp_concurrent = Path(tempfile.mkdtemp())
            def init_gw(_):
                return IntegrationGateway(repo_root=temp_concurrent, nonce_db_path=temp_concurrent / "nonces.sqlite3").signing_secret

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                secrets_list = list(executor.map(init_gw, range(4)))

            self.assertEqual(len(set(secrets_list)), 1)
            self.assertIsNotNone(secrets_list[0])

            # 4. Human approver issuance constraint: Non-human cannot issue approval records
            gw_trusted = IntegrationGateway(
                repo_root=temp_dev,
                nonce_db_path=temp_dev / "nonces.sqlite3",
                signing_secret="trusted_master_key",
            )
            auth_agent = AuthContext(
                user_id="agent-worker",
                project_id="proj_prod_001",
                scopes={"projects:write", "evidence:write"},
                is_human=False,
                client_type="agent_runtime",
            )
            with self.assertRaises(PermissionError) as cm_agent:
                gw_trusted.create_approval_record(auth_agent, "openclone_sync_memory", {"project_id": "proj_prod_001"})
            self.assertIn("not an authenticated human approver", str(cm_agent.exception))

            # 5. Gateway unavailable in sync_to_memory fails closed
            # Force gateway initialization failure
            res_no_gw = self.pia.sync_to_memory(
                {"project_id": "p1"},
                "/invalid/nonexistent/workspace",
                human_approved=True,
                approval_record={"signature": "mock"},
            )
            self.assertEqual(res_no_gw["status"], "DENIED")
            self.assertFalse(res_no_gw["persisted"])

        finally:
            if orig_env is not None:
                os.environ["OPENCLONE_ENV"] = orig_env
            elif "OPENCLONE_ENV" in os.environ:
                del os.environ["OPENCLONE_ENV"]

            if orig_sec is not None:
                os.environ["OPENCLONE_SIGNING_SECRET"] = orig_sec
            elif "OPENCLONE_SIGNING_SECRET" in os.environ:
                del os.environ["OPENCLONE_SIGNING_SECRET"]

    def test_stage_1_human_provenance_and_legacy_digest_audit(self):
        """Focused tests for human provenance, fabricated contexts, and unsigned digest rejection."""
        import os
        from openclone.integrations.gateway import AuthContext, IntegrationGateway, PolicyVerdict

        gw = IntegrationGateway(signing_secret="prov_key_test_001")

        # 1. Unauthenticated caller (auth=None)
        with self.assertRaises(PermissionError):
            gw.create_approval_record(None, "openclone_sync_memory", {"project_id": "p1"})

        # 2. AI agent (is_human=False, client_type="mcp_client")
        agent_auth = AuthContext(
            user_id="mcp_agent",
            project_id="p1",
            scopes={"projects:write", "evidence:write", "release:approve"},
            is_human=False,
            client_type="mcp_client",
        )
        with self.assertRaises(PermissionError) as cm_agent:
            gw.create_approval_record(agent_auth, "openclone_sync_memory", {"project_id": "p1"})
        self.assertIn("not an authenticated human approver", str(cm_agent.exception))

        # 3. Fabricated human context (is_human=True, but client_type="generic" and no verified token claims)
        fabricated_auth = AuthContext(
            user_id="impersonator",
            project_id="p1",
            scopes={"projects:write"},
            is_human=True,
            client_type="generic",  # unverified client
        )
        with self.assertRaises(PermissionError) as cm_fab:
            gw.create_approval_record(fabricated_auth, "openclone_sync_memory", {"project_id": "p1"})
        self.assertIn("Untrusted provenance", str(cm_fab.exception))

        # 4. Genuine trusted human approval (via authenticate_token)
        maintainer_auth = gw.authenticate_token("test-valid-token")
        self.assertIsNotNone(maintainer_auth)
        self.assertTrue(maintainer_auth.is_human)
        self.assertTrue(maintainer_auth.token_claims.get("verified"))
        rec = gw.create_approval_record(maintainer_auth, "openclone_sync_memory", {"project_id": "default"})
        self.assertIn("signature", rec)
        self.assertIn("nonce", rec)

        # 5. Legacy 64-char hex digest CANNOT authorize openclone_sync_memory
        digest_64 = "f" * 64
        policy_res = gw.evaluate_policy(
            maintainer_auth,
            "openclone_sync_memory",
            {"project_id": "default", "approval_digest": digest_64},
            approval_digest=digest_64,
        )
        self.assertEqual(policy_res.verdict, PolicyVerdict.REQUIRES_HUMAN_APPROVAL)
        self.assertIn("requires authentic human cryptographic approval", policy_res.reason)

        with self.assertRaises(PermissionError) as cm_digest_exec:
            gw.execute(
                maintainer_auth,
                "openclone_sync_memory",
                {"project_id": "default", "approval_digest": digest_64},
                approval_digest=digest_64,
            )
        self.assertIn("Approval Required", str(cm_digest_exec.exception))

        # 6. Windows production ACL protection check
        orig_env = os.environ.get("OPENCLONE_ENV")
        try:
            os.environ["OPENCLONE_ENV"] = "production"
            if os.name == "nt":
                # On Windows in production, local file ACLs cannot be validated via os.stat
                dummy_file = self.base / ".openclone" / ".signing_secret"
                dummy_file.parent.mkdir(parents=True, exist_ok=True)
                dummy_file.write_text("dummy", encoding="utf-8")
                self.assertFalse(gw._verify_secret_file_permissions(dummy_file))
        finally:
            if orig_env is not None:
                os.environ["OPENCLONE_ENV"] = orig_env
            elif "OPENCLONE_ENV" in os.environ:
                del os.environ["OPENCLONE_ENV"]


if __name__ == "__main__":
    unittest.main()
