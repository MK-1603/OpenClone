---
id: distributed-systems-engineering
name: Distributed Systems Engineering Skill
version: 1.0.0
category: distributed
description: CAP theorem, PACELC, distributed consensus, saga patterns, leader election, partitions, and distributed locks.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/distributed-systems-engineering/SKILL.md
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

See canonical specification at [`../../framework/skills/distributed-systems-engineering/SKILL.md`](../../framework/skills/distributed-systems-engineering/SKILL.md).
