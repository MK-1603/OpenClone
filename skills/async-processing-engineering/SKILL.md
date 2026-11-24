---
id: async-processing-engineering
name: Asynchronous Processing & Messaging Skill
version: 1.0.0
category: backend
description: Message brokers, queues, background workers, at-least-once delivery, transactional outbox pattern, dead-letter queues, and idempotent consumers.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/async-processing-engineering/SKILL.md
triggers:
  - async
  - queue
  - queues
  - background job
  - background worker
  - rabbitmq
  - kafka
  - redis streams
  - dead letter queue
  - dlq
  - outbox pattern
  - transactional outbox
  - idempotent consumer
negative_triggers:
  - synchronous-only
  - static-site
precedence: 25
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
  - cli
pre_build_gates:
  - Broker technology selected based on scale (DB queue vs RabbitMQ vs Kafka)
  - Message schema and serialization format defined
  - Consumer idempotency key and deduplication mechanism specified
finish_gates:
  - Dead-Letter Queue (DLQ) configured for poison message containment
  - Transactional Outbox pattern implemented for database-to-message consistency
  - Worker concurrency, visibility timeouts, and retry backoffs verified
verification:
  - Duplicate delivery handling test pass (idempotent consumer verification)
  - DLQ routing and poison message isolation test pass
---

# Asynchronous Processing & Messaging — Specialist Skill
**Version:** `1.0.0` | **Category:** `backend` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone Backend & Distributed Intelligence  
**Workforce Alignment:** `backend-engineer`, `distributed-systems-engineer`

See canonical specification at [`../../framework/skills/async-processing-engineering/SKILL.md`](../../framework/skills/async-processing-engineering/SKILL.md).
