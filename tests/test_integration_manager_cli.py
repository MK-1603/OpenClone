"""Tests for Integration Manager, REST Gateway, and CLI command dispatcher."""
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.openclone.integrations.cli import handle_integrations, handle_platforms
from src.openclone.integrations.manager import IntegrationManager
from src.openclone.integrations.rest import OpenCloneRESTGateway


class TestIntegrationManagerAndCLI(unittest.TestCase):
    """Test IntegrationManager operations, REST Gateway dispatch, and CLI commands."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.manager = IntegrationManager(self.temp_dir)
        self.rest = OpenCloneRESTGateway(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_manager_discover_and_status(self):
        discovered = self.manager.discover_platforms()
        self.assertGreaterEqual(len(discovered), 6)

        status = self.manager.get_status()
        self.assertEqual(status["workspace_root"], str(self.temp_dir))
        self.assertGreaterEqual(status["total_supported"], 6)

    def test_manager_connect_with_backup(self):
        res = self.manager.connect_platform("vscode")
        self.assertEqual(res["status"], "CONNECTED")
        mcp_path = self.temp_dir / ".vscode" / "mcp.json"
        self.assertTrue(mcp_path.exists())

        # Connect again to trigger backup
        res2 = self.manager.connect_platform("vscode")
        self.assertEqual(res2["status"], "CONNECTED")
        backup_dir = self.temp_dir / ".openclone" / "backups"
        self.assertTrue(backup_dir.exists())
        backups = list(backup_dir.glob("vscode_*"))
        self.assertGreaterEqual(len(backups), 1)

    def test_manager_health_check(self):
        self.manager.connect_platform("vscode")
        hc = self.manager.health_check("vscode")
        self.assertEqual(hc["status"], "PASS")

        all_hc = self.manager.health_check()
        self.assertEqual(all_hc["status"], "COMPLETED")

    def test_rest_gateway_endpoints(self):
        # Health
        res_health = self.rest.dispatch("GET", "/api/v1/health")
        self.assertEqual(res_health["status"], "healthy")

        # Capabilities
        res_caps = self.rest.dispatch("GET", "/api/v1/capabilities")
        self.assertGreaterEqual(res_caps["total"], 20)

        # Projects
        res_proj = self.rest.dispatch("GET", "/api/v1/projects")
        self.assertGreaterEqual(len(res_proj["projects"]), 1)

        # Plans
        res_plan = self.rest.dispatch("POST", "/api/v1/plans", {"prompt": "Create REST gateway test"})
        self.assertIn("plan_id", res_plan)

        # Agents
        res_agents = self.rest.dispatch("GET", "/api/v1/agents")
        self.assertGreaterEqual(res_agents["total"], 1)

        # Verification
        res_verif = self.rest.dispatch("GET", "/api/v1/verification")
        self.assertEqual(res_verif["status"], "PASS")

    def test_cli_platforms_commands(self):
        with patch("sys.stdout", new_callable=io.StringIO):
            code_disc = handle_platforms(["discover"])
            self.assertEqual(code_disc, 0)

            code_list = handle_platforms(["list"])
            self.assertEqual(code_list, 0)

            code_stat = handle_platforms(["status"])
            self.assertEqual(code_stat, 0)

    def test_cli_integrations_commands(self):
        with patch("sys.stdout", new_callable=io.StringIO):
            code_list = handle_integrations(["list"])
            self.assertEqual(code_list, 0)


if __name__ == "__main__":
    unittest.main()
