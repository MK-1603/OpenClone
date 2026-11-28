"""Automated Test Suite for OpenClone System Design & Communication Engineering.

Tests cover:
- Capacity Estimator (RPS, storage growth, bandwidth, cache sizing, queue workers)
- System Design Decision Engine (Monolith-First Rule, ADR generation)
- 20 Canonical Real-World System Design Case Studies
- Mermaid System Diagram Generator (C4 Context, Container, Sequence, Data Flow)
- Multi-Channel Communication Infrastructure (Email, SMS, Push, In-App, Real-Time WebSockets)
- User Preferences & Time-Zone Aware Quiet-Hour Filtering
- Mandatory Security Notification Override
- Cryptographic Delivery Ledger & Tamper-Evident SHA-256 Hash Chaining
- WebSocket Handshake Authentication, Presence Tracking, and Connection Reaping
- SMS GSM-7 vs UCS-2 Encoding & Segmentation
- Skill Engine discovery & loading for all registered skills (29 specialist skills)
"""
from __future__ import annotations

import time
import unittest
from pathlib import Path

from src.openclone.communication import (
    ChannelType,
    DeliveryLedger,
    DeliveryStatus,
    FcmPushProvider,
    MockEmailProvider,
    MockPushProvider,
    MockSmsProvider,
    NotificationCategory,
    NotificationDispatcher,
    NotificationPayload,
    NotificationPriority,
    PreferenceEngine,
    ProviderFailoverManager,
    ResendEmailProvider,
    TwilioSmsProvider,
    UserPreference,
    WebSocketSessionManager,
)
from src.openclone.skills.engine import SkillRegistry, SkillSelector
from src.openclone.system_design import (
    ADRGenerator,
    CapacityEstimator,
    CaseStudyArchitecture,
    QualityAttributes,
    SystemDesignCatalogue,
    SystemDesignDecisionEngine,
    SystemDiagramGenerator,
    SystemRequirements,
    TrafficProfile,
)

ROOT = Path(__file__).resolve().parents[1]


# ============================================================================
# 1. SYSTEM DESIGN & CAPACITY TESTS
# ============================================================================

class TestSystemDesignCapacity(unittest.TestCase):
    """Verifies back-of-the-envelope capacity calculations and report generation."""

    def setUp(self):
        self.estimator = CapacityEstimator()

    def test_capacity_estimation_calculations(self):
        profile = TrafficProfile(
            daily_active_users=100_000,
            monthly_active_users=1_000_000,
            actions_per_user_per_day=20,
            read_to_write_ratio=10.0,
            avg_read_payload_bytes=4_096,
            avg_write_payload_bytes=2_048,
            peak_surge_multiplier=3.0,
        )
        report = self.estimator.estimate(profile)

        # 100k users * 20 actions = 2,000,000 actions / 86400s ≈ 23.15 req/s
        self.assertAlmostEqual(report.avg_rps, 23.15, places=1)
        self.assertAlmostEqual(report.peak_rps, 23.15 * 3.0, places=1)

        # Storage calculations
        self.assertGreater(report.storage.daily_raw_gb, 0.0)
        self.assertGreater(report.storage.annual_total_provisioned_tb, 0.0)
        self.assertAlmostEqual(
            report.storage.five_year_total_tb,
            report.storage.annual_total_provisioned_tb * 5.0,
            places=2,
        )

        # Bandwidth calculations
        self.assertGreater(report.bandwidth.avg_ingress_mbps, 0.0)
        self.assertGreater(report.bandwidth.avg_egress_mbps, 0.0)
        self.assertGreater(report.bandwidth.monthly_egress_tb, 0.0)

        # Cache Sizing (80/20 Pareto)
        self.assertGreater(report.cache.recommended_cache_ram_gb, 0.0)
        self.assertGreaterEqual(report.cache.recommended_nodes, 2)

        # Queue Sizing
        self.assertGreaterEqual(report.queue.min_worker_concurrency, 1)
        self.assertGreaterEqual(report.queue.peak_worker_concurrency, report.queue.min_worker_concurrency)

        # Markdown Report Generation
        md = report.to_markdown()
        self.assertIn("# System Capacity & Sizing Estimation Report", md)
        self.assertIn("100,000", md)
        self.assertIn("Daily Active Users (DAU)", md)
        self.assertIn("Pareto 80/20 Rule", md)


class TestSystemDesignDecisionEngine(unittest.TestCase):
    """Verifies architecture pattern evaluation and formal ADR generation."""

    def setUp(self):
        self.engine = SystemDesignDecisionEngine()

    def test_monolith_first_standard_evaluation(self):
        req = SystemRequirements(
            project_name="B2B Billing Portal",
            functional_summary="Subscription management and invoice generation",
            peak_rps=250.0,
            total_data_gb=150.0,
            multi_tenant=True,
        )
        rec = self.engine.evaluate(req)
        self.assertIn("Modular Monolith", rec.primary_pattern)
        self.assertEqual(rec.operational_complexity, "Low")
        self.assertTrue(any("Row-Level Security" in w for w in rec.warnings))

        # Generate ADR
        adr_md = ADRGenerator.generate_adr("ADR-001", "Adopt Modular Monolith Architecture", req, rec)
        self.assertIn("# ADR-ADR-001: Adopt Modular Monolith Architecture", adr_md)
        self.assertIn("Status:** APPROVED", adr_md)
        self.assertIn("Chosen Architecture:** `Modular Monolith", adr_md)

    def test_offline_sync_architecture(self):
        req = SystemRequirements(
            project_name="Field Inspector App",
            functional_summary="Inspections conducted in remote areas without cellular connectivity",
            peak_rps=50.0,
            total_data_gb=20.0,
            requires_offline_sync=True,
        )
        rec = self.engine.evaluate(req)
        self.assertEqual(rec.primary_pattern, "Offline-First Client-Server Architecture")
        self.assertIn("SQLite", rec.database_tier)

    def test_extreme_throughput_recommends_distributed_services(self):
        req = SystemRequirements(
            project_name="Global Ride Hailing Dispatch",
            functional_summary="High-volume location ingestion and trip state coordination",
            peak_rps=25_000.0,
            total_data_gb=50_000.0,
            real_time_updates=True,
        )
        rec = self.engine.evaluate(req)
        self.assertEqual(rec.primary_pattern, "Event-Driven Distributed Microservices")
        self.assertEqual(rec.operational_complexity, "High")


class TestSystemDesignCaseStudies(unittest.TestCase):
    """Verifies all 20 canonical real-world system design case studies are indexed."""

    def test_all_20_case_studies_exist(self):
        cases = SystemDesignCatalogue.list_all()
        self.assertEqual(len(cases), 20)

        expected_ids = [f"CS-{i:02d}" for i in range(1, 21)]
        actual_ids = [c.case_id for c in cases]
        self.assertEqual(actual_ids, expected_ids)

        # Inspect specific case studies
        auth_case = SystemDesignCatalogue.get("CS-01")
        self.assertIsNotNone(auth_case)
        self.assertEqual(auth_case.name, "Authentication & Identity System")

        ride_case = SystemDesignCatalogue.get("CS-11")
        self.assertIsNotNone(ride_case)
        self.assertIn("H3", ride_case.summary)

        saas_case = SystemDesignCatalogue.get("CS-16")
        self.assertIsNotNone(saas_case)
        self.assertIn("RLS", saas_case.summary)


class TestSystemDiagramGenerator(unittest.TestCase):
    """Verifies generation of valid Mermaid system diagrams."""

    def test_c4_context_diagram(self):
        diag = SystemDiagramGenerator.generate_c4_context(
            system_name="E-Commerce Core",
            user_types=["Customer", "Store Admin"],
            external_systems=["Stripe Payment", "SendGrid Email"],
            core_description="Order and catalogue management",
        )
        self.assertTrue(diag.startswith("```mermaid"))
        self.assertIn("flowchart TD", diag)
        self.assertIn("Customer", diag)
        self.assertIn("Stripe Payment", diag)
        self.assertTrue(diag.endswith("```"))

    def test_sequence_diagram(self):
        diag = SystemDiagramGenerator.generate_sequence_diagram(
            title="User Checkout Flow",
            participants=["Client", "APIGateway", "PaymentService"],
            steps=[
                ("Client", "APIGateway", "POST /checkout"),
                ("APIGateway", "PaymentService", "Authorize Payment"),
            ],
        )
        self.assertIn("sequenceDiagram", diag)
        self.assertIn("Client->>APIGateway: POST /checkout", diag)


# ============================================================================
# 2. COMMUNICATION & NOTIFICATION TESTS
# ============================================================================

class TestNotificationPreferences(unittest.TestCase):
    """Verifies user preference enforcement, quiet hours, and mandatory security override."""

    def test_mandatory_security_notification_never_suppressed(self):
        pref = UserPreference(
            user_id="user_123",
            allowed_channels=[ChannelType.IN_APP],  # Email disabled
            opted_out_categories=[NotificationCategory.MARKETING],
            quiet_hours_enabled=True,
            quiet_hours_start_hour=0,
            quiet_hours_end_hour=24,  # Always in quiet hours
        )
        payload = NotificationPayload(
            notification_id="notif_sec_01",
            recipient_id="user_123",
            category=NotificationCategory.SECURITY,
            priority=NotificationPriority.CRITICAL_SECURITY,
            channels=[ChannelType.EMAIL, ChannelType.SMS],
            subject="Unauthorized login attempt detected",
            body_text="A login from unknown IP was blocked.",
            recipient_email="sec@openclone.org",
            recipient_phone="+15551234567",
        )
        # Security notifications must override all user preferences and quiet hours
        evaluation = PreferenceEngine.evaluate(payload, pref)
        self.assertIn(ChannelType.EMAIL, evaluation.approved_channels)
        self.assertIn(ChannelType.SMS, evaluation.approved_channels)
        self.assertEqual(len(evaluation.suppressed_channels), 0)

    def test_quiet_hours_suppresses_push_and_sms(self):
        # Local time: 23:00 (11 PM) -> quiet hours active
        fake_epoch = 23 * 3600.0
        pref = UserPreference(
            user_id="user_456",
            allowed_channels=[ChannelType.EMAIL, ChannelType.SMS, ChannelType.MOBILE_PUSH],
            quiet_hours_enabled=True,
            quiet_hours_start_hour=22,
            quiet_hours_end_hour=8,
            user_timezone_offset_hours=0.0,
        )
        payload = NotificationPayload(
            notification_id="notif_rem_01",
            recipient_id="user_456",
            category=NotificationCategory.REMINDER,
            priority=NotificationPriority.NORMAL,
            channels=[ChannelType.EMAIL, ChannelType.SMS, ChannelType.MOBILE_PUSH],
            subject="Your weekly digest is ready",
            body_text="Click here to review your activity.",
            recipient_email="digest@openclone.org",
            recipient_phone="+15559876543",
        )
        evaluation = PreferenceEngine.evaluate(payload, pref, current_epoch=fake_epoch)
        # Email allowed asynchronously; SMS and Push suppressed during quiet hours
        self.assertIn(ChannelType.EMAIL, evaluation.approved_channels)
        self.assertNotIn(ChannelType.SMS, evaluation.approved_channels)
        self.assertNotIn(ChannelType.MOBILE_PUSH, evaluation.approved_channels)
        self.assertEqual(len(evaluation.suppressed_channels), 2)


class TestNotificationDispatcher(unittest.TestCase):
    """Verifies end-to-end multi-channel dispatch, failover, idempotency, and audit ledger."""

    def setUp(self):
        self.failover_mgr = ProviderFailoverManager()
        self.primary_email = MockEmailProvider("primary_ses", should_fail=True, is_retryable=True)
        self.secondary_email = MockEmailProvider("secondary_resend", should_fail=False)
        self.failover_mgr.register_email_provider(self.primary_email)
        self.failover_mgr.register_email_provider(self.secondary_email)

        self.dispatcher = NotificationDispatcher(failover_manager=self.failover_mgr)

    def test_email_provider_failover(self):
        payload = NotificationPayload(
            notification_id="notif_failover_01",
            recipient_id="user_789",
            category=NotificationCategory.TRANSACTIONAL,
            priority=NotificationPriority.TRANSACTIONAL,
            channels=[ChannelType.EMAIL],
            subject="Invoice #1042",
            body_text="Your payment of $49.00 succeeded.",
            recipient_email="customer@openclone.org",
        )
        res = self.dispatcher.dispatch(payload)
        ch_res = res["channel_results"]["email"]
        self.assertTrue(ch_res["success"])
        # Verified failover to secondary provider
        self.assertEqual(ch_res["provider"], "secondary_resend")
        self.assertEqual(self.primary_email.sent_count, 1)
        self.assertEqual(self.secondary_email.sent_count, 1)

    def test_idempotency_key_prevents_duplicate_dispatch(self):
        payload = NotificationPayload(
            notification_id="notif_idemp_01",
            recipient_id="user_001",
            category=NotificationCategory.TRANSACTIONAL,
            priority=NotificationPriority.TRANSACTIONAL,
            channels=[ChannelType.EMAIL],
            subject="Order Placed",
            body_text="Order #999 created.",
            recipient_email="order@openclone.org",
            idempotency_key="idemp_key_abc_123",
        )
        # First dispatch
        res1 = self.dispatcher.dispatch(payload)
        self.assertIn("channel_results", res1)

        # Immediate second dispatch with same key
        res2 = self.dispatcher.dispatch(payload)
        self.assertEqual(res2["status"], "duplicate_suppressed")
        self.assertEqual(res2["idempotency_key"], "idemp_key_abc_123")

    def test_delivery_ledger_hash_chain_integrity(self):
        ledger = self.dispatcher.ledger
        self.assertTrue(ledger.verify_integrity())

        # Dispatch a notification to create ledger entries
        payload = NotificationPayload(
            notification_id="notif_ledger_01",
            recipient_id="user_audit",
            category=NotificationCategory.SYSTEM,
            priority=NotificationPriority.NORMAL,
            channels=[ChannelType.EMAIL],
            subject="System Maintenance",
            body_text="Maintenance scheduled for Sunday.",
            recipient_email="all@openclone.org",
        )
        self.dispatcher.dispatch(payload)

        # Verify ledger has records and integrity check passes
        self.assertGreater(len(ledger.attempts), 0)
        self.assertTrue(ledger.verify_integrity())

        # Intentionally tamper with a hash to verify tampering detection
        ledger.attempts[0].sha256_hash = "tampered_hash_123"
        self.assertFalse(ledger.verify_integrity())


class TestWebSocketSessionManager(unittest.TestCase):
    """Verifies WebSocket handshake auth, room broadcasting, presence, and session reaping."""

    def setUp(self):
        self.manager = WebSocketSessionManager()

    def test_unauthenticated_connection_rejected(self):
        with self.assertRaises(PermissionError):
            self.manager.connect("conn_bad", "user_1", auth_token="")

        with self.assertRaises(PermissionError):
            self.manager.connect("conn_bad2", "user_1", auth_token="invalid")

    def test_connection_lifecycle_and_room_broadcast(self):
        # Connect 2 clients for user_1 and 1 for user_2
        c1 = self.manager.connect("conn_1", "user_1", auth_token="valid_jwt_token_1")
        c2 = self.manager.connect("conn_2", "user_1", auth_token="valid_jwt_token_2")
        c3 = self.manager.connect("conn_3", "user_2", auth_token="valid_jwt_token_3")

        self.assertEqual(self.manager.active_connection_count(), 3)
        self.assertTrue(self.manager.get_presence("user_1"))
        self.assertTrue(self.manager.get_presence("user_2"))
        self.assertFalse(self.manager.get_presence("user_unknown"))

        # Room subscription
        self.manager.join_room("conn_1", "project:alpha")
        self.manager.join_room("conn_3", "project:alpha")
        self.assertEqual(self.manager.broadcast_to_room("project:alpha", "chat_msg", {}), 2)

        # Disconnect c1
        self.manager.disconnect("conn_1")
        self.assertEqual(self.manager.active_connection_count(), 2)
        # user_1 still present via conn_2
        self.assertTrue(self.manager.get_presence("user_1"))

        # Disconnect c2
        self.manager.disconnect("conn_2")
        self.assertFalse(self.manager.get_presence("user_1"))

    def test_stale_connection_reaping(self):
        c = self.manager.connect("conn_stale", "user_stale", auth_token="valid_token")
        # Simulate idle for 120 seconds
        c.last_ping_at = time.time() - 120.0
        reaped = self.manager.clean_stale_connections(max_idle_seconds=60.0)
        self.assertEqual(reaped, 1)
        self.assertEqual(self.manager.active_connection_count(), 0)


class TestSmsSegmentation(unittest.TestCase):
    """Verifies GSM-7 vs UCS-2 SMS character segment calculation."""

    def test_gsm7_ascii_segmentation(self):
        short_ascii = "Hello from OpenClone verification!"
        self.assertEqual(TwilioSmsProvider.calculate_segments(short_ascii), 1)

        # 200 ASCII characters = 2 segments (160 + 40)
        long_ascii = "A" * 200
        self.assertEqual(TwilioSmsProvider.calculate_segments(long_ascii), 2)

    def test_ucs2_unicode_segmentation(self):
        # Unicode / Emoji triggers UCS-2 (70 chars per segment)
        unicode_text = "🚀 OpenClone Security OTP: 987654. Do not share. " + ("B" * 60)
        # Total length > 70 with non-ASCII
        self.assertEqual(TwilioSmsProvider.calculate_segments(unicode_text), 2)


# ============================================================================
# 3. SKILL ENGINE DISCOVERY & VALIDATION TESTS
# ============================================================================

class TestSkillEngineAllRegisteredSkills(unittest.TestCase):
    """Verifies that all registered specialist skills (29 total) resolve on disk with valid manifests."""

    def setUp(self):
        self.registry = SkillRegistry(root=ROOT)
        self.selector = SkillSelector(registry=self.registry)

    def test_all_skills_registered_and_resolvable(self):
        skills = self.registry.list_all()
        self.assertGreaterEqual(len(skills), 29)
        errors = self.registry.validate_all()
        self.assertEqual(errors, [], f"Expected 0 path resolution errors, found: {errors}")

    def test_system_design_skill_selection(self):
        task = "Perform system design capacity estimation and generate C4 container diagram for high-throughput SaaS"
        decision = self.selector.select(task_description=task)
        selected_ids = [s.id for s in decision["selected_skills"]]
        self.assertIn("system-design-engineering", selected_ids)

    def test_communication_skill_selection(self):
        task = "Build a multi-channel notification engine with email deliverability, SMS OTP, and WebSocket presence"
        decision = self.selector.select(task_description=task)
        selected_ids = [s.id for s in decision["selected_skills"]]
        self.assertIn("communication-infrastructure", selected_ids)
        self.assertIn("email-engineering", selected_ids)
        self.assertIn("sms-engineering", selected_ids)
        self.assertIn("realtime-systems-engineering", selected_ids)


if __name__ == "__main__":
    unittest.main()
