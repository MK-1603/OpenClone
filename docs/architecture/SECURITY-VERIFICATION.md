# OPENCLONE — SECURITY & HARNESS VERIFICATION REPORT

## 1. Security Architecture & Controls

OpenClone enforces strict defense-in-depth execution boundaries:

1. **Deny-by-Default Executable Allowlisting:**
   - [workforce.py:592-594](file:///d:/New%20folder/OpenClone/src/openclone/runtime/workforce.py#L592-L594): Only executables declared in project policy (`policy["allowed_executables"]`) can be executed. Unvetted binaries raise `PermissionError`.
2. **Path Confinement & Directory Traversal Protection:**
   - [workforce.py:596-597](file:///d:/New%20folder/OpenClone/src/openclone/runtime/workforce.py#L596-L597): Commands must execute strictly within the project directory. Any path resolving outside raises `PermissionError`.
3. **In-Memory Multi-Pass Secret Redaction:**
   - [workforce.py:79-85](file:///d:/New%20folder/OpenClone/src/openclone/runtime/workforce.py#L79-L85): All stdout, stderr, and task outputs are filtered across regex patterns masking AWS keys, GitHub tokens, OpenAI keys, and generic credential patterns (`[REDACTED]`).
4. **Cross-Platform Process-Tree Termination:**
   - POSIX: `os.killpg(proc.pid, signal.SIGKILL)`
   - Windows: Windows Job Objects via `ctypes.windll.kernel32.CreateJobObjectW` and `AssignProcessToJobObject` with fallback to `taskkill /F /T /PID`.
5. **Tamper-Evident Audit Ledger:**
   - Every state transition, approval, execution, and gate check is cryptographically hashed with SHA-256 into the append-only SQLite ledger (`verify_chain()` validated).
6. **Untrusted Codebase Policy in Reverse Engineering:**
   - Inspected repository files, README files, comments, and scripts are treated strictly as untrusted data. Zero evaluation or automated execution of target code occurs during Level 1 static analysis.
