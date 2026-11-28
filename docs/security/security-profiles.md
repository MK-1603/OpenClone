# OpenClone Security Profiles
**Layered Verification Tiers for Development, CI, and Deployment**  
**Specification:** v1.0.0 | **Authority:** Security Standard

---

## 1. Profile Matrix

OpenClone defines seven distinct, non-overlapping security execution profiles to deliver proportionate feedback without developer friction:

| Profile Identifier | Target Triggers | Network Active? | Scanners Executed | Gate Behavior |
| :--- | :--- | :---: | :--- | :--- |
| `quick-local` | Pre-commit, local dev | **No** | TruffleHog (diff), Semgrep (fast rules) | Advisory / Local Block |
| `pull-request` | PR open/synchronize | Limited | TruffleHog, Semgrep, Trivy (vuln), Claude Security Review | **Blocking Gate** |
| `full-repository` | Nightly, scheduled | Controlled | All SAST, Trivy (full), ClamAV, Codex Security | **Blocking Gate** |
| `agent-supply-chain`| MCP/Skill install | Controlled | NVIDIA SkillSpector, AST analyzer | **Pre-install Gate** |
| `authorized-dynamic`| Staging test (Opt-in) | **Yes** (Allowlist) | Nuclei, Strix | Non-blocking Audit |
| `llm-red-team` | Model eval (Opt-in) | **Yes** (Allowlist) | Microsoft PyRIT | Evaluation Report |
| `release` | Tagged release build | Controlled | TruffleHog, Trivy (SBOM + Vuln), License Lock | **Release Gate** |

---

## 2. Profile Execution Rules

### `quick-local`
- Runs in `< 5 seconds` over staged or modified files only.
- Offline execution strictly enforced; zero remote network socket calls.

### `pull-request`
- Enforces zero open `CRITICAL` or `HIGH` vulnerabilities.
- Generates SARIF report uploaded to GitHub Code Scanning.

### `authorized-dynamic`
- Requires valid `security/authorized_targets.json` entry and active human approval token.
- Rejects wildcard IP ranges (`0.0.0.0/0`) or public top-level domains.
