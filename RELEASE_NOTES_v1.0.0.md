# OpenClone (AISDF) v1.0.0 — Initial Stable Production Release

> **"Build with Any AI. Governed by One Engineering Standard."**

OpenClone is proud to announce its **Inaugural Production Release: v1.0.0**.

---

## 📌 Release Concept & Versioning Note: The Starting Point is Now (v1.0.0)

While earlier experimental development branches and architectural explorations were labeled internally as *2.0.0 drafts*, this release formally establishes the **Canonical 1.0.0 Production Baseline** under strict [Semantic Versioning (SemVer)](https://semver.org/).

**"The first starting is now."** Version `1.0.0` guarantees:
1. **Stable Core APIs and Control Plane**: Zero breaking contract shifts without major version increments.
2. **Production-Ready Governance**: Fully deterministic state machines, human approval bindings, and cryptographic ledger hashing.
3. **Verified Cross-Platform Runtime**: Tested and passing across Linux, macOS (Apple Silicon), and Windows.

---

## 🚀 Key Capabilities in v1.0.0

### 1. Governed Specialist Workforce (72 Engineering Roles)
- **72 Native Worker Contracts** spanning 12 multidisciplinary teams: Security, Architecture, UX/UI Design, Backend, Quality Engineering, AI/ML, DevOps, and Mobile.
- **Strict Least-Privilege Boundaries**: Sensitive operations (`write`, `execute`, `release`, `destructive_change`) require explicit, verifiable human authorization.

### 2. Paperclip Authoritative Approval Gateway
- **Cryptographic Digest Binding**: Approvals are cryptographically bound to the canonical 64-character SHA-256 task digest, automatically invalidating upon any scope or dependency modification.
- **Replay Protection**: Persistent nonce storage prevents replay attacks.
- **Sliding-Window Rate Limiting**: Token-bucket rate limiter defending inbound webhooks and control plane endpoints.

### 3. Topological Engineering Dashboard
- **Kahn's Cycle Detection**: Validates Directed Acyclic Graphs (DAGs) and prevents circular task dependency deadlocks.
- **Topological Tiers**: Organizes parallelizable tasks into executable topological waves.
- **Path Traversal Protection**: Hardened workspace boundaries blocking arbitrary filesystem escape.

### 4. Deterministic Mobile Testing & Store Compliance Lab
- **Sanitized Execution**: Hardened ADB device interaction eliminating shell command injection vulnerabilities.
- **Device ID Strict Regex Validation**: Validates device IDs against `^[a-zA-Z0-9._:-]+$`.
- **Automated Store Compliance Scanner**: Audits package manifests against Google Play and Apple App Store submission policies.

### 5. Multi-Host Coding Agent Integration
- Native stdio / SSE **Model Context Protocol (MCP)** server providing 20 registered tools for Claude Code, Google Antigravity, OpenAI Codex, and Cursor.

---

## 📦 Installation & Quickstart

### Method 1: Install via Git / Pip (Recommended)
```bash
pip install git+https://github.com/MK-1603/OpenClone.git
```

*Windows Note: If `openclone` is not on your PATH, run:*
```cmd
set PATH=%PATH%;%LOCALAPPDATA%\Python\pythoncore-3.15-64\Scripts
```
*or execute via Python directly:*
```cmd
python -m openclone --version
```

### Method 2: Download Compiled Wheel from this Release
Download `openclone-1.0.0-py3-none-any.whl` from the Assets below, then install:
```bash
pip install openclone-1.0.0-py3-none-any.whl
```

---

## 🛠️ Essential Commands

```bash
# 1. Check system environment health
openclone doctor

# 2. View all 72 governed worker contracts
openclone workers

# 3. Initialize a governed project workspace
openclone init --project ./my-project --name "MyFirstApp" --owner "Developer"

# 4. Run repository quality gates & schema checks
openclone check list --project .

# 5. Verify cryptographic tamper-evident ledger integrity
openclone verify-ledger --project ./my-project
```

---

## 🔬 Automated Verification & Test Evidence

Every release artifact is validated through deterministic CI/CD quality gates:
- **351 Automated Tests Passing (100%)** across runtime, security, compliance, and integration suites.
- **Zero Broken Links** across 951 documentation files (`tools/check_links.py`).
- **56 Reusable Capability Engines** and **16 JSON Schemas** verified conformant (`tools/validate_repository.py`).
- **Multi-OS Wheel Smoke Test**: Verified clean build, install, and execution on:
  - `ubuntu-latest` (Python 3.10, 3.11, 3.12)
  - `macos-latest` (Python 3.10, 3.11, 3.12)
  - `windows-latest` (Python 3.10, 3.11, 3.12)

---

## 🔐 Cryptographic Checksums (SHA-256)
All release assets are cryptographically hashed and listed in `SHA256SUMS.txt`.
