# Authorization, Scopes & Identity Model

OpenClone enforces **zero-trust least privilege** across all integration surfaces. No AI host is granted universal administrative permissions.

---

## 1. Scoped Permission Taxonomy

| Scope | Description | Permitted Capabilities |
|---|---|---|
| `projects:read` | Read project metadata, architecture, and knowledge. | `openclone_list_projects`, `openclone_get_project_context`, `openclone_search_project_knowledge` |
| `checklists:read` | Inspect lifecycle phases, tasks, and quality gates. | `openclone_get_checklist`, `openclone_get_quality_gate` |
| `tasks:read` | Inspect task details and handoff contracts. | `openclone_generate_ide_handoff` |
| `tasks:write` | Advance task lifecycle states and submit reports. | `openclone_update_task_status`, `openclone_submit_implementation_report` |
| `evidence:write` | Attach observable code diffs, logs, screenshots. | `openclone_submit_evidence` |
| `verification:request` | Request deterministic independent verification. | `openclone_request_verification` |
| `defects:write` | Log and update defects blocking gates. | `openclone_create_defect` |
| `release:read` | Assess pre-production release readiness. | `openclone_get_release_readiness` |
| `release:approve` | Cryptographically authorize cloud deployment. | `openclone_approve_release_deployment` |

---

## 2. Authentication Tokens

The Integration Gateway (`src/openclone/integrations/gateway.py`) authenticates callers via OAuth 2.1 / OIDC Bearer Tokens:
- **`oc_live_...`:** Full maintainer token granting read, write, and approval scopes.
- **`oc_ide_...`:** Scoped IDE agent token restricted to task execution and evidence attachment.
- **`oc_ro_...`:** Read-only token for external audit or guest inspectors.

---

## 3. Cross-Project Boundary Isolation

Every request is evaluated against the authenticated user's `project_id`. Any attempt by an agent to access or mutate resources in another project raises an immediate `Cross-project access violation` exception and logs an audit security event.
