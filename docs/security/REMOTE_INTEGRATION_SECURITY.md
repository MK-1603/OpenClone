# Remote Integration Security Specification

**Version:** 2.0.0  
**Classification:** Security Architecture & Threat Model  
**Status:** IMPLEMENTED  

---

## 1. Scope & Objective

This document defines the cryptographic, transport, and authorization security controls for remote inbound and outbound integrations within OpenClone, with specific focus on the Paperclip adapter, external agent orchestrators, and webhook callbacks.

---

## 2. Threat Model & Mitigations

| Threat ID | Threat Vector | Impact | Architectural Mitigation |
| :--- | :--- | :--- | :--- |
| **THREAT-01** | **Man-in-the-Middle (MitM) Tampering** | Attacker intercepts and modifies remote task instructions. | Transport Layer Security (TLS 1.3) required. HMAC-SHA256 request signing over canonical body. |
| **THREAT-02** | **Replay Attack** | Attacker captures valid signed request and resends it to trigger redundant executions. | Nonce tracking (`X-OpenClone-Nonce`) combined with a strict 300-second timestamp drift ceiling (`X-OpenClone-Timestamp`). |
| **THREAT-03** | **Approval Spoofing** | Compromised agent crafts metadata `{"human_approved": true}` without human consent. | Explicit rejection of boolean approvals. Cryptographic SHA-256 approval digest verification against ledger. |
| **THREAT-04** | **Secret Leakage in Version Control** | Hardcoded API keys or credentials committed to repository. | Zero-secret policy, `.env.template` enforcement, automated pre-commit secret scans (`scan_secrets.py`). |
| **THREAT-05** | **Denial of Service (DoS)** | Volumetric task submission flooding SQLite ledger. | Payload length limits (10 MB ceiling) and rate limiting on ingestion endpoints. |

---

## 3. Cryptographic Signature Scheme (HMAC-SHA256)

Every HTTP request to an OpenClone integration endpoint must supply three mandatory headers:

```http
X-OpenClone-Timestamp: <UNIX_TIMESTAMP_SECONDS>
X-OpenClone-Nonce: <UNIQUE_UUID_OR_RANDOM_STRING>
X-OpenClone-Signature: <HEX_ENCODED_HMAC_SHA256>
```

### Signature Generation Algorithm

1. Ensure the timestamp is within 300 seconds of the server's current UTC time:
   $$|\text{timestamp}_{\text{client}} - \text{timestamp}_{\text{server}}| \le 300$$
2. Construct the canonical signing payload:
   $$\text{canonical} = \text{timestamp} \mathbin{\Vert} \text{nonce} \mathbin{\Vert} \text{raw\_body}$$
3. Compute HMAC using SHA-256:
   $$\text{signature} = \text{HMAC-SHA256}(\text{secret}, \text{canonical}).\text{hexdigest}()$$
4. Validate signature using constant-time comparison (`hmac.compare_digest`) to prevent timing side-channel attacks.

```python
import hmac
import hashlib

def verify_request_signature(secret: str, timestamp: str, nonce: str, body: bytes, expected_sig: str) -> bool:
    message = f"{timestamp}:{nonce}:".encode("utf-8") + body
    computed = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed.lower(), expected_sig.lower())
```

---

## 4. Replay Nonce Cache Lifecycle

To preserve low operational overhead and zero external dependencies, nonces are tracked within an ephemeral memory cache with periodic pruning of entries older than 600 seconds.

- **Storage:** `set` of `(nonce, timestamp)` tuples.
- **Verification:** If `nonce` exists in set, the request is rejected immediately with HTTP 401 Unauthorized.
- **Pruning:** On each validation cycle, expired nonces (`now - timestamp > 600`) are evicted.

---

## 5. Human Approval Verification Specification

External agents attempting to dispatch high-risk operations (file writes outside sandbox, deployments, database migrations) must include authoritative human approval:

```json
{
  "task_id": "task-eng-9021",
  "command": "deploy",
  "metadata": {
    "human_approved": true,
    "approval_digest": "4a5e1e53b93f...64_hex_characters...",
    "approver_id": "security-lead@enterprise.org"
  }
}
```

The runtime enforces:
1. `len(approval_digest) == 64` and matches hexadecimal character set `[0-9a-fA-F]`.
2. `approver_id` must not be null or empty.
3. The digest must match the task's expected cryptographic signature registered in `workforce.sqlite3`.
