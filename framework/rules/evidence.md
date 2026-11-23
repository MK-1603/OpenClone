---
trigger: always_on
---

# OpenClone Evidence & Verification Rules

- **No Self-Attestation:** AI agents cannot declare tasks `VERIFIED` without physical proof (code diff, observable test logs, or UI screenshot).
- **Quality Gates Block:** A phase cannot transition to completed if any mandatory item is unverified or if unresolved High or Critical defects exist.
- **Durable State:** Record progress in `PROGRESS.md` and session handoffs in `HANDOFF.md` to prevent catastrophic context amnesia.
