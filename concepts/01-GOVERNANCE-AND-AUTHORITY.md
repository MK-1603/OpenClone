# Concept 01: Governance & Authority Boundary (Primary Specification)

## 1. Core Principle
Humans remain the ultimate authority for software requirements, architectural decisions, destructive commands, security waivers, and release sign-offs. Artificial intelligence models propose plans and synthesize artifacts, but deterministic control planes and authorized humans decide.

## 2. Invariants
1. **Deny-by-Default:** An agent possesses zero write, execute, or network permissions until explicitly authorized in its validated worker manifest and active task contract.
2. **No Model Self-Approval:** Model output or conversational assertions cannot grant permissions, waive security checks, or transition task states.
3. **Cryptographic Revocation:** Any alteration to a task specification revokes previous human approvals immediately.

## 3. Implementation
Enforced by the OpenClone deterministic runtime (`runtime/aisdf_runtime/workforce.py`) via the human approver allow-list and SHA-256 task digest matching.
