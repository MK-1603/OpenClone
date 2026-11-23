# OpenClone — Repository Migration Plan & Quality Gates

## Phased Migration Execution
1. **Phase 1: Pre-Flight Audit & Baseline:** Read-only inventory, SHA-256 duplicate clustering, reference graph generation.
2. **Phase 2: Case-Collision & Directory Hygiene:** Consolidate `ASSESSMENT/` into `assessments/historical/`; archive `docs/v4/` to `docs/archive/v4/`.
3. **Phase 3: Canonical Package Establishment:** Create `runtime/openclone_runtime/` and `tools/openclone_runtime/`; maintain backward-compatibility wrappers.
4. **Phase 4: Multi-IDE Adapter Alignment:** Update Antigravity, Cursor, Claude Code, and Codex adapter rules to `openclone`.
5. **Phase 5: Document Authority Alignment:** Establish canonical `OPENCLONE-*.md` specifications and rulebook with forwarding notices.
6. **Phase 6: Independent Verification:** 118 automated tests passing; repository validator verified.
