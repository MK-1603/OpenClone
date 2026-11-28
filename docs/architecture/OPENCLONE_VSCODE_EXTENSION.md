# OpenClone 2.0 — Native Visual Studio Code AI Chat Extension

## 1. Product Overview

The **OpenClone VS Code Extension** (`openclone-vscode`, v2.0.0) transforms Visual Studio Code into a governed, conversational AI engineering environment connected directly to the **OpenClone Universal Platform Core**.

Rather than running an isolated or superficial chatbot, the extension communicates directly with:
- **Model Intelligence Engine (MIE):** 16 registered AI models (Gemini Pro/Flash, Claude 3.5/3.7, OpenAI GPT-4o/o3, Ollama).
- **Agent Workforce:** 72 specialized engineering worker contracts across Core, Architecture, Security, QA, and Data divisions.
- **Deterministic Governance:** Human approval gates with cryptographic SHA-256 digest binding and tamper-evident audit ledger hashing.
- **Workspace Intelligence:** Active editor file context, real-time git branch tracking, and language-aware prompt augmentation.

---

## 2. Extension Architecture & Key Components

```
OpenClone VS Code Extension (extensions/vscode/)
├── package.json               # Manifest with Activity Bar container, Webview view, commands & menus
├── resources/
│   ├── icon.png               # High-resolution extension icon (128x128)
│   └── icon.svg               # Scalable vector branding icon
├── src/
│   ├── extension.js           # Activation entrypoint registering tree views, commands & providers
│   ├── chatViewProvider.js    # vscode.WebviewViewProvider managing chat lifecycle & strict CSP
│   ├── contextManager.js      # Active editor file, selection, and language context extractor
│   └── runtimeClient.js       # HTTP client connecting to OpenClone REST Gateway (/api/v1/*)
└── media/
    ├── chatView.html          # Clean Webview structure with header, selector bar & chat feed
    ├── chatView.css           # Minimalist theme adhering to OpenClone UI guidelines (gold #D4AF37)
    └── chatView.js            # Controller script handling messaging, markdown, code copy & approvals
```

---

## 3. Communication Protocol

The extension connects to the local or remote **OpenClone REST Gateway** over HTTP JSON:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/health` | `GET` | Health status, gateway version, workspace root, and active git branch |
| `/api/v1/models` | `GET` | Catalog of 16 AI models with context window, pricing, and streaming support |
| `/api/v1/providers` | `GET` | Connectivity check for Gemini, OpenAI, Anthropic, and Ollama |
| `/api/v1/agents` | `GET` | Catalog of 72 governed agent workforce contracts |
| `/api/v1/chat` | `POST` | Dispatches user message, model/agent selection, and editor context to MIE |
| `/api/v1/conversation/history` | `GET` | Retrieves recent multi-turn session history |
| `/api/v1/conversation/clear` | `POST` | Clears conversation state and resets session memory |
| `/api/v1/approvals` | `POST` | Records human cryptographic approval/rejection for high-risk operations |
| `/api/v1/plans` | `POST` | Decomposes high-level requirements into topological task graphs |
| `/api/v1/execution` | `POST` | Executes governed engineering task with SHA-256 audit ledger evidence |

---

## 4. Visual Design & Aesthetics

The Webview UI strictly adheres to OpenClone Phase 9 design principles:
- **Monochrome Foundation:** Native VS Code background and foreground tokens (`--vscode-sideBar-background`, `--vscode-foreground`).
- **Restrained Accent:** Gold `#D4AF37` for branding, badges, headers, and quick-action chips.
- **Context Bar:** Displays active file (`src/openclone/oc_cli.py : L1-L45`) with Detach/Attach controls.
- **Syntax Highlighting & Copy:** Monospace code blocks with one-click copy buttons.
- **Approval Cards:** In-chat cryptographic digest verification with **Approve** and **Reject** buttons.

---

## 5. Installation & Usage Instructions

### Step 1: Install Extension into VS Code
From terminal or PowerShell:
```bash
code --install-extension OpenClone-2.0.0.vsix
```
Or inside VS Code:
1. Open the **Extensions** view (`Ctrl+Shift+X`).
2. Click the `...` menu (Views and More Actions) in the top right.
3. Select **Install from VSIX...**
4. Select `OpenClone-2.0.0.vsix`.

### Step 2: Start OpenClone Gateway
Start the OpenClone REST Gateway in the background:
```bash
python -m src.openclone.integrations.rest --port 8000
```

### Step 3: Use the AI Chat Panel
1. Click the **OpenClone** icon in the Activity Bar.
2. Select desired model (`Auto Route (MIE)`, `gemini-2.5-pro`, `gpt-4o`, etc.) or agent (`Software Architect`, `Security Auditor`).
3. Select code in any editor window to automatically attach context.
4. Click Quick Action chips: **Explain**, **Debug**, **Refactor**, **Tests**, or **Review**.
