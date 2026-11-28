---
id: DEC-0001
title: Use Append-Only SQLite for Audit Ledger
status: APPROVED
date: 2026-11-20
deciders: [Principal Architect, Security Officer]
---

# DEC-0001: Use Append-Only SQLite for Audit Ledger

## Context & Problem Statement
Autonomous AI agents require an immutable, tamper-evident audit trail of all state transitions, tool invocations, and cryptographic approvals without introducing heavy external database infrastructure.

## Decision
We utilize a local, append-only SQLite database with SHA-256 hash chaining of sequential ledger events.

## Consequences
- **Positive:** Zero external network latency; deterministic cross-session portability; tamper-evident verification.
- **Negative:** Single-writer concurrency constraints, mitigated by local write-ahead logging (WAL).
