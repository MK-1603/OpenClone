# HTTP REST API & OpenAPI 3.1 Specification

For AI environments that do not support MCP or require standard HTTP integrations (e.g. ChatGPT Actions, n8n, automated webhooks), OpenClone provides a complete **OpenAPI 3.1.0** REST API interface.

---

## 1. Specification Generation

The specification is dynamically generated from canonical capabilities via `src/openclone/integrations/openapi.py` and exported to `adapters/chatgpt/openapi.json`.

```bash
# Export latest OpenAPI schema:
python -c "import json; from src.openclone.integrations.openapi import generate_openapi_spec; open('adapters/chatgpt/openapi.json', 'w').write(json.dumps(generate_openapi_spec(), indent=2))"
```

---

## 2. Core Endpoints

All endpoints require Bearer Token authentication (`Authorization: Bearer <token>`):

| Method | Endpoint Path | Description | Required Scope |
|---|---|---|---|
| `GET` | `/v1/capabilities/openclone_list_projects` | List active projects | `projects:read` |
| `GET` | `/v1/capabilities/openclone_get_project_context` | Retrieve project context & rules | `projects:read` |
| `GET` | `/v1/capabilities/openclone_get_checklist` | Retrieve 22-phase lifecycle tasks | `checklists:read` |
| `POST` | `/v1/capabilities/openclone_update_task_status` | Advance task state | `tasks:write` |
| `POST` | `/v1/capabilities/openclone_submit_evidence` | Attach verifiable proof | `evidence:write` |
| `GET` | `/v1/capabilities/openclone_get_quality_gate` | Evaluate phase quality gate | `checklists:read` |
| `POST` | `/v1/capabilities/openclone_create_defect` | Log a tracked defect | `defects:write` |
| `GET` | `/v1/capabilities/openclone_get_release_readiness` | Assess production readiness | `release:read` |
| `POST` | `/v1/capabilities/openclone_approve_release_deployment` | Authorize cloud rollout | `release:approve` |

---

## 3. Webhook Event Notifications

Outbound webhooks deliver cryptographically signed JSON payloads (`X-OpenClone-Signature: sha256=<hex>`):
- `task.blocked`
- `evidence.attached`
- `verification.completed`
- `quality_gate.evaluated`
- `release.approved`
