"""Unit tests for Reverse Engineering Level 2 ephemeral test sandbox runner."""
import tempfile
import unittest
from pathlib import Path

from src.openclone.reverse_engineering.engine import ReverseEngineeringEngine
from src.openclone.reverse_engineering.models import CoverageStatus, ExecutionLevel


class TestReverseEngineeringLevel2(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)
        self.engine = ReverseEngineeringEngine(workspace_root=self.workspace)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_level2_without_human_approval_raises_permission_error(self):
        """Verify Level 2 analysis without human_approved=True raises PermissionError."""
        with self.assertRaises(PermissionError):
            self.engine.analyze(execution_level=ExecutionLevel.LEVEL_2_RUNTIME, human_approved=False)

    def test_level2_with_human_approval_executes_runtime_analysis(self):
        """Verify Level 2 analysis with human_approved=True marks runtime analysis as COMPLETE."""
        report = self.engine.analyze(execution_level=ExecutionLevel.LEVEL_2_RUNTIME, human_approved=True)

        self.assertEqual(report.execution_level, ExecutionLevel.LEVEL_2_RUNTIME)
        self.assertEqual(report.coverage.runtime_analysis, CoverageStatus.COMPLETE)


if __name__ == "__main__":
    unittest.main()
