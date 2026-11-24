---
id: distributed-systems-engineering
name: Distributed Systems Engineering Skill
version: 1.0.0
category: distributed
description: CAP theorem, PACELC, distributed consensus, saga patterns, leader election, partitions, and distributed locks.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/distributed-systems-engineering/SKILL.md
triggers:
  - distributed systems
  - distributed
  - cap theorem
  - pacelc
  - consensus
  - raft
  - paxos
  - saga pattern
  - distributed transactions
  - distributed lock
  - redlock
  - partition
negative_triggers:
  - single-node-only
  - monolith-only
precedence: 26
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
  - cli
pre_build_gates:
  - Consistency model explicit (strong vs eventual consistency documented)
  - Partition tolerance and partial failure modes mapped
  - Distributed transaction alternative chosen (Saga vs 2PC avoided)
finish_gates:
  - Compensating transactions verified for all Saga steps
  - Lease-based TTL verified on all distributed locks
  - Split-brain and clock-skew defenses verified
verification:
  - Network partition simulation / chaos test pass
  - Saga compensation recovery test pass
---

# Distributed Systems Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `distributed` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone Backend & Distributed Intelligence  
**Workforce Alignment:** `distributed-systems-engineer`, `principal-architect`

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Guide the engineering of multi-node distributed systems, managing partial failures, consensus, distributed data consistency, and distributed workflow orchestration without introducing unwarranted operational fragility.

### Boundaries
- **In Scope:** CAP and PACELC trade-offs, consensus (Raft/Paxos), distributed locking with lease expiration, Saga pattern (orchestrated and choreographed), eventual consistency, and split-brain mitigation.
- **Out of Scope:** Single-server local process synchronization.

---

## 2. CANONICAL DISTRIBUTED RULES

1. **Avoid Distributed Transactions (2PC):** Two-Phase Commit is blocking, fragile to coordinator crashes, and performs poorly. Use the **Saga Pattern** with compensating actions for multi-service transactions.
2. **Distributed Locks Require Leases:** Any distributed lock (e.g. Redis Redlock, ZooKeeper znode) must include an explicit time-to-live (TTL) lease and a fencing token (monotonically increasing counter) to prevent split-brain execution when a worker stalls due to GC pauses.
3. **Expect Network Partitions:** Networks are unreliable. Systems must explicitly define behavior during network partitions: either reject writes to preserve consistency (CP) or accept writes and reconcile conflicts later (AP).
