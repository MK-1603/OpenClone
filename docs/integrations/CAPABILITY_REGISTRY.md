# Canonical Capability Registry

The **Canonical Capability Registry** (`src/openclone/integrations/capabilities.py`) provides the single source of truth for all tools and operations exposed across MCP, HTTP/OpenAPI, and local CLI.

---

## 1. Capability Taxonomy

| Capability Identifier | Name | Category | Risk Classification | Required Scopes | Human Approval |
|---|---|---|---|---|:---:|
| `openclone_list_projects` | List Projects | `project_discovery` | `READ_ONLY` | `projects:read` | No |
| `openclone_get_project_context` | Get Project Context | `project_discovery` | `READ_ONLY` | `projects:read` | No |
| `openclone_search_project_knowledge` | Search Project Knowledge | `knowledge_guidance` | `READ_ONLY` | `projects:read` | No |
| `openclone_get_checklist` | Get Lifecycle Checklist | `lifecycle_tasks` | `READ_ONLY` | `checklists:read` | No |
| `openclone_update_task_status` | Update Task Status | `lifecycle_tasks` | `HIGH_RISK_WRITE` | `tasks:write` | No (Requires Evidence) |
| `openclone_submit_implementation_report` | Submit Implementation Report | `lifecycle_tasks` | `LOW_RISK_WRITE` | `tasks:write` | No |
| `openclone_submit_evidence` | Submit Evidence Artifact | `evidence_verification` | `LOW_RISK_WRITE` | `evidence:write` | No |
| `openclone_request_verification` | Request Independent Verification | `evidence_verification` | `READ_ONLY` | `verification:request` | No |
| `openclone_get_quality_gate` | Evaluate Quality Gate | `defects_gates` | `READ_ONLY` | `checklists:read` | No |
| `openclone_create_defect` | Log Defect | `defects_gates` | `LOW_RISK_WRITE` | `defects:write` | No |
| `openclone_generate_ide_handoff` | Generate Scoped IDE Handoff | `handoff_release` | `READ_ONLY` | `tasks:read` | No |
| `openclone_get_release_readiness` | Get Release Readiness | `handoff_release` | `READ_ONLY` | `release:read` | No |
| `openclone_approve_release_deployment` | Approve Release Deployment | `handoff_release` | `PRODUCTION_IMPACT` | `release:approve` | **Yes (SHA-256 Digest)** |
| `openclone_get_status` | Get OpenClone Status | `knowledge_guidance` | `READ_ONLY` | `projects:read` | No |
| `openclone_get_guidance` | Get Specialized Guidance | `knowledge_guidance` | `READ_ONLY` | `projects:read` | No |

---

## 2. Risk Classifications

- **`READ_ONLY`:** Safe inspection tools that query state without modifying repository files or metadata.
- **`LOW_RISK_WRITE`:** Non-destructive record creation (e.g. logging a defect, attaching evidence artifact).
- **`HIGH_RISK_WRITE`:** State modifications affecting verification standing (e.g. transitioning task to `VERIFIED`).
- **`DESTRUCTIVE`:** Deletion or overwriting of existing project assets or historical audit records.
- **`EXTERNAL_SIDE_EFFECT`:** Outbound network notifications, webhook calls, or third-party service sync.
- **`PRODUCTION_IMPACT`:** Cloud deployment, database migration, or live infrastructure provisioning.
