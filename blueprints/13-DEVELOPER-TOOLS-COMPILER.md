# Blueprint 13: Developer Tools, CLI & Compilers

**Project Family:** `developer_tools_and_languages`  
**Primary Project Type:** `cli_developer_tool`, `compiler_toolchain`  
**Maturity Status:** `OPERATIONAL`  
**Complexity Level:** `MEDIUM` to `LARGE`  
**Default Delivery Targets:** `linux`, `windows`, `macos`

---

## 1. Goals & Scope
- Command-line utilities, software development kits (SDKs), compilers, interpreters, AST linters, and developer extension platforms.
- Emphasizes POSIX exit codes, structured JSON/YAML stdout output, error diagnostics with source file highlighting, type stubs, and semantic versioning.

## 2. Classification Rules
- Matched when the project's primary interface is the terminal shell, an importable SDK package, an AST parser/compiler, or an IDE extension.

## 3. Intake Questions & Required Information
1. Tool type: CLI utility, SDK library, compiler/transpiler, or IDE extension.
2. Argument parsing: subcommands, flags, environment variable overrides.
3. Output modes: human-friendly colored terminal vs. machine-readable `--json`.
4. Packaging: PyPI wheel, npm package, Cargo binary, Homebrew formula.

## 4. Domain & Capability Mapping
- **Mandatory Domains:** `01-SPECIFICATION`, `02-ARCHITECTURE`, `10-TESTING-AND-QA`, `13-DEPENDENCY-MANAGEMENT`, `18-DOCUMENTATION`.
- **Mandatory Engines:** `E-001`, `E-002`, `E-010`, `E-013`, `E-018`.

## 5. Specialist Workforce
- `systems-programmer`: Subprocess handling, POSIX signals, and cross-platform compilation.
- `compiler-engineer`: Lexing, AST visitor patterns, and intermediate representations.
- `developer-advocate`: Interactive `--help` documentation and man pages.

## 6. Verification & Delivery Artifacts
- Comprehensive CLI flag matrix tests asserting non-zero exit codes on failure.
- Exported strict type definitions (.d.ts / pyi stubs).
- Performance execution benchmark (CLI startup latency < 100ms).
