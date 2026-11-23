# Upstream IP Compliance Report: codex-security (SEC-003)

**Audit Number:** `REPO-AUDIT-14`  
**Repository ID:** `SEC-003`  
**Canonical URL:** [https://github.com/openai/codex-security](https://github.com/openai/codex-security)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `codex-security`
- **Original Owner / Organization:** `openai`
- **Target URL:** https://github.com/openai/codex-security
- **Local Maintainer Path:** `.openclone-dev\upstream\security\SEC-003`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `35373239d9319e5f5ada1f135f13a7da5c01c909`
- **Commit Date:** `2026-11-22`
- **Description:** Automated vulnerability triage, analysis rubrics, and remediation verification patterns.
- **Primary Languages:** Python, Markdown
- **Core Technologies:** AI Vulnerability Triage, SARIF Parser

## 2. License Identification
- **Declared License:** `Apache-2.0`
- **License Category:** `PERMISSIVE`
- **License File Location:** `SEC-003/LICENSE` or constituent file
- **SPDX Identifier:** `Apache-2.0`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) 2026 OpenAI`
- **Original Authors / Maintainers:** `openai` and community contributors.
- **Assertion of Ownership:** OpenClone asserts ZERO ownership over upstream intellectual property.

## 4. Relevant File-Level Licenses & Exceptions
- **Root License:** `Apache-2.0` applies across repository files unless explicitly overridden.
- **Exceptions:** None

## 5. Reusable Capabilities
- **Concepts:** Architecture design, technical patterns, workflow sequencing.
- **Functional Value:** Integrates with OpenClone capability framework without copying entire application codebases.

## 6. Reuse Restrictions
- **Code Reuse:** `ALLOWED WITH CONDITIONS`
- **Documentation Reuse:** `ALLOWED WITH CONDITIONS`
- **Asset Reuse:** `NOT APPLICABLE`
- **Specific Conditions:** Apache 2.0: Synthesized into domain 14 triage rules.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) 2026 OpenAI` in downstream notices.
- Must cite source URL: `https://github.com/openai/codex-security`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `NO`
- **Skill Distribution:** `YES`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `NO`
- **Redistribution Terms:** `YES (APACHE-2.0 NOTICE)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** Python, Markdown
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `Apache 2.0: Synthesized into domain 14 triage rules.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `35373239d9319e5f5ada1f135f13a7da5c01c909`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\security\SEC-003`
- License Manifest: `integrations/manifests/SEC-003.manifest.json`