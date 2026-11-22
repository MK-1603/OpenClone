# OpenClone — Conflict & Decision Register
**Version:** 1.0.0  
**Scope:** Formal record of architectural trade-offs, potential specification contradictions, and resolution decisions.

---

## 1. Conflict & Decision Records

### CDR-001: End-User Cloning vs. Zero-Install Portable Package
- **Issue:** Earlier prompt versions (`v1.0.0`–`v1.4.0`) described OpenClone as a monolithic repository that users clone and run locally. Newer prompts (`v2.0.0`, `v2.1.0`, `v2.2.0`) emphasize a portable, zero-install workflow where end users create applications using only a `PROJECT.md` file without cloning OpenClone.
- **Precedence Hierarchy:** Rule 1 & Rule 2: Explicit product direction + latest canonical user specification.
- **Resolution:**
  - **End Users:** Use the 100% portable `PROJECT.md`-first zero-install workflow. They download or copy the master prompt into ChatGPT or Claude and work inside their own repository.
  - **Maintainers / Contributors:** Clone OpenClone to run tests, validate schemas, or host the optional local SQLite control plane.
- **Status:** Resolved & Documented in `README.md` and `QUICK-START.md`.

---

### CDR-002: Design Skill Authority Conflict
- **Issue:** 11 external UI repositories were referenced (e.g., `taste-skill`, `shadcn/ui`, `design-md-chrome`, `hallmark`, `impeccable`, `typography-skills`). If loaded simultaneously without hierarchy, AI agents receive conflicting art-direction rules (e.g. brutalism vs. glassmorphism vs. Swiss international style).
- **Precedence Hierarchy:** Specific subsystem authority + least privilege.
- **Resolution:** Established strict **Design-Skill Precedence Hierarchy**:
  1. `PROJECT.md` (Explicit user constraints have supreme authority)
  2. Visual Extraction (`design-md-chrome` — extracts brand tokens from existing sites)
  3. Art Direction (`taste-skill` — sets visual theme, enforces anti-slop rules)
  4. Component Primitives (`shadcn/ui` — provides unstyled, accessible UI components)
  5. Typography Standards (`typography-standards` — modular scales and vertical rhythm)
  6. Quality Critique (`hallmark` / `impeccable` — conducts post-build review)
  7. Accessibility Verification (`a11y` — WCAG 2.2 AA audit)
- **Status:** Resolved & Enforced in `src/openclone/skills/engine.py` and `registries/SKILL-REGISTRY.md`.

---

### CDR-003: Dynamic Pentest (Strix) Execution Authorization
- **Issue:** Strix provides autonomous dynamic application security testing (DAST) using LLM agents. Uncontrolled execution against unauthorized targets or production hosts violates safety policies and legal boundaries.
- **Precedence Hierarchy:** Platform safety and security policies override feature convenience.
- **Resolution:**
  - Strix is classified as an **Optional Isolated Tool**.
  - Requires explicit written owner authorization and a strictly bounded target allowlist (`http://localhost`, `127.0.0.1`).
  - Must execute inside an isolated Docker container with zero access to production credentials or external host networks.
- **Status:** Resolved & Documented in `docs/integrations/strix-dynamic-testing.md`.

---

### CDR-004: LLM Router Integration Strategy
- **Issue:** 8 candidate open-source LLM routers were proposed (`freellm`, `omniroute`, `free-llm-router`, etc.). Blindly adopting a third-party proxy can create single-point-of-failure vulnerabilities, credential leaks, or latency overhead.
- **Precedence Hierarchy:** Engineering quality: prove concrete product need before adding dependencies.
- **Resolution:**
  - Evaluated all 8 router candidates in `docs/integrations/llm-router-comparison.md`.
  - OpenClone provides direct, lightweight model provider adapters by default. External routers remain optional documented drop-ins for environments requiring dynamic failover or rate-limit pooling.
- **Status:** Resolved & Documented.

---

### CDR-005: Knowledge Catalogues vs. Code Feature Bloat
- **Issue:** The concept catalogues encompass 232 UI styles, 580 backend topics, and 1,095 AI topics. Attempting to implement every concept as a hardcoded engine in the core repository would produce immense maintenance bloat.
- **Precedence Hierarchy:** Engineering principle: Catalogues are knowledge taxonomies, not a feature backlog.
- **Resolution:**
  - Catalogues are structured as indexed knowledge references in `docs/knowledge/` and `docs/knowledge-catalogues/`.
  - Queryable at runtime through the OpenClone MCP Server tool `get_guidance`.
  - Mapped to product capability classes: `CORE_PRODUCT`, `INTERNAL_ENGINEERING`, `OPTIONAL_INTEGRATION`, `REFERENCE_KNOWLEDGE`.
- **Status:** Resolved & Documented.
