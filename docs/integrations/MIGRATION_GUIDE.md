# Migration & Backward Compatibility Guide

The Universal Integration upgrade maintains **100% backward compatibility** with existing OpenClone adapters, CLI workflows, and MCP configurations.

---

## 1. Preserved Interfaces

- **Existing MCP Tools:** `openclone_get_status`, `openclone_search_knowledge`, `openclone_explain_concept`, `openclone_run_workflow`, `openclone_validate_project`, `openclone_get_guidance`, and `openclone_list_capabilities` continue to function unchanged with identical input/output schemas.
- **Existing Adapters:** Existing configuration files (`adapters/antigravity/`, `adapters/claude-code/`, `adapters/cursor/`, `adapters/codex/`) do not require breaking changes.
- **CLI Commands:** `openclone` and `aisdf` continue to default to the deterministic workforce runtime while adding `openclone mcp`, `openclone lifecycle`, and `openclone skill`.

---

## 2. Upgrading to Canonical Capabilities

To leverage the new 22-phase lifecycle and independent verification tools from external hosts:

1. **In MCP Clients:** Pass `{"all": true}` to `tools/list` or invoke the newly registered canonical tools directly by ID (e.g. `openclone_get_checklist`, `openclone_submit_evidence`).
2. **In ChatGPT / OpenAPI Clients:** Point to the newly exported `adapters/chatgpt/openapi.json` to access the full REST interface.
3. **In Webhook Consumers:** Configure signature verification for `X-OpenClone-Signature` on lifecycle state transitions.
