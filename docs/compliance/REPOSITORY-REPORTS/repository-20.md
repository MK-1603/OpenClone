# Upstream IP Compliance Report: skillspector (SEC-009)

**Audit Number:** `REPO-AUDIT-20`  
**Repository ID:** `SEC-009`  
**Canonical URL:** [https://github.com/NVIDIA/skillspector](https://github.com/NVIDIA/skillspector)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `skillspector`
- **Original Owner / Organization:** `NVIDIA`
- **Target URL:** https://github.com/NVIDIA/skillspector
- **Local Maintainer Path:** `.openclone-dev\upstream\security\SEC-009`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `f9bb13dd1667eb4e7ac97b8ebace3160041ed571`
- **Commit Date:** `2026-11-22`
- **Description:** Security audit and inspection framework for AI skills, agent tools, and prompt injection defenses.
- **Primary Languages:** Python
- **Core Technologies:** Static Analysis, YAML Skill Validator, PyLint AST

## 2. License Identification
- **Declared License:** `Apache-2.0`
- **License Category:** `PERMISSIVE`
- **License File Location:** `SEC-009/LICENSE` or constituent file
- **SPDX Identifier:** `Apache-2.0`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) 2026 NVIDIA Corporation`
- **Original Authors / Maintainers:** `NVIDIA` and community contributors.
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
- **Specific Conditions:** Apache 2.0: Retain NVIDIA copyright and patent grant notices.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) 2026 NVIDIA Corporation` in downstream notices.
- Must cite source URL: `https://github.com/NVIDIA/skillspector`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `YES`
- **Skill Distribution:** `YES`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `NO`
- **Redistribution Terms:** `YES (APACHE-2.0 NOTICE)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** Python
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `Apache 2.0: Retain NVIDIA copyright and patent grant notices.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `f9bb13dd1667eb4e7ac97b8ebace3160041ed571`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\security\SEC-009`
- License Manifest: `integrations/manifests/SEC-009.manifest.json`