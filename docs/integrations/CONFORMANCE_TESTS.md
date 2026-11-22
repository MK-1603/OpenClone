# Conformance Testing & Verification Suite

All integrations are verified by the automated test suite in `tests/test_universal_integrations.py`.

---

## 1. Conformance Matrix

| Test Suite / Method | Coverage | Pass Criteria | Status |
|---|---|---|:---:|
| `test_canonical_capability_registry` | Canonical registration, categorization, MCP tool transformation | All 15 capabilities registered with valid schemas | :white_check_mark: PASS |
| `test_gateway_authentication_and_scopes` | Bearer token validation, scope enforcement | Unauthorized scopes rejected with `PermissionError` | :white_check_mark: PASS |
| `test_gateway_cross_project_isolation` | Multi-tenant boundary isolation | Cross-project access fails with isolation error | :white_check_mark: PASS |
| `test_gateway_human_approval_enforcement` | Production impact gate and SHA-256 digest | Deployment without valid digest blocked | :white_check_mark: PASS |
| `test_gateway_secret_redaction` | Sensitive token stripping from inputs/outputs | Zero secrets exposed in logs or return dicts | :white_check_mark: PASS |
| `test_openapi_spec_generation_and_rest_dispatch` | OpenAPI 3.1 generation and REST dispatch | Valid schema, dispatch executes via Gateway | :white_check_mark: PASS |
| `test_mcp_server_extended_tools` | MCP tools/list and tools/call for canonical capabilities | Tools discoverable and callable via JSON-RPC | :white_check_mark: PASS |
| `test_mcp_server_resources_primitives` | MCP resources/list and resources/read | Overview, checklist, rulebook URIs resolve | :white_check_mark: PASS |
| `test_mcp_server_prompts_primitives` | MCP prompts/list and prompts/get | Planning, implementing, verifying prompts return | :white_check_mark: PASS |

---

## 2. Test Execution Command

```bash
python -m unittest discover -s tests -p "test_universal_integrations.py" -v
```
All 9 test cases pass in under 0.1 seconds.
