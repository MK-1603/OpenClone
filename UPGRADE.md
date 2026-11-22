# UPGRADE.md — OpenClone Evolution, Versioning & Upgrade Guide

## 1. Upgrade Philosophy & Guarantees

OpenClone is designed as a **long-term stable, upgradable engineering operating system**. As AI models, IDEs, and tools evolve, the framework's control plane preserves your project truth, approval history, audit ledgers, and architectural decisions without requiring destructive resets or manual data migrations.

### Non-Negotiable Backward Compatibility Commitments:
1. **Deterministic Immutability:** Historical audit ledger events are cryptographically hash-chained (`verify-ledger`). Future OpenClone runtime versions will always be able to traverse, verify, and validate ledgers created by prior versions.
2. **Canonical Project Continuity:** `PROJECT.md` and `AGENTS.md` formats remain readable and valid across versions. New governance fields are introduced with sensible default values.
3. **No Silent Re-Planning:** Tasks marked `SUCCEEDED` remain immutable. Upgrading the framework never re-triggers or invalidates completed work.
4. **Semantic Versioning:** OpenClone follows Strict Semantic Versioning 2.0.0 (`MAJOR.MINOR.PATCH`).
   - **PATCH:** Bug fixes, performance optimizations, scanner pin updates (100% backward compatible).
   - **MINOR:** New specialist roles, new engine specs, new workflows, new tool adapters (100% backward compatible).
   - **MAJOR:** Breaking changes to state schemas, API surfaces, or approval semantics (accompanied by automated database migration scripts).

---

## 2. Upgrading Existing Workspaces

When you update OpenClone to a newer version, use the built-in diagnostic and migration utilities to ensure your project workspaces remain fully aligned.

### Step 1: Run Pre-Flight Diagnostics (`doctor`)

To check workspace health and compatibility:

```bash
python openclone.py doctor --project path/to/your/project
# or with installed CLI:
openclone doctor --project path/to/your/project
```

The diagnostic command verifies:
* Presence and integrity of `PROJECT.md` and `AGENTS.md`.
* State store existence (`.aisdf/` or `.openclone/`).
* SQLite ledger hash-chain integrity.
* Security scanner lockfile pins.
* Identifies any pending schema updates.

### Step 2: Automated Workspace Migration (`upgrade`)

To automatically migrate an existing project database and schema:

```bash
python openclone.py upgrade --project path/to/your/project --actor "Your Name"
# or with installed CLI:
openclone upgrade --project path/to/your/project --actor "Your Name"
```

The upgrader:
1. Inspects the SQLite database (`workforce.sqlite3`).
2. Creates any newly required tables (`approvers`, `checks`, `findings`) idempotently.
3. Migrates legacy v4 schema fields to the hardened v1.0.0+ hash-chained standard.
4. Records an immutable `PROJECT_UPGRADED` event into the tamper-evident ledger.
5. Re-verifies the complete hash chain.

---

## 3. Extending and Upgrading Capabilities

### Adding or Upgrading Tool Adapters
Adapters reside in `adapters/` and bridge OpenClone to external agents (Claude Code, Cursor, Antigravity, OpenHands, OpenCode).
To upgrade or add an adapter:
1. Implement the interface defined in `runtime/adapters/WORKER-ADAPTER-CONTRACT.md`.
2. Map your tool's native execution events to OpenClone lifecycle states (`PLANNED`, `READY`, `RUNNING`, `SUCCEEDED`, `FAILED`).
3. Verify conformance using the checklist in `adapters/CONFORMANCE.md`.

### Adding Custom Specialist Roles
1. Define a role manifest JSON in `workforce/registry/workers/<role-name>.json`.
2. Declare the required permission profile (`allowed_actions`, `approval_required_for`).
3. Add the human-readable role guide in `workforce/teams/<TEAM>/roles/<ROLE-NAME>.md`.
4. Validate schema compliance with `python tools/validate_repository.py`.

### Upgrading Security Scanner Pins
OpenClone cryptographically locks security tooling by 40-character commit SHAs in `security/scanners.lock.json`. To refresh tool pins:
```bash
python tools/pin_scanners.py
```
This updates scanner hashes deterministically and generates a verifiable diff.

---

## 4. Release History & Deprecation Schedule

| Version | Status | State Store | Ledger Standard | Migration Support |
|---|---|---|---|---|
| **v1.0.0** | **Current Stable** | SQLite v2 | SHA-256 Hash-Chained | Native |
| **v4.0.0 (Legacy)** | Superseded | SQLite v1 | Unchained Events | Auto-migrated by `openclone upgrade` |
| **v3.x (Historical)** | Archived | Filesystem JSON | Historical artifacts | Preserved in `docs/release-history/` |

---

<div align="center">

**OpenClone** · *Build with Any AI. Governed by One Engineering Standard.*  
Repository: [github.com/MK-1603/aisdf](https://github.com/MK-1603/aisdf) · Licensed under MIT

</div>
