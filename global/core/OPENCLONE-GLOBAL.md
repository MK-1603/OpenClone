# OpenClone Global Operating Standard
**Version:** 1.0.0 | **Scope:** Global AI Coding Environment Specification  
**Canonical Identity:** OpenClone (MK-1603/OpenClone)

---

## 1. Purpose

The OpenClone Global layer provides a single, host-agnostic engineering and governance foundation that installs once on a developer workstation and operates consistently across all supported AI coding environments (Google Antigravity, Claude Code, OpenAI Codex, Cursor, VS Code, ChatGPT, and Generic MCP clients).

---

## 2. Precedence Hierarchy

When conflicting instructions or configurations arise, AI agents and runtime systems MUST adhere to the following deterministic precedence order:

1. **Project Rule:** `AGENTS.md`, `.cursor/rules/`, `.claude/`, `.agents/rules/` in the project repository.
2. **Project Configuration:** Project `.openclone/config.yaml` and active task plans.
3. **Global Configuration:** User-level `~/.openclone/config.yaml` and `OPENCLONE-GLOBAL.md`.
4. **Framework Defaults:** Upstream default configurations and framework rules (`framework/rules/`).

A higher layer always overrides a lower layer. No global default may override an explicit project instruction.

---

## 3. Universal Global Rules

All AI coding agents governed by OpenClone MUST obey the following non-negotiable standards:

### 3.1 Strict Anti-Slop
- Never introduce dependencies, frameworks, databases, caches, or services without concrete justification.
- Never write placeholder, mock, or incomplete implementations in production code paths.
- Avoid unnecessary refactoring, reformatting, or mass renaming outside the approved task scope.

### 3.2 Evidence & Truthful Maturity
- Every implementation claim must be backed by verifiable command output or test logs.
- Never claim tests pass without executing them.
- Follow the Truthful Maturity Model: `PROPOSED`, `SPECIFIED`, `IMPLEMENTED`, `TESTED`, `INTEGRATED`, `CERTIFIED`.

### 3.3 Security & Least Privilege
- Deny by default: never execute untrusted code without explicit containment.
- Secrets redaction: never commit, log, or transmit credentials or private keys.
- Sandbox boundary enforcement: all subprocess operations must run within approved directory boundaries.

### 3.4 No Fake Execution
- Real execution output is mandatory for every phase exit and verification gate.

---

## 4. Enabling OpenClone in a Project

To initialize OpenClone governance in an existing codebase:
```bash
# Initialize project contract and local state ledger
openclone init
```
This generates the project `PROJECT.md`, `AGENTS.md`, and `.openclone/` directory structure.
