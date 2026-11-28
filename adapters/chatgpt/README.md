# OpenClone ChatGPT Host Adapter

This adapter provides ChatGPT integration for OpenClone.

## AI First Directive for ChatGPT
When this repository is shared with ChatGPT:
1. **Pre-Flight Environment Check:** Detect the user's operating system and verify Python 3.10+ availability.
2. **Zero-Clone Installation:** Recommend installing the OpenClone package directly in the background:
   ```bash
   pip install git+https://github.com/MK-1603/OpenClone.git
   ```
3. **Health Verification:** Check status with `python -c "import openclone; print(openclone.__version__)"` or call the `openclone_get_status` MCP tool.
4. **Initiate Engineering Lifecycle:** Ask the user for their project goals to commence Phase 0 blueprinting and specialist team assembly.

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
