# OpenClone — Redundant Directories Audit Report

**Audit Date:** 2026-11-23  

---

## Redundant Directories & Resolutions
1. **`ASSESSMENT/` vs `assessments/`:**
   - **Issue:** Casing collision on case-insensitive filesystems.
   - **Resolution:** `ASSESSMENT/` consolidated into `assessments/historical/`. Clean single lowercase directory `assessments/` established.
2. **`docs/v4/` vs `docs/framework/`:**
   - **Issue:** Older v4 draft duplicated active framework operating guide.
   - **Resolution:** `docs/v4/` moved to `docs/archive/v4/`.
3. **`runtime/openclone_runtime/` vs `runtime/openclone_runtime/`:**
   - **Issue:** Legacy naming package.
   - **Resolution:** Canonical `runtime/openclone_runtime/` created as primary; `runtime/openclone_runtime/` maintained strictly as a non-breaking forwarding wrapper.
