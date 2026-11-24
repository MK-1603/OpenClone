---
name: saas-security-baseline
description: 19-point SaaS security verification, RLS, server authorization, rate limits, secret masking.
version: 1.0.0
---

# SaaS Security Baseline Skill

## Overview
# SaaS Security Baseline & Verification Checklist
**19 Essential Controls + Mature Application Security Standards**  
*OpenClone Global Security Intelligence | Defensible Security by Construction*

---

## 1. Principles of Defensible Security

1. **Server-Side Enforcement**: Client-side validation, hidden UI links, and front-end guards provide user guidance, NOT security. Every authorization, validation, and business rule MUST execute on the server.
2. **Deny by Default & Least Privilege**: Every private endpoint denies access unless authenticated; every database query is scoped to the tenant/user.
3. **Evidence-Based Compliance**: A security control is only marked `PASS` if it is verified with observable tests, automated scans, or reproducible configuration checks.

---

## 2. The 19-Point SaaS Security Baseline Matrix

| # | Security Control | Threat Mitigated | Primary Enforcement Location | Verification Method | Required Test / Evidence |
|---|---|---|---|---|---|
| **01** | **Row 
... Full baseline specification available in docs/security/saas-security-baseline.md
