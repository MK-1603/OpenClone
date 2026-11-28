# Upstream IP Compliance Report: claude-code-security-review (SEC-006)

**Audit Number:** `REPO-AUDIT-17`  
**Repository ID:** `SEC-006`  
**Canonical URL:** [https://github.com/anthropics/claude-code-security-review](https://github.com/anthropics/claude-code-security-review)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `claude-code-security-review`
- **Original Owner / Organization:** `anthropics`
- **Target URL:** https://github.com/anthropics/claude-code-security-review
- **Local Maintainer Path:** `.openclone-dev\upstream\security\SEC-006`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `0c6a49f1fa56a1d472575da86a94dbc1edb78eda`
- **Commit Date:** `2026-02-11`
- **Description:** GitHub Action and workflow automating pull request security review with Claude Code.
- **Primary Languages:** TypeScript, Shell
- **Core Technologies:** GitHub Actions Core, Claude Code API

## 2. License Identification
- **Declared License:** `MIT`
- **License Category:** `PERMISSIVE`
- **License File Location:** `SEC-006/LICENSE` or constituent file
- **SPDX Identifier:** `MIT`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) 2026 Anthropic, PBC`
- **Original Authors / Maintainers:** `anthropics` and community contributors.
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
- **Specific Conditions:** MIT: Retain Anthropic copyright notice in phase 18 verification rules.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) 2026 Anthropic, PBC` in downstream notices.
- Must cite source URL: `https://github.com/anthropics/claude-code-security-review`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `NO`
- **Skill Distribution:** `YES`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `NO`
- **Redistribution Terms:** `YES (WITH ATTRIBUTION)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** TypeScript, Shell
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `MIT: Retain Anthropic copyright notice in phase 18 verification rules.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `0c6a49f1fa56a1d472575da86a94dbc1edb78eda`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\security\SEC-006`
- License Manifest: `integrations/manifests/SEC-006.manifest.json`