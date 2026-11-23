# Upstream IP Compliance Report: trufflehog (SEC-008)

**Audit Number:** `REPO-AUDIT-19`  
**Repository ID:** `SEC-008`  
**Canonical URL:** [https://github.com/trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `trufflehog`
- **Original Owner / Organization:** `trufflesecurity`
- **Target URL:** https://github.com/trufflesecurity/trufflehog
- **Local Maintainer Path:** `.openclone-dev\upstream\security\SEC-008`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `4ef51f69ca6347aaa76a5e64a87eac9c0c909f71`
- **Commit Date:** `2026-11-20`
- **Description:** High-entropy secret scanner searching git repositories, s3 buckets, and filesystems for exposed keys.
- **Primary Languages:** Go
- **Core Technologies:** Go, Shannon Entropy, API Key Detectors

## 2. License Identification
- **Declared License:** `GPL-3.0`
- **License Category:** `STRONG COPYLEFT`
- **License File Location:** `SEC-008/LICENSE` or constituent file
- **SPDX Identifier:** `GPL-3.0`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (C) 2022 Truffle Security Co.`
- **Original Authors / Maintainers:** `trufflesecurity` and community contributors.
- **Assertion of Ownership:** OpenClone asserts ZERO ownership over upstream intellectual property.

## 4. Relevant File-Level Licenses & Exceptions
- **Root License:** `GPL-3.0` applies across repository files unless explicitly overridden.
- **Exceptions:** None

## 5. Reusable Capabilities
- **Concepts:** Architecture design, technical patterns, workflow sequencing.
- **Functional Value:** Integrates with OpenClone capability framework without copying entire application codebases.

## 6. Reuse Restrictions
- **Code Reuse:** `PROHIBITED UNDER IDENTIFIED TERMS`
- **Documentation Reuse:** `ALLOWED WITH CONDITIONS`
- **Asset Reuse:** `NOT APPLICABLE`
- **Specific Conditions:** GPL-3.0: Copyleft applies. Direct source inclusion prohibited. Subprocess CLI execution only.

## 7. Attribution Requirements
- Must preserve: `Copyright (C) 2022 Truffle Security Co.` in downstream notices.
- Must cite source URL: `https://github.com/trufflesecurity/trufflehog`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `YES`
- **Skill Distribution:** `NO`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `YES`
- **Redistribution Terms:** `YES (GPL-3.0 BOUNDARY: CLI ONLY)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** Go
- **Copyleft Contamination Risk:** HIGH (GPL/LGPL copyleft isolation required)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `GPL-3.0: Copyleft applies. Direct source inclusion prohibited. Subprocess CLI execution only.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `4ef51f69ca6347aaa76a5e64a87eac9c0c909f71`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\security\SEC-008`
- License Manifest: `integrations/manifests/SEC-008.manifest.json`