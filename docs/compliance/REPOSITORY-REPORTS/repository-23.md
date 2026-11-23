# Upstream IP Compliance Report: pyrit (SEC-012)

**Audit Number:** `REPO-AUDIT-23`  
**Repository ID:** `SEC-012`  
**Canonical URL:** [https://github.com/microsoft/pyrit](https://github.com/microsoft/pyrit)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `pyrit`
- **Original Owner / Organization:** `microsoft`
- **Target URL:** https://github.com/microsoft/pyrit
- **Local Maintainer Path:** `.openclone-dev\upstream\security\SEC-012`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `817523458433ef20c1316418bab10be312535416`
- **Commit Date:** `2026-11-22`
- **Description:** Python Risk Identification Tool for Generative AI red-teaming and prompt injection evaluation.
- **Primary Languages:** Python
- **Core Technologies:** Generative AI Evaluators, Attack Strategies, Azure OpenAI SDK

## 2. License Identification
- **Declared License:** `MIT`
- **License Category:** `PERMISSIVE`
- **License File Location:** `SEC-012/LICENSE` or constituent file
- **SPDX Identifier:** `MIT`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) Microsoft Corporation`
- **Original Authors / Maintainers:** `microsoft` and community contributors.
- **Assertion of Ownership:** OpenClone asserts ZERO ownership over upstream intellectual property.

## 4. Relevant File-Level Licenses & Exceptions
- **Root License:** `MIT` applies across repository files unless explicitly overridden.
- **Exceptions:** None

## 5. Reusable Capabilities
- **Concepts:** Architecture design, technical patterns, workflow sequencing.
- **Functional Value:** Integrates with OpenClone capability framework without copying entire application codebases.

## 6. Reuse Restrictions
- **Code Reuse:** `ALLOWED WITH CONDITIONS`
- **Documentation Reuse:** `ALLOWED WITH CONDITIONS`
- **Asset Reuse:** `NOT APPLICABLE`
- **Specific Conditions:** MIT: Retain Microsoft copyright notice in pyrit_adapter.py.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) Microsoft Corporation` in downstream notices.
- Must cite source URL: `https://github.com/microsoft/pyrit`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `YES`
- **Skill Distribution:** `NO`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `YES`
- **Redistribution Terms:** `YES (WITH ATTRIBUTION)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** Python
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `MIT: Retain Microsoft copyright notice in pyrit_adapter.py.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `817523458433ef20c1316418bab10be312535416`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\security\SEC-012`
- License Manifest: `integrations/manifests/SEC-012.manifest.json`