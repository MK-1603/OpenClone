# Third-Party Notices and Open-Source Attribution

OpenClone incorporates, references, and interfaces with open-source software and specifications under their respective licenses.

---

## 1. Taste Skill
- **Upstream Repository**: https://github.com/Leonxlnx/taste-skill
- **License**: MIT License
- **Copyright**: Copyright (c) 2024 Leonxlnx
- **Role in OpenClone**: Anti-AI-slop design governance, visual morphism design tokens, component finish gates, and browser layout/performance audit engine located in `skills/taste-skill/`.

---

## 2. Model Context Protocol (MCP)
- **Specification**: Model Context Protocol Specification (2024-11-05)
- **Maintainer**: Anthropic / Model Context Protocol Community
- **License**: MIT License
- **Role in OpenClone**: Native client/server interoperability standard for cross-IDE tool execution (`src/openclone/mcp/`).

---

## 3. Evaluated External LLM Routers & Gateways
The following projects were evaluated in accordance with the OpenClone Architecture Standards as external design references:
- **alienz-dev/llm-router** (MIT License) - `https://github.com/alienz-dev/llm-router`
- **Gmagl/omniroute** (Apache-2.0 License) - `https://github.com/Gmagl/omniroute`
- **Devansh-365/freellm** (MIT License) - `https://github.com/Devansh-365/freellm`
- **kaiser-data/free-llm-proxy-router** (MIT License) - `https://github.com/kaiser-data/free-llm-proxy-router`
- **nabinkhadka/free-llm-api** (Apache-2.0 License) - `https://github.com/nabinkhadka/free-llm-api`
- **YeomanYe/free-llm-router** (MIT License) - `https://github.com/YeomanYe/free-llm-router`
- **tashfeenahmed/freellmapi** (MIT License) - `https://github.com/tashfeenahmed/freellmapi`

---

## 4. Pinned Security Engines & Toolchain
OpenClone orchestrates the following security scanners under their respective licenses via isolated subprocess boundaries:
- **TruffleHog**: AGPL-3.0 - Truffle Security (`https://github.com/trufflesecurity/trufflehog`)
- **Semgrep**: LGPL-2.1 - Semgrep, Inc. (`https://github.com/semgrep/semgrep`)
- **Trivy**: Apache-2.0 - Aqua Security Software Ltd. (`https://github.com/aquasecurity/trivy`)
- **NVIDIA SkillSpector**: Apache-2.0 - NVIDIA Corporation (`https://github.com/NVIDIA/skillspector`)
- **Nuclei**: MIT License - ProjectDiscovery, Inc. (`https://github.com/projectdiscovery/nuclei`)
- **Strix**: MIT License - Strix Security (`https://github.com/usestrix/strix`)
- **Microsoft PyRIT**: MIT License - Microsoft Corporation (`https://github.com/microsoft/pyrit`)
- **ClamAV**: GPL-2.0 - Cisco Systems, Inc. (`https://github.com/Cisco-Talos/clamav`)
