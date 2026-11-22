# Concept 05: Cryptographic Audit Ledger (Primary Specification)

## 1. Core Principle
Every decision, task transition, human approval, command execution, and test check is committed to an append-only, tamper-evident SQLite database using cryptographic SHA-256 hash chaining.

## 2. Invariants
1. **Hash Chaining:** Each new event hashes the payload combined with the preceding event's hash:
   `hash = SHA256(event_id + task_id + event_type + actor + payload + prev_hash)`
2. **Tamper Detection:** The `verify-ledger` command traverses the entire event chain. Any post-hoc mutation of actor, payload, or event type fails verification immediately.
