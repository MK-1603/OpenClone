# Concept 03: Specialist Workforce (Primary Specification)

## 1. Core Principle
Complex software engineering requires distinct, accountable specialist capabilities rather than unconstrained generalist prompting. OpenClone defines 72 specialist roles across 12 teams (Product, UX, Architecture, Frontend, Mobile, Backend, Data, AI/ML, Security, QA, Platform/Ops, Specialized EGM).

## 2. Invariants
1. **Role Contracts:** Every worker has an explicit manifest (`workforce/registry/workers/*.json`) defining allowed actions.
2. **Least-Privilege Enforcement:** Roles without execute permissions cannot run terminal processes. Independent reviewers cannot modify files.
