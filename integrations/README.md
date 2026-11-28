# OpenClone Integrations Architecture & Subsystems

This directory houses the OpenClone external repository integration layer:

- [`registry/`](registry/): Canonical machine-readable registry (`upstream_registry.json`) for the 27 upstream repositories.
- [`manifests/`](manifests/): Declarative capability and integration manifests for every audited upstream tool.
- [`adapters/`](adapters/): Thin, bounded runtime adapters for external capabilities (design tokens, dynamic pentesting, scanner gateway, red-teaming).

See [`docs/integrations/INTEGRATION-REGISTRY.md`](../docs/integrations/INTEGRATION-REGISTRY.md) and [`docs/integrations/INTEGRATION-DECISIONS.md`](../docs/integrations/INTEGRATION-DECISIONS.md) for normative specifications.
