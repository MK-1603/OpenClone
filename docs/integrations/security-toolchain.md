# Security Toolchain Integration & Scanner Lock
**12-Tool Orchestration Architecture, Classification, and Safety Profiles**  
**Specification:** v1.0.0 | **Authority:** Security Standard

---

## 1. Scope & Execution Principles

OpenClone orchestrates security analysis through an isolated, profile-based security runner. The framework enforces strict boundaries:
- **No Indiscriminate Scanning**: Scanners run only against approved project targets and file boundaries.
- **No Unsafe Execution**: Dynamic penetration tools (Nuclei, Strix) are strictly opt-in and restricted to verified, user-authorized endpoints.
- **Zero Secret Commits**: Sensitive credentials are automatically redacted before logging, reporting, or evidence hashing.
- **Deterministic Tool Pinning**: All scanner engines are pinned via immutable version and hash manifests in [`security/scanners.lock.json`](file:///d:/New%20folder/OpenClone/security/scanners.lock.json).

---

## 2. Security Tool Classification Matrix

| Category | Candidate Engine | Upstream Repository | Execution Mode | OpenClone Profile | Privilege Level |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Secrets Detection** | **TruffleHog** | `github.com/trufflesecurity/trufflehog` | Local CLI | `quick-local`, `pull-request` | Read-only |
| **Static Analysis (SAST)** | **Semgrep** | `github.com/semgrep/semgrep` | Local CLI | `quick-local`, `pull-request` | Read-only |
| **Software Supply-Chain** | **Trivy** | `github.com/aquasecurity/trivy` | Local CLI | `pull-request`, `release` | Read-only |
| **Agent / MCP Supply-Chain**| **NVIDIA SkillSpector** | `github.com/NVIDIA/skillspector` | Local Analyzer | `agent-supply-chain` | Read-only |
| **Malware Analysis** | **ClamAV** | `github.com/Cisco-Talos/clamav` | Isolated Daemon | `full-repository`, `release` | Read-only |
| **Cloud Infrastructure Audit**| **Cloudflare Security Audit**| `github.com/cloudflare/security-audit-skill` | Skill Runner | `full-repository` | Scoped API |
| **AI Vulnerability Discovery**| **OpenAI Codex Security** | `github.com/openai/codex-security` | LLM Review | `full-repository` | Read-only |
| **AI Diff Review** | **Claude Code Security Review**| `github.com/anthropics/claude-code-security-review`| LLM Review | `pull-request` | Read-only |
| **Dynamic Pentesting** | **Nuclei** | `github.com/projectdiscovery/nuclei` | Network Runner | `authorized-dynamic` (Opt-in)| Restricted Network |
| **AI Agent Penetration** | **Strix** | `github.com/usestrix/strix` | Sandboxed Agent| `authorized-dynamic` (Opt-in)| Isolated Container |
| **LLM Red Teaming** | **Microsoft PyRIT** | `github.com/microsoft/pyrit` | Red-Team Suite | `llm-red-team` (Opt-in) | Isolated Test Env |
| **Agent Security Research** | **BLA (Blind LLM Agents)** | `github.com/qybaihe/bla` | Research Runner| `research` | Isolated Benchmark |

---

## 3. Normalized Finding Schema

All security tool outputs are parsed into a normalized, lossless finding format:

```json
{
  "finding_id": "SEC-TRUFFLE-001-a1b2",
  "source_tool": "trufflehog",
  "source_rule_id": "generic-api-key",
  "category": "SECRET_EXPOSURE",
  "title": "Unredacted API Key in Source File",
  "severity_original": "CRITICAL",
  "severity_normalized": "CRITICAL",
  "confidence": "HIGH",
  "status": "OPEN",
  "file_path": "config/settings.py",
  "line_start": 42,
  "line_end": 42,
  "evidence": "api_key = \"***REDACTED***\"",
  "remediation": "Move credential to environment variable or secrets manager.",
  "scan_profile": "quick-local",
  "scan_run_id": "run-20261122-001"
}
```

---

## 4. Execution Sandbox & Target Authorization

Dynamic engines (`Nuclei`, `Strix`) and LLM red-teaming frameworks (`PyRIT`) require pre-flight verification:
1. Target allowlist check: Scans are rejected unless the target domain/IP is explicitly listed in `security/authorized_targets.json`.
2. Written confirmation gate: Interactive terminal assurance or cryptographically signed policy approval is required prior to socket creation.
3. Network egress boundary: Scans execute within containerized networks preventing lateral movement to production VPCs.
