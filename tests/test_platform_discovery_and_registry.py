"""Tests for Platform Discovery Engine and Platform Capability Registry."""
import unittest
from pathlib import Path

from src.openclone.integrations.discovery import PlatformDiscoveryEngine
from src.openclone.integrations.registry import PlatformCapabilityRegistry, PlatformMaturity, get_platform_registry


class TestPlatformDiscoveryAndRegistry(unittest.TestCase):
    """Verify registry declarations and platform discovery mechanisms."""

    def setUp(self):
        self.registry = get_platform_registry()
        self.discovery = PlatformDiscoveryEngine()

    def test_registry_canonical_platforms_present(self):
        expected_ids = {"antigravity", "vscode", "cursor", "jetbrains", "zed", "claude-code", "codex", "generic"}
        registered_ids = {d.platform_id for d in self.registry.list_all()}
        for pid in expected_ids:
            self.assertIn(pid, registered_ids)

    def test_registry_maturity_tiers(self):
        antigravity = self.registry.get("antigravity")
        self.assertIsNotNone(antigravity)
        self.assertEqual(antigravity.maturity, PlatformMaturity.VERIFIED)

        vscode = self.registry.get("vscode")
        self.assertIsNotNone(vscode)
        self.assertEqual(vscode.maturity, PlatformMaturity.VERIFIED)

        generic = self.registry.get("generic")
        self.assertIsNotNone(generic)
        self.assertEqual(generic.maturity, PlatformMaturity.EXPERIMENTAL)

    def test_discovery_engine_probes_platforms(self):
        platforms = self.discovery.discover_all()
        self.assertGreaterEqual(len(platforms), 6)
        ids = {p.platform_id for p in platforms}
        self.assertIn("antigravity", ids)
        self.assertIn("vscode", ids)
        self.assertIn("cursor", ids)
        self.assertIn("jetbrains", ids)
        self.assertIn("zed", ids)
        self.assertIn("generic", ids)

    def test_system_summary(self):
        summary = self.discovery.get_system_summary()
        self.assertIn("os", summary)
        self.assertIn("total_supported_platforms", summary)
        self.assertGreaterEqual(summary["total_supported_platforms"], 6)


if __name__ == "__main__":
    unittest.main()
