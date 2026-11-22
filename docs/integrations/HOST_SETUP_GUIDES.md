# AI Host Setup & Configuration Guides

Step-by-step setup guides for connecting supported AI hosts to OpenClone.

---

## 1. Google Antigravity Setup

Antigravity natively executes the local MCP server over stdio.

1. In your Antigravity workspace settings, configure the OpenClone plugin:
```json
{
  "plugins": {
    "openclone": {
      "path": "adapters/antigravity/plugin",
      "mcp": {
        "command": "python",
        "args": ["-m", "src.openclone.cli", "mcp"]
      }
    }
  }
}
```
2. Inherited rules are loaded automatically from `adapters/antigravity/plugin/rules/aisdf.md`.

---

## 2. Claude Code & Claude Desktop Setup

Configure OpenClone as a stdio server in your `claude_desktop_config.json` (or `.mcp.json` for Claude Code):

```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.cli", "mcp"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

---

## 3. Cursor Composer Setup

In your project root, create or edit `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "openclone": {
      "command": "python",
      "args": ["-m", "src.openclone.cli", "mcp"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```
Add anti-slop rules to `.cursor/rules/aisdf.mdc` (copied from `adapters/cursor/.cursor/rules/aisdf.mdc`).

---

## 4. ChatGPT Setup (Actions via OpenAPI)

For ChatGPT web and custom GPTs:
1. Export the OpenAPI 3.1 specification:
   `adapters/chatgpt/openapi.json`
2. Create a new Custom GPT in ChatGPT.
3. Paste instructions from `adapters/chatgpt/custom-gpt-instructions.md`.
4. In "Actions", import `adapters/chatgpt/openapi.json` and configure Bearer Authentication using token `oc_live_...`.
