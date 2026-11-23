# OpenClone ChatGPT Host Adapter

This adapter provides ChatGPT integration for OpenClone.

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
