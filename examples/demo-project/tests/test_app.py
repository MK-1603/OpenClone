"""Test app entry point."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from app import SAMPLE_NOTE
from notedigest.engine import NoteDigestEngine

class TestApp(unittest.TestCase):
    def test_sample_note_digest(self):
        engine = NoteDigestEngine()
        res = engine.process(SAMPLE_NOTE)
        self.assertEqual(len(res.decisions), 2)
        self.assertGreaterEqual(len(res.action_items), 4)

if __name__ == "__main__":
    unittest.main()
