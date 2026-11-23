# OpenClone Global Layer

The **Global Layer** enables developers to install OpenClone once on their workstation and have consistent governance, anti-slop rules, and capability standards across all AI coding tools and IDEs.

---

## Directory Architecture

```
global/
├── README.md                           # This document
├── core/                               # Host-neutral core governance & defaults
│   ├── OPENCLONE-GLOBAL.md             # Global governance standard and precedence rules
│   └── config.default.yaml             # Neutral configuration template
├── hosts/                              # Pre-packaged host adapters
│   ├── antigravity/                    # Google Antigravity plugin package
│   ├── claude-code/                    # Claude Code marketplace & plugin manifests
│   ├── codex/                          # OpenAI Codex configuration & MCP manifests
│   ├── cursor/                         # Cursor global rule template
│   ├── vscode/                         # VS Code MCP configuration
│   ├── chatgpt/                        # Custom GPT instructions & OpenAPI schemas
│   └── generic-mcp/                    # Generic MCP server configuration
├── installer/                          # Transactional global install / uninstall scripts
│   ├── install-global.cmd              # Windows installation entrypoint
│   ├── install-global.sh               # POSIX installation entrypoint
│   ├── uninstall-global.cmd            # Windows uninstallation entrypoint
│   ├── uninstall-global.sh             # POSIX uninstallation entrypoint
│   └── verify-global.py                # Checksum & integrity verification tool
└── docs/                               # Global layer documentation
    ├── GLOBAL-PLUGIN-INSTALLATION.md   # Installation guide
    └── HOST-COMPATIBILITY.md           # Supported host compatibility matrix
```

---

## Precedence Model

OpenClone enforces strict 4-tier configuration precedence:
`project rule > project .openclone > ~/.openclone global > framework defaults`
