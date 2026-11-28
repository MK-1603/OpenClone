# OpenClone — Module Ownership & Responsibility Map

| Module Path | Responsible Owner | What Belongs Inside | What Must NOT Belong Inside |
|---|---|---|---|
| `src/openclone/` | Core Platform Team | CLI commands, MCP server, global installer, skill engines | Direct business logic of client applications, heavy data stores |
| `runtime/openclone_runtime/` | Systems & Runtime Team | Task DAG state machine, SQLite audit ledger, release gate | LLM API calls, UI components, external network calls |
| `integrations/` | Integrations & Security Team | 28 upstream adapters, capability manifests, gateway router | Upstream third-party source vendoring |
| `domains/` | Domain Architecture Leads | 31 normative engineering domains, rulebooks, policies | Executable runtime binaries or compiled code |
| `engines/` | Engine Architecture Leads | 56 capability engine execution contracts (`E-001` to `E-056`) | Concrete application code |
| `workforce/` | Multi-Agent Systems Team | 72 specialist role contracts and manifests across 12 teams | Hardcoded LLM prompts with static API keys |
| `skills/taste-skill/` | UI/UX & Design Engineering | Anti-AI-slop design system tokens, 13 governance tests | Non-visual or unrelated CLI logic |
