# Upstream IP Compliance Report: improve (ENG-003)

**Audit Number:** `REPO-AUDIT-26`  
**Repository ID:** `ENG-003`  
**Canonical URL:** [https://github.com/shadcn/improve](https://github.com/shadcn/improve)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `improve`
- **Original Owner / Organization:** `shadcn`
- **Target URL:** https://github.com/shadcn/improve
- **Local Maintainer Path:** `.openclone-dev\upstream\software-engineering\ENG-003`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `cac56e1ebd3c279aa9153616cfeac7b174ab90f9`
- **Commit Date:** `2026-09-12`
- **Description:** Codebase inspection, architectural X-ray, and systematic refactoring workflows for existing codebases.
- **Primary Languages:** TypeScript, Node.js
- **Core Technologies:** Commander.js, AST Parser, Prettier

## 2. License Identification
- **Declared License:** `MIT`
- **License Category:** `PERMISSIVE`
- **License File Location:** `ENG-003/LICENSE` or constituent file
- **SPDX Identifier:** `MIT`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) 2024 shadcn`
- **Original Authors / Maintainers:** `shadcn` and community contributors.
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
- **Specific Conditions:** MIT: Retain copyright notice in Workflow WF-002 documentation.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) 2024 shadcn` in downstream notices.
- Must cite source URL: `https://github.com/shadcn/improve`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `NO`
- **Skill Distribution:** `YES`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `NO`
- **Redistribution Terms:** `YES (WITH ATTRIBUTION)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** TypeScript, Node.js
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `MIT: Retain copyright notice in Workflow WF-002 documentation.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `cac56e1ebd3c279aa9153616cfeac7b174ab90f9`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\software-engineering\ENG-003`
- License Manifest: `integrations/manifests/ENG-003.manifest.json`