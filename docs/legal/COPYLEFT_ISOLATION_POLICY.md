# OpenClone — Copyleft Isolation Policy

## Policy Mandate
OpenClone is licensed under the permissive MIT License. To ensure safe commercial and open-source distribution without triggering viral copyleft obligations:

1. **Strict Subprocess Boundary:**
   - Tools governed by GPL or LGPL (`semgrep`, `trufflehog`, `clamav`) must NEVER be statically or dynamically linked into OpenClone Python modules.
   - All invocations must occur strictly as independent external operating system processes via `subprocess.run` or daemon TCP/UNIX sockets.
2. **Zero In-Tree Vendoring:**
   - Source code from copyleft repositories must never be committed to or vendored into the OpenClone distribution package.
3. **User-Provided Tools:**
   - OpenClone detects whether the user has installed these tools locally; OpenClone does not distribute GPL binaries.
