# OpenClone Upstream Update & Cadence Management Policy

**Document ID:** `POL-UPSTREAM-UPDATE-CADENCE-v1.0.0`  
**Product:** OpenClone 2.0 Universal AI Software Engineering Platform  
**Standard:** AISDF Standard 1.0.0  
**Status:** `NORMATIVE OPERATIONAL POLICY`  

---

## 1. Upstream Update Principles

OpenClone prioritizes **deterministic stability, reproducibility, and security** over chasing every upstream commit.

### Core Policies
1. **No Automatic Production Updates:** OpenClone NEVER auto-updates upstream integrations in production or default plugin bundles. Upstream updates must be intentionally reviewed, evaluated, and committed.
2. **Cryptographic Commit Pinning:** Every upstream integration is locked to a verified Git commit SHA recorded in [`integrations/registry/upstream_registry.json`](../../integrations/registry/upstream_registry.json).
3. **Change Detection Gate:** Before updating any pinned commit, maintainers must verify:
   - Has the license changed or become restrictive?
   - Have new third-party dependencies or pre-install scripts been introduced?
   - Does the update introduce breaking schema or capability changes?
   - Do all automated integration tests pass against the update candidate?

---

## 2. Governed 6-Step Update Workflow

```text
1. Upstream Release / Commit Detected
                │
                ▼
2. Fetch Candidate in .openclone-dev/upstream/
                │
                ▼
3. Run License & Supply-Chain Diff
   (Check for license modifications or new binary blobs)
                │
                ▼
4. Run Integration Test Suite
   (python -m unittest tests/integrations/test_upstream_integrations.py)
                │
                ▼
5. Update Manifests & Commit Pinning
   (Update integrations/manifests/<ID>.manifest.json & upstream_registry.json)
                │
                ▼
6. Human Review & Pull Request Sign-off
```

---

## 3. Maintenance Commands

Maintainers use the following commands to audit and check for upstream updates:

```bash
# 1. Inspect current status of all 27 registered integrations
python tools/upstream_manager.py status

# 2. Check for new upstream commits and print diff summaries
python tools/upstream_manager.py check-updates

# 3. Verify registry schema and integration manifests
python -m unittest tests/integrations/test_upstream_integrations.py -v
```

---

## 4. Emergency Revocation & Deprecation

If an upstream repository is compromised, changes its license to proprietary/commercial terms, or is deleted:
1. **Immediate Quarantine:** The affected integration status is transitioned to `BLOCKED_SECURITY_REVIEW` or `BLOCKED_LICENSE_REVIEW`.
2. **Decouple Capabilities:** The associated adapter falls back to native OpenClone implementations or returns a graceful unavailable message.
3. **Registry Audit Record:** An immutable revocation entry is committed to [`docs/integrations/INTEGRATION-DECISIONS.md`](INTEGRATION-DECISIONS.md).
