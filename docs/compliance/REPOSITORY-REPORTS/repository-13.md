# Upstream IP Compliance Report: nuclei (SEC-002)

**Audit Number:** `REPO-AUDIT-13`  
**Repository ID:** `SEC-002`  
**Canonical URL:** [https://github.com/projectdiscovery/nuclei](https://github.com/projectdiscovery/nuclei)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `nuclei`
- **Original Owner / Organization:** `projectdiscovery`
- **Target URL:** https://github.com/projectdiscovery/nuclei
- **Local Maintainer Path:** `.openclone-dev\upstream\security\SEC-002`
- **Original Branch:** `dev`
- **Pinned Commit SHA:** `e169d3bb5d6c39eeb3de02219fcb1267bfbac5fe`
- **Commit Date:** `2026-11-21`
- **Description:** Fast and customizable vulnerability scanner based on simple YAML-based DSL templates.
- **Primary Languages:** Go
- **Core Technologies:** Go 1.21+, YAML Engine, Network Protocol Handlers

## 2. License Identification
- **Declared License:** `MIT`
- **License Category:** `PERMISSIVE`
- **License File Location:** `SEC-002/LICENSE` or constituent file
- **SPDX Identifier:** `MIT`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) 2020-present ProjectDiscovery, Inc.`
- **Original Authors / Maintainers:** `projectdiscovery` and community contributors.
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
- **Specific Conditions:** MIT: Executable CLI invoked via scanner gateway; never statically linked.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) 2020-present ProjectDiscovery, Inc.` in downstream notices.
- Must cite source URL: `https://github.com/projectdiscovery/nuclei`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `YES`
- **Skill Distribution:** `NO`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `YES`
- **Redistribution Terms:** `YES (EXTERNAL PROCESS ONLY)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** Go
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `MIT: Executable CLI invoked via scanner gateway; never statically linked.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `e169d3bb5d6c39eeb3de02219fcb1267bfbac5fe`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\security\SEC-002`
- License Manifest: `integrations/manifests/SEC-002.manifest.json`