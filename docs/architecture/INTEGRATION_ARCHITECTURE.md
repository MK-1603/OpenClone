# OpenClone — Upstream Integration Architecture

## Upstream Integration Standards
All 28 upstream repositories follow a standardized architectural schema:
- **Registry:** `integrations/registry/upstream_registry.json`
- **Manifests:** `integrations/manifests/{ID}.manifest.json`
- **Adapters:** `integrations/adapters/`
- **Attribution:** `THIRD_PARTY_NOTICES.md` & `NOTICE`
- **License Compliance:** `THIRD_PARTY_LICENSES.md` & `docs/legal/`

## Isolation Levels
- `NATIVE_SKILL`: Permissive MIT/Apache code integrated into `skills/` (e.g. `taste-skill`).
- `SUBPROCESS_ADAPTER`: Invoked as external CLI processes across clean stdin/stdout boundaries (e.g. `strix`, `semgrep`, `trufflehog`, `trivy`, `pyrit`).
- `REFERENCE_ONLY`: Design patterns, curated curriculum, and architectural heuristics (e.g. `shadcn/ui`, `build-your-own-x`).
