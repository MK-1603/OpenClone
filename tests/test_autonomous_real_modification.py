"""Unit tests for Autonomous Engineering Engine atomic file modifications and confinement."""
import tempfile
import unittest
from pathlib import Path

from src.openclone.autonomous.engine import AutonomousExecutionEngine
from src.openclone.autonomous.models import TaskNode
from src.openclone.runtime.workforce import Ledger


class TestAutonomousRealModification(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)
        self.engine = AutonomousExecutionEngine(workspace_root=self.workspace)
        self.ledger = Ledger(self.workspace)

    def tearDown(self):
        try:
            self.ledger.close()
        except Exception:
            pass
        self.temp_dir.cleanup()

    def test_atomic_file_write_success(self):
        """Verify task writes a real file atomically with valid syntax."""
        task = TaskNode(
            task_id="t-write-001",
            title="Create helper utility",
            worker_role="backend-engineer",
            action="code",
            target_path="src/utils/math_helper.py",
            file_content="def add(a: int, b: int) -> int:\n    return a + b\n",
        )

        result = self.engine._execute_task(task, self.workspace, self.ledger)

        self.assertTrue(result.success)
        target_file = self.workspace / "src/utils/math_helper.py"
        self.assertTrue(target_file.is_file())
        self.assertIn("def add", target_file.read_text(encoding="utf-8"))

    def test_path_traversal_escape_rejected(self):
        """Verify task attempting to escape workspace root is rejected with error."""
        task = TaskNode(
            task_id="t-escape-001",
            title="Malicious escape attempt",
            worker_role="backend-engineer",
            action="code",
            target_path="../../escaped_secret.txt",
            file_content="secret",
        )

        result = self.engine._execute_task(task, self.workspace, self.ledger)

        self.assertFalse(result.success)
        self.assertIn("escapes workspace root", result.output)
        self.assertFalse((self.workspace.parent / "escaped_secret.txt").exists())

    def test_syntax_error_rejected_before_commit(self):
        """Verify python syntax error fails execution without corrupting target file."""
        target_file = self.workspace / "src/bad_code.py"
        task = TaskNode(
            task_id="t-bad-syntax",
            title="Syntax error code",
            worker_role="backend-engineer",
            action="code",
            target_path="src/bad_code.py",
            file_content="def broken_syntax(:\n    pass\n",
        )

        result = self.engine._execute_task(task, self.workspace, self.ledger)

        self.assertFalse(result.success)
        self.assertFalse(target_file.exists())


if __name__ == "__main__":
    unittest.main()
