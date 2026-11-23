"""NoteDigest demo entrypoint."""
from notedigest.engine import NoteDigestEngine

SAMPLE_NOTE = """
# Product Sync: OpenClone Architecture Review

The team reviewed the OpenClone v2.0 global runtime integration.

DECIDED: We will enforce deterministic human approval gates for all destructive commands.
DECIDED: Model Intelligence Engine will auto-route complex reasoning tasks to GPT-6.

Tasks for this sprint:
- @DevOps will configure GitHub Actions CI for multi-platform checks (due Friday)
- @Frontend will integrate the official OpenClone brand identity into the web dashboard
- TODO: Stress-test SQLite tamper-evident ledger under concurrent writes
- [ ] Implement WCAG AAA contrast verification in the UI finish-gate reviewer
"""

def main():
    engine = NoteDigestEngine()
    result = engine.process(SAMPLE_NOTE)
    print(engine.format_markdown(result))

if __name__ == "__main__":
    main()
