---
name: secure-engineering
description: Enforces zero-trust controls, least-privilege tool execution, automated secret scanning, token redaction, and environment isolation.
version: 2.0.0
---

# Secure Engineering Skill

## Purpose
Implements layered defense-in-depth security controls across application, API, database, and CI/CD pipelines.

## Key Steps
1. Enforce .env protection (never commit secrets to version control).
2. Run tools/scan_secrets.py to detect credentials in tracked files.
3. Apply parameterized queries and row-level security for database access.
4. Mask sensitive tokens in audit logs and terminal output.
5. Enforce fail-closed permission gates on external network and destructive operations.
