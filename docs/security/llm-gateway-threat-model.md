# LLM Gateway & Agent Tooling Threat Model
**STRIDE Analysis, Boundary Protections, and Mitigation Controls**  
**Specification:** v1.0.0 | **Authority:** Security Standard

---

## 1. System Context & Threat Surface

The OpenClone model router and agent execution plane constitute high-value security boundaries because they handle provider credentials, source code context, and tool execution requests.

```text
[ Untrusted Source Code / PRs ] 
               │
               ▼
[ OpenClone Pre-flight & Prompt Engine ] ── (Redaction Filter) ──► [ External Model Provider ]
               │                                                          │
               ▼                                                          ▼
[ Task Contract & Approval Hash ]                               [ Untrusted Model Output ]
               │                                                          │
               ▼                                                          ▼
[ Deterministic Tool Sandbox ] ◄──────── (Strict Schema / AST) ───────────┘
```

---

## 2. STRIDE Threat Analysis & Mitigations

### 2.1 Spoofing (Identity & Approvals)
- **Threat**: Attacker tampers with task descriptions or approval records to bypass human authorization gates.
- **Mitigation**: Task parameters and approval payloads are cryptographically hashed using SHA-256. Any modification to task scope invalidates the digest and halts execution.

### 2.2 Tampering (State & Evidence)
- **Threat**: LLM modifies audit logs or task ledger files to hide failed checks or unauthorized changes.
- **Mitigation**: Audit ledgers use append-only HMAC chain digests. Log modifications cause verification failure during gate evaluation (`test_ledger_tampering_detected`).

### 2.3 Repudiation
- **Threat**: User or agent denies executing consequential actions (e.g., deployments or file deletions).
- **Mitigation**: Every action generates an immutable audit record containing timestamp, correlation ID, approver ID, command hash, and environment metadata.

### 2.4 Information Disclosure (Credentials & Secrets)
- **Threat**: Sensitive API keys, private tokens, or database passwords leak into prompts, logs, or commit histories.
- **Mitigation**: Multi-pattern secret redaction filter (`\b(api[_-]?key|secret[_-]?key|secret|token|passw(?:or)?d)\b`) masks values before persistence or transmission. Child execution processes do not inherit caller secret environment variables.

### 2.5 Denial of Service (Resource Exhaustion)
- **Threat**: Recursive delegation storms, infinite retry loops, or unbounded LLM token consumption.
- **Mitigation**: Enforced execution depth limits (max recursion depth: 3), deterministic timeouts (30s default), and budget token caps per session.

### 2.6 Elevation of Privilege (Command Injection & Traversal)
- **Threat**: Malicious prompt or path traversal (`../../etc/passwd`) escapes project root or executes unauthorized binaries.
- **Mitigation**: Workspace isolation strictly forbids cwd escape (`test_cwd_escape_and_env_leak_refused`). Shell commands require explicit structured argument lists (`list[str]`), rejecting raw shell-string interpolation.
