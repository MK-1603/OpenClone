# OpenClone — Architectural Gap Analysis

## 1. Identified Architectural Gaps & Resolutions
1. **Module Separation (`src/openclone` vs `runtime/`):**
   - *Previous State:* Runtime control plane was embedded in `runtime/openclone_runtime/`, while high-level CLI was in `src/openclone/`.
   - *Target State:* `src/openclone/` serves as the public platform entrypoint, CLI, and MCP service; `runtime/openclone_runtime/` serves as the deterministic local control plane engine. Strict down-stack dependency flow enforced.
2. **Case Sensitivity & Directory Overlap:**
   - *Previous State:* `ASSESSMENT/` collided with `assessments/` on Windows/macOS.
   - *Target State:* Single canonical lowercase directory: `assessments/` with historical assessments under `assessments/historical/`.
3. **Copyleft Subprocess Quarantine:**
   - *Previous State:* Informal separation of external tools.
   - *Target State:* Formalized in `docs/legal/COPYLEFT_ISOLATION_POLICY.md` with zero in-tree vendoring and strict process execution boundaries.
