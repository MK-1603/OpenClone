# Upstream IP Compliance Report: hue (ENG-001)

**Audit Number:** `REPO-AUDIT-24`  
**Repository ID:** `ENG-001`  
**Canonical URL:** [https://github.com/cloudera/hue](https://github.com/cloudera/hue)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `hue`
- **Original Owner / Organization:** `cloudera`
- **Target URL:** https://github.com/cloudera/hue
- **Local Maintainer Path:** `.openclone-dev\upstream\software-engineering\ENG-001`
- **Original Branch:** `master`
- **Pinned Commit SHA:** `7ad92b1820d62a0d5fde38889a1d16646d7a397f`
- **Commit Date:** `2026-10-30`
- **Description:** Open source SQL Assistant, schema explorer, and query development workbench.
- **Primary Languages:** Python, JavaScript
- **Core Technologies:** Django, Knockout.js, PyHive, SQL Parser

## 2. License Identification
- **Declared License:** `Apache-2.0`
- **License Category:** `PERMISSIVE`
- **License File Location:** `ENG-001/LICENSE` or constituent file
- **SPDX Identifier:** `Apache-2.0`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) 2013-2026 Cloudera, Inc.`
- **Original Authors / Maintainers:** `cloudera` and community contributors.
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
- **Specific Conditions:** Apache 2.0: UX patterns referenced. Monolithic code not vendored.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) 2013-2026 Cloudera, Inc.` in downstream notices.
- Must cite source URL: `https://github.com/cloudera/hue`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `NO`
- **Skill Distribution:** `NO`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `NO`
- **Redistribution Terms:** `YES (APACHE-2.0 NOTICE)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** Python, JavaScript
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `Apache 2.0: UX patterns referenced. Monolithic code not vendored.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `7ad92b1820d62a0d5fde38889a1d16646d7a397f`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\software-engineering\ENG-001`
- License Manifest: `integrations/manifests/ENG-001.manifest.json`