# Concept 09: Independent Assurance & EGM (Primary Specification)

## 1. Core Principle
Authors cannot independently audit their own changes. OpenClone enforces the **Clean-Context "Goldfish" Protocol** for critical code, architecture, and security reviews.

## 2. Invariants
1. **Context Isolation:** Independent reviewers run in a pristine context window without access to author reasoning or drafts.
2. **Read-Only Boundary:** The `independent-code-reviewer` and `independent-security-auditor` roles have zero write or execute privileges.
3. **Formal Findings Schema:** Review deficiencies are recorded as schema-validated JSON. Only authorized humans can accept risk or grant time-bound waivers.
