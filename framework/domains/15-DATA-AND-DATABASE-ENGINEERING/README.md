# 15 — Data & Database Engineering
**OpenClone Canonical Engineering Domain**  
*Governed by OpenClone Global Standards | Domain Owner: Database Architect / Lead Database Engineer*

---

## 1. Purpose & Scope
This domain defines the canonical OpenClone guidance for relational and non-relational database design, data modeling, schema evolution, query optimization, indexing strategies, transactions, connection pooling, replication, and disaster recovery.

## 2. Core Database Engineering Standards
- **Data Modeling & Normalization:** Model conceptual, logical, and physical schemas (3NF for relational OLTP; denormalized read models where query benchmarks justify it). Enforce foreign keys, unique constraints, and check constraints at the database level.
- **ACID & Concurrency:** Enforce appropriate transaction isolation levels (`READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`). Prevent lost updates, race conditions, and deadlocks using optimistic locking (version columns) or row-level pessimistic locking (`SELECT ... FOR UPDATE`).
- **Index Engineering:** Design selective B-tree, composite, partial, and covering indexes based on actual query patterns. Monitor index write amplification and bloat.
- **Zero-Downtime Migrations:** Use expand-and-contract patterns for backward-incompatible schema changes. Version-control all migrations. Destructive DDL (`DROP TABLE`, `ALTER TABLE ... DROP COLUMN`) is prohibited without verified rollback/recovery strategies and explicit authorization.
- **Tenant Isolation:** Enforce Row-Level Security (RLS) or tenant-scoped isolation. Never trust client-supplied tenant IDs without server-side validation.
- **Backup Verification:** A backup is not verified until automated restore testing succeeds with verified RPO and RTO metrics.

## 3. Related Specialist Skills
- [`database-engineering`](../../skills/database-engineering/SKILL.md) — Data modeling, SQL optimization, migrations, indexing, and recovery.
- [`multi-tenant-engineering`](../../skills/multi-tenant-engineering/SKILL.md) — Database RLS, schema isolation, and cross-tenant leakage testing.

## 4. References & Catalogues
- Knowledge Catalogue: [`../../../docs/reference/guidance/backend-system-design-catalogue.md`](../../../docs/reference/guidance/backend-system-design-catalogue.md)
- Security Guard: `src/openclone/security/database.py` (`DatabaseSecurityGuard`)
