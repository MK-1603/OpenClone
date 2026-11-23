# OpenClone — Dependency Direction & Boundary Map

## Rules of Dependency Direction
1. **Down-Stack Only:** High-level platform modules (`src/openclone/`) may import from the local control plane (`runtime/openclone_runtime/`). The runtime must NEVER import from `src/openclone/`.
2. **Zero Inward Coupling from Integrations:** Upstream adapters in `integrations/adapters/` must communicate via standard interfaces and never mutate runtime state directly.
3. **Copyleft Quarantine:** Copyleft tools (`semgrep`, `trufflehog`, `clamav`) must remain behind subprocess/pipe boundaries. Zero dynamic or static Python linking is permitted.
