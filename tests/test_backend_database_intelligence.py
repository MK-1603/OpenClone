"""Automated Test Suite for OpenClone Backend, Database & Distributed Systems Intelligence.

Tests cover:
- Architecture Decision Engine & Monolith-First Rule
- Multi-tier Rate Limiter (Token Bucket, Sliding Window, HTTP 429 headers)
- Database Migration Guard (destructive DDL, unindexed foreign keys, lock risks)
- Production Readiness Scorecard across 15 production categories
"""
from __future__ import annotations

import unittest
from pathlib import Path

from src.openclone.backend.architecture_decision import (
    BackendArchitectureDecisionEngine,
    WorkloadProfile,
)
from src.openclone.backend.migration_guard import (
    DatabaseMigrationGuard,
    MigrationSafetyLevel,
)
from src.openclone.backend.rate_limiter import (
    RateLimitAlgorithm,
    RateLimiter,
    RateLimitPolicy,
)
from src.openclone.backend.scorecard import (
    BackendProductionScorecard,
    ScorecardStatus,
)

ROOT = Path(__file__).resolve().parents[1]


class TestBackendArchitectureDecisionEngine(unittest.TestCase):
    """Verifies architectural recommendations and adherence to Monolith-First Rule."""

    def setUp(self):
        self.engine = BackendArchitectureDecisionEngine()

    def test_monolith_first_standard_workload(self):
        profile = WorkloadProfile(
            project_name="Standard SaaS",
            archetype="saas",
            peak_writes_per_second=200.0,
            peak_reads_per_second=1500.0,
            data_volume_gb=100.0,
        )
        decision = self.engine.evaluate(profile)
        self.assertEqual(decision.pattern, "Modular Monolith")
        self.assertTrue(any("Modular Monolith satisfies concurrency" in r for r in decision.rationale))
        self.assertIn("PostgreSQL", decision.database)

    def test_offline_sync_recommends_embedded(self):
        profile = WorkloadProfile(
            project_name="Field Mobile App",
            archetype="mobile",
            peak_writes_per_second=50.0,
            peak_reads_per_second=200.0,
            data_volume_gb=10.0,
            requires_offline=True,
        )
        decision = self.engine.evaluate(profile)
        self.assertIn("SQLite", decision.database)

    def test_extreme_scale_recommends_distributed_services(self):
        profile = WorkloadProfile(
            project_name="High-Volume Telemetry Platform",
            archetype="telemetry",
            peak_writes_per_second=15_000.0,
            peak_reads_per_second=50_000.0,
            data_volume_gb=20_000.0,
        )
        decision = self.engine.evaluate(profile)
        self.assertEqual(decision.pattern, "Event-Driven Microservices")
        self.assertEqual(decision.operational_complexity, "HIGH")


class TestRateLimiter(unittest.TestCase):
    """Verifies token bucket and sliding window rate limiting."""

    def setUp(self):
        self.limiter = RateLimiter()

    def test_token_bucket_allows_burst_then_throttles(self):
        client = "192.168.1.100"
        policy = RateLimitPolicy(
            name="burst_tier",
            limit=5,
            window_seconds=1,
            algorithm=RateLimitAlgorithm.TOKEN_BUCKET,
            burst_capacity=5,
        )
        for _ in range(5):
            dec = self.limiter.is_allowed(client, custom_policy=policy)
            self.assertTrue(dec.allowed)

        # 6th request must be throttled
        throttled = self.limiter.is_allowed(client, custom_policy=policy)
        self.assertFalse(throttled.allowed)
        self.assertGreater(throttled.retry_after_seconds, 0)
        self.assertIn("RateLimit-Limit", throttled.headers)
        self.assertIn("Retry-After", throttled.headers)

    def test_sliding_window_counter(self):
        sw_policy = RateLimitPolicy(
            name="login_tier",
            limit=3,
            window_seconds=10,
            algorithm=RateLimitAlgorithm.SLIDING_WINDOW_COUNTER,
        )
        client = "user@test.org"
        for _ in range(3):
            self.assertTrue(self.limiter.is_allowed(client, custom_policy=sw_policy).allowed)
        self.assertFalse(self.limiter.is_allowed(client, custom_policy=sw_policy).allowed)


class TestDatabaseMigrationGuard(unittest.TestCase):
    """Verifies automated DDL static analysis and expand-and-contract safety checks."""

    def test_drop_table_blocked(self):
        sql = "DROP TABLE users;"
        level, findings = DatabaseMigrationGuard.inspect(sql)
        self.assertEqual(level, MigrationSafetyLevel.DESTRUCTIVE_BLOCKED)
        self.assertGreater(len(findings), 0)
        self.assertIn("Destructive Table Drop", findings[0].finding_type)

    def test_unindexed_foreign_key_warned(self):
        sql = """
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
        level, findings = DatabaseMigrationGuard.inspect(sql)
        self.assertEqual(level, MigrationSafetyLevel.WARNING_REQUIRES_REVIEW)
        self.assertTrue(any("Unindexed Foreign Key" in f.finding_type for f in findings))


class TestBackendProductionScorecard(unittest.TestCase):
    """Verifies comprehensive production readiness evaluation across 15 categories."""

    def test_scorecard_evaluation(self):
        audit_data = {
            "architecture": {"status": "PASS", "score": 100.0, "evidence": "Monolith-First verified"},
            "api": {"status": "PASS", "score": 100.0, "evidence": "OpenAPI contracts strictly typed"},
            "database": {"status": "PASS", "score": 100.0, "evidence": "Foreign keys indexed, RLS enabled"},
            "security": {"status": "PASS", "score": 100.0, "evidence": "Zero secrets logged, TLS 1.3 enforced"},
            "rate_limiting": {"status": "PASS", "score": 100.0, "evidence": "Tiered token bucket active"},
            "caching": {"status": "PASS", "score": 100.0, "evidence": "Cache-aside with TTL and XFetch"},
            "async_processing": {"status": "PASS", "score": 100.0, "evidence": "DLQ configured with alert"},
            "distributed_systems": {"status": "PASS", "score": 100.0, "evidence": "Saga pattern with compensation"},
            "reliability": {"status": "PASS", "score": 100.0, "evidence": "Circuit breaker and health probes"},
            "performance": {"status": "PASS", "score": 100.0, "evidence": "p99 < 200ms latency budgeted"},
            "observability": {"status": "PASS", "score": 100.0, "evidence": "Structured JSON + trace_id"},
            "testing": {"status": "PASS", "score": 100.0, "evidence": "100% test pass on CI"},
            "deployment": {"status": "PASS", "score": 100.0, "evidence": "Zero-downtime rolling update"},
            "data_governance": {"status": "PASS", "score": 100.0, "evidence": "GDPR deletion retention policy"},
            "cost": {"status": "PASS", "score": 100.0, "evidence": "Capacity headroom within budget"},
        }
        res = BackendProductionScorecard.evaluate(project_name="TestApp", audit_data=audit_data)
        self.assertEqual(res.overall_status, ScorecardStatus.PASS)
        self.assertEqual(res.passed_categories, 15)
        self.assertEqual(res.failed_categories, 0)
        self.assertEqual(len(res.blocking_issues), 0)


if __name__ == "__main__":
    unittest.main()
