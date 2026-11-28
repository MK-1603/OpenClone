# Developer Guide: Adding a Router Adapter

## 1. Overview
This guide defines the process for contributing an external LLM router or gateway adapter to OpenClone.

## 2. Implementation Steps

1. **Implement Provider Protocol**:
   Subclass `openclone.core.providers.base.ProviderAdapter` and implement all abstract methods:
   - `validate_configuration()`
   - `list_models()`
   - `get_capabilities(model)`
   - `generate(request)`
   - `stream(request)`
   - `cancel(request_id)`
   - `normalize_error(error)`

2. **Register Capabilities**:
   Declare supported features explicitly in `capabilities.json`. Do not advertise capabilities that have not been tested.

3. **Enforce SSRF & Localhost Protection**:
   All user-supplied endpoint URLs must be validated:
   - Reject non-loopback private IP ranges (e.g., `10.0.0.0/8`, `192.168.0.0/16`, `169.254.169.254`) unless explicitly running in `offline-local` mode.
   - Enforce HTTPS for all remote cloud gateways.

4. **Add Unit & Conformance Tests**:
   - Provide unit tests mocking downstream HTTP responses.
   - Verify that cancelled requests terminate upstream socket streams cleanly.
   - Verify that credentials are redacted from log outputs.
