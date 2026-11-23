# AGENTS.md — NoteDigest Operating Contract
## Version 1.0.0

This operating contract governs all human contributors and AI coding agents working inside NoteDigest.

**Canonical Product:** NoteDigest  
**Governing Standard:** OpenClone Software Engineering Framework (AISDF)  
**Parent Framework:** `MK-1603/OpenClone`

---

## 1. Instruction Precedence
1. System and environment safety boundaries.
2. Explicit human owner instructions.
3. This `AGENTS.md` operating contract.
4. `PROJECT.md` source of truth and invariant boundaries.
5. Code, tests, and documentation.

## 2. Invariant Engineering Rules
- **No Hallucinated Claims:** Do not claim a test passed or feature works without real command execution and verifiable exit code 0.
- **Scope Discipline:** Only implement approved features in `PROJECT.md`. No unsolicited refactoring, unnecessary dependencies, or architectural sprawl.
- **Standard Library First:** Prefer Python's standard library over heavy third-party dependencies unless explicitly authorized.
- **Deterministic Approvals:** Human approvers decide on schema, architectural, and destructive actions.

## 3. Verification Standards
Before declaring any task complete:
1. Run all unit tests: `python -m unittest discover -s tests`.
2. Verify zero broken links and exact casing.
3. Record exact execution commands and evidence.
