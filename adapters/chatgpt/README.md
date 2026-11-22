# OpenClone ChatGPT Host Adapter
## Hosted MCP & Custom GPT Integration Guide

This directory provides integration assets for connecting OpenClone to ChatGPT via Remote MCP or Custom GPT Actions.

---

## Architecture Overview

Unlike desktop IDEs that invoke local Python subprocesses over stdio, ChatGPT communicates via remote HTTPS:

```
[ChatGPT / Custom GPT]
         |
         | (HTTPS / SSE / JSON-RPC 2.0 or OpenAPI 3.1)
         v
[OpenClone MCP Gateway / Reverse Proxy] (TLS + OAuth 2.0 / Bearer Auth)
         |
         v
[OpenClone Shared MCP Server] (`src/openclone/mcp/server.py`)
         |
         v
[OpenClone Core Knowledge & Control Plane]
```

---

## 1. Remote Server Deployment

To expose OpenClone tools to ChatGPT:
1. Run the MCP server behind a lightweight HTTP/SSE wrapper (e.g. FastAPI, Quart, or Cloudflare Worker).
2. Configure authentication using Bearer tokens or OAuth 2.0.
3. Protect against SSRF and unauthorized network egress by binding tools in read-only mode for public chat interfaces.

---

## 2. Setting Up a Custom GPT

1. In ChatGPT, navigate to **Explore GPTs** -> **Create a GPT**.
2. Set Name: `OpenClone Software Architect`.
3. Paste the contents of [`custom-gpt-instructions.md`](custom-gpt-instructions.md) into the **Instructions** tab.
4. In **Actions**, import the OpenAPI schema generated from OpenClone MCP tools (`tools/list`).
5. Configure Authentication with your Bearer token or OAuth client.
