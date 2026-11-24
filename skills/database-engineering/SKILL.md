---
id: database-engineering
name: Database Engineering Skill
version: 1.0.0
category: database
description: Relational & NoSQL modeling, SQL engineering, indexing, transactions, ACID, MVCC, query optimization, migrations, and restore-verified backups.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: skills/database-engineering/SKILL.md
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

See canonical specification at [`../../framework/skills/database-engineering/SKILL.md`](../../framework/skills/database-engineering/SKILL.md).
