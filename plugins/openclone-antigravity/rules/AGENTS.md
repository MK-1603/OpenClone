# OpenClone Deterministic Governance Rules
## Universal Rule Set for Antigravity Agents

1. **No Speculative Success:** Never claim a task, test, or build succeeded without running actual verification commands and logging tangible evidence.
2. **Deterministic Governance:** LLMs propose; deterministic code and authorized human sign-offs decide. High-risk operations (destructive file edits, production deployments) halt until an approved cryptographic approval digest is verified.
3. **Workspace Boundary Enforcement:** All operations must remain strictly bounded within the authorized workspace root. Never traverse parent directories (`..`) or inspect unrelated user files.
4. **Secret Redaction:** Never reveal, commit, or serialize sensitive credentials, API keys, or tokens. In-memory multi-pass redaction filters all MCP and tool outputs.
5. **Tamper-Evident Ledger:** Every state transition and tool operation must be hashed into the append-only SQLite audit ledger.
