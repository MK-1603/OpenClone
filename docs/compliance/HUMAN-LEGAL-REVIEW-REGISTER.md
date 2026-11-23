# OpenClone Human Legal & Compliance Review Register

**Document ID:** `REG-HUMAN-LEGAL-REVIEW-v1.0.0`  
**Standard:** AISDF Standard 1.0.0  
**Status:** `PENDING HUMAN SIGN-OFF`  

---

## Items Escalated for Human / Legal Approval

1. **Unstop-UI (UI-004) License Status:**
   - *Observation:* No root LICENSE or LICENSE.txt found in repository.
   - *Action Taken:* Quarantined in maintainer workspace; marked `BLOCKED_LICENSE_REVIEW`.
   - *Decision Needed:* Retain as unintegrated research reference or purge from maintainer checkout.

2. **Copyleft Subprocess Boundaries (SEC-005, SEC-008, SEC-010):**
   - *Observation:* Semgrep (LGPL-2.1), TruffleHog (GPL-3.0), and ClamAV (GPL-2.0) have copyleft terms.
   - *Action Taken:* Integrated strictly as external subprocesses and daemon connections without shared memory or static linking.
   - *Decision Needed:* Confirm that CLI pipe invocation satisfies OpenClone's MIT licensing distribution goals.

3. **Apache 2.0 Patent Grants (UI-005, UI-010, SEC-001, SEC-003, SEC-007, SEC-009, ENG-001):**
   - *Observation:* 7 repositories are governed by Apache-2.0 with explicit patent grants.
   - *Action Taken:* Apache 2.0 NOTICE sections added to `THIRD-PARTY-NOTICES.md`.
   - *Decision Needed:* Formal sign-off on third-party attribution text.