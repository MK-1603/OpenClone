# OpenClone Legally Cautious & Technically Useful Reuse Strategy

**Document ID:** `STRAT-IP-REUSE-v1.0.0`  
**Product:** OpenClone 2.0 Universal AI Software Engineering Platform  
**Standard:** AISDF Standard 1.0.0  
**Author:** Compliance & Repository Architecture Team  

---

## 1. The 4-Tier Reuse Strategy

### Tier 1: Canonical Reference & Synthesis (Zero Code Copying)
- **Applied to:** `UI-002` (shadcn), `UI-003` (interface-design), `UI-008` (ui-ux-pro-max), `UI-009`, `UI-010` (impeccable), `SEC-003` (codex-security), `SEC-011` (bla), `ENG-001` (hue), `ENG-003` (improve).
- **Approach:** Study architectural principles, component APIs, and critique taxonomies. Synthesize clean, original OpenClone guidelines in `domains/` and `docs/knowledge/`.

### Tier 2: Clean-Room Reimplementation & Native Adapters
- **Applied to:** `UI-001` (design-md-chrome), `SEC-001` (strix), `SEC-009` (skillspector), `SEC-012` (pyrit), `ENG-004` (TokenEconomizer).
- **Approach:** Write original, clean Python implementations of the core concepts (design token normalization, target-allowlisted pentest gating, prompt injection detection, dual-tier context management).

### Tier 3: External Process Subprocess Gating (Copyleft Quarantine)
- **Applied to:** `SEC-002` (nuclei), `SEC-005` (semgrep), `SEC-007` (trivy), `SEC-008` (trufflehog), `SEC-010` (clamav).
- **Approach:** Pinned in `security/scanners.lock.json`. Executed strictly via external subprocess pipes or Docker containers. Never statically linked into OpenClone.

### Tier 4: Total Exclusion (License Ambiguity)
- **Applied to:** `UI-004` (Unstop-UI).
- **Approach:** Completely excluded from distribution and integration until upstream author commits an explicit open-source license.