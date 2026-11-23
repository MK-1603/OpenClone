# Upstream IP Compliance Report: design-md-chrome (UI-001)

**Audit Number:** `REPO-AUDIT-01`  
**Repository ID:** `UI-001`  
**Canonical URL:** [https://github.com/bergside/design-md-chrome](https://github.com/bergside/design-md-chrome)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `design-md-chrome`
- **Original Owner / Organization:** `bergside`
- **Target URL:** https://github.com/bergside/design-md-chrome
- **Local Maintainer Path:** `.openclone-dev\upstream\ui-ux\UI-001`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `8e07614fb18752ab1ee14dd65a8ff93e63c9b13b`
- **Commit Date:** `2026-05-25`
- **Description:** Chrome extension to extract computed design tokens and CSS into formatted Markdown.
- **Primary Languages:** JavaScript, HTML, CSS
- **Core Technologies:** WebExtensions API, DOM Parser, CSSOM

## 2. License Identification
- **Declared License:** `MIT`
- **License Category:** `PERMISSIVE`
- **License File Location:** `UI-001/LICENSE` or constituent file
- **SPDX Identifier:** `MIT`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) 2026 Bergside`
- **Original Authors / Maintainers:** `bergside` and community contributors.
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
- **Specific Conditions:** Preserve copyright notice and MIT license header.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) 2026 Bergside` in downstream notices.
- Must cite source URL: `https://github.com/bergside/design-md-chrome`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `YES`
- **Skill Distribution:** `YES`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `YES`
- **Redistribution Terms:** `YES (WITH ATTRIBUTION)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** JavaScript, HTML, CSS
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `Preserve copyright notice and MIT license header.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `8e07614fb18752ab1ee14dd65a8ff93e63c9b13b`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\ui-ux\UI-001`
- License Manifest: `integrations/manifests/UI-001.manifest.json`