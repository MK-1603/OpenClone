# Upstream IP Compliance Report: TokenEconomizer (ENG-004)

**Audit Number:** `REPO-AUDIT-27`  
**Repository ID:** `ENG-004`  
**Canonical URL:** [https://github.com/microsoft/TokenEconomizer](https://github.com/microsoft/TokenEconomizer)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `TokenEconomizer`
- **Original Owner / Organization:** `microsoft`
- **Target URL:** https://github.com/microsoft/TokenEconomizer
- **Local Maintainer Path:** `.openclone-dev\upstream\software-engineering\ENG-004`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `1bfeccdcecf48333b22762ad1dd9e36c6dc065df`
- **Commit Date:** `2026-11-19`
- **Description:** Token budget optimization, prompt deduplication, and context compression for large language models.
- **Primary Languages:** Python
- **Core Technologies:** tiktoken, Context Truncation, Similarity Deduplication

## 2. License Identification
- **Declared License:** `MIT`
- **License Category:** `PERMISSIVE`
- **License File Location:** `ENG-004/LICENSE` or constituent file
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
- **Specific Conditions:** MIT: Retain Microsoft copyright in context optimization documentation.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) Microsoft Corporation` in downstream notices.
- Must cite source URL: `https://github.com/microsoft/TokenEconomizer`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `YES (OPTIMIZER)`
- **Adapter Distribution:** `NO`
- **Skill Distribution:** `NO`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `NO`
- **Redistribution Terms:** `YES (WITH ATTRIBUTION)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** Python
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `MIT: Retain Microsoft copyright in context optimization documentation.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `1bfeccdcecf48333b22762ad1dd9e36c6dc065df`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\software-engineering\ENG-004`
- License Manifest: `integrations/manifests/ENG-004.manifest.json`