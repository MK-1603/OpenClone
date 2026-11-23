# Upstream IP Compliance Report: trivy (SEC-007)

**Audit Number:** `REPO-AUDIT-18`  
**Repository ID:** `SEC-007`  
**Canonical URL:** [https://github.com/aquasecurity/trivy](https://github.com/aquasecurity/trivy)  
**Audit Date:** 2026-11-23  
**Compliance Status:** `APPROVED WITH CONDITIONS`  

---

## 1. Repository Identity
- **Repository Name:** `trivy`
- **Original Owner / Organization:** `aquasecurity`
- **Target URL:** https://github.com/aquasecurity/trivy
- **Local Maintainer Path:** `.openclone-dev\upstream\security\SEC-007`
- **Original Branch:** `main`
- **Pinned Commit SHA:** `edf9f5c13d27ba1f6b1bc747f2f41a383dc56dc9`
- **Commit Date:** `2026-11-20`
- **Description:** Comprehensive security scanner for container images, file systems, git repos, and misconfigurations.
- **Primary Languages:** Go
- **Core Technologies:** Go 1.22+, Vulnerability Database, SBOM Parser

## 2. License Identification
- **Declared License:** `Apache-2.0`
- **License Category:** `PERMISSIVE`
- **License File Location:** `SEC-007/LICENSE` or constituent file
- **SPDX Identifier:** `Apache-2.0`

## 3. Copyright Ownership Evidence
- **Copyright Statement:** `Copyright (c) 2019-present Aqua Security Software Ltd.`
- **Original Authors / Maintainers:** `aquasecurity` and community contributors.
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
- **Specific Conditions:** Apache 2.0: Managed via scanners.lock.json; external process invocation.

## 7. Attribution Requirements
- Must preserve: `Copyright (c) 2019-present Aqua Security Software Ltd.` in downstream notices.
- Must cite source URL: `https://github.com/aquasecurity/trivy`.
- Must retain license text in distribution package third-party notices.

## 8. Redistribution Conditions
- **Core Distribution:** `NO`
- **Adapter Distribution:** `YES`
- **Skill Distribution:** `NO`
- **Documentation Distribution:** `YES`
- **Optional Module Distribution:** `YES`
- **Redistribution Terms:** `YES (APACHE-2.0 NOTICE)`

## 9. Dependency & Supply Chain Risks
- **Languages / Managers:** Go
- **Copyleft Contamination Risk:** LOW (Permissive / Isolated)
- **Telemetry / Network Concerns:** None detected in inspected source.

## 10. OpenClone Integration Recommendation
- **Integration Decision:** `Apache 2.0: Managed via scanners.lock.json; external process invocation.`
- **Boundary Recommendation:** Keep checkout isolated in `.openclone-dev/upstream/`. Distribute only thin adapters or synthesized rules.

## 11. Unresolved Questions & Legal Flags
- None for permissive/copyleft-bounded repositories.

## 12. Evidence References
- Git Commit Verification: `git rev-parse HEAD` -> `edf9f5c13d27ba1f6b1bc747f2f41a383dc56dc9`
- Checkout Location: `D:\New folder\OpenClone\.openclone-dev\upstream\security\SEC-007`
- License Manifest: `integrations/manifests/SEC-007.manifest.json`