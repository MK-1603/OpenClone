---
id: database-engineering
name: Database Engineering Skill
version: 1.0.0
category: database
description: Relational & NoSQL modeling, SQL engineering, indexing, transactions, ACID, MVCC, query optimization, migrations, and restore-verified backups.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/database-engineering/SKILL.md
triggers:
  - database
  - sql
  - postgres
  - postgresql
  - sqlite
  - mysql
  - schema
  - migrations
  - indexing
  - query optimization
  - explain analyze
  - connection pooling
  - transactions
  - acid
  - foreign key
negative_triggers:
  - frontend-only
  - no-database
  - static-site
precedence: 21
dependencies: []
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
  - cli
pre_build_gates:
  - Entity-Relationship Diagram and normalized schema defined
  - Foreign key and unique constraints specified
  - Migration script pre-flight check pass (0 unindexed FKs, 0 destructive DDL)
finish_gates:
  - Migration rollback or forward recovery plan verified
  - Query execution plans verified (0 unindexed full table scans on large tables)
  - Parameterized queries enforced across all data access
verification:
  - Automated migration runner and rollback test pass
  - Database constraint and isolation test pass
---

# Database Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `database` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone Backend & Database Intelligence  
**Workforce Alignment:** `database-architect`, `database-engineer`

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Ensure data integrity, optimal query performance, concurrency safety, zero-downtime schema evolution, and verified disaster recovery across relational and distributed databases.

### Boundaries
- **In Scope:** Relational (PostgreSQL, MySQL, SQLite) and NoSQL data modeling, SQL queries (CTEs, window functions), B-tree/GIN indexing, transaction isolation (ACID, MVCC), optimistic/pessimistic locking, connection pooling (PgBouncer), zero-downtime migrations (expand-and-contract), and backup restoration testing.
- **Out of Scope:** Client-side state management and frontend UI components.

---

## 2. CORE DATABASE ENGINEERING PRINCIPLES

1. **Schema Integrity:** Enforce foreign keys, unique constraints, NOT NULL checks, and domain validation at the database layer. Application-level validation is never a substitute for relational constraints.
2. **Zero-Downtime Migrations (Expand-and-Contract):**
   - **Phase 1 (Expand):** Add new nullable column or new table. Deploy code that writes to both old and new columns.
   - **Phase 2 (Backfill):** Backfill historical data in small asynchronous batches.
   - **Phase 3 (Contract):** Deploy code reading only from the new column. Remove old column references.
   - **Phase 4 (Cleanup):** Drop old column in a separate, isolated migration.
3. **Index Engineering:**
   - Always index foreign key columns to prevent full-table share locks on parent updates/deletes.
   - Use `CREATE INDEX CONCURRENTLY` in production PostgreSQL to prevent blocking read/write transactions.
   - Avoid over-indexing: each index adds write amplification and maintenance overhead.
4. **Transaction Safety:**
   - Keep transactions as short as possible. Never perform external network HTTP calls or file uploads inside an active database transaction.
   - Use optimistic locking (`version` column) for web applications to detect and prevent lost updates.
5. **Verified Backups:** A backup is not verified until automated restore testing succeeds with verified RPO and RTO metrics.
