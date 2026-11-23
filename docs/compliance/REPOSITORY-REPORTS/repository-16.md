# Upstream IP Compliance Report: semgrep (SEC-005)

**Audit Number:** `REPO-AUDIT-16`  
**Repository ID:** `SEC-005`  
**Canonical URL:** [https://github.com/semgrep/semgrep](https://github.com/semgrep/semgrep)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `semgrep`
- **Original Owner / Organization:** `semgrep`
- **Target URL:** https://github.com/semgrep/semgrep
- **Local Maintainer Path:** `.openclone-dev\upstream\security\SEC-005`
- **Original Branch:** `develop`
- **Pinned Commit SHA:** `c4dbe9ee2fc6d0022ba02ef6b97c5954ed9549e3`
- **Commit Date:** `2026-11-20`
- **Description:** Fast, lightweight static analysis engine for finding bugs, enforcing standards, and secret detection.
- **Primary Languages:** OCaml, Python
- **Core Technologies:** Tree-sitter, AST Matcher, CLI SAST

## 2. License Identification
- **Declared License:** `LGPL-2.1`
- **License Category:** `WEAK COPYLEFT`
- **License File Location:** `SEC-005/LICENSE` or constituent file
- **SPDX Identifier:** `LGPL-2.1`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) 2019-2026 Semgrep, Inc.`
- **Original Authors / Maintainers:** `semgrep` and community contributors.
- **Assertion of Ownership:** OpenClone asserts ZERO ownership over upstream intellectual property.

## 4. Relevant File-Level Licenses & Exceptions
- **Root License:** `LGPL-2.1` applies across repository files unless explicitly overridden.
- **Exceptions:** None

## 5. Reusable Capabilities
- **Concepts:** Architecture design, technical patterns, workflow sequencing.
- **Functional Value:** Integrates with OpenClone capability framework without copying entire application codebases.

## 6. Reuse Restrictions
- **Code Reuse:** `PROHIBITED UNDER IDENTIFIED TERMS`
- **Documentation Reuse:** `ALLOWED WITH CONDITIONS`
- **Asset Reuse:** `NOT APPLICABLE`
- **Specific Conditions:** LGPL-2.1: Direct code vendoring prohibited. Invoked strictly as external CLI subprocess.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) 2019-2026 Semgrep, Inc.` in downstream notices.
- Must cite source URL: `https://github.com/semgrep/semgrep`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `YES`
- **Skill Distribution:** `NO`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `YES`
- **Redistribution Terms:** `YES (LGPL BOUNDARY: CLI ONLY)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** OCaml, Python
- **Copyleft Contamination Risk:** HIGH (GPL/LGPL copyleft isolation required)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `LGPL-2.1: Direct code vendoring prohibited. Invoked strictly as external CLI subprocess.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `c4dbe9ee2fc6d0022ba02ef6b97c5954ed9549e3`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\security\SEC-005`
- License Manifest: `integrations/manifests/SEC-005.manifest.json`