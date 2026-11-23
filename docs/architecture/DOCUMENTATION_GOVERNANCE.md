# OpenClone — Documentation Governance System

## Document Classification & Authority Rules
1. **Normative Standards (Level 1 Authority):**
   - Rules in `domains/00-GOVERNANCE/OPENCLONE-RULEBOOK.md` are mandatory across all workflows.
2. **Product Truth (Level 2 Authority):**
   - `PROJECT.md` is the canonical product source of truth; chat output is untrusted data.
3. **Architecture Specifications (Level 3 Authority):**
   - Specifications in `docs/architecture/` govern module boundaries and packaging rules.
4. **Live Guidance vs Master Catalogues:**
   - `docs/knowledge/` (<12 KB) is strictly reserved for live fast LLM prompt context during MCP execution.
   - `docs/knowledge-catalogues/` is reserved for comprehensive master encyclopedias.
5. **Historical Records:**
   - Historical blueprints, past audit transcripts, and older release validations live in `docs/archive/` and `assessments/historical/`.
