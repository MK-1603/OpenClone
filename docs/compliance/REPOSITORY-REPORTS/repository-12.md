# Upstream IP Compliance Report: strix (SEC-001)

**Audit Number:** `REPO-AUDIT-12`  
**Repository ID:** `SEC-001`  
**Canonical URL:** [https://github.com/usestrix/strix](https://github.com/usestrix/strix)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `strix`
- **Original Owner / Organization:** `usestrix`
- **Target URL:** https://github.com/usestrix/strix
- **Local Maintainer Path:** `.openclone-dev\upstream\security\SEC-001`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `a1ccf777d80e812edf23fc8b82bdc17def6143ac`
- **Commit Date:** `2026-11-19`
- **Description:** Autonomous AI penetration testing agent and dynamic security assessment platform.
- **Primary Languages:** Python, Dockerfile
- **Core Technologies:** FastAPI, Docker, Playwright, LLM Orchestration

## 2. License Identification
- **Declared License:** `Apache-2.0`
- **License Category:** `PERMISSIVE`
- **License File Location:** `SEC-001/LICENSE` or constituent file
- **SPDX Identifier:** `Apache-2.0`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) 2026 Strix Team`
- **Original Authors / Maintainers:** `usestrix` and community contributors.
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
- **Specific Conditions:** Apache 2.0: Optional isolated Docker adapter; target allowlist required.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) 2026 Strix Team` in downstream notices.
- Must cite source URL: `https://github.com/usestrix/strix`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `YES`
- **Skill Distribution:** `NO`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `YES`
- **Redistribution Terms:** `YES (APACHE-2.0 NOTICE)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** Python, Dockerfile
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `Apache 2.0: Optional isolated Docker adapter; target allowlist required.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `a1ccf777d80e812edf23fc8b82bdc17def6143ac`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\security\SEC-001`
- License Manifest: `integrations/manifests/SEC-001.manifest.json`