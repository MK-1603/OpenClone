"""Rule-based text analysis and extraction engine for NoteDigest."""
import re
from typing import List, Tuple
from .models import ActionItem, Decision, KeyPoint


class NoteExtractor:
    """Extracts structured decisions, actions, and key points from unstructured notes."""

    ACTION_PATTERNS = [
        re.compile(r'(?:TODO|ACTION|TASK):\s*(.+)', re.IGNORECASE),
        re.compile(r'\[\s*\]\s*(.+)', re.IGNORECASE),
        re.compile(r'(?:^|\n)[-*]\s*@?([A-Za-z0-9_-]+)\s*(?:will|to|shall)\s*(.+)', re.IGNORECASE),
        re.compile(r'(?:^|\n)[-*]\s*(.+?)\s*\(Assigned to:\s*@?([A-Za-z0-9_-]+)(?:,\s*Due:\s*([^)]+))?\)', re.IGNORECASE),
    ]

    DECISION_PATTERNS = [
        re.compile(r'(?:DECIDED|DECISION|AGREED|RESOLVED):\s*(.+)', re.IGNORECASE),
        re.compile(r'(?:^|\n)[-*]\s*(?:We decided|Team agreed|Approved)\s*(?:to|that)?\s*(.+)', re.IGNORECASE),
    ]

    QUESTION_PATTERNS = [
        re.compile(r'(?:QUESTION|OPEN QUESTION|TBD|UNRESOLVED):\s*(.+)', re.IGNORECASE),
        re.compile(r'(?:^|\n)[-*]\s*(.+?\?)', re.IGNORECASE),
    ]

    DEADLINE_PATTERNS = [
        re.compile(r'\b(?:by|due|before|deadline:?)\s+([A-Za-z]+(?:\s+\d{1,2}(?:st|nd|rd|th)?|\s+\d{4})?|\d{4}-\d{2}-\d{2})\b', re.IGNORECASE),
    ]

    def extract_action_items(self, text: str) -> List[ActionItem]:
        items: List[ActionItem] = []
        seen = set()
        count = 1

        for line in text.splitlines():
            line_str = line.strip()
            if not line_str:
                continue

            for pattern in self.ACTION_PATTERNS:
                m = pattern.search(line_str)
                if m:
                    groups = m.groups()
                    desc = ""
                    owner = "Unassigned"
                    deadline = None

                    if len(groups) == 1:
                        desc = groups[0].strip()
                    elif len(groups) >= 2 and groups[0] and not groups[0].startswith("http"):
                        if len(groups) == 3 and groups[2]:
                            desc = groups[0].strip()
                            owner = groups[1].strip()
                            deadline = groups[2].strip()
                        else:
                            owner = groups[0].strip()
                            desc = groups[1].strip()

                    # Extract inline deadline if not already found
                    if not deadline:
                        dl_match = self.DEADLINE_PATTERNS[0].search(desc)
                        if dl_match:
                            deadline = dl_match.group(1).strip()

                    # Clean desc
                    desc = re.sub(r'\s*\(Assigned.*', '', desc).strip()
                    desc = re.sub(r'\b(?:by|due|deadline:?)\s+.*', '', desc, flags=re.IGNORECASE).strip()

                    if desc and desc not in seen:
                        seen.add(desc)
                        priority = "High" if any(w in desc.lower() for w in ["urgent", "critical", "blocker", "asap"]) else "Normal"
                        items.append(ActionItem(
                            id=f"ACT-{count:03d}",
                            description=desc,
                            owner=owner,
                            deadline=deadline,
                            priority=priority
                        ))
                        count += 1
                    break

        return items

    def extract_decisions(self, text: str) -> List[Decision]:
        decisions: List[Decision] = []
        seen = set()
        count = 1

        for line in text.splitlines():
            line_str = line.strip()
            if not line_str:
                continue

            for pattern in self.DECISION_PATTERNS:
                m = pattern.search(line_str)
                if m:
                    summary = m.group(1).strip()
                    if summary and summary not in seen:
                        seen.add(summary)
                        decisions.append(Decision(
                            id=f"DEC-{count:03d}",
                            summary=summary
                        ))
                        count += 1
                    break

        return decisions

    def extract_open_questions(self, text: str) -> List[str]:
        questions: List[str] = []
        seen = set()

        for line in text.splitlines():
            line_str = line.strip()
            if not line_str:
                continue

            for pattern in self.QUESTION_PATTERNS:
                m = pattern.search(line_str)
                if m:
                    q = m.group(1).strip()
                    if q and q not in seen:
                        seen.add(q)
                        questions.append(q)
                    break

        return questions

    def extract_key_points(self, text: str) -> List[KeyPoint]:
        points: List[KeyPoint] = []
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        for p in paragraphs:
            # Skip bullet lists that were pure actions/decisions
            if p.startswith(("#", "-", "*")) and ("DECIDED:" in p or "TODO:" in p or "ACTION:" in p):
                continue
            first_line = p.splitlines()[0].strip()
            if first_line.startswith("#"):
                topic = first_line.lstrip("#").strip()
                body = " ".join([l.strip() for l in p.splitlines()[1:] if l.strip()])
                if body:
                    points.append(KeyPoint(topic=topic, details=body))
            elif len(p.split()) > 10:
                first_sentence = p.split(".")[0].strip() + "."
                points.append(KeyPoint(topic=first_sentence[:50], details=p))

        return points[:5]
