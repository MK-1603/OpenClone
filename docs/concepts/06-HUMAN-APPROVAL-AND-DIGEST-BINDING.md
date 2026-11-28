# Concept 06: Human Approval & Digest Binding (Primary Specification)

## 1. Core Principle
Approvals are tied to specific, immutable task content, not arbitrary labels. An approval is cryptographically bound to the SHA-256 digest of the task specification.

## 2. Invariants
1. **Registered Approvers Only:** Approvals can only be registered by humans present in the `.aisdf` approver registry.
2. **Digest Verification:** When transitioning to `READY` and before executing `run`, the runtime re-hashes the task and confirms it matches the approved digest.
3. **Interactive Assurance:** Approvals made at an interactive terminal carry high assurance; non-interactive stamps are flagged and gated.

---

## 4. Architectural Alternatives & Operational Trade-Offs

## 1. Alternate Paradigm: Asynchronous Multi-Sig PR Webhook Gateway
In enterprise distributed teams, developers and leads approve changes asynchronously in GitHub/GitLab Pull Requests rather than local terminals. The alternate model provides **GitHub Review Integration**.

## 2. How the Alternate Operates
1. **Plan Pull Request:** OpenClone opens a PR containing the proposed plan JSON and specification.
2. **Reviewer Sign-Off:** Required maintainers submit GitHub PR reviews with explicit approving state.
3. **Webhook Callback:** An OpenClone webhook ingestion script verifies the GitHub signature, maps the GitHub username to a registered approver, and records the approval digest into the local ledger.

## 3. Trade-Off Analysis
* **Strengths:** Fits enterprise pull-request workflows and multi-stakeholder governance.
* **Risks:** Requires network connectivity and webhook infrastructure.
