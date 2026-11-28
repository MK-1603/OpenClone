# Upstream IP Compliance Report: shadcn-ui (UI-002)

**Audit Number:** `REPO-AUDIT-02`  
**Repository ID:** `UI-002`  
**Canonical URL:** [https://github.com/shadcn-ui/ui](https://github.com/shadcn-ui/ui)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `shadcn-ui`
- **Original Owner / Organization:** `shadcn-ui`
- **Target URL:** https://github.com/shadcn-ui/ui
- **Local Maintainer Path:** `.openclone-dev\upstream\ui-ux\UI-002`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `bfa64ff4d1cb7317d2403ecb176df6826d4caffc`
- **Commit Date:** `2026-11-21`
- **Description:** Accessible, customizable component templates and primitives built with Radix UI and Tailwind CSS.
- **Primary Languages:** TypeScript, React, CSS
- **Core Technologies:** Radix UI, Tailwind CSS, Next.js, Turborepo

## 2. License Identification
- **Declared License:** `MIT`
- **License Category:** `PERMISSIVE`
- **License File Location:** `UI-002/LICENSE` or constituent file
- **SPDX Identifier:** `MIT`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) 2023 shadcn`
- **Original Authors / Maintainers:** `shadcn-ui` and community contributors.
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
- **Specific Conditions:** Preserve copyright notice and MIT license in downstream components.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) 2023 shadcn` in downstream notices.
- Must cite source URL: `https://github.com/shadcn-ui/ui`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `NO`
- **Skill Distribution:** `YES`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `YES`
- **Redistribution Terms:** `YES (WITH ATTRIBUTION)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** TypeScript, React, CSS
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `Preserve copyright notice and MIT license in downstream components.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `bfa64ff4d1cb7317d2403ecb176df6826d4caffc`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\ui-ux\UI-002`
- License Manifest: `integrations/manifests/UI-002.manifest.json`