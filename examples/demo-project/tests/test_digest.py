"""Tests for NoteDigest core engine and extractors."""
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from notedigest.models import ActionItem, Decision, DigestResult
from notedigest.extractor import NoteExtractor
from notedigest.engine import NoteDigestEngine


SAMPLE_TRANSCRIPT = """
# Sprint Planning & Product Sync - Q1 Roadmap

The team discussed the upcoming Q1 deliverables for the customer portal.
Alex outlined the infrastructure needs, while Jordan reviewed client feedback.

DECIDED: We will migrate all user authentication to passkey / OAuth2 by March 15.
DECIDED: Deprecate the legacy v1 REST endpoint on April 1st.

Key tasks assigned during the call:
- @Alex will configure OAuth2 identity provider credentials (due March 5)
- @Jordan shall implement the frontend passkey login UI (due March 12)
- TODO: Fix critical session timeout bug on mobile Safari (URGENT)
- [ ] Write integration test coverage for authentication callbacks

Open questions remaining:
- Question: What is the fallback if a user loses their passkey device?
- Do we need SOC2 compliance documentation before the enterprise rollout?
"""


class TestNoteDigest(unittest.TestCase):
    def setUp(self):
        self.engine = NoteDigestEngine()
        self.extractor = NoteExtractor()

    def test_extract_decisions(self):
        decisions = self.extractor.extract_decisions(SAMPLE_TRANSCRIPT)
        self.assertEqual(len(decisions), 2)
        self.assertEqual(decisions[0].id, "DEC-001")
        self.assertIn("migrate all user authentication", decisions[0].summary)
        self.assertEqual(decisions[1].id, "DEC-002")
        self.assertIn("Deprecate the legacy v1", decisions[1].summary)

    def test_extract_action_items(self):
        actions = self.extractor.extract_action_items(SAMPLE_TRANSCRIPT)
        self.assertGreaterEqual(len(actions), 4)

        # Check Alex task
        alex_action = next((a for a in actions if a.owner == "Alex"), None)
        self.assertIsNotNone(alex_action)
        self.assertIn("configure OAuth2", alex_action.description)
        self.assertEqual(alex_action.deadline, "March 5")

        # Check Jordan task
        jordan_action = next((a for a in actions if a.owner == "Jordan"), None)
        self.assertIsNotNone(jordan_action)
        self.assertIn("frontend passkey login", jordan_action.description)

        # Check Urgent priority
        urgent_action = next((a for a in actions if "session timeout" in a.description.lower()), None)
        self.assertIsNotNone(urgent_action)
        self.assertEqual(urgent_action.priority, "High")

    def test_extract_open_questions(self):
        questions = self.extractor.extract_open_questions(SAMPLE_TRANSCRIPT)
        self.assertEqual(len(questions), 2)
        self.assertTrue(any("passkey device" in q for q in questions))
        self.assertTrue(any("SOC2 compliance" in q for q in questions))

    def test_end_to_end_engine(self):
        result = self.engine.process(SAMPLE_TRANSCRIPT)
        self.assertIsInstance(result, DigestResult)
        self.assertEqual(result.title, "Sprint Planning & Product Sync - Q1 Roadmap")
        self.assertGreater(result.raw_word_count, 50)
        self.assertEqual(len(result.decisions), 2)
        self.assertGreaterEqual(len(result.action_items), 4)
        self.assertEqual(len(result.open_questions), 2)

        md = self.engine.format_markdown(result)
        self.assertIn("# Sprint Planning & Product Sync - Q1 Roadmap", md)
        self.assertIn("## Key Decisions", md)
        self.assertIn("## Action Items & Ownership", md)
        self.assertIn("Alex", md)
        self.assertIn("Jordan", md)

    def test_json_serialization(self):
        result = self.engine.process(SAMPLE_TRANSCRIPT)
        data = self.engine.to_dict(result)
        self.assertIn("title", data)
        self.assertIn("decisions", data)
        self.assertIn("action_items", data)
        self.assertEqual(len(data["decisions"]), 2)

    def test_empty_content(self):
        result = self.engine.process("   \n  \n  ")
        self.assertEqual(result.raw_word_count, 0)
        self.assertEqual(len(result.decisions), 0)
        self.assertEqual(len(result.action_items), 0)


if __name__ == "__main__":
    unittest.main()
