---
id: async-processing-engineering
name: Asynchronous Processing & Messaging Skill
version: 1.0.0
category: backend
description: Message brokers, queues, background workers, at-least-once delivery, transactional outbox pattern, dead-letter queues, and idempotent consumers.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/async-processing-engineering/SKILL.md
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

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Decouple time-consuming operations from synchronous HTTP request/response lifecycles, guarantee reliable event delivery, handle spikes gracefully, and prevent message loss during worker crashes.

### Boundaries
- **In Scope:** Message queues (RabbitMQ, SQS, Redis Streams, Kafka), background job schedulers, worker pool concurrency, at-least-once delivery semantics, Transactional Outbox pattern, idempotent consumers, and Dead-Letter Queues (DLQ).
- **Out of Scope:** Client-side background sync.

---

## 2. CANONICAL ASYNC & MESSAGING RULES

1. **Transactional Outbox Pattern:**
   Never write to a database and publish to a message broker in two separate uncoordinated steps (dual-write problem). Instead:
   - Insert business entity and outbox event record in a single local database transaction.
   - An asynchronous relay worker reads outbox table records and publishes to the broker with at-least-once delivery.
2. **Idempotent Consumers:**
   Because networks and brokers retry, assume messages will be delivered more than once. Every message consumer must be idempotent by:
   - Storing processed `message_id`s in a deduplication table with a unique constraint.
   - Using conditional database updates (`UPDATE accounts SET balance = balance + 10 WHERE id = 1 AND version = 2`).
3. **Dead-Letter Queues (DLQ):**
   Unprocessable or poison messages must not block consumer processing loops. After a bounded retry count (e.g. 3 attempts with exponential backoff), route the message to a DLQ with an alert for manual operator triage.
