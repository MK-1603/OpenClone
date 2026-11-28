# OpenClone IDE Extension Development Guide
## Extension Architecture & Development for VS Code, Cursor, JetBrains, and Zed

**Version:** 1.0.0  
**Target:** Extension Authors, Tool Developers, and Platform Engineers  
**Canonical Product:** OpenClone 2.0

---

## 1. Universal Extension Philosophy

OpenClone extensions follow a **Zero-Duplication Architecture**:
- The extension acts strictly as a UI shell, context provider, and presentation client.
- All intelligence, task decomposition, agent routing, execution safety, and ledger hashing remain inside the OpenClone Core and Gateway.
- Extensions communicate with OpenClone via the standardized Model Context Protocol (MCP), Agent Client Protocol (ACP), or local JSON-RPC / REST APIs.

---

## 2. Visual Studio Code Extension

### 2.1. Manifest (`package.json`)
The VS Code extension exposes an OpenClone Activity Bar container, custom TreeViews, and commands:

```json
{
  "name": "openclone-vscode",
  "displayName": "OpenClone Universal Engineering",
  "description": "Governed AI software engineering intelligence for Visual Studio Code",
  "version": "2.0.0",
  "publisher": "openclone",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": ["Programming Languages", "Machine Learning", "Testing"],
  "contributes": {
    "viewsContainers": {
      "activitybar": [
        {
          "id": "openclone-explorer",
          "title": "OpenClone",
          "icon": "resources/icon.svg"
        }
      ]
    },
    "views": {
      "openclone-explorer": [
        {
          "id": "openclone.planView",
          "name": "Execution Plan"
        },
        {
          "id": "openclone.workersView",
          "name": "Workforce & Agents"
        },
        {
          "id": "openclone.ledgerView",
          "name": "Audit Ledger"
        }
      ]
    },
    "commands": [
      {
        "command": "openclone.inspect",
        "title": "OpenClone: Inspect Workspace"
      },
      {
        "command": "openclone.plan",
        "title": "OpenClone: Generate Implementation Plan"
      },
      {
        "command": "openclone.run",
        "title": "OpenClone: Execute Governed Engineering Task"
      }
    ]
  }
}
```

### 2.2. Automated Configuration (`.vscode/mcp.json`)
For instant IDE integration without compiling the full extension, OpenClone can configure the workspace MCP client:
```json
{
  "servers": {
    "openclone": {
      "type": "stdio",
      "command": "oc.exe",
      "args": ["mcp"]
    }
  }
}
```

---

## 3. Cursor AI Editor Integration

Cursor supports MCP configuration in `.cursor/mcp.json` or `%USERPROFILE%\.cursor\mcp.json`:

```json
{
  "mcpServers": {
    "openclone": {
      "command": "oc.exe",
      "args": ["mcp"]
    }
  }
}
```

Coupled with `.cursorrules` in the repository root, Cursor models are instructed to query OpenClone tools before making multi-file modifications:
```markdown
# OpenClone Governance Rule for Cursor
Before performing multi-file refactors or adding dependencies:
1. Call `openclone_inspect_repository` to verify git and workspace state.
2. Call `openclone_generate_plan` to validate task dependencies and check risk level.
3. Call `openclone_get_verification_results` after modifications to ensure all quality gates pass.
```

---

## 4. JetBrains IDE Integration

JetBrains IDEs (IntelliJ IDEA, PyCharm, WebStorm, GoLand, Rider) support external tools and MCP integration via `.idea/mcp.json` or JetBrains AI Assistant tool settings:

```json
{
  "servers": [
    {
      "name": "OpenClone",
      "command": "oc.exe",
      "args": ["mcp"]
    }
  ]
}
```

---

## 5. Zed Editor Integration

Zed context server configuration in `settings.json`:
```json
{
  "context_servers": {
    "openclone": {
      "command": "oc",
      "args": ["mcp"]
    }
  }
}
```
Or ACP integration where enabled.
