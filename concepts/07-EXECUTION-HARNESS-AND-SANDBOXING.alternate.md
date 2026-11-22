# Concept 07: Execution Harness & Sandboxing (Alternate Specification)

## 1. Alternate Paradigm: Ephemeral Micro-VM / Docker Sandbox
When running untrusted code or third-party agent contributions, process-level allowlisting is insufficient. The alternate model provides **Containerized Micro-VM Isolation**.

## 2. How the Alternate Operates
1. **Ephemeral Containers:** Each task executes inside a transient, non-root Docker or Podman container with a read-only root filesystem.
2. **Network Namespaces:** Network access is disabled by default (`--network none`) unless explicitly whitelisted for dependency fetching.
3. **Mounted Workspace:** Only the project directory is mounted with restricted permissions. Host credentials and SSH keys are physically inaccessible.

## 3. Trade-Off Analysis
* **Strengths:** True operating-system level isolation, safe for multi-tenant and autonomous code execution.
* **Risks:** Requires Docker/container runtime installed and configured on the host.
