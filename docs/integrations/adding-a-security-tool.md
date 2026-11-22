# Developer Guide: Adding a Security Tool Adapter

## 1. Overview
This guide defines the process for adding a static analysis, secrets, supply-chain, or dynamic testing engine to OpenClone's security orchestrator.

## 2. Tool Manifest Requirements

Every tool must declare a JSON manifest conforming to `schemas/security-tool-manifest.schema.json`:
- `tool_id`: Unique identifier (e.g., `sec-trivy`)
- `version_pin`: Exact pinned version or SHA256 digest
- `supported_profiles`: List of profiles (`quick-local`, `pull-request`, `full-repository`, etc.)
- `requires_network`: Boolean flag
- `requires_privileged_runtime`: Boolean flag (default `false`)
- `output_format`: `sarif` | `json` | `text`

## 3. Integration Rules
1. **Never Shell String Concatenate**: Execute tool binaries using structured command argument arrays (`[binary, arg1, arg2]`).
2. **Deterministic Timeouts**: All scanner runs must have an enforceable timeout (default: 60s for local, 300s for full-repo).
3. **Parse Output into Normalized Findings**: Map tool-specific severities into OpenClone standard severities (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`).
4. **Redact Sensitive Payloads**: Ensure file contents containing secrets are masked prior to persistence.
