# OpenClone Checklist Item Schema Contract
**Version:** 1.0.0  
**Scope:** Data model contract for checklist items, subtasks, verification checks, evidence records, and defects.

---

## 1. Field Specification Contract

```json
{
  "id": "PHASE_01_DISCOVERY_TASK_01",
  "project_id": "openclone-saas-01",
  "parent_id": "PHASE_01_DISCOVERY",
  "phase_id": "PHASE_01_DISCOVERY",
  "category": "Problem Definition",
  "title": "Define Core Problem Statement & User Pain Points",
  "description": "Describe root problem, frequency, severity, and distinction between symptoms and causes.",
  "why_it_matters": "Prevents building solutions for non-existent or misunderstood user problems.",
  "type": "TASK",
  "applicability": "REQUIRED",
  "applicability_reason": "Standard lifecycle requirement",
  "status": "VERIFIED",
  "priority": "CRITICAL",
  "risk_level": "HIGH",
  "requirement_ids": ["REQ-001"],
  "dependency_ids": [],
  "acceptance_criteria": [
    "Problem statement documented with target audience",
    "Pain points ranked by severity"
  ],
  "verification_method": "automated_test",
  "verification_command": "python -m unittest tests/test_discovery.py",
  "evidence_refs": [
    {
      "id": "EV_01",
      "evidence_type": "code_diff",
      "ref": "docs/PRD.md",
      "description": "PRD problem statement",
      "produced_by": "human_architect",
      "timestamp": "2026-11-22T17:00:00Z",
      "checksum": "a1b2c3d4e5f60718"
    }
  ],
  "checks": [
    {
      "id": "CHECK_01",
      "item_id": "PHASE_01_DISCOVERY_TASK_01",
      "title": "Verify problem statement in PRD",
      "min_level": "V2_ARTIFACT_PRESENT",
      "outcome": "PASS",
      "verified_by": "independent_verifier",
      "verified_at": "2026-11-22T17:05:00Z"
    }
  ],
  "defects": [],
  "assignee_type": "ai_agent",
  "assignee_id": "claude-code",
  "reviewer_id": "security-officer",
  "waiver_reason": null,
  "version": "1.0.0",
  "created_at": "2026-11-22T16:50:00Z",
  "updated_at": "2026-11-22T17:05:00Z",
  "completed_at": "2026-11-22T17:00:00Z",
  "verified_at": "2026-11-22T17:05:00Z"
}
```

---

## 2. Immutability & Audit Guarantee

- All state transitions and evidence attachments append an immutable audit record to `audit_log`.
- Digest checksums (`SHA-256`) bind evidence to task states, preventing retroactive evidence manipulation.
