# OpenClone ChatGPT Host Adapter

This adapter provides ChatGPT integration for OpenClone.

## AI First Directive for ChatGPT
When this repository is shared with ChatGPT:
1. **Pre-Flight Environment Check:** Detect the user's operating system and verify Python 3.10+ availability.
2. **Zero-Clone Installation:** Recommend installing the OpenClone package directly in the background:
   ```bash
   pip install git+https://github.com/MK-1603/OpenClone.git
   ```
3. **Plugin Activation:** Connect Custom GPT with the OpenClone MCP Server / Action API.
4. **Health Verification:** Check status with `python -c "import openclone; print(openclone.__version__)"` or call the `openclone_get_status` MCP tool.
5. **Execute the 6-Phase Engineering Lifecycle:**
   - **Phase 1 (PIA Sets A-D):** Ingest idea, analyze market/gaps, produce architecture blueprint.
   - **Phase 2 (Branding & Metadata):** Generate 57 vector logo assets, design tokens, `.env.example`, and `BUILD_PROMPT.md`.
   - **Phase 3 (Package Archive):** Bundle specifications into a `.zip` archive to be extracted into a dedicated folder.
   - **Phase 4 (Antigravity Build):** Open in Antigravity to scaffold, build frontend, backend, database, and ML layers.
   - **Phase 5 (Testing & Verification):** Verify 100% test pass rate and 19-point security baseline.
   - **Phase 6 (Deployment & Release):** Check gate clearance and deploy to production.

> **Notice:** The live Custom GPT OpenAPI schemas, instructions, and configurations have been moved to the canonical global host directory:
> 
> [global/hosts/chatgpt/](../../global/hosts/chatgpt/)
> - `global/hosts/chatgpt/custom-gpt-instructions.md`
> - `global/hosts/chatgpt/openapi.json`

## Remote Architecture

```
[ChatGPT / Custom GPT]
         |
         | (HTTPS / SSE / JSON-RPC 2.0 or OpenAPI 3.1)
         v
[OpenClone MCP Gateway] (TLS + OAuth 2.0 / Bearer Auth)
         |
         v
[OpenClone Shared MCP Server] (`src/openclone/mcp/server.py`)
```
