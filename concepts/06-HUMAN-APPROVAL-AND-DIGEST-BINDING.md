# Concept 06: Human Approval & Digest Binding (Primary Specification)

## 1. Core Principle
Approvals are tied to specific, immutable task content, not arbitrary labels. An approval is cryptographically bound to the SHA-256 digest of the task specification.

## 2. Invariants
1. **Registered Approvers Only:** Approvals can only be registered by humans present in the `.aisdf` approver registry.
2. **Digest Verification:** When transitioning to `READY` and before executing `run`, the runtime re-hashes the task and confirms it matches the approved digest.
3. **Interactive Assurance:** Approvals made at an interactive terminal carry high assurance; non-interactive stamps are flagged and gated.
