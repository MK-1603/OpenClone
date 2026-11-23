# Concept 05: Cryptographic Audit Ledger (Primary Specification)

## 1. Core Principle
Every decision, task transition, human approval, command execution, and test check is committed to an append-only, tamper-evident SQLite database using cryptographic SHA-256 hash chaining.

## 2. Invariants
1. **Hash Chaining:** Each new event hashes the payload combined with the preceding event's hash:
   `hash = SHA256(event_id + task_id + event_type + actor + payload + prev_hash)`
2. **Tamper Detection:** The `verify-ledger` command traverses the entire event chain. Any post-hoc mutation of actor, payload, or event type fails verification immediately.

---

## 4. Architectural Alternatives & Operational Trade-Offs

## 1. Alternate Paradigm: Git-Native Signed Commit Stream
In repositories where developers prefer not to maintain a SQLite database file, the alternate approach uses **Git Commit Metadata as the Audit Ledger**.

## 2. How the Alternate Operates
1. **Event-Per-Commit:** Every task transition or approval generates an empty or metadata git commit on an orphaned audit branch (e.g., `openclone-audit`).
2. **GPG / SSH Signatures:** Commits are cryptographically signed using the approver's or system's SSH/GPG key.
3. **Distributed Auditing:** Leveraging Git's native Merkle tree guarantees tamper evidence while making the audit log easily pushable to remote hosts (GitHub, GitLab) without database replication.

## 3. Trade-Off Analysis
* **Strengths:** Zero local database footprint, native git branch integration.
* **Risks:** Higher filesystem latency per event; git history bloat for high-frequency test loops.
