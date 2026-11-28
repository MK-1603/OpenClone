# Paperclip Security & Authoritative Approval Verification

**Repository:** `MK-1603/OpenClone`  
**Date:** 2026-11-24  
**Audit Classification:** Security Assurance & Verification Report  
**Target Modules:** `src/openclone/integrations/paperclip/connector.py`, `src/openclone/integrations/paperclip/server.py`  

---

## 1. Executive Summary

This report establishes independent verification of the security architecture governing external Paperclip integrations. External metadata alone (`"human_approved": true`) is fundamentally unauthoritative. Protection of sensitive operations (such as production deployments, database dropping, key rotation) requires cryptographic binding to an authoritative approval record that cannot be forged, replayed, expired, modified, or applied across workspace boundaries.

---

## 2. Threat Analysis & Security Controls

| Threat Vector | Description | Architectural Mitigation | Code Location |
|---|---|---|---|
| **THREAT-1: Metadata Spoofing** | External agent passes `metadata={"human_approved": true}` to self-authorize destructive actions. | The connector rejects any sensitive task lacking a registered `approval_id` in the `AuthoritativeApprovalStore`. | `connector.py:180-195` |
| **THREAT-2: Forged Digest** | Attacker creates an arbitrary 64-char hex string as `approval_digest`. | The digest must match the deterministic SHA-256 hash of canonical task parameters (`org_id:task_id:workspace:action:title:description`). | `connector.py:197-205` |
| **THREAT-3: Content Tampering** | Attacker obtains approval for `Deploy v1.0` then mutates description to `Drop billing tables`. | Canonical task digest changes; constant-time check (`hmac.compare_digest`) fails. | `connector.py:120-130` |
| **THREAT-4: Approval Replay** | Attacker re-submits a previously executed sensitive task reusing an old approval ID. | The approval record is atomically marked `consumed = True` upon execution. Re-use raises "Approval has already been consumed". | `connector.py:100-110` |
| **THREAT-5: Expiration Bypass** | Attacker uses a stale approval record past its validity window. | The store checks `current_time <= expires_at`. Stale approvals raise "Approval has expired". | `connector.py:102-105` |
| **THREAT-6: Cross-Workspace Escape** | Approval granted for `test-app` is applied against `production-infra`. | Normalized path containment strictly checks `rec.workspace_root == target_workspace`. | `connector.py:112-116` |
| **THREAT-7: Action Mismatch** | Approval granted for `deploy to prod` is attempted on `delete database`. | Action string must match the requested sensitive operation exactly. | `connector.py:118-120` |
| **THREAT-8: Unauthorized Approver** | Unregistered or untrusted identity signs an approval. | Approver identity must belong to the authorized human approvers policy whitelist. | `connector.py:108-111` |
| **THREAT-9: Replay Attack on HTTP API** | Attacker captures and re-sends valid signed HTTP requests. | SQLite-backed atomic primary key constraint on `paperclip_nonces(nonce)` blocks duplicate nonces across server instances and restarts. | `server.py:100-120` |
| **THREAT-10: Denial of Service** | Flooding endpoint with massive payloads or volumetric requests. | 10MB payload ceiling (`MAX_REQUEST_BYTES`) and sliding-window rate limiting per client IP. | `server.py:27-46` |

---

## 3. Mathematical & Cryptographic Specifications

### Canonical Task Digest Formulation
$$\text{TaskDigest} = \text{SHA256}(\text{org\_id} \mathbin{\Vert} \text{task\_id} \mathbin{\Vert} \text{workspace} \mathbin{\Vert} \text{action} \mathbin{\Vert} \text{title} \mathbin{\Vert} \text{description})$$

### HTTP Request Signature Canonical String
$$\text{Signature} = \text{HMAC-SHA256}(\text{secret}, \text{METHOD} \mathbin{\Vert} \text{PATH} \mathbin{\Vert} \text{TIMESTAMP} \mathbin{\Vert} \text{NONCE} \mathbin{\Vert} \text{SHA256}(\text{body}))$$

---

## 4. Test Scenario Coverage Matrix

The test suite in `tests/test_paperclip_and_mobile_compliance.py` and `tests/test_enterprise_operational_intelligence.py` validates all required conditions:

| Test ID | Scenario | Expected Outcome | Result |
|---|---|---|:---:|
| `TC-PAP-01` | `human_approved: true` without approval record | `NEEDS_APPROVAL`: Missing approval record | **PASS** |
| `TC-PAP-02` | Invalid SHA-256 digest format (e.g. non-hex / wrong length) | `NEEDS_APPROVAL`: Invalid SHA-256 format | **PASS** |
| `TC-PAP-03` | Task title/description mutated after approval | `NEEDS_APPROVAL`: Task digest mismatch | **PASS** |
| `TC-PAP-04` | Replayed approval (attempting to consume twice) | `NEEDS_APPROVAL`: Already consumed | **PASS** |
| `TC-PAP-05` | Expired approval timestamp | `NEEDS_APPROVAL`: Approval expired | **PASS** |
| `TC-PAP-06` | Approval issued for different workspace root | `NEEDS_APPROVAL`: Workspace mismatch | **PASS** |
| `TC-PAP-07` | Approval issued for different action | `NEEDS_APPROVAL`: Action mismatch | **PASS** |
| `TC-PAP-08` | Approver identity not in authorized policy | `NEEDS_APPROVAL`: Unauthorized approver | **PASS** |
| `TC-PAP-09` | Valid bound approval with correct digest and approver | `ACCEPTED` / `IN_PROGRESS` | **PASS** |
| `TC-PAP-10` | HTTP HMAC-SHA256 signature verification | `200 Authorized` | **PASS** |
| `TC-PAP-11` | HTTP Duplicate nonce replay (persistent SQLite) | `401 Duplicate nonce detected` | **PASS** |
| `TC-PAP-12` | HTTP Expired timestamp (>300s drift) | `401 Request timestamp expired` | **PASS** |
| `TC-PAP-13` | HTTP Rate limiting (>120 reqs/min) | `429 TooManyRequests` | **PASS** |
| `TC-PAP-14` | HTTP Payload exceeding 10MB | `413 PayloadTooLarge` | **PASS** |
