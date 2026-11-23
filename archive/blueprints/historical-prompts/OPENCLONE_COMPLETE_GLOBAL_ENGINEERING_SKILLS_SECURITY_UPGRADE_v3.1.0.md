# OPENCLONE — COMPLETE GLOBAL ENGINEERING, SKILLS, DESIGN, SECURITY & README UPGRADE
**Unified repository-wide implementation specification**  
**Target:** OpenClone Global Upgrade v3.0.0  
**Execution environment:** Antigravity or another verified coding agent, with the existing OpenClone repository open  
**Primary outcome:** A polished, usable, globally documented OpenClone workflow in which every relevant skill is discoverable, selected, loaded, applied, and verified—not merely present in the repository.

---

# 0. THE MISSION

Perform one coordinated upgrade of the existing OpenClone repository. Combine and reconcile:

1. The PROJECT.md-first, portable project-generation workflow.
2. The global README and first-time user onboarding correction.
3. The 27-repository design, security, and engineering collection supplied by the user.
4. The earlier LLM router collection and multi-model / multi-IDE direction.
5. The 19-point SaaS security checklist.
6. The UI design catalogues: 86 visual styles and the expanded 232-style/pattern/approach taxonomy.
7. The backend and system-design catalogue: 580 topics.
8. The AI catalogue: 1,095 numbered entries across foundations, ML, deep learning, LLMs, prompting, context, RAG, agents, automation, protocols, multimodal systems, production, safety, and product engineering.
9. Motion, animation, interaction, and accessibility guidance.
10. Skill discovery, skill activation, skill application, and skill-effectiveness verification.
11. Anti-AI-slop governance, quality gates, security tool governance, continuity, traceability, and evidence-based completion.

This is not a request to paste every catalogue entry into every prompt. It is a request to build a **coherent, searchable, modular engineering knowledge and skill system** that applies only the relevant knowledge to each project and proves that the selected skills influenced the output.

## The corrected end-user product model

**PROJECT.md → ChatGPT / Claude → Portable Project Package → User's Own AI Coding IDE → Verified Project**

An end user must NOT need to clone, install, run, or add OpenClone as a dependency merely to use the project-generation methodology.

- ChatGPT/Claude analyze the supplied `PROJECT.md`, clarify material gaps, and produce a portable project package.
- The user opens their own target repository in an AI coding IDE.
- The IDE agent inspects the real repository, reads project instructions, selects relevant skills, implements, tests, and verifies.
- OpenClone's own repository is cloned only by maintainers/contributors who want to develop OpenClone itself.

The root README must teach this usage model first. Maintainer setup must be clearly separated.

---

# 1. NON-NEGOTIABLE PRINCIPLES

1. **Audit before editing:** inspect the real repository and current Git state.
2. **No clone-first end-user workflow:** never present cloning OpenClone as a prerequisite.
3. **No false claims:** do not claim a skill, integration, provider, adapter, command, or feature works until verified.
4. **Skill presence is not skill application:** a skill file existing does not prove it was discovered, selected, loaded, followed, or validated.
5. **Relevant skills only:** do not load every skill or catalogue for every project.
6. **No AI slope:** no unnecessary dependencies, agents, services, abstractions, features, or prompt bloat.
7. **Preserve upstream licenses and attribution:** never blindly copy or merge third-party repositories.
8. **Human approval:** require approval for material product, architecture, security, data, cost, destructive, or live-target decisions.
9. **Security by design:** enforce server-side authorization, tenant isolation, validation, and least privilege.
10. **Evidence over claims:** tests, scans, skill application, and completion must be evidenced.
11. **Portable outputs:** generated project packages must work independently of OpenClone source code.
12. **Maintainable knowledge:** catalogues are structured and versioned, with provenance and review dates.

---

# 2. PHASE ZERO — REPOSITORY BASELINE AND FORENSIC AUDIT

Before changing anything, inspect:

```bash
git status --short
git branch --show-current
git log -5 --oneline
```

Inspect:
- root README and every README;
- all agent instruction files (AGENTS.md, CLAUDE.md, GEMINI.md, IDE-specific files, and equivalents);
- skill folders and every skill manifest/frontmatter;
- prompts, rules, hooks, scripts, commands, templates, registries, and routing logic;
- UI/UX, frontend, animation, typography, design-system, backend, system-design, AI, and security knowledge;
- IDE adapters and model/provider integrations;
- external router and security-tool integrations;
- project generation and export;
- tests, fixtures, CI, package scripts, docs, examples, and release configuration.

Create an **audit matrix** before implementation:

| Area | Exists? | Actual entry point | Current behavior | Defect/gap | Proposed change | Verification |
|---|---|---|---|---|---|---|

Do not assume a capability exists because an old README, planning document, or memory says it exists. Verify the implementation.

Preserve all pre-existing user changes. Do not reset, clean, or overwrite unrelated files.

---

# 3. CRITICAL WORKSTREAM — WHY SKILLS ARE NOT BEING APPLIED

This is a root-cause investigation, not a cosmetic skills-folder rewrite.

## 3.1 Diagnose the entire skill lifecycle

For every skill, trace this lifecycle:

```text
Skill file exists
      |
      v
Manifest/frontmatter parses
      |
      v
Skill is indexed/discoverable
      |
      v
Task is classified
      |
      v
Skill is selected as relevant
      |
      v
Skill instructions are loaded into active context
      |
      v
Agent follows required workflow
      |
      v
Output is checked against skill requirements
      |
      v
Evidence records skill application
```

A failure at any step means the skill may not actually be applied.

## 3.2 Investigate these failure classes

### A. Discovery failures
- Skills stored in directories the target IDE does not scan.
- Wrong directory nesting or naming.
- Missing, malformed, or incompatible skill metadata.
- Incorrect frontmatter keys or unsupported manifest schema.
- Skill files excluded by `.gitignore`, packaging, or export.
- Broken symlinks or paths that work only on one operating system.
- Case-sensitive path errors.
- Skills present in the source repo but absent from the generated project package.

### B. Trigger and selection failures
- Skill descriptions too vague to trigger.
- Descriptions do not name task types, technologies, artifacts, or expected outcomes.
- Duplicate or competing skills.
- No task classifier or no skill-selection stage.
- Overly broad selection that causes context overload.
- Relevant skill is ranked below irrelevant skills.
- Skills depend on hidden chat context instead of explicit task signals.
- No fallback when no skill matches.

### C. Loading and context failures
- Skill metadata is discovered but the body is never loaded.
- Only part of a skill is loaded due to token limits.
- Referenced files are not included.
- Relative links resolve incorrectly.
- Skill instructions conflict with global instructions.
- Instruction precedence is undefined.
- A skill is listed in a prompt but not actually provided to the agent.
- IDE adapters use different skill-loading conventions.

### D. Application failures
- Agent acknowledges a skill but ignores its required steps.
- Skill is treated as optional inspiration instead of an executable workflow.
- No explicit deliverables or acceptance criteria.
- No enforcement of design/security/engineering rules.
- Generic coding behavior overrides specialized skill behavior.
- Skills are not invoked at the point in the workflow where they matter.
- No quality check compares the result with the skill's standards.

### E. Verification failures
- No tests that prove discovery, selection, loading, and application.
- No trace from task → selected skill → applied instruction → output evidence.
- No telemetry or diagnostic explanation for skipped skills.
- README claims skills are automatic without proof.
- No regression tests for IDE-specific skill packaging.

## 3.3 Build a skill registry

Create or normalize a machine-readable registry, using the repository's current architecture and formats where possible. Each skill record should contain:

- stable `skill_id`;
- display name;
- category and subcategory;
- purpose;
- task triggers and negative triggers;
- supported technologies and artifacts;
- prerequisites;
- input expectations;
- required workflow steps;
- required outputs;
- constraints and anti-patterns;
- verification checklist;
- source/provenance;
- license;
- version;
- supported IDE/agent environments;
- compatibility status;
- enabled/experimental/deprecated status;
- related and conflicting skills.

Do not invent a new runtime or database if a simple registry in the existing format is sufficient.

## 3.4 Define skill selection

Implement a deterministic and explainable selection process:

1. Classify the user's task and project domain.
2. Extract technologies, artifacts, risks, and requested outcomes.
3. Match positive and negative triggers.
4. Apply prerequisite and compatibility checks.
5. Rank candidate skills by relevance and task criticality.
6. Select a small, bounded set.
7. Resolve conflicts using explicit precedence.
8. Load the full instructions and necessary referenced assets.
9. Explain selected and skipped skills.
10. Validate the result against selected skill requirements.

The selection output should identify:
- selected skills;
- why each was selected;
- which instructions/assets were loaded;
- when they are to be applied;
- skipped candidates and reasons;
- conflicts and resolution;
- verification evidence.

Do not simply inject the entire skills catalogue into every prompt.

## 3.5 Skill precedence and conflict resolution

Define one clear precedence policy, consistent with actual IDE behavior:

1. System/platform safety constraints.
2. Explicit user requirements and approvals.
3. Target repository's governing instructions.
4. OpenClone global engineering and anti-slop policies.
5. Selected domain skills.
6. Optional recommendations and examples.

If actual IDE instruction precedence differs, document the difference in its adapter and do not claim a universal precedence rule.

Resolve conflicting skills by:
- explicit user requirement;
- repository standards;
- task-specific applicability;
- safety/security requirements;
- more specific verified instruction;
- documented tie-breaker.

Do not merge incompatible styles or architectures automatically. Surface material conflicts.

## 3.6 Skill application evidence

For each meaningful task, maintain a compact `SKILL_APPLICATION_REPORT.md` or equivalent execution record containing:

| Field | Meaning |
|---|---|
| Task ID | Current task |
| Skill ID | Selected skill |
| Selection reason | Trigger or requirement |
| Loaded source | Actual file/path/version |
| Required actions | Steps the skill required |
| Applied actions | What the agent actually did |
| Evidence | Files, diffs, tests, screenshots, reports |
| Status | Applied / Partially applied / Skipped / Blocked |
| Reason | Explanation for exceptions |

Do not claim that a skill was applied merely because it was selected or mentioned.

## 3.7 Skill activation tests

Build automated tests for:
- valid skill manifest parsing;
- invalid metadata detection;
- skill discovery from supported directories;
- duplicate IDs and naming collisions;
- trigger matching;
- positive and negative trigger behavior;
- prerequisite enforcement;
- ranking and selection;
- context loading and referenced-file resolution;
- conflict resolution;
- platform-specific packaging;
- generated package inclusion;
- actual application report generation;
- skipped-skill reason reporting.

Create realistic task fixtures:
- build a SaaS dashboard;
- design a premium landing page;
- implement a database-backed API;
- secure a multi-tenant SaaS;
- implement AI RAG and agents;
- add motion to a responsive UI;
- refactor a legacy repository.

For each fixture, assert which skills should be selected and which should not. Add an application-quality check that verifies expected outputs, not merely that a skill name appears in a prompt.

## 3.8 User-facing skill diagnostics

Provide a simple way to answer:
- Which skills were discovered?
- Which skills were selected for this task?
- Why were they selected?
- Were their full instructions loaded?
- Which files/assets were referenced?
- Which required actions were completed?
- Which skills were skipped and why?
- What evidence proves application?

If the existing product has no UI for this, generate a readable Markdown report and CLI/diagnostic output only if the existing architecture supports it. Do not build a dashboard just for this.

---

# 4. GLOBAL KNOWLEDGE CATALOGUE — NORMALIZE, INDEX, RETRIEVE

The user supplied several large catalogues. Preserve them as source material, validate them, normalize duplicates, and make them retrievable by domain. Do not flatten everything into one giant prompt.

## 4.1 UI design knowledge

Preserve both:
- the original **86 UI visual styles and aesthetics** list;
- the expanded **232 UI styles, patterns, and approaches** catalogue.

The expanded catalogue covers:
- classic and foundational styles;
- depth, surfaces, and dimensional styles;
- contemporary aesthetics;
- retro, futuristic, and experimental styles;
- color and visual treatment;
- layout and composition;
- typography-driven styles;
- interaction and motion;
- product/application interface patterns;
- AI-native and emerging interfaces;
- device and spatial interfaces;
- accessibility and inclusive approaches.

Important taxonomy rule: the 232 entries are not all mutually exclusive visual styles. They mix aesthetics, layouts, interaction patterns, application types, technologies, and accessibility approaches. Preserve those distinctions.

For each design entry, provide structured metadata where feasible:
- concept name and category;
- what it means;
- visual characteristics;
- suitable product contexts;
- component/layout implications;
- color, typography, spacing, and surface considerations;
- accessibility and responsive risks;
- motion implications;
- anti-patterns;
- implementation references/examples if verified.

Do not force every design style into a product. Select an appropriate visual direction based on brand, audience, product purpose, accessibility, and constraints.

## 4.2 Backend and system-design knowledge

Preserve the user's 580-topic backend/system-design catalogue. Normalize into categories including:
- architecture strategies;
- load balancing;
- rate limiting;
- resilience and circuit breakers;
- queues and messaging;
- distributed systems and consistency;
- database architecture and scaling;
- caching;
- API architecture and communication;
- authentication and authorization;
- security engineering;
- performance;
- scalability;
- background jobs and workflow processing;
- observability;
- deployment and infrastructure;
- event-driven systems;
- multi-tenant SaaS;
- advanced distributed patterns;
- capacity planning;
- testing and reliability;
- networking;
- AI backend infrastructure;
- advanced architecture and platform engineering.

The catalogue is a learning/knowledge taxonomy, not a requirement that every project use every pattern. Use architecture decision criteria and scale-stage awareness.

## 4.3 AI knowledge catalogue

Preserve the user's 1,095-entry AI catalogue and its learning sequence. Normalize into:
- AI foundations and mathematics;
- machine learning and algorithms;
- ML engineering;
- deep learning and architectures;
- generative AI and LLM fundamentals;
- training, fine-tuning, inference, and optimization;
- prompt engineering and context engineering;
- RAG, embeddings, vector search, and knowledge graphs;
- agents, planning, orchestration, memory, and multi-agent systems;
- automation and integrations;
- MCP, A2A, tool schemas, auth, and sandboxing;
- multimodal AI: vision, audio, speech, video, 3D, spatial;
- application domains;
- development lifecycle and MLOps/LLMOps;
- evaluation, safety, security, and governance;
- AI product engineering and SaaS;
- research, emerging technologies, and ecosystem tools;
- advanced AI system design.

Preserve the original note that category totals are thematic and may overlap; do not claim 1,095 independent algorithms.

## 4.4 Motion and animation knowledge

The supplied UI catalogue explicitly includes motion and interaction topics such as microinteractions, motion-driven UI, parallax, scrollytelling, scroll-driven behavior, physics-based interaction, gestures, drag-and-drop, hover/cursor-driven behavior, magnetic UI, kinetic UI, morphing, view transitions, progressive blur, animated UI, interactive 3D, and spatial interaction.

Audit whether OpenClone already has a separate animation/motion skill or catalogue. If missing, create a structured motion-design module covering, where relevant:
- transition design;
- microinteractions;
- state-change feedback;
- entrance/exit choreography;
- hover, focus, press, drag, and gesture motion;
- scroll-linked animation;
- page and view transitions;
- loading and progress animation;
- skeleton and shimmer states;
- spring/physics motion;
- SVG/canvas/3D motion;
- reduced-motion alternatives;
- performance budgets and compositor-friendly properties;
- interruption, cancellation, and accessibility;
- timing, easing, duration, sequencing, and consistency.

Do not add motion for decoration alone. Motion must communicate state, hierarchy, continuity, or feedback. Respect `prefers-reduced-motion` and user settings.

## 4.5 Taxonomy quality

- Preserve source names and IDs where practical.
- Detect duplicate and near-duplicate concepts.
- Keep aliases and cross-references instead of deleting useful terminology.
- Distinguish a design aesthetic from a layout pattern, technology, algorithm, protocol, and practice.
- Add source provenance and last-reviewed metadata.
- Avoid claiming a catalogue is an official standard.
- Provide search/tags and domain retrieval in the existing knowledge system.
- Keep learning catalogues separate from project execution rules.

---

# 5. THE 27 GITHUB REPOSITORIES — INTAKE AND GOVERNED INTEGRATION

Do not blindly clone and merge all 27 repositories into OpenClone core. Treat each as an external candidate to inspect, evaluate, pin, and integrate through a thin adapter, curated knowledge extraction, or optional tool route.

For every candidate:
1. Verify the repository exists and current canonical URL.
2. Inspect owner, purpose, maintenance, release activity, open issues, and security posture.
3. Read LICENSE and attribution requirements.
4. Review README, docs, install scripts, dependencies, permissions, and network behavior.
5. Determine whether it is a skill, library, app, CLI, dataset, or reference.
6. Evaluate overlap with existing OpenClone capabilities.
7. Decide: `ADOPT`, `ADAPT`, `REFERENCE`, `OPTIONAL_ADAPTER`, `DEFER`, or `REJECT`.
8. Record rationale and version/commit.
9. Add only the minimum necessary integration.
10. Add tests and docs proving it works.
11. Keep upstream provenance and license notices.
12. Define update and removal procedure.

## 5.1 UI / UX / Frontend Design — 11 repositories

1. Design MD Chrome — https://github.com/bergside/design-md-chrome  
   Purpose: extract website design systems into Markdown.
2. shadcn/ui — https://github.com/shadcn-ui/ui  
   Purpose: accessible and reusable React UI components.
3. Interface Design — https://github.com/Dammyjay93/interface-design  
   Purpose: AI-assisted interface design workflows.
4. Unstop UI — https://github.com/Mohit-Raj-Singh/Unstop-UI  
   Purpose: UI implementation and design inspiration.
5. Anthropic Frontend Design — https://github.com/anthropics/skills/tree/main/skills/frontend-design  
   Purpose: frontend design skill for AI coding workflows.
6. Taste Skill — https://github.com/Leonxlnx/taste-skill  
   Purpose: AI-assisted frontend art direction and design quality.
7. Hallmark — https://github.com/Nutlope/hallmark  
   Purpose: anti-AI-slop design skill for Claude Code, Cursor, and Codex.
8. UI UX Pro Max — https://github.com/nextlevelbuilder/ui-ux-pro-max-skill  
   Purpose: UI/UX design intelligence and design-system guidance.
9. Frontend Design Skills — https://github.com/flitzrrr/frontend-design-skills  
   Purpose: curated frontend design skills for multiple AI coding tools.
10. Impeccable — https://github.com/pbakaus/impeccable  
    Purpose: design vocabulary and workflows to improve, critique, and audit AI-generated interfaces.
11. Typography Skills — https://github.com/jpoindexter/typography-skills  
    Purpose: typography standards and coding-agent skills.

### Required design integration behavior

- Compare overlapping skills before adoption.
- Preserve the existing Taste Skill and current anti-AI-slop governance unless a verified improvement is approved.
- Do not let multiple design skills fight over global visual direction.
- Establish a design-skill selection order: product brief/brand constraints → design-system extraction (if reference exists) → art direction → UI architecture/components → typography → critique/audit → implementation verification.
- Treat shadcn/ui as a component source/tooling ecosystem, not a visual design style.
- Treat design inspiration repositories as references, not production dependencies.
- Generate a project-specific design brief and tokens only when required.
- Enforce no generic AI gradients, default purple/blue glow, random glass panels, emoji icons, gratuitous cards, or inconsistent spacing unless explicitly requested by the product brief.
- Do not impose one global aesthetic on every project.

## 5.2 Security Engineering — 12 repositories

12. Strix — https://github.com/usestrix/strix  
    Purpose: autonomous AI-powered penetration testing.
13. Nuclei — https://github.com/projectdiscovery/nuclei  
    Purpose: template-based vulnerability scanning.
14. OpenAI Codex Security — https://github.com/openai/codex-security  
    Purpose: AI-assisted vulnerability discovery and remediation.
15. Cloudflare Security Audit Skill — https://github.com/cloudflare/security-audit-skill  
    Purpose: security auditing codebases using AI agents.
16. Semgrep — https://github.com/semgrep/semgrep  
    Purpose: static analysis and vulnerability detection.
17. Claude Code Security Review — https://github.com/anthropics/claude-code-security-review  
    Purpose: AI-assisted security reviews for code changes.
18. Trivy — https://github.com/aquasecurity/trivy  
    Purpose: scan containers, dependencies, and cloud configurations.
19. TruffleHog — https://github.com/trufflesecurity/trufflehog  
    Purpose: detect exposed credentials, API keys, and secrets.
20. NVIDIA SkillSpector — https://github.com/NVIDIA/skillspector  
    Purpose: inspect AI agent skills for malicious behavior.
21. ClamAV — https://github.com/Cisco-Talos/clamav  
    Purpose: open-source antivirus and malware detection.
22. BLA — https://github.com/qybaihe/bla  
    Purpose: research into LLM-based security agents.
23. Microsoft PyRIT — https://github.com/microsoft/pyrit  
    Purpose: red-team generative AI systems and applications.

### Required security integration behavior

- Use a risk-based security profile.
- Integrate through optional adapters or documented external commands.
- Do not vendor complete upstream repositories into core.
- Do not run arbitrary scripts without inspection.
- Do not require all 12 tools for every project.
- Keep Strix dynamic testing optional and disabled by default.
- Require explicit authorization, exact target allowlists, permitted environment, test window, accounts, request/rate/budget limits, and network restrictions before live testing.
- Never test unauthorized third-party or production targets.
- Treat AI security tools as decision support; validate findings and remediation.
- Preserve finding evidence and map findings to remediation and retest.

## 5.3 Software / Development Engineering — 4 repositories

24. Cloudera Hue — https://github.com/cloudera/hue  
    Purpose: SQL editor, database exploration, and data warehouse interface.
25. Superpowers — https://github.com/obra/superpowers  
    Purpose: structured software development workflows for coding agents.
26. shadcn Improve — https://github.com/shadcn/improve  
    Purpose: AI-assisted codebase analysis and implementation planning.
27. Microsoft TokenEconomizer — https://github.com/microsoft/TokenEconomizer  
    Purpose: LLM token usage optimization and efficiency.

### Required engineering integration behavior

- Superpowers: compare with current planning, debugging, testing, and execution workflows; adopt only non-conflicting improvements.
- shadcn Improve: assess as a codebase analysis/planning reference; avoid duplicate planner layers.
- TokenEconomizer: evaluate measurable token/context savings without degrading correctness or removing necessary instructions.
- Cloudera Hue: treat as a substantial database/query application reference, not a library or default OpenClone dependency. Extract relevant UX/SQL workflow ideas only if useful.

---

# 6. PREVIOUSLY IDENTIFIED LLM ROUTER CANDIDATES

Audit these earlier candidates as a separate group. Do not merge them into the 27 count.

1. Devansh-365/freellm — https://github.com/Devansh-365/freellm
2. kaiser-data/free-llm-proxy-router — https://github.com/kaiser-data/free-llm-proxy-router
3. nabinkhadka/free-llm-api — https://github.com/nabinkhadka/free-llm-api
4. YeomanYe/free-llm-router — https://github.com/YeomanYe/free-llm-router
5. alienz-dev/llm-router — https://github.com/alienz-dev/llm-router
6. MajidAsghariTabrizi/free-best-router — https://github.com/MajidAsghariTabrizi/free-best-router
7. tashfeenahmed/freellmapi — https://github.com/tashfeenahmed/freellmapi
8. Gmagl/omniroute — https://github.com/Gmagl/omniroute

Verify each candidate's current repository identity and status. Compare:
- provider support and authentication;
- model discovery;
- routing policies;
- fallback behavior;
- streaming;
- rate limits and quotas;
- usage/cost tracking;
- privacy and data handling;
- logging and observability;
- deployment and operational complexity;
- license and maintenance.

Recommend at most one primary router unless there is a concrete need for more. Do not adopt a “free” router without verifying its terms, reliability, privacy, and actual upstream provider limitations. Never promise free unlimited model access.

---

# 7. MULTI-MODEL, MULTI-PROVIDER, MULTI-IDE GOVERNANCE

Keep these distinct:

## Planning assistants
- ChatGPT
- Claude
- Gemini
- Grok
- Qwen
- other assistants only when the prompt workflow has been tested.

## Coding IDEs / agents
- Antigravity
- Claude Code
- Codex
- Qwen Code
- Kiro
- Kilo Code
- Cursor
- VS Code agents/extensions
- Zed
- Cline
- Roo Code
- OpenCode
- Aider
- GitHub Copilot
- JetBrains AI
- Windsurf
- others only after current compatibility verification.

## Model providers / runtimes
- OpenAI
- Anthropic
- Google Gemini
- xAI
- Qwen
- DeepSeek
- Mistral
- Cohere
- compatible gateways
- Ollama
- LM Studio
- vLLM
- llama.cpp
- others only where implemented and verified.

Do not conflate an IDE adapter with a model-provider adapter. A model provider API does not automatically mean an IDE integration exists.

For each adapter document:
- verified version/date;
- capabilities;
- authentication method;
- supported skill format and locations;
- instruction precedence;
- context and file access behavior;
- limitations;
- test status.

Keep portable canonical project files as the source of truth. Generate thin IDE-specific wrappers only when necessary.

---

# 8. GLOBAL SAAS SECURITY BASELINE — 19 CHECKS

Implement the user's 19-point checklist as a **security verification baseline**, not as a claim that checking boxes alone makes an app secure.

For each applicable control, identify the threat, implementation location, verification method, evidence, and status.

1. **Row Level Security (RLS):** enforce tenant/user data isolation in the database where supported; test cross-tenant access.
2. **Authentication on every API route:** protect every private endpoint server-side; explicitly document public routes.
3. **Never trust the frontend:** enforce validation, authorization, ownership, and business rules on the server.
4. **Rate limiting:** apply endpoint- and identity-aware limits, including abuse-sensitive actions.
5. **Sanitize/validate user input:** use schema validation and context-appropriate output encoding; do not rely on one generic sanitizer.
6. **Parameterized queries:** prevent SQL injection; prohibit unsafe string-built SQL unless safely parameterized.
7. **Lock down CORS:** explicit allowed origins, methods, and headers; do not use permissive wildcard credentials.
8. **HTTPS everywhere:** TLS in transit, secure cookies, and correct proxy/TLS configuration.
9. **Stop IDOR/BOLA:** verify object-level ownership/authorization on every resource operation.
10. **Debug mode off in production:** disable debug endpoints, verbose errors, stack traces, and unsafe diagnostics.
11. **CAPTCHA on public forms:** use risk-based bot protection for exposed forms; avoid adding CAPTCHA to every private action without need.
12. **Log admin actions:** tamper-resistant audit events for sensitive administrative actions; redact secrets and sensitive payloads.
13. **Private storage buckets:** default private, scoped access, short-lived signed URLs, and authorization checks.
14. **Hide admin pages properly:** UI hiding is not authorization; enforce role/permission checks server-side and at data access.
15. **Update vulnerable packages:** dependency scanning, patch policy, lockfile integrity, and exception tracking.
16. **Check file upload types:** validate content/signature, size, extension, storage path, scanning, and safe processing.
17. **Claude security review:** run an AI-assisted review where available, but treat it as supplementary and validate findings.
18. **Security headers:** configure CSP, HSTS, frame protections, content type, referrer, and permissions policies as appropriate.
19. **Verify webhook signatures:** verify signatures, timestamps, replay protection, and idempotency before processing.

## Additional controls required for mature SaaS

Do not stop at the 19 checks. Evaluate:
- CSRF;
- XSS;
- SSRF;
- broken function-level access control;
- privilege escalation;
- session fixation and rotation;
- MFA/passkeys for privileged users;
- password reset abuse;
- secret/key management and rotation;
- encryption at rest;
- tenant context propagation;
- tenant-aware cache keys;
- audit log retention;
- backup/restore and disaster recovery;
- webhook replay and idempotency;
- security incident response;
- privacy, retention, export, and deletion;
- supply-chain provenance;
- CI/CD permissions and secret exposure;
- AI prompt injection, data exfiltration, unsafe tool calls, and model output validation where AI is used.

Never mark a control as passed without evidence. Use statuses `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`, `NOT_APPLICABLE`, and `ACCEPTED_RISK`.

---

# 9. PREMIUM UI/UX, DESIGN SYSTEM, AND FRONTEND QUALITY

The goal is high-quality, coherent, product-specific design—not maximum visual effects.

## 9.1 Design workflow

For every UI project, the selected design skills should execute in this order:

1. Understand product, users, brand, platform, and task.
2. Inspect existing UI and design references.
3. Select a design direction with rationale.
4. Define design tokens: color, typography, spacing, radii, elevation, borders, motion, breakpoints.
5. Define layout and information hierarchy.
6. Define reusable components and states.
7. Implement responsive behavior.
8. Add purposeful interaction and motion.
9. Run accessibility and visual QA.
10. Compare final implementation against approved design intent.

## 9.2 Design-system requirements

Where relevant, generate:
- semantic color tokens;
- typography scale and font roles;
- spacing scale;
- layout/container rules;
- grid and breakpoints;
- border/radius/elevation tokens;
- focus, hover, active, disabled, loading, error, empty, and success states;
- component variants;
- icon policy;
- motion tokens and reduced-motion behavior;
- accessibility contrast rules;
- responsive and density rules.

Do not impose one palette or one style globally. Respect the project's brand and existing design system.

## 9.3 Frontend implementation quality

Verify:
- semantic HTML;
- reusable but not over-abstracted components;
- keyboard navigation;
- screen-reader labels;
- focus management;
- responsive mobile/tablet/desktop layouts;
- appropriate touch targets;
- form validation and error recovery;
- loading, empty, offline, and retry states;
- image optimization;
- layout shift and performance;
- route-level error handling;
- accessible dialogs, menus, tabs, and popovers;
- visual consistency.

## 9.4 Motion quality

For every animation:
- state the purpose;
- define trigger and end state;
- choose duration/easing consistently;
- avoid blocking interaction;
- support interruption and reduced motion;
- avoid layout thrashing and unnecessary re-renders;
- use performant properties where practical;
- verify keyboard and touch equivalents;
- avoid motion that harms comprehension or accessibility.

---

# 10. BACKEND, SYSTEM DESIGN, AND PRODUCTION ENGINEERING

Use the 580-topic catalogue as a knowledge source, not a mandatory architecture checklist.

For each project, assess the actual workload:
- expected users and tenant count;
- traffic and request rates;
- concurrency;
- read/write patterns;
- data size and growth;
- latency and availability targets;
- failure modes;
- budget and operational capacity.

Then select only justified patterns for:
- architecture;
- API design;
- database and indexing;
- tenant isolation;
- caching;
- queues/background jobs;
- rate limiting;
- circuit breakers/retries/timeouts;
- load balancing and scaling;
- observability;
- CI/CD and deployment;
- backup/restore;
- resilience and disaster recovery.

Require a reason for introducing microservices, distributed queues, extra databases, caches, service meshes, or complex orchestration. A modular monolith may be more appropriate for many early-stage products.

## Backend implementation acceptance

- authorization enforced server-side;
- tenant isolation verified;
- schema constraints and migrations reviewed;
- transactions/idempotency used where required;
- API contracts and error semantics documented;
- timeouts/retries bounded;
- secrets managed outside source;
- structured logs redact sensitive data;
- health checks and monitoring fit deployment needs;
- backup/restore and rollback considered;
- performance assumptions measured or labeled unverified.

---

# 11. AI ENGINEERING, AGENTS, AND TOKEN EFFICIENCY

Use the 1,095-topic catalogue selectively.

For AI-enabled projects, assess:
- provider/model choice and capability fit;
- provider abstraction only if multiple providers are required;
- structured outputs and validation;
- prompt and context versioning;
- tool schemas and permissions;
- RAG quality and retrieval evaluation;
- memory isolation and retention;
- agent state and recovery;
- human approval for risky actions;
- prompt injection and tool abuse;
- token budgets and cost controls;
- rate limits, retries, fallbacks, and circuit breakers;
- observability and evaluation;
- data privacy and provider retention policies.

## Token/context optimization

Apply:
- task-relevant skill retrieval;
- progressive disclosure;
- compact canonical instructions;
- deduplicated context;
- stable references rather than repeated full catalogues;
- prompt caching where supported and useful;
- context budgets;
- concise handoffs;
- model selection by task complexity.

Never remove necessary security, architecture, or acceptance instructions solely to reduce tokens. Measure savings and output quality.

---

# 12. ANTI-AI-SLOP AND DESIGN GOVERNANCE

Preserve and improve existing Taste Skill and anti-AI-slop governance.

Enforce:
- no generic default landing-page structure without product rationale;
- no random gradient/glow/glass decoration;
- no arbitrary card grids;
- no inconsistent spacing or typography;
- no meaningless icons or emoji-as-interface-icons;
- no fake charts, placeholder data, or fake functionality presented as real;
- no decorative animation without purpose;
- no overbuilt abstractions or speculative features;
- no duplicated dependencies;
- no unrequested architecture changes.

The agent must:
1. inspect the existing product and design system;
2. identify the product's actual visual needs;
3. choose a direction;
4. implement with consistency;
5. critique its own result against the selected skill checklist;
6. fix visible defects;
7. provide evidence of final QA.

Anti-slop rules must be actionable and testable where possible. Avoid vague rules such as “make it beautiful.”

---

# 13. PROJECT.md-FIRST PORTABLE BUILD WORKFLOW

## 13.1 User workflow

1. User prepares or supplies `PROJECT.md`.
2. User opens ChatGPT or Claude.
3. User provides the OpenClone Project Intelligence master prompt and `PROJECT.md`.
4. Assistant analyzes requirements, business rules, UX, architecture, AI, security, cost, and operations as relevant.
5. Assistant asks focused questions for material blockers.
6. User approves key decisions.
7. Assistant generates a portable package.
8. User opens their own target repository in their preferred AI coding IDE.
9. IDE agent reads the package and inspects the actual repository.
10. Agent selects and applies relevant skills.
11. Agent implements in verified vertical slices.
12. Agent updates traceability, tests, progress, and handoff.
13. Agent performs an independent completion audit.

## 13.2 Conditional portable package

Generate only applicable files:

```text
PROJECT_PACKAGE/
├── PROJECT.md
├── BUILD_PROMPT.md
├── AGENT_INSTRUCTIONS.md
├── IMPLEMENTATION_PLAN.md
├── ACCEPTANCE_MATRIX.md
├── SKILL_SELECTION_REPORT.md
├── SKILL_APPLICATION_REPORT.md
├── ARCHITECTURE.md              # when useful
├── API_SPECIFICATION.md         # if APIs exist
├── SECURITY_PLAN.md             # when applicable
├── DATA_LIFECYCLE.md            # if persistent/sensitive data exists
├── DECISIONS.md                 # when decisions need recording
├── COST_ESTIMATE.md             # when meaningful costs exist
├── PROGRESS.md                  # multi-step projects
├── HANDOFF.md                   # multi-session projects
├── CHANGELOG.md                 # once implementation begins
└── IDE_ADAPTER.md               # only when needed
```

The generated package must not require OpenClone source code or a running OpenClone service.

## 13.3 Requirement traceability

Every approved requirement should map to:
`Requirement → Design/Decision → Task → Code Location → Test → Evidence → Status`

Do not fabricate code paths or test evidence before the IDE has inspected and implemented the target repository.

## 13.4 Change impact

A material change must identify affected requirements, architecture, data, APIs, tasks, skills, security controls, tests, and docs. Obtain approval for changes to scope, behavior, data, security, architecture, or material cost.

## 13.5 Continuity

`PROGRESS.md` tracks completed/in-progress/pending/blocked work.

`HANDOFF.md` records verified state, Git status, changed files, tests, blockers, decisions, approvals, and next actions.

A new session must inspect the actual repository and Git state before trusting the handoff.

---

# 14. GLOBAL README — REWRITE THE USER EXPERIENCE

The root `README.md` is the public front door. Rewrite it to teach **how to use OpenClone**, not primarily how to clone its source.

## Required opening message

Use a clear positioning statement, verified against actual capability:

> OpenClone is a portable AI-assisted project engineering workflow that helps turn a `PROJECT.md` into an implementation-ready project package for your preferred AI coding IDE. Use ChatGPT or Claude to clarify and plan the project, then give the generated instructions to your IDE agent to build and verify your own repository.

## Required README sections

1. Project name and concise description.
2. Value proposition and primary CTA: **Start with PROJECT.md**.
3. What OpenClone is.
4. How it works diagram.
5. Do I need to clone OpenClone? — **No, not for the primary user workflow.**
6. Quick Start in beginner-friendly steps.
7. What you need.
8. ChatGPT/Claude workflow.
9. Portable package contents.
10. Choosing a coding IDE.
11. Skill selection and application diagnostics.
12. UI/UX, backend, AI, and security knowledge.
13. 27 external repository collection and integration status, preferably in dedicated docs.
14. 19-point SaaS security baseline and additional controls.
15. Motion, accessibility, and quality.
16. Progress and session handoff.
17. Example walkthrough.
18. Documentation index.
19. Verified integrations and compatibility status.
20. Limitations and user responsibilities.
21. Maintainer/contributor setup (clearly separated).
22. License and acknowledgements.

## Mandatory no-clone wording

> **You do not need to clone or install the OpenClone repository to use the PROJECT.md-first workflow.** Provide your `PROJECT.md` to ChatGPT or Claude with the OpenClone master prompt, review the generated portable project package, and use it inside the AI coding IDE where your own project repository lives. Cloning OpenClone is only for people who want to inspect, contribute to, or develop OpenClone itself.

Do not put clone/install commands in the end-user Quick Start. Put verified maintainer setup at the bottom or in `CONTRIBUTING.md`.

## Quick Start

1. Prepare `PROJECT.md`.
2. Open ChatGPT or Claude.
3. Provide the canonical OpenClone master prompt and project file.
4. Answer material clarification questions and approve decisions.
5. Generate the portable project package.
6. Open the user's own target repository in the chosen AI IDE.
7. Give the IDE agent `BUILD_PROMPT.md` and project instructions.
8. Let the IDE inspect repository and select relevant skills.
9. Implement one milestone at a time and run tests.
10. Review `SKILL_APPLICATION_REPORT.md`, `ACCEPTANCE_MATRIX.md`, and final evidence.
11. Use `HANDOFF.md` to resume across sessions.

Link only to files that exist and are reachable. Verify all internal links, anchors, badges, and external URLs.

## README claim policy

Classify capabilities:
- implemented and tested;
- implemented but not fully tested;
- documented/compatible but not tested;
- experimental;
- planned;
- unsupported.

Do not claim integrations or automatic skill application without tests.

---

# 15. GLOBAL DOCUMENTATION AND KNOWLEDGE ARCHITECTURE

Create or update a clean documentation hierarchy consistent with the current repository:

```text
README.md
CONTRIBUTING.md
docs/
├── getting-started/
│   ├── overview.md
│   ├── project-md-workflow.md
│   ├── chatgpt-claude-setup.md
│   └── ide-handoff.md
├── project-generation/
│   ├── package-format.md
│   ├── requirements-and-traceability.md
│   ├── change-impact.md
│   └── session-continuity.md
├── skills/
│   ├── skill-system.md
│   ├── skill-authoring.md
│   ├── skill-selection.md
│   ├── skill-diagnostics.md
│   └── compatibility-matrix.md
├── knowledge/
│   ├── ui-ux-catalogue.md
│   ├── motion-animation.md
│   ├── backend-system-design.md
│   └── ai-engineering.md
├── security/
│   ├── saas-security-baseline.md
│   ├── tool-governance.md
│   └── authorized-testing.md
├── integrations/
│   ├── repositories.md
│   ├── ide-adapters.md
│   ├── model-providers.md
│   └── router-evaluation.md
└── maintainers/
    ├── development-setup.md
    ├── architecture.md
    └── release-process.md
```

This is a proposed logical organization, not a mandate to recreate the whole repository. Reuse existing paths and avoid duplicating documents. Establish canonical ownership and link to it from README.

---

# 16. IMPLEMENTATION PHASES

Perform the upgrade in controlled phases. Do not try to implement all 27 integrations simultaneously.

## Phase 1 — Baseline and claim audit
- Inspect current repository.
- Build audit matrix.
- Identify actual skill execution failure points.
- Inventory existing catalogues and integration overlap.
- Establish no-clone user workflow.

**Exit:** verified baseline and prioritized implementation plan.

## Phase 2 — Skill system repair
- Fix manifest/schema and discovery paths.
- Fix trigger descriptions and selection.
- Fix instruction loading and referenced resources.
- Define precedence/conflict resolution.
- Add application reporting.
- Add regression fixtures and tests.

**Exit:** task fixtures prove the right skills are selected, loaded, and applied.

## Phase 3 — Knowledge taxonomy and retrieval
- Preserve 86 and 232 UI catalogues.
- Preserve 580 backend topics.
- Preserve 1,095 AI entries.
- Add motion/animation module if missing.
- Normalize tags, aliases, categories, provenance, and duplicates.
- Implement relevance-based retrieval.

**Exit:** knowledge can be retrieved selectively without loading the full catalogue.

## Phase 4 — External repository evaluation
- Inspect all 27 repos.
- Inspect the 8 router candidates separately.
- Record license, health, overlap, security, and adoption decision.
- Adopt only useful candidates incrementally.

**Exit:** integration decision matrix with pinned sources and evidence.

## Phase 5 — Security baseline
- Implement the 19 controls as a reusable assessment matrix.
- Add relevant additional SaaS/AI security checks.
- Integrate optional scanners and tools through safe adapters.
- Enforce authorization for dynamic/live testing.

**Exit:** testable security baseline with truthful status and evidence.

## Phase 6 — Design, motion, and frontend quality
- Integrate selected design skills without conflict.
- Preserve Taste Skill and anti-slop policy.
- Add design tokens, component and UX quality gates.
- Add motion and reduced-motion validation.

**Exit:** sample UI task proves design skills are applied and output meets quality checks.

## Phase 7 — Backend and AI engineering quality
- Add risk-based architecture selection.
- Add API, data, reliability, scaling, and observability guidance.
- Add AI provider/model, agent, RAG, cost, and evaluation guidance.
- Add token/context efficiency without sacrificing quality.

**Exit:** representative backend and AI task fixtures pass architecture and acceptance checks.

## Phase 8 — PROJECT.md package and continuity
- Improve requirement extraction and clarification.
- Generate portable package conditionally.
- Add traceability and change impact.
- Add progress and handoff.
- Add skill selection/application reports.

**Exit:** a sample project can be prepared for an IDE without OpenClone runtime dependency.

## Phase 9 — Global README and docs
- Rewrite root README.
- Correct clone-first end-user instructions.
- Separate maintainer setup.
- Align docs, links, examples, and integration status.

**Exit:** first-time user can follow the workflow from README alone.

## Phase 10 — End-to-end verification and release readiness
- Run tests and docs checks.
- Test supported IDE package outputs.
- Verify skill diagnostics and application evidence.
- Review security and license obligations.
- Review final diff and changelog.

**Exit:** evidence-backed final report.

---

# 17. REQUIRED TEST SCENARIOS

At minimum, create or update representative fixtures for:

1. Premium SaaS dashboard with a provided design system.
2. New responsive landing page with no supplied visual reference.
3. Existing React app needing a targeted UI improvement.
4. Backend API with authentication and tenant isolation.
5. SaaS with RLS and object-level authorization.
6. File upload and private storage workflow.
7. AI RAG application with provider fallback and token budgets.
8. Agent workflow with tools and human approval.
9. Motion-heavy interface with reduced-motion support.
10. Legacy repository where existing architecture must be preserved.
11. New session resuming from HANDOFF.md.
12. Requirement change that triggers impact analysis.
13. Unauthorized dynamic scan request that must be blocked.
14. Security finding through remediation and retest.
15. Skill with malformed metadata that must be reported.
16. Task where no specialized skill applies and fallback behavior is correct.

For each scenario, verify:
- selected skills;
- loaded instruction files;
- skipped skills and reasons;
- generated artifacts;
- implementation or planning quality;
- acceptance evidence;
- no-clone portability where relevant.

---

# 18. DEFINITION OF DONE

This global upgrade is complete only when:

## Skills
- [ ] Root cause of non-applied skills is identified with evidence.
- [ ] Skill manifests and discovery are validated.
- [ ] Task classification and selection work.
- [ ] Full instructions and referenced assets load correctly.
- [ ] Precedence and conflict resolution are documented.
- [ ] Selected, loaded, applied, and skipped states are distinct.
- [ ] Skill application reports contain real evidence.
- [ ] Regression tests cover supported task types and IDE packaging.

## Knowledge
- [ ] 86 UI styles are preserved.
- [ ] 232 UI styles/patterns/approaches are preserved and categorized accurately.
- [ ] 580 backend/system-design topics are preserved.
- [ ] 1,095 AI catalogue entries are preserved.
- [ ] Motion/animation coverage is audited and completed where missing.
- [ ] Duplicate/overlapping terms have aliases or relationships rather than careless deletion.
- [ ] Retrieval is selective and context-efficient.

## Integrations
- [ ] All 27 repositories have a verified evaluation record.
- [ ] All 8 router candidates have a separate evaluation record.
- [ ] License and provenance are recorded for adopted material.
- [ ] No unnecessary full-repository vendoring.
- [ ] Integration status in README matches actual tests.

## Security
- [ ] The 19 SaaS security checks are represented in a testable baseline.
- [ ] Additional relevant SaaS and AI security controls are assessed.
- [ ] Security tools are optional and risk-based.
- [ ] Live dynamic testing requires explicit authorization and allowlisting.
- [ ] Findings have remediation and retest lifecycle.

## Product workflow
- [ ] PROJECT.md is the primary user input.
- [ ] ChatGPT/Claude create a portable package.
- [ ] The user's own IDE inspects the actual repository.
- [ ] No OpenClone clone/install/runtime is required for the primary workflow.
- [ ] Traceability and change-impact management work.
- [ ] Progress and handoff support multi-session work.

## Documentation
- [ ] Root README explains how to use OpenClone.
- [ ] No-clone statement is prominent.
- [ ] Maintainer setup is separate.
- [ ] Global docs are consistent.
- [ ] Links and anchors are checked.
- [ ] Unsupported features are labeled accurately.

## Quality
- [ ] Tests pass or are truthfully marked blocked/not run.
- [ ] Final diff has no unrelated destructive changes.
- [ ] No secrets are exposed.
- [ ] Documentation and integration claims are evidence-based.

---

# 19. REQUIRED FINAL REPORT

Return a structured implementation report:

1. **Repository baseline:** branch, Git status, architecture, relevant modules.
2. **Skill failure root cause:** exact reasons skills were not applied; classify discovery, trigger, loading, precedence, execution, or verification failures.
3. **Skill-system changes:** files changed, selection behavior, loading, diagnostics, and tests.
4. **Knowledge catalogues:** counts preserved, taxonomy corrections, retrieval behavior, motion/animation gap status.
5. **27-repository matrix:** each repository's decision, license, version/commit, integration approach, and evidence.
6. **8-router matrix:** each candidate's assessment and final recommendation.
7. **19-point SaaS security matrix:** status and evidence for each control.
8. **UI/UX and frontend:** skills applied, design QA, motion/accessibility evidence.
9. **Backend/system design:** selected patterns and rationale for representative tasks.
10. **AI engineering:** provider, agent, RAG, cost, token/context, and evaluation improvements.
11. **README:** exact global sections rewritten and no-clone onboarding location.
12. **Portable workflow:** demonstrate PROJECT.md → package → user's IDE → implementation → tests → handoff.
13. **Tests:** exact commands, results, and checks not run.
14. **Limitations:** unverified adapters, deferred repositories, unsupported features.
15. **Next actions:** only genuine remaining work.

Do not report an item as integrated because a link was added. Distinguish `ADOPTED`, `ADAPTED`, `REFERENCED`, `OPTIONAL`, `DEFERRED`, and `REJECTED`.

Do not report a skill as applied because it was mentioned in a prompt. Distinguish `DISCOVERED`, `SELECTED`, `LOADED`, `APPLIED`, and `VERIFIED`.

---

# 20. FINAL EXECUTION COMMAND

You are working inside the existing OpenClone repository.

**Do not return only a plan or another generic prompt. Execute the repository audit and implement this upgrade in phases.**

Start by:
1. inspecting the current Git/repository state;
2. diagnosing why skills are not being applied;
3. auditing the root README and global docs;
4. inventorying all existing skills, knowledge catalogues, and integrations;
5. creating the audit matrix and prioritized implementation plan.

Then implement the phases in order, testing after each meaningful change. Do not blindly clone or merge all external repositories. Do not claim unsupported integrations. Preserve existing user work. Keep the end-user no-clone workflow central.

The final outcome must be a **clean, premium, reliable, explainable OpenClone engineering system** whose skills are not merely stored—they are correctly discovered, selected, loaded, applied, and verified—and whose README clearly teaches a new user how to use it from `PROJECT.md` to a completed project.


---

# 21. CRITICAL FOLLOW-UP — UI/UX QUALITY STILL FEELS 80–90%, AND ALL REPOSITORIES HAVE BEEN ADDED

## 21.1 The problem to solve

The user reports that UI/UX quality and the overall visual feel still seem roughly 80–90% complete, even after adding the recommended UI/UX and security repositories.

Do not assume that adding repositories automatically improves output. Repository presence is only an input. The system must prove that:
- each added repository was actually inspected;
- its useful skill, rules, assets, or code were integrated into the correct location;
- the active IDE can discover and load those materials;
- the task classifier selects the right skills;
- the coding agent follows the selected instructions;
- the resulting UI visibly improves;
- visual and security quality are independently evaluated.

The objective is not to chase an arbitrary 100% score. The objective is to identify the remaining quality gap, explain it with evidence, and close the highest-impact issues without adding unnecessary complexity.

## 21.2 First action: verify the user's actual added repositories

The user says they have already added the supplied UI/UX and security repositories. Therefore, **do not tell them to clone or add them again**.

Inspect the actual current checkout and identify where each repository landed:
- vendored directory;
- skills directory;
- submodule;
- package dependency;
- copied documentation;
- generated reference;
- external tool installation;
- IDE-specific skill location.

Create a repository intake and integration audit with one row per candidate:

| Repository | Present in checkout? | Exact path / commit | License checked? | Content inspected? | Integration type | Discoverable by IDE? | Selected in task test? | Applied? | Evidence | Gap |
|---|---|---|---|---|---|---|---|---|---|---|

For each repository, verify:
1. It is present at the expected path or installed through a documented mechanism.
2. The checked-out commit/version is known.
3. The license and attribution requirements were reviewed.
4. Its contents were actually read; a folder name or README link is not sufficient.
5. Useful capabilities were integrated into the skill registry, adapter, reference catalogue, or tool invocation layer.
6. No unnecessary duplicate skill or conflicting instruction was introduced.
7. The target IDE can discover it from the real project context.
8. A representative task triggers it.
9. The instructions are loaded at the correct point.
10. The final artifact demonstrates the expected behavior.

If the repository is present but not integrated, classify it as `PRESENT_NOT_INTEGRATED`.
If integrated but not discoverable, classify it as `INTEGRATED_NOT_DISCOVERABLE`.
If discoverable but not selected, classify it as `DISCOVERED_NOT_SELECTED`.
If selected but not loaded, classify it as `SELECTED_NOT_LOADED`.
If loaded but ignored, classify it as `LOADED_NOT_APPLIED`.
If applied but not verified, classify it as `APPLIED_NOT_VERIFIED`.
Use `VERIFIED_APPLIED` only when evidence supports the claim.

Do not silently classify a repository as integrated just because its files exist.

## 21.3 UI/UX quality audit — score the actual product, not the repository count

Run a design-quality audit against a real representative screen or project fixture. Use screenshots or browser-rendered output when the environment supports them. Inspect desktop and mobile states. Do not award points for merely having a design skill installed.

Score each dimension from 0–5 and calculate a weighted score out of 100:

| Dimension | Weight | What to inspect |
|---|---:|---|
| Product identity and art direction | 12 | Does the interface have a deliberate, product-specific visual identity? |
| Layout and hierarchy | 12 | Is information priority clear, balanced, and scannable? |
| Typography | 10 | Font choice, scale, line length, hierarchy, readability |
| Color and contrast | 8 | Semantic palette, consistency, contrast, restraint |
| Spacing and composition | 8 | Rhythm, alignment, density, whitespace |
| Components and states | 10 | Consistent components and complete interactive states |
| Responsive behavior | 10 | Mobile/tablet/desktop layouts, overflow, touch behavior |
| Interaction and usability | 8 | Navigation, feedback, forms, focus, error recovery |
| Motion and transitions | 6 | Purposeful, consistent, performant, reduced-motion support |
| Accessibility | 8 | Keyboard, semantics, labels, focus, contrast, assistive technology |
| Craft and detail | 8 | Icons, borders, surfaces, empty/loading states, visual polish |
| **Total** | **100** | |

Scoring rule:
- 0 = absent/broken;
- 1 = seriously deficient;
- 2 = inconsistent or incomplete;
- 3 = acceptable baseline;
- 4 = strong and coherent;
- 5 = exceptional and consistently executed.

Weighted score = sum of `(dimension score / 5) × dimension weight`.

Interpretation:
- 95–100: exceptional; only minor refinements remain.
- 90–94: premium and production-ready for the audited scope.
- 80–89: strong but noticeable quality gaps remain.
- 70–79: inconsistent; another design pass is required.
- Below 70: redesign or major correction is needed.

A score is valid only if accompanied by:
- screen/route audited;
- viewport sizes;
- evidence/screenshots or rendered links where available;
- defects observed;
- rationale for each score;
- prioritized remediation list;
- retest score after changes.

Do not invent a score when no visual artifact can be inspected. Mark it `NOT SCORED — NO RENDERED EVIDENCE`.

## 21.4 Diagnose why the UI still feels generic or unfinished

Specifically inspect for:
- generic AI-generated landing-page composition;
- repetitive card grids;
- excessive rounded panels;
- excessive glassmorphism, blur, glow, gradients, or shadows;
- default purple/blue AI visual language without brand justification;
- inconsistent typography or too many font weights;
- weak content hierarchy;
- arbitrary spacing and alignment;
- poor density for data-heavy screens;
- oversized headings and empty hero sections;
- weak navigation and unclear active states;
- missing empty, loading, error, success, disabled, and permission states;
- inconsistent icons or emoji used as interface icons;
- fake charts, fake metrics, and placeholder content;
- mobile layout treated as a compressed desktop;
- animation added without meaning;
- motion that causes distraction or accessibility problems;
- inaccessible contrast, focus, keyboard, and screen-reader behavior;
- visual components that look polished individually but do not form one coherent system.

For every defect, identify its root cause:
- missing product/brand direction;
- missing design-system tokens;
- skill not discovered;
- skill not selected;
- skill not loaded;
- skill instruction too vague;
- conflicting design skills;
- agent ignored required workflow;
- insufficient reference/context;
- poor implementation;
- missing visual QA;
- no feedback/iteration loop.

## 21.5 Premium design execution protocol

For a UI task, require the coding agent to complete these stages in order:

### Stage A — Understand before designing
- Identify product type, target users, primary user jobs, platform, and business goal.
- Inspect existing screens and repository conventions.
- Read any supplied brand/design references.
- Identify constraints and accessibility requirements.
- Do not start by selecting a fashionable aesthetic.

### Stage B — Establish a visual direction
Create a concise design brief with:
- product personality;
- visual concept;
- hierarchy and composition;
- typography direction;
- semantic color direction;
- surface and depth treatment;
- density strategy;
- interaction character;
- motion principles;
- accessibility constraints.

The visual direction must be justified by the product and users, not by trend imitation.

### Stage C — Define a coherent design system
Create or update only the necessary:
- semantic design tokens;
- typography roles and scale;
- spacing and layout system;
- responsive breakpoints;
- surface, border, radius, and elevation rules;
- component variants;
- interaction states;
- iconography rules;
- motion tokens;
- reduced-motion behavior.

Use the existing system when it is good. Do not replace it merely to demonstrate a new skill.

### Stage D — Implement a representative vertical slice
Build one representative screen and its real interaction states first. Validate the visual direction before replicating the system across every route.

### Stage E — Visual and usability critique
Inspect the rendered result at minimum:
- narrow mobile viewport;
- typical mobile viewport;
- tablet viewport;
- laptop/desktop viewport;
- wide desktop viewport where relevant.

Check actual content, not only empty skeletons. Test navigation, forms, dialogs, menus, keyboard, focus, and error states.

### Stage F — Iterate
Fix the highest-impact defects first:
1. broken hierarchy and usability;
2. layout/responsive defects;
3. typography and spacing inconsistency;
4. color and contrast;
5. component/state inconsistency;
6. motion and microinteraction details;
7. minor visual polish.

Repeat the visual audit and record before/after scores. Do not claim improvement without comparable evidence.

## 21.6 Avoid design-skill overload

The user has added multiple design repositories. More design skills can make output worse when they conflict or compete.

Create a capability map and assign each skill a focused responsibility. Example:

| Capability | Primary responsibility | Other skills |
|---|---|---|
| Product-specific art direction | One selected primary art-direction skill | Others provide optional critique |
| Design-system extraction | Extract tokens and patterns from a supplied reference | Do not invent a new design direction |
| Component implementation | Existing component library and project conventions | Component references only |
| Typography | Typography rules and hierarchy | Avoid competing global font prescriptions |
| Design vocabulary and critique | Identify and explain design defects | Do not override approved brand decisions |
| Anti-slop review | Detect generic or low-quality output | Preserve approved visual direction |
| Accessibility | Validate semantics, keyboard, contrast, and motion | Must not be treated as optional polish |

Rules:
- One primary art-direction authority per project unless the user requests alternatives.
- Multiple skills may contribute specialized checks, but cannot independently redefine the design system.
- Resolve conflict before implementation.
- Keep user-approved design tokens and brand decisions authoritative.
- Do not combine every repository's visual preferences into one interface.
- Keep a short explanation of which design skill owns which decision.

## 21.7 Security repository integration verification

Because the user has already added the security repositories, audit the actual installed copies and integrations rather than asking for them again.

For each security repository/tool, verify:
- exact version/commit;
- license;
- executable or skill entry point;
- installation state;
- dependency and runtime requirements;
- permissions and network access;
- configuration and secret handling;
- whether it runs locally or remotely;
- which project stages invoke it;
- supported output formats;
- severity mapping and false-positive handling;
- remediation and retest workflow;
- evidence of a safe test run on an owned/local fixture.

Create a security integration matrix:

| Tool/repository | Present | Runnable | Safe config | Trigger point | Test fixture | Findings parsed | Remediation flow | Evidence |
|---|---|---|---|---|---|---|---|---|

Do not run Strix, Nuclei, or any dynamic/live scanner against a target without explicit authorization and a precise allowlist. Use local intentionally vulnerable fixtures or authorized staging targets. Never test random public targets.

## 21.8 Security coverage mapping

Map the user's 19 controls to actual enforcement locations and tools. Example:

| Control | Primary enforcement | Supporting tools | Required test |
|---|---|---|---|
| RLS / tenant isolation | Database policy and server tenant context | Semgrep/AI review as support | Cross-tenant read/write denied |
| Auth on API routes | Server middleware/route guards | Static review | Unauthenticated private route denied |
| Frontend untrusted | Server-side validation and authorization | Semgrep | Tampered client request rejected |
| Rate limiting | API gateway/server/Redis | Load test | Burst and sustained abuse bounded |
| Input validation | Schema validation and output encoding | Semgrep | Invalid/malicious input handled safely |
| Parameterized queries | DB access layer | Semgrep | Injection fixture rejected |
| CORS | Server/proxy configuration | Security header scan | Unapproved origin denied |
| HTTPS | Hosting and proxy configuration | TLS/header checks | HTTP redirects or is rejected |
| IDOR/BOLA | Object-level authorization | AI review and tests | Cross-user object access denied |
| Debug mode | Production configuration | Trivy/config review | Debug endpoints and verbose errors absent |
| CAPTCHA/bot controls | Public form risk controls | Integration tests | Abuse control behavior verified |
| Admin audit log | Admin service/domain layer | Log review | Sensitive action creates redacted audit event |
| Private storage | Storage policy and signed URL service | Config scanner | Unauthorized object access denied |
| Admin access | RBAC/ABAC server-side | Semgrep/AI review | Direct route/API access denied |
| Dependency updates | Lockfile and CI policy | Trivy | Known vulnerable dependency detected |
| File upload | Upload pipeline | ClamAV/Trivy where relevant | Spoofed type, oversized, malicious fixture blocked |
| AI security review | Pull request/release review | Claude/Codex/Cloudflare skills where available | Findings triaged and verified |
| Security headers | Web server/edge config | Nuclei/header tests on authorized fixture | Required headers present |
| Webhook signatures | Webhook ingress | Unit/integration tests | Invalid, replayed, stale signatures rejected |

Tool support is supplementary. A scanner cannot replace correct application-level authorization and tests.

## 21.9 AI-slop gate — make it operational

Add a final AI-slop review to every UI implementation. It must answer:

1. Does the design look specific to this product, or could it belong to any generic SaaS?
2. Is the hierarchy intentional?
3. Is every card, panel, gradient, shadow, and animation necessary?
4. Are there repeated patterns without information value?
5. Is the visual system consistent across routes?
6. Does the mobile version feel deliberately designed?
7. Are actual data and real states represented?
8. Are accessibility and reduced-motion requirements met?
9. Were selected design skills actually applied?
10. What three changes would most improve the experience?

Output:
- `PASS`, `NEEDS_REVISION`, or `BLOCKED`;
- evidence and exact affected routes/components;
- prioritized fixes;
- retest result.

Do not use a subjective “AI feel” score alone. Pair the qualitative review with the weighted UI/UX audit and concrete defects.

## 21.10 Add end-to-end regression scenarios for already-added repositories

Create tests that exercise the actual current integration:
- Design MD Chrome: given a reference page or supplied design tokens, verify extracted design information reaches the design brief.
- shadcn/ui: verify components are used only when compatible with the target stack and project conventions.
- Anthropic Frontend Design / Taste Skill / Hallmark / UI UX Pro Max / Impeccable / Typography Skills: verify selection, instruction loading, conflict handling, and output review for relevant tasks.
- Security Audit Skill / Semgrep / Trivy / TruffleHog: verify safe local fixture execution or documented invocation, result parsing, and actionable reporting.
- Strix / Nuclei: verify authorization gate blocks unapproved targets; only use owned local fixtures for permitted tests.
- ClamAV: verify file scanning integration only if file-upload functionality exists in the target project.
- NVIDIA SkillSpector: verify skill inspection workflow against safe test skills, including a deliberately suspicious fixture.
- PyRIT / BLA / Codex Security / Claude Security Review: verify supported invocation and report handling; do not claim automated execution if only documentation/reference integration exists.

For any repository that cannot be executed in CI, test its adapter/contract with mocks and clearly label live integration as not verified.

---

# 22. FOLLOW-UP EXECUTION INSTRUCTIONS

The user has stated that the recommended UI/UX and security repositories have already been added. Treat that as the current working assumption, but verify the actual repository state.

Do not:
- ask the user to add or clone those repositories again;
- assume they are correctly integrated;
- create duplicate copies;
- score the UI without viewing a rendered artifact;
- award a premium score because many skills exist;
- add more design skills just to increase the count;
- run dynamic security tools against unauthorized systems.

Do:
1. inspect the exact current checkout and added repository paths;
2. trace each added repository through discovery, selection, loading, application, and verification;
3. identify why the UI still feels 80–90% complete;
4. render and inspect representative screens if possible;
5. produce a weighted UI/UX score with evidence;
6. identify concrete AI-slop defects and root causes;
7. audit the 19 security controls against real code and tests;
8. verify the installed security tool adapters safely;
9. fix the highest-impact gaps;
10. rerun the same audit and report before/after results.

**Do not stop at documenting the diagnosis. Implement safe, clearly scoped fixes in the existing repository, run the relevant tests, and report what remains unverified.**
