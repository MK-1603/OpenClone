# AGENT.md — OpenClone AI Engineering Operating Contract

## Version 2.0.0

This file governs AI coding agents operating within the OpenClone repository, including Claude Code, Codex, Google Antigravity, Cursor, OpenHands, and human contributors.

**Canonical Product:** OpenClone  
**Product Category:** Universal AI Engineering Platform  
**Framework:** AI Engineering Framework (AIEF)  
**Canonical Package:** `openclone`  
**Primary CLI:** `openclone`  
**Legacy CLI Alias:** `aisdf`  
**Canonical Repository:** `MK-1603/OpenClone`  
**Tagline:** *Build with Any AI. Governed by One Engineering Standard.*

---

## 1. Instruction Precedence

When executing engineering tasks, adhere to this strict hierarchy:

1. Platform/system/developer safety constraints and execution sandboxes.
2. Explicit, current human owner instructions.
3. This `AGENT.md` and `AGENTS.md` operating contracts.
4. Approved `PROJECT.md`, governance rules, security baseline, and active approved plans.
5. Canonical architecture specifications (`docs/architecture/`).
6. Relevant test suites, schemas, and source code.
7. Historical notes and generated summaries.

If instructions conflict, **never silently choose the permissive option**. Record the conflict and request clarification from the owner if it affects scope, security, architecture, or compatibility.

---

## 2. Mandatory Session Pre-Flight

Before undertaking any modifications:

1. Confirm repository root directory.
2. Inspect current branch and latest commit.
3. Run `git status --short` and verify all user changes. **Never reset, clean, force checkout, or discard user changes.**
4. Identify the approved task and its explicit acceptance criteria.
5. Review relevant sections of `PROJECT.md`, `README.md`, and affected test suites.
6. Verify local toolchain and environment permissions.
7. Record unknowns and uncertainties rather than guessing.

---

## 3. Product Identity & Backward-Compatibility Guarantee

- **Target Identity:** OpenClone is the official universal platform identity.
- **Packaging Invariant:** The Python package name, distribution identifier, and import root MUST remain `openclone`.
- **CLI Invariant:** The primary executable command MUST remain `openclone`, with `aisdf` supported as a legacy alias.
- **Zero-Removal Principle:** Do not remove, rename, or deprecate existing working modules without an explicit migration and human authorization. Platform modernization is strictly additive and non-breaking.

---

## 4. Scope Control — Strict "No AI Slope" Policy

Only implement the approved task.

Before introducing any feature, dependency, module, service, abstraction, or external integration, verify:

- What concrete engineering problem it solves.
- Why existing capabilities in the repository are insufficient.
- Why a smaller or simpler change is inadequate.
- The maintenance, security, and operational overhead.
- How it will be deterministically verified by automated tests.

Do not perform unsolicited mass formatting, refactors, renamings, or code reorganizations.

---

## 5. Evidence & Truthful Maturity

Classify all capabilities with truthful maturity labels:

- `PROPOSED`
- `SPECIFIED`
- `IMPLEMENTED`
- `TESTED`
- `INTEGRATED`
- `INDEPENDENTLY_VERIFIED`
- `DEPLOYED`
- `PARTIALLY_IMPLEMENTED`
- `NEEDS_HARDENING`
- `MISSING`
- `REQUIRES_COMPATIBILITY`

**Never claim:**

- A component is tested without running the test suite and capturing execution output.
- A platform build is complete without building the artifact.
- A feature is production-ready without reproducible verification.
- An updater is safe without transaction rollback tests.

---

## 6. Human Approval Boundaries

Obtain explicit human approval before:

- Altering core requirements, product scope, data models, or public API interfaces.
- Introducing paid external services or cloud resources.
- Adding third-party package dependencies.
- Deleting or modifying existing public files or CLI subcommands.
- Executing destructive filesystem or data operations.
- Tagging, branching, merging, publishing releases, or pushing to remote git origins.

AI agents cannot approve their own work. A generated plan is not an approval.

---

## 7. Security & Sandboxing Invariants

- **Deny by default:** Least-privilege execution across all processes and tool invocations.
- **Credential Protection:** Never expose, log, or commit `.env` files, API keys, private certificates, or secrets.
- **Process Containment:** Subprocess execution must use argument arrays (`argv`), never raw shell strings (`shell=True`).
- **Path Sanitization:** Enforce strict containment within approved workspace roots; prevent path traversal attacks (`..`).
- **Update Verification:** All downloaded artifacts must undergo cryptographic SHA-256 verification and compatibility checks before staging.

---

## 8. Deterministic Platform Governance

LLMs propose; deterministic code and authorized human engineers decide.

- Task states must transition through the formal finite state machine (`DRAFT` $\rightarrow$ `PLANNED` $\rightarrow$ `APPROVED` $\rightarrow$ `READY` $\rightarrow$ `RUNNING` $\rightarrow$ `SUCCEEDED`/`FAILED`).
- Task plans are locked to cryptographic SHA-256 digests. Any scope modification automatically revokes prior approvals.
- All actions, approvals, and transitions must be recorded in the hash-chained SQLite audit ledger.

---

## 9. Testing & Zero-Regression Standards

Before declaring any task or milestone complete:

1. Run the full pytest test suite (`pytest tests/`) and confirm **351+ tests pass with 0 failures**.
2. Run repository integrity checks (`python tools/validate_repository.py`).
3. Run relative link verification (`python tools/check_links.py`).
4. Inspect the complete git diff (`git diff`).
5. Ensure zero regression across existing workforce, planning, approval, and MCP capabilities.

---

## 10. Definition of Done

A task is complete **only** when its acceptance criteria are met, automated test evidence is captured on disk, canonical documentation is updated, the git diff is reviewed, and required human approvals are documented.
