---
id: LES-0001
severity: HIGH
verified_date: 2026-11-24
---

# LES-0001: Pin Security Tool Commit SHAs

## Observation
Floating branch references or tags in security scanners introduce supply chain risks where upstream changes could alter verification behavior without notice.

## Resolution
All 14 security scanner entries in `security/scanners.lock.json` are pinned to immutable 40-character commit SHAs. Automated repository validation verifies pin integrity on every build.
