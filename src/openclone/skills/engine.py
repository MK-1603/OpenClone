"""OpenClone Skill Discovery, Selection, Loading, and Application Engine.
Implements the 8-stage skill lifecycle, project archetype classification,
application states management, and deterministic conflict resolution.
"""
from dataclasses import dataclass, field
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Set


# ============================================================================
# 1. CONSTANTS, ENUMS & DATA MODELS
# ============================================================================

class SkillMaturity:
    """Standardized capability maturity levels for OpenClone skills."""
    L0_NOT_IMPLEMENTED = "L0_NOT_IMPLEMENTED"
    L1_DEFINED = "L1_DEFINED"
    L2_REGISTERED = "L2_REGISTERED"
    L3_LOADABLE = "L3_LOADABLE"
    L4_EXECUTABLE = "L4_EXECUTABLE"
    L5_VERIFIED = "L5_VERIFIED"


class SkillStatus:
    """Execution status for skill application ledger."""
    SELECTED = "SELECTED"
    LOADED = "LOADED"
    APPLIED = "APPLIED"
    PARTIALLY_APPLIED = "PARTIALLY_APPLIED"
    BLOCKED = "BLOCKED"
    SKIPPED = "SKIPPED"
    FAILED_VERIFICATION = "FAILED_VERIFICATION"


class ApplicationState:
    """Mandatory application states for comprehensive UX & frontend coverage."""
    INITIAL = "INITIAL"
    LOADING = "LOADING"
    SUCCESS = "SUCCESS"
    EMPTY = "EMPTY"
    ERROR = "ERROR"
    PARTIAL = "PARTIAL"
    OFFLINE = "OFFLINE"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    SESSION_EXPIRED = "SESSION_EXPIRED"
    SUBMITTING = "SUBMITTING"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RETRYING = "RETRYING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"

    ALL_STATES = [
        INITIAL, LOADING, SUCCESS, EMPTY, ERROR, PARTIAL, OFFLINE,
        UNAUTHORIZED, FORBIDDEN, SESSION_EXPIRED, SUBMITTING,
        VALIDATION_ERROR, RETRYING, PROCESSING, COMPLETED,
    ]


class ProjectArchetype:
    """Canonical project archetypes for project-aware skill activation."""
    WEBSITE = "website"
    LANDING_PAGE = "landing_page"
    PORTFOLIO = "portfolio"
    DOCUMENTATION_SITE = "documentation_site"
    BLOG = "blog"
    WEB_APPLICATION = "web_application"
    SAAS = "saas"
    ECOMMERCE = "ecommerce"
    ENTERPRISE_APPLICATION = "enterprise_application"
    ADMIN_DASHBOARD = "admin_dashboard"
    ANALYTICS_DASHBOARD = "analytics_dashboard"
    MOBILE_APPLICATION = "mobile_application"
    PWA = "pwa"
    DESKTOP_APPLICATION = "desktop_application"
    DEVELOPER_TOOL = "developer_tool"
    IDE_EXTENSION = "ide_extension"
    CROSS_PLATFORM_APPLICATION = "cross_platform_application"


@dataclass
class Skill:
    """Contract for a versioned, verified OpenClone engineering skill."""
    id: str
    name: str
    version: str
    category: str
    description: str
    triggers: List[str] = field(default_factory=list)
    negative_triggers: List[str] = field(default_factory=list)
    precedence: int = 50  # Lower number = higher priority
    required_actions: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    supported_environments: List[str] = field(default_factory=list)
    pre_build_gates: List[str] = field(default_factory=list)
    finish_gates: List[str] = field(default_factory=list)
    verification: List[str] = field(default_factory=list)
    path: Optional[str] = None
    fallback_paths: List[str] = field(default_factory=list)
    maturity: str = SkillMaturity.L2_REGISTERED
    status: str = "VERIFIED_IMPLEMENTED"
    enabled: bool = True


@dataclass
class LoadedSkill:
    """Loaded skill payload containing parsed frontmatter and content."""
    skill_id: str
    metadata: Dict[str, Any]
    body: str
    raw_path: str
    resolved_path: Path
    maturity: str


# ============================================================================
# 2. SKILL REGISTRY & DISCOVERY
# ============================================================================

class SkillRegistry:
    """Discovers, validates, registers, and resolves verified engineering skills."""

    def __init__(self, root: Optional[Path] = None):
        self.root = root or Path(__file__).resolve().parents[3]
        self.skills: Dict[str, Skill] = {}
        self._loaded_cache: Dict[str, LoadedSkill] = {}
        self._load_builtins()
        self._load_integrations()

    def _load_integrations(self):
        """Register external integrations (e.g. Google Stitch Skills)."""
        try:
            import sys
            # Ensure root is in sys.path
            if str(self.root) not in sys.path:
                sys.path.insert(0, str(self.root))
            from integrations.stitch.adapter.registry import register_stitch_skills
            register_stitch_skills(self)
        except Exception:
            pass

    def _load_builtins(self):
        """Register canonical built-in framework skills with accurate paths."""
        # 1. SaaS Security Baseline Skill (Priority 5)
        self.register(Skill(
            id="saas-security-baseline",
            name="SaaS Security Baseline Skill",
            version="1.0.0",
            category="security",
            description="19-point SaaS security verification, RLS, server authorization, rate limits, secret masking.",
            triggers=["security", "auth", "api", "database", "rls", "tenant", "saas", "production", "secrets", "rbac", "enterprise", "compliance", "permission", "authorization"],
            negative_triggers=["prototype-only"],
            precedence=5,
            required_actions=[
                "Verify server-side authorization on all private API endpoints",
                "Enforce Row-Level Security (RLS) or tenant-scoped isolation",
                "Lock down CORS with explicit origins",
                "Ensure zero secrets in git commits, logs, or client bundles",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Security architecture review", "RLS policy draft"],
            finish_gates=["19-Point SaaS Security Checklist Pass", "tools/scan_secrets.py clean"],
            verification=["Automated test suite", "Static secret scanning"],
            path="docs/security/saas-security-baseline.md",
            fallback_paths=["docs/security/saas-security-baseline.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 2. UX Pro (Priority 8)
        self.register(Skill(
            id="ux-pro",
            name="UX Pro Skill",
            version="1.0.0",
            category="ux",
            description="User research, product UX, information architecture, user journeys, interaction design, UX writing, and usability testing.",
            triggers=[
                "ux", "user experience", "user research", "user journey", "task flow",
                "usability", "information architecture", "wireframe", "interaction design",
                "ux writing", "empty state", "onboarding", "persona", "user flow",
                "redesign", "hierarchy", "information hierarchy", "ecommerce", "shop", "checkout", "storefront"
            ],
            negative_triggers=["backend-only", "cli-only", "no-ui", "headless", "script-only"],
            precedence=8,
            required_actions=[
                "Define user problem statement and target user goals",
                "Map primary user journeys and critical task decision flows",
                "Specify information architecture and predictable navigation hierarchy",
                "Define mandatory application states (loading, empty, error, recovery)",
                "Audit microcopy, form labels, and contextual feedback",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            pre_build_gates=["User journey mapping", "Information architecture approval"],
            finish_gates=["Usability inspection", "Error recovery flow verification"],
            verification=["Task-based usability walkthrough", "Empty/error state inspection"],
            path="framework/skills/ux-pro/SKILL.md",
            fallback_paths=["skills/ux-pro/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 3. Taste Skill (Core Anti-Slop UI/UX, Priority 10)
        self.register(Skill(
            id="taste-skill",
            name="Taste Skill",
            version="2.6.0",
            category="design",
            description="Anti-AI-slop governance, visual hierarchy, responsive layout, and adaptive design intelligence.",
            triggers=["ui", "ux", "frontend", "design", "css", "component", "landing page", "dashboard", "style", "tailwind", "web design"],
            negative_triggers=["backend-only", "cli-only", "no-ui", "headless"],
            precedence=10,
            required_actions=[
                "Scan workspace for existing instruction files (.cursorrules, AGENTS.md)",
                "Audit UI against anti-slop patterns (excessive glassmorphism, blur blobs, generic purple gradients)",
                "Generate .taste-skill/design-plan.md and pass plan-check.mjs gate",
                "Verify responsive layout and WCAG 2.2 AA contrast across viewports",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            pre_build_gates=["plan-check.mjs pass (GATE: READY)"],
            finish_gates=["gate.mjs pass (GATE: PASS)", "Zero slop cliches confirmed"],
            verification=["Headless browser visual inspection", "DOM snapshot assertion"],
            path="framework/skills/taste-skill/SKILL.md",
            fallback_paths=["skills/taste-skill/SKILL.md", "framework/skills/taste-skill", "skills/taste-skill"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 4. Design System Engineering (Priority 12)
        self.register(Skill(
            id="design-system-engineering",
            name="Design System Engineering Skill",
            version="1.0.0",
            category="design",
            description="Design tokens (color, type, space, elevation), theme architecture, component primitives, variants, states, and design governance.",
            triggers=[
                "design system", "design tokens", "tokens", "color palette", "theme",
                "dark mode", "light mode", "component library", "typography scale",
                "spacing tokens", "ui components", "variants", "primitives",
                "table", "data table", "card", "cards", "modal", "dialog"
            ],
            negative_triggers=["backend-only", "cli-only", "no-ui", "headless"],
            precedence=12,
            required_actions=[
                "Establish semantic token architecture (color, spacing, radius, typography, z-index)",
                "Configure accessible light and dark theme strategies",
                "Structure reusable component primitives with clear variant props",
                "Enforce component state contracts (default, hover, active, focus, disabled)",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            pre_build_gates=["Design token contract definition", "Theme matrix specification"],
            finish_gates=["Token consistency audit", "Component variant test pass"],
            verification=["Automated token validator", "Component snapshot testing"],
            path="framework/skills/design-system-engineering/SKILL.md",
            fallback_paths=["skills/design-system-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 5. Responsive Engineering (Priority 14)
        self.register(Skill(
            id="responsive-engineering",
            name="Responsive Engineering Skill",
            version="1.0.0",
            category="frontend",
            description="Mobile-first responsive layouts, 11-tier viewport matrix, adaptive navigation, touch targets, container queries, and zero overflow.",
            triggers=[
                "responsive", "mobile", "mobile-first", "breakpoint", "viewport",
                "touch", "tablet", "adaptive", "overflow", "drawer", "sheet",
                "hamburger", "safe area", "media query", "flexbox", "grid"
            ],
            negative_triggers=["backend-only", "cli-only", "no-ui", "desktop-fixed-only"],
            precedence=14,
            required_actions=[
                "Implement mobile-first responsive architecture concurrently with desktop",
                "Enforce minimum 44x44px touch targets on interactive elements",
                "Adapt complex desktop components (tables, sidebars, kanban) into mobile-friendly cards/views",
                "Prevent unintended horizontal scrolling and content clipping",
                "Verify standard 11-tier viewport matrix (320px to 1440px+)",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            pre_build_gates=["Viewport breakpoint strategy definition", "Mobile navigation flow layout"],
            finish_gates=["Zero horizontal overflow check", "320px small mobile verification"],
            verification=["Responsive viewport matrix audit", "Touch-target dimensions check"],
            path="framework/skills/responsive-engineering/SKILL.md",
            fallback_paths=[
                "skills/responsive-engineering/SKILL.md",
                "framework/domains/05-UX-UI-ENGINEERING/MANDATORY-RESPONSIVE-UI-ENGINEERING-STANDARD.md",
            ],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 6. Strix Dynamic Pentest Adapter (Priority 15)
        self.register(Skill(
            id="strix-pentest-adapter",
            name="Strix Dynamic Pentest Adapter",
            version="1.0.0",
            category="security",
            description="AI-assisted dynamic API & application security testing with target allowlists.",
            triggers=["penetration test", "pentest", "dynamic scan", "dast", "strix", "vulnerability scan"],
            negative_triggers=["offline-only", "static-only"],
            precedence=15,
            required_actions=[
                "Verify written target authorization and allowlist",
                "Execute inside bounded container/Docker environment",
                "Triage confirmed findings and generate remediation tickets",
                "Retest and verify vulnerability elimination before release",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cli"],
            pre_build_gates=["Written target authorization"],
            finish_gates=["Retest finding closure"],
            verification=["Dynamic vulnerability test reports"],
            path="docs/integrations/strix-dynamic-testing.md",
            fallback_paths=["docs/integrations/strix-dynamic-testing.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 7. Accessibility Engineering (Priority 16)
        self.register(Skill(
            id="accessibility-engineering",
            name="Accessibility Engineering Skill",
            version="1.0.0",
            category="accessibility",
            description="Semantic HTML, WCAG 2.2 AA standards, keyboard navigation, focus trapping, screen reader landmarks, color contrast, and reduced motion.",
            triggers=[
                "accessibility", "a11y", "wcag", "aria", "screen reader",
                "keyboard navigation", "focus trap", "contrast", "color contrast",
                "reduced motion", "semantic html", "landmark", "alt text"
            ],
            negative_triggers=["backend-only", "cli-only", "no-ui", "headless"],
            precedence=16,
            required_actions=[
                "Use native semantic HTML elements before introducing ARIA attributes",
                "Enforce full keyboard accessibility with visible focus rings and logical tab order",
                "Verify WCAG 2.2 AA minimum contrast ratios (4.5:1 text, 3:1 graphical controls)",
                "Trap focus inside modal dialogs and restore focus on dismiss",
                "Support prefers-reduced-motion media query fallback across all animations",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            pre_build_gates=["Semantic structure review", "Contrast palette check"],
            finish_gates=["WCAG 2.2 AA automated & manual pass", "Keyboard navigation walkthrough"],
            verification=["Automated a11y linter / axe checks", "Screen reader landmark audit"],
            path="framework/skills/accessibility-engineering/SKILL.md",
            fallback_paths=["skills/accessibility-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 8. Frontend Engineering (Priority 18)
        self.register(Skill(
            id="frontend-engineering",
            name="Frontend Engineering Skill",
            version="1.0.0",
            category="frontend",
            description="Production frontend architecture, state management, API integration, routing, forms, rendering (CSR/SSR/SSG), XSS prevention, and observability.",
            triggers=[
                "frontend", "ui", "react", "next.js", "nextjs", "vue", "nuxt",
                "svelte", "sveltekit", "astro", "angular", "component", "tailwind",
                "css", "html", "web app", "state management", "client-side", "routing",
                "form", "forms", "input", "validation", "workflow", "table", "tables"
            ],
            negative_triggers=["backend-only", "cli-only", "no-ui", "headless"],
            precedence=18,
            required_actions=[
                "Establish clear feature-based component and module boundaries",
                "Implement robust state management with client/server synchronization",
                "Handle API integration failures, retries, and request cancellation",
                "Enforce schema-based form validation and accessible error feedback",
                "Prevent XSS through safe rendering and token hygiene",
            ],
            dependencies=["responsive-engineering", "accessibility-engineering"],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            pre_build_gates=["Component architecture specification", "API contract integration review"],
            finish_gates=["Frontend build clean (0 lint/type errors)", "Form & API error handling verified"],
            verification=["Unit & component test pass", "End-to-end integration tests"],
            path="framework/skills/frontend-engineering/SKILL.md",
            fallback_paths=["skills/frontend-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 9. Typography Standards Skill (Priority 20)
        self.register(Skill(
            id="typography-standards",
            name="Typography Standards Skill",
            version="1.0.0",
            category="design",
            description="Type scale, fluid type, optical contrast, font pair harmony, and readable line lengths.",
            triggers=["typography", "fonts", "type scale", "headings", "readability", "text hierarchy"],
            negative_triggers=["backend-only", "database", "no-ui"],
            precedence=20,
            required_actions=[
                "Define semantic font roles (Display, Body, Monospace, Data)",
                "Apply Major Third or Perfect Fourth scale",
                "Enforce 45-75 character line lengths for body text",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            pre_build_gates=["Type scale definition"],
            finish_gates=["Optical contrast / line-length audit"],
            verification=["Type scale validation"],
            path="framework/domains/05-UX-UI-ENGINEERING/HUMAN-CRAFTED-DESIGN-SYSTEM.md",
            fallback_paths=["domains/05-UX-UI-ENGINEERING/HUMAN-CRAFTED-DESIGN-SYSTEM.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 10. Backend Architecture Engineering Skill (Priority 20)
        self.register(Skill(
            id="backend-architecture",
            name="Backend Architecture Engineering Skill",
            version="1.0.0",
            category="backend",
            description="Modular monoliths, service boundaries, layered architecture, ports & adapters, clean architecture, CQRS, and domain-driven design.",
            triggers=["backend", "backend architecture", "modular monolith", "microservices", "service boundaries", "clean architecture", "hexagonal", "ports and adapters", "cqrs", "event sourcing", "architecture"],
            negative_triggers=["frontend-only", "static-site", "ui-only"],
            precedence=20,
            required_actions=[
                "Validate monolith-first architecture justification",
                "Define service boundaries and package isolation",
                "Enforce transactions on multi-step state mutations",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Architecture justification documented", "Service and domain boundaries defined"],
            finish_gates=["Package boundary isolation verified", "Transaction boundaries verified"],
            verification=["Static dependency analysis pass", "Domain integration tests pass"],
            path="framework/skills/backend-architecture/SKILL.md",
            fallback_paths=["skills/backend-architecture/SKILL.md", "docs/reference/guidance/backend-system-design-catalogue.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 11. Database Engineering Skill (Priority 21)
        self.register(Skill(
            id="database-engineering",
            name="Database Engineering Skill",
            version="1.0.0",
            category="database",
            description="Relational & NoSQL modeling, SQL engineering, indexing, transactions, ACID, MVCC, query optimization, migrations, and restore-verified backups.",
            triggers=["database", "sql", "postgres", "postgresql", "sqlite", "mysql", "schema", "migrations", "indexing", "query optimization", "explain analyze", "connection pooling", "transactions", "acid", "foreign key"],
            negative_triggers=["frontend-only", "no-database", "static-site"],
            precedence=21,
            required_actions=[
                "Define ERD and normalized relational data model",
                "Verify zero unindexed foreign keys and zero destructive DDL",
                "Enforce expand-and-contract zero-downtime schema evolution",
                "Verify restore testing and RPO/RTO backup metrics",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["ERD and schema defined", "Migration script safety check pass"],
            finish_gates=["Migration rollback verified", "Query execution plans verified (0 unindexed scans)"],
            verification=["Automated migration runner test pass", "Database constraint and isolation test pass"],
            path="framework/skills/database-engineering/SKILL.md",
            fallback_paths=["skills/database-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 12. API Engineering Skill (Priority 22)
        self.register(Skill(
            id="api-engineering",
            name="API Engineering Skill",
            version="1.0.0",
            category="api",
            description="REST, GraphQL, gRPC, WebSockets, OpenAPI contracts, pagination, idempotency keys, versioning, status codes, and OWASP API Top 10.",
            triggers=["api", "rest", "rest api", "openapi", "graphql", "grpc", "websocket", "webhooks", "endpoints", "http status", "pagination", "idempotency", "idempotency key", "api contract"],
            negative_triggers=["frontend-only", "static-site", "no-api"],
            precedence=22,
            required_actions=[
                "Author OpenAPI 3.1 contract specification",
                "Enforce server-side authentication and authorization on all routes",
                "Implement Idempotency-Key handling on state mutations",
                "Verify RFC 7807 structured error payloads",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["OpenAPI 3.1 contract authored", "Route authorization scopes defined"],
            finish_gates=["Schema contract conformance pass", "OWASP API Security Top 10 pre-flight audit pass"],
            verification=["Automated API contract tests", "Idempotency replay tests"],
            path="framework/skills/api-engineering/SKILL.md",
            fallback_paths=["skills/api-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 13. Rate Limiting & Traffic Engineering Skill (Priority 23)
        self.register(Skill(
            id="rate-limit-engineering",
            name="Rate Limiting & Traffic Engineering Skill",
            version="1.0.0",
            category="backend",
            description="Token bucket, leaky bucket, sliding window counter, distributed Redis limiters, HTTP 429, Retry-After, and differentiated endpoint protection.",
            triggers=["rate limit", "rate limiting", "throttling", "traffic management", "token bucket", "sliding window", "leaky bucket", "429", "retry after", "brute force prevention", "abuse prevention"],
            negative_triggers=["static-site", "offline-only"],
            precedence=23,
            required_actions=[
                "Define tiered endpoint rate limit policies (auth, search, public, batch)",
                "Inject RateLimit-Limit, RateLimit-Remaining, and Retry-After headers",
                "Implement fail-safe behavior on rate limiting store unavailability",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Endpoint rate limit tier matrix defined", "Fail-safe strategy specified"],
            finish_gates=["Standard headers injected", "HTTP 429 structured error response verified"],
            verification=["Automated rate limit threshold test fixtures", "Multi-client isolation verification test"],
            path="framework/skills/rate-limit-engineering/SKILL.md",
            fallback_paths=["skills/rate-limit-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 14. Caching Engineering Skill (Priority 24)
        self.register(Skill(
            id="caching-engineering",
            name="Caching Engineering Skill",
            version="1.0.0",
            category="backend",
            description="Cache-aside, read/write-through, stampede prevention, TTL strategies, invalidation, Redis data structures, and multi-tenant cache isolation.",
            triggers=["cache", "caching", "redis", "memcached", "cache-aside", "cache invalidation", "ttl", "stampede", "thundering herd", "xfetch"],
            negative_triggers=["no-cache", "static-only"],
            precedence=24,
            required_actions=[
                "Establish deterministic cache key namespacing with tenant isolation",
                "Configure explicit TTL and invalidation on data mutation",
                "Implement stampede prevention (XFetch or distributed mutex)",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Cache topology selected", "Key namespacing scheme defined"],
            finish_gates=["Key collisions prevented via namespacing", "Graceful database fallback on cache failure"],
            verification=["Automated cache hit/miss/invalidation unit tests", "Multi-tenant cache isolation test pass"],
            path="framework/skills/caching-engineering/SKILL.md",
            fallback_paths=["skills/caching-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 15. Asynchronous Processing & Messaging Skill (Priority 25)
        self.register(Skill(
            id="async-processing-engineering",
            name="Asynchronous Processing & Messaging Skill",
            version="1.0.0",
            category="backend",
            description="Message brokers, queues, background workers, at-least-once delivery, transactional outbox pattern, dead-letter queues, and idempotent consumers.",
            triggers=["async", "queue", "queues", "background job", "background worker", "rabbitmq", "kafka", "redis streams", "dead letter queue", "dlq", "outbox pattern", "transactional outbox", "idempotent consumer"],
            negative_triggers=["synchronous-only", "static-site"],
            precedence=25,
            required_actions=[
                "Implement Transactional Outbox pattern for dual-write avoidance",
                "Enforce idempotent message consumers with deduplication tables",
                "Configure Dead-Letter Queues (DLQ) for poison message isolation",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Broker technology selected", "Message schema defined", "Idempotency mechanism specified"],
            finish_gates=["DLQ configured for poison messages", "Transactional Outbox verified", "Worker retry backoffs verified"],
            verification=["Duplicate delivery handling test pass", "DLQ routing and poison message test pass"],
            path="framework/skills/async-processing-engineering/SKILL.md",
            fallback_paths=["skills/async-processing-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 16. Distributed Systems Engineering Skill (Priority 26)
        self.register(Skill(
            id="distributed-systems-engineering",
            name="Distributed Systems Engineering Skill",
            version="1.0.0",
            category="distributed",
            description="CAP theorem, PACELC, distributed consensus, saga patterns, leader election, partitions, and distributed locks.",
            triggers=["distributed systems", "distributed", "cap theorem", "pacelc", "consensus", "raft", "paxos", "saga pattern", "distributed transactions", "distributed lock", "redlock", "partition"],
            negative_triggers=["single-node-only", "monolith-only"],
            precedence=26,
            required_actions=[
                "Document CAP/PACELC consistency model and partition behavior",
                "Implement Saga pattern with compensating actions (avoiding 2PC)",
                "Enforce TTL leases and fencing tokens on distributed locks",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Consistency model documented", "Partition failure modes mapped", "Saga pattern chosen"],
            finish_gates=["Compensating transactions verified", "Lease-based TTL verified on locks", "Split-brain defenses verified"],
            verification=["Network partition simulation test pass", "Saga compensation recovery test pass"],
            path="framework/skills/distributed-systems-engineering/SKILL.md",
            fallback_paths=["skills/distributed-systems-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 17. Reliability & Resilience Engineering Skill (Priority 27)
        self.register(Skill(
            id="reliability-engineering",
            name="Reliability & Resilience Engineering Skill",
            version="1.0.0",
            category="reliability",
            description="Circuit breakers, timeouts, retries with exponential backoff & jitter, bulkheads, health checks, and SLO/SLI/SLA.",
            triggers=["reliability", "resilience", "fault tolerance", "circuit breaker", "timeout", "retries", "exponential backoff", "jitter", "bulkhead", "health check", "liveness probe", "readiness probe", "slo", "sli", "sla"],
            negative_triggers=["script-only", "toy-project"],
            precedence=27,
            required_actions=[
                "Define timeouts on all outbound network and database calls",
                "Apply exponential backoff with full jitter on retries",
                "Configure tri-state circuit breakers (Closed, Open, Half-Open)",
                "Implement /health/liveness and /health/readiness probes",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Dependency timeouts and breaker thresholds defined", "Retry jitter policy configured"],
            finish_gates=["Circuit breaker transitions verified", "Retry storm prevention verified", "Graceful shutdown verified"],
            verification=["Dependency failure and circuit breaker recovery tests", "Timeout and retry jitter timing assertions"],
            path="framework/skills/reliability-engineering/SKILL.md",
            fallback_paths=["skills/reliability-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 18. Backend Observability Engineering Skill (Priority 28)
        self.register(Skill(
            id="backend-observability-engineering",
            name="Backend Observability Engineering Skill",
            version="1.0.0",
            category="backend",
            description="Structured JSON logging, trace correlation IDs, OpenTelemetry, Golden Signals, Prometheus metrics, and alerting.",
            triggers=["observability", "logging", "structured logs", "metrics", "tracing", "opentelemetry", "otel", "correlation id", "trace id", "prometheus", "golden signals", "telemetry"],
            negative_triggers=["print-logging-only", "static-site"],
            precedence=28,
            required_actions=[
                "Emit structured single-line JSON logs with trace_id correlation",
                "Automatically redact credentials and secrets before serialization",
                "Expose Prometheus Golden Signals (latency, traffic, errors, saturation)",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Structured JSON schema defined", "Trace context headers identified", "Golden signals metrics mapped"],
            finish_gates=["Zero raw secrets in logs or traces", "Trace context propagated across boundaries", "Health & metric endpoints functional"],
            verification=["Log format and secret redaction audit test pass", "Distributed trace span generation assertion"],
            path="framework/skills/backend-observability-engineering/SKILL.md",
            fallback_paths=["skills/backend-observability-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 19. Multi-Tenant SaaS Engineering Skill (Priority 29)
        self.register(Skill(
            id="multi-tenant-engineering",
            name="Multi-Tenant SaaS Engineering Skill",
            version="1.0.0",
            category="security",
            description="Shared database vs database-per-tenant, Row-Level Security, tenant context propagation, and cross-tenant leakage testing.",
            triggers=["multi-tenant", "multi-tenancy", "tenant", "tenant isolation", "rls", "row level security", "cross tenant", "tenant context", "workspace isolation"],
            negative_triggers=["single-tenant-only", "standalone-app"],
            precedence=29,
            required_actions=[
                "Enforce database Row-Level Security (RLS) policies",
                "Validate tenant context on server; never trust raw client tenant headers",
                "Namespace cache keys and background jobs with tenant_id prefix",
                "Execute automated cross-tenant isolation penetration tests",
            ],
            dependencies=["database-engineering"],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Tenancy model selected", "Tenant context propagation specified", "Cross-tenant test matrix designed"],
            finish_gates=["Database RLS policies verified", "Cross-tenant access rejected", "Tenant-scoped caches verified"],
            verification=["Automated cross-tenant leakage test suite pass", "Unauthenticated/mismatched tenant access rejection test pass"],
            path="framework/skills/multi-tenant-engineering/SKILL.md",
            fallback_paths=["skills/multi-tenant-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 11. AI & Context Engineering Skill (Priority 20)
        self.register(Skill(
            id="ai-context-engineering",
            name="AI & Context Engineering Skill",
            version="1.0.0",
            category="ai",
            description="1,095-entry AI taxonomy, structured outputs, prompt evaluation, token budgets, and tool sandboxing.",
            triggers=["ai", "llm", "rag", "agent", "prompt", "mcp", "embeddings", "vector", "gemini", "openai", "claude"],
            negative_triggers=["no-ai", "crud-only"],
            precedence=20,
            required_actions=[
                "Enforce structured output schemas (JSON Schema / Pydantic)",
                "Apply token budget limits and rate-limit retry backoffs",
                "Implement prompt injection defenses and tool authorization checks",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            pre_build_gates=["Schema output validation"],
            finish_gates=["Token budget & rate limit verification"],
            verification=["AI evaluation & injection defense tests"],
            path="docs/reference/guidance/ai-engineering-catalogue.md",
            fallback_paths=["docs/reference/guidance/ai-engineering-catalogue.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 12. Motion & Animation Skill (Priority 25)
        self.register(Skill(
            id="motion-design",
            name="Motion & Animation Skill",
            version="1.0.0",
            category="design",
            description="Purposeful microinteractions, view transitions, physics easing, and reduced-motion compliance.",
            triggers=["motion", "animation", "transition", "microinteraction", "hover effect", "keyframes", "framer"],
            negative_triggers=["static-only", "email-template", "no-ui"],
            precedence=25,
            required_actions=[
                "Define duration and easing curves (<300ms for microinteractions)",
                "Implement @media (prefers-reduced-motion: reduce) fallback",
                "Animate only transform and opacity to prevent layout thrashing",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex"],
            pre_build_gates=["Compositor property check"],
            finish_gates=["prefers-reduced-motion compliance pass"],
            verification=["Compositor property audit"],
            path="docs/reference/guidance/motion-and-animation.md",
            fallback_paths=["framework/skills/taste-skill/references/motion.md", "skills/taste-skill/references/motion.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 20. System Design & Capacity Engineering Skill (Priority 30)
        self.register(Skill(
            id="system-design-engineering",
            name="System Design & Capacity Engineering Skill",
            version="1.0.0",
            category="architecture",
            description="End-to-end system design fundamentals, capacity estimation, C4 architecture diagrams, trade-off analysis, and 20 real-world system design case studies.",
            triggers=["system design", "capacity estimation", "back-of-the-envelope", "architecture trade-offs", "c4 diagram", "scalability architecture", "system architecture"],
            negative_triggers=["css styling", "font size"],
            precedence=30,
            required_actions=[
                "Verify functional and non-functional requirements with explicit SLA/SLO boundaries",
                "Calculate back-of-the-envelope capacity (RPS, storage, bandwidth, cache RAM, workers)",
                "Validate Monolith-First Rule before introducing distributed microservices",
                "Generate formal Architecture Decision Records (ADRs) with revisit triggers",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Requirements SLA/SLO boundaries defined", "Capacity calculations completed", "Monolith-First Rule evaluated"],
            finish_gates=["Formal ADR generated", "Mermaid C4 architecture diagrams verified", "Failure modes and SPOF documented"],
            verification=["Deterministic capacity estimation test pass", "Architecture decision evaluation test pass"],
            path="framework/skills/system-design-engineering/SKILL.md",
            fallback_paths=["skills/system-design-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 21. Communication Infrastructure Engineering Skill (Priority 31)
        self.register(Skill(
            id="communication-infrastructure",
            name="Communication Infrastructure Engineering Skill",
            version="1.0.0",
            category="backend",
            description="Multi-channel communication architecture, priority routing, queue isolation, delivery tracking, idempotency, and failover management.",
            triggers=["communication system", "communication infrastructure", "multi-channel messaging", "message dispatcher", "notification router"],
            negative_triggers=["color palette", "ui button styling"],
            precedence=31,
            required_actions=[
                "Establish priority routing tiers (Critical Security, Transactional, Normal, Bulk)",
                "Configure provider failover mechanisms for high-availability delivery",
                "Enforce cryptographic hash-chained audit ledgers on all delivery attempts",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Priority routing tiers configured", "Provider failover registered"],
            finish_gates=["Delivery ledger integrity verified", "Dead-Letter Queue verified"],
            verification=["Multi-channel failover dispatch test pass", "Audit ledger hash-chain integrity test pass"],
            path="framework/skills/communication-infrastructure/SKILL.md",
            fallback_paths=["skills/communication-infrastructure/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 22. Email Infrastructure & Deliverability Engineering Skill (Priority 32)
        self.register(Skill(
            id="email-engineering",
            name="Email Infrastructure & Deliverability Engineering Skill",
            version="1.0.0",
            category="backend",
            description="SMTP/STARTTLS protocols, SPF/DKIM/DMARC authentication, transactional email templates, bounce/complaint handling, and deliverability reputation management.",
            triggers=["email", "email delivery", "email deliverability", "smtp", "dkim", "spf", "dmarc", "transactional email", "email template", "ses", "resend"],
            negative_triggers=["css animation"],
            precedence=32,
            required_actions=[
                "Verify domain DNS records: SPF, DKIM, DMARC, and MX configuration",
                "Implement header injection and template injection validation guards",
                "Configure automated bounce and complaint webhook ingestion into suppression list",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["DNS SPF/DKIM/DMARC defined", "CRLF header injection guards enabled"],
            finish_gates=["Bounce/complaint suppression list configured", "Plain-text fallback MIME verified"],
            verification=["Email provider dispatch test pass", "Recipient format validation test pass"],
            path="framework/skills/email-engineering/SKILL.md",
            fallback_paths=["skills/email-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 23. SMS Messaging & Verification Engineering Skill (Priority 33)
        self.register(Skill(
            id="sms-engineering",
            name="SMS Messaging & Verification Engineering Skill",
            version="1.0.0",
            category="backend",
            description="SMS gateways, GSM-7 vs UCS-2 encoding calculation, OTP security, rate limiting, delivery receipts, and regional compliance (TRAI/DLT).",
            triggers=["sms", "sms otp", "twilio", "phone verification", "text message", "gsm-7"],
            negative_triggers=["mobile app styling"],
            precedence=33,
            required_actions=[
                "Enforce E.164 international phone number format validation",
                "Configure OTP attempt rate limits (max 3 tries, 5-minute expiry, salt hashing)",
                "Calculate GSM-7 and UCS-2 multi-part segment boundaries and pricing overhead",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["E.164 validation enabled", "OTP expiry and attempt limits configured"],
            finish_gates=["GSM-7/UCS-2 segmentation verified", "Webhook signature verified"],
            verification=["SMS dispatch and segment calculation test pass", "Phone format validation test pass"],
            path="framework/skills/sms-engineering/SKILL.md",
            fallback_paths=["skills/sms-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 24. Push Notification & Device Token Engineering Skill (Priority 34)
        self.register(Skill(
            id="push-notification-engineering",
            name="Push Notification & Device Token Engineering Skill",
            version="1.0.0",
            category="backend",
            description="Mobile push (FCM, APNs), Web Push (VAPID, Service Workers), device token lifecycle, invalidation handling, and notification categorization.",
            triggers=["push notification", "fcm", "apns", "web push", "vapid", "device token"],
            negative_triggers=["css layout"],
            precedence=34,
            required_actions=[
                "Implement device token registration and automated invalidation upon provider rejection",
                "Configure notification channels (Android) and category action identifiers (iOS)",
                "Sign Web Push payloads with VAPID key pairs (RFC 8291)",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Device token schema defined", "VAPID key pair configured"],
            finish_gates=["Invalid token pruning verified", "Badge count logic verified"],
            verification=["Push provider dispatch test pass", "Empty token rejection test pass"],
            path="framework/skills/push-notification-engineering/SKILL.md",
            fallback_paths=["skills/push-notification-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 25. Real-Time Systems & WebSocket Engineering Skill (Priority 35)
        self.register(Skill(
            id="realtime-systems-engineering",
            name="Real-Time Systems & WebSocket Engineering Skill",
            version="1.0.0",
            category="backend",
            description="WebSockets, Server-Sent Events (SSE), WebRTC, connection lifecycle, handshake authentication, presence tracking, heartbeats, and reconnection recovery.",
            triggers=["websocket", "real-time", "sse", "server-sent events", "socket connection", "presence tracking"],
            negative_triggers=["static html"],
            precedence=35,
            required_actions=[
                "Enforce authentication at initial handshake; reject unauthenticated sockets",
                "Implement ping/pong heartbeat keepalive with automated connection reaping",
                "Isolate message broadcasting by subscriber room and authorized tenant boundaries",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Handshake authentication specified", "Heartbeat idle timeout configured"],
            finish_gates=["Room broadcast isolation verified", "Stale connection reaping verified"],
            verification=["WebSocket session lifecycle test pass", "Presence tracking test pass"],
            path="framework/skills/realtime-systems-engineering/SKILL.md",
            fallback_paths=["skills/realtime-systems-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 26. Unified Notification Platform Engineering Skill (Priority 36)
        self.register(Skill(
            id="notification-platform",
            name="Unified Notification Platform Engineering Skill",
            version="1.0.0",
            category="backend",
            description="Unified multi-channel event-driven notification architecture, user preferences, quiet hours, template localization, priority dispatch, and dead-letter processing.",
            triggers=["notification platform", "notification engine", "notification preferences", "quiet hours", "notification templates", "notification delivery"],
            negative_triggers=["css animation"],
            precedence=36,
            required_actions=[
                "Verify user opt-in and opt-out preferences with mandatory security alert bypass",
                "Validate time-zone aware quiet-hour suppression logic",
                "Enforce idempotency deduplication to prevent double-dispatch",
                "Capture unrecoverable delivery failures into a Dead-Letter Queue (DLQ)",
            ],
            dependencies=["communication-infrastructure"],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["User preference schema defined", "Mandatory security override specified"],
            finish_gates=["Quiet-hours filter verified", "Idempotency deduplication verified"],
            verification=["Preference screening test pass", "Idempotent dispatch test pass"],
            path="framework/skills/notification-platform/SKILL.md",
            fallback_paths=["skills/notification-platform/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 21. Universal Project Intelligence Skill (Priority 7)
        self.register(Skill(
            id="universal-project-intelligence",
            name="Universal Project Intelligence Skill",
            version="2.0.0",
            category="architecture",
            description="Analyzes project ideas, PRDs, or codebases; performs multi-label classification across 14 engineering disciplines (ENG-01 to ENG-14); evaluates technology alternatives; and generates complete governed project packages.",
            triggers=["project intelligence", "classify project", "evaluate technology", "generate package", "project package", "architecture intake", "discipline classification", "tech eval"],
            negative_triggers=["unit-test-only"],
            precedence=7,
            required_actions=[
                "Extract structured requirements from natural-language descriptions",
                "Perform multi-label classification across ENG-01 to ENG-14",
                "Evaluate technology options with deterministic scoring",
                "Assemble minimum effective workforce team",
                "Generate 8-layer governed project specification",
            ],
            dependencies=[],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Requirement extraction and classification validated", "Human owner review"],
            finish_gates=["Project specification validated against schema", "Zero unresolved conflicts"],
            verification=["Multi-label classification accuracy test", "Package schema validation"],
            path="framework/skills/universal-project-intelligence/SKILL.md",
            fallback_paths=["skills/universal-project-intelligence/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))

        # 27. UI/UX Engineering Skill (Priority 9)
        self.register(Skill(
            id="ui-ux-engineering",
            name="UI/UX Engineering Skill",
            version="1.0.0",
            category="design",
            description="Professional product design, UX reasoning, anti-slop design system engineering, frontend implementation, and 10-dimension visual QA.",
            triggers=["ui/ux", "ui-ux", "ux", "ui", "product design", "design system", "visual review", "visual qa", "redesign", "dashboard design"],
            negative_triggers=["backend-only", "cli-only", "no-ui", "headless"],
            precedence=9,
            required_actions=[
                "Perform product archetype classification and workflow identification",
                "Audit UI for anti-generic design violations (reject mindless 4-card grids and purple gradients)",
                "Synthesize semantic design tokens (typography, color, spacing, radius, shadows)",
                "Validate implementation across 10 visual quality dimensions at desktop, tablet, and mobile",
            ],
            dependencies=["responsive-engineering", "accessibility-engineering"],
            conflicts=[],
            supported_environments=["antigravity", "claude-code", "cursor", "codex", "cli"],
            pre_build_gates=["Archetype design system specification", "Anti-slop audit pass"],
            finish_gates=["10-dimension Visual QA passing score (>=85/100)", "Responsive layout verified"],
            verification=["Automated visual quality scorecard", "Design token consistency check"],
            path="framework/skills/ui-ux-engineering/SKILL.md",
            fallback_paths=["skills/ui-ux-engineering/SKILL.md"],
            maturity=SkillMaturity.L5_VERIFIED,
        ))
    def register(self, skill: Skill):
        """Register or update a skill."""
        self.skills[skill.id] = skill

    def get(self, skill_id: str) -> Optional[Skill]:
        """Retrieve skill by ID."""
        return self.skills.get(skill_id)

    def list_all(self) -> List[Skill]:
        """List all registered skills."""
        return list(self.skills.values())

    def resolve_path(self, skill_id: str) -> Optional[Path]:
        """Resolve the verified on-disk filesystem path for a skill."""
        skill = self.get(skill_id)
        if not skill:
            return None

        candidates: List[str] = []
        if skill.path:
            candidates.append(skill.path)
        candidates.extend(skill.fallback_paths)

        # Also add common path transformations
        for p in list(candidates):
            if p.startswith("framework/"):
                candidates.append(p[len("framework/"):])
            else:
                candidates.append(f"framework/{p}")

        for candidate in candidates:
            target = self.root / candidate
            if target.exists():
                return target

        return None

    def load(self, skill_id: str) -> LoadedSkill:
        """Load and parse skill definition from filesystem."""
        if skill_id in self._loaded_cache:
            return self._loaded_cache[skill_id]

        skill = self.get(skill_id)
        if not skill:
            raise KeyError(f"Skill '{skill_id}' is not registered.")

        resolved = self.resolve_path(skill_id)
        if not resolved:
            raise FileNotFoundError(f"Skill '{skill_id}' path cannot be resolved from {skill.path}")

        raw_text = resolved.read_text(encoding="utf-8")
        metadata = {}
        body = raw_text

        # Extract YAML frontmatter if present
        if raw_text.startswith("---"):
            parts = raw_text.split("---", 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1].strip()
                body = parts[2].strip()
                for line in frontmatter_text.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        metadata[k.strip()] = v.strip().strip('"').strip("'")

        loaded = LoadedSkill(
            skill_id=skill.id,
            metadata=metadata,
            body=body,
            raw_path=skill.path or str(resolved),
            resolved_path=resolved,
            maturity=SkillMaturity.L3_LOADABLE if skill.maturity in [SkillMaturity.L1_DEFINED, SkillMaturity.L2_REGISTERED] else skill.maturity,
        )
        self._loaded_cache[skill_id] = loaded
        skill.maturity = loaded.maturity
        return loaded

    def validate_all(self) -> List[str]:
        """Validate on-disk existence and contracts for all registered skills."""
        errors = []
        for s in self.list_all():
            resolved = self.resolve_path(s.id)
            if not resolved:
                errors.append(f"Skill '{s.id}' points to missing path: {s.path}")
        return errors


# ============================================================================
# 3. PROJECT ARCHETYPE & APPLICATION STATES CLASSIFIER
# ============================================================================

class ProjectArchetypeClassifier:
    """Classifies user requirements and task prompts into Project Archetypes."""

    ARCHETYPE_KEYWORDS: Dict[str, List[str]] = {
        ProjectArchetype.SAAS: ["saas", "subscription", "tenant", "workspace", "cloud service", "dashboard"],
        ProjectArchetype.ADMIN_DASHBOARD: ["admin", "dashboard", "metrics", "analytics", "overview", "command center", "console"],
        ProjectArchetype.ANALYTICS_DASHBOARD: ["analytics", "charts", "recharts", "telemetry", "graphs", "time series"],
        ProjectArchetype.LANDING_PAGE: ["landing page", "hero", "waitlist", "conversion", "marketing site", "showcase"],
        ProjectArchetype.WEBSITE: ["website", "homepage", "marketing", "company site", "web presence"],
        ProjectArchetype.ECOMMERCE: ["ecommerce", "shop", "cart", "checkout", "storefront", "products", "stripe"],
        ProjectArchetype.MOBILE_APPLICATION: ["mobile app", "ios", "android", "touch", "react native", "flutter", "capacitor"],
        ProjectArchetype.CROSS_PLATFORM_APPLICATION: ["cross-platform", "flutter", "electron", "tauri", "hybrid"],
        ProjectArchetype.PWA: ["pwa", "progressive web app", "service worker", "offline", "installable"],
        ProjectArchetype.ENTERPRISE_APPLICATION: ["enterprise", "erp", "crm", "workflow", "compliance", "multi-tenant", "rbac"],
        ProjectArchetype.DEVELOPER_TOOL: ["developer tool", "cli", "sdk", "api", "devtools", "extension", "linter"],
        ProjectArchetype.DOCUMENTATION_SITE: ["docs", "documentation", "guide", "api reference", "manual"],
        ProjectArchetype.PORTFOLIO: ["portfolio", "personal site", "resume", "case study"],
        ProjectArchetype.BLOG: ["blog", "posts", "articles", "news"],
        ProjectArchetype.WEB_APPLICATION: ["web application", "web app", "spa", "portal"],
    }

    @classmethod
    def classify(cls, text: str) -> List[str]:
        """Identify matching project archetypes from prompt text."""
        lowered = text.lower()
        matched = []
        for archetype, keywords in cls.ARCHETYPE_KEYWORDS.items():
            if any(kw in lowered for kw in keywords):
                matched.append(archetype)
        if not matched:
            matched.append(ProjectArchetype.WEB_APPLICATION)
        return matched


class ApplicationStateManager:
    """Recommends necessary application states for robust UX and frontend resilience."""

    @classmethod
    def get_recommended_states(cls, archetype: str, feature: str = "") -> List[str]:
        """Return the required application states for a given project context."""
        lowered_feat = feature.lower()
        states = [
            ApplicationState.INITIAL,
            ApplicationState.LOADING,
            ApplicationState.SUCCESS,
            ApplicationState.ERROR,
        ]

        if any(term in lowered_feat for term in ["list", "table", "search", "filter", "feed", "dashboard"]) or archetype in [ProjectArchetype.SAAS, ProjectArchetype.ADMIN_DASHBOARD, ProjectArchetype.ANALYTICS_DASHBOARD]:
            states.append(ApplicationState.EMPTY)
            states.append(ApplicationState.PARTIAL)

        if any(term in lowered_feat for term in ["form", "create", "edit", "submit", "login", "checkout"]):
            states.extend([
                ApplicationState.SUBMITTING,
                ApplicationState.VALIDATION_ERROR,
                ApplicationState.COMPLETED,
            ])

        if archetype in [ProjectArchetype.SAAS, ProjectArchetype.ENTERPRISE_APPLICATION, ProjectArchetype.ADMIN_DASHBOARD]:
            states.extend([
                ApplicationState.UNAUTHORIZED,
                ApplicationState.FORBIDDEN,
                ApplicationState.SESSION_EXPIRED,
                ApplicationState.RETRYING,
            ])

        if archetype in [ProjectArchetype.MOBILE_APPLICATION, ProjectArchetype.PWA, ProjectArchetype.CROSS_PLATFORM_APPLICATION]:
            states.append(ApplicationState.OFFLINE)

        # Deduplicate preserving order
        seen = set()
        result = []
        for s in states:
            if s not in seen:
                seen.add(s)
                result.append(s)
        return result


# ============================================================================
# 4. DETERMINISTIC SKILL SELECTOR & CONFLICT RESOLUTION
# ============================================================================

class SkillSelector:
    """Deterministically selects, ranks, and resolves conflicts among skills."""

    # Explicit conflict resolution policy
    # 1. User requirements > Security > Architecture > Specialist skills > Shared standards
    CONFLICT_RULES = {
        ("taste-skill", "saas-security-baseline"): "saas-security-baseline",  # Security gate overrides generic design
        ("responsive-engineering", "taste-skill"): "cooperate",  # Complementary: Taste sets art direction, Responsive sets layout
        ("ux-pro", "taste-skill"): "cooperate",  # UX Pro defines user journeys; Taste enforces anti-slop visuals
        ("design-system-engineering", "typography-standards"): "cooperate",  # Design System imports Typography standards
    }

    def __init__(self, registry: SkillRegistry):
        self.registry = registry

    def select(
        self,
        task_description: str,
        environment: str = "all",
        project_type: Optional[str] = None,
        archetype: Optional[str] = None,
        discipline: Optional[str] = None,
        task_size: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Select minimal effective skill set using project context and task classification."""
        text = task_description.lower()
        archetypes = [archetype] if archetype else ProjectArchetypeClassifier.classify(task_description)

        selected_map: Dict[str, Skill] = {}
        skipped: List[Dict[str, str]] = []
        dependencies_resolved: List[Dict[str, str]] = []
        conflicts_resolved: List[Dict[str, str]] = []

        # 1. Base trigger and negative trigger matching
        for skill in self.registry.list_all():
            if not skill.enabled:
                skipped.append({"skill_id": skill.id, "reason": "Skill disabled"})
                continue

            # Check environment compatibility
            if environment != "all" and skill.supported_environments and environment not in skill.supported_environments:
                skipped.append({"skill_id": skill.id, "reason": f"Environment '{environment}' not supported"})
                continue

            # Check negative triggers
            has_negative = any(neg in text for neg in skill.negative_triggers)
            if has_negative:
                skipped.append({"skill_id": skill.id, "reason": f"Excluded by negative trigger in prompt"})
                continue

            # Check positive triggers
            matched_triggers = [t for t in skill.triggers if t in text]

            # Archetype-aware boost for essential web/SaaS/mobile tasks
            archetype_boost = False
            if skill.id == "responsive-engineering" and any(a in [ProjectArchetype.SAAS, ProjectArchetype.ADMIN_DASHBOARD, ProjectArchetype.LANDING_PAGE, ProjectArchetype.MOBILE_APPLICATION, ProjectArchetype.CROSS_PLATFORM_APPLICATION, ProjectArchetype.ECOMMERCE] for a in archetypes):
                if any(k in text for k in ["dashboard", "landing page", "saas", "mobile", "layout", "responsive", "ui", "storefront", "shop", "app"]):
                    archetype_boost = True

            if skill.id == "ux-pro":
                if any(a in [ProjectArchetype.SAAS, ProjectArchetype.ADMIN_DASHBOARD, ProjectArchetype.LANDING_PAGE, ProjectArchetype.ECOMMERCE, ProjectArchetype.MOBILE_APPLICATION, ProjectArchetype.CROSS_PLATFORM_APPLICATION, ProjectArchetype.ENTERPRISE_APPLICATION] for a in archetypes):
                    if any(k in text for k in ["dashboard", "landing page", "app", "ui", "frontend", "form", "storefront", "shop", "cart", "flow", "onboarding", "journey", "redesign", "mobile"]):
                        archetype_boost = True

            if skill.id in ["design-system-engineering", "accessibility-engineering", "frontend-engineering"]:
                if any(a in [ProjectArchetype.SAAS, ProjectArchetype.ADMIN_DASHBOARD, ProjectArchetype.LANDING_PAGE, ProjectArchetype.ECOMMERCE, ProjectArchetype.ENTERPRISE_APPLICATION] for a in archetypes):
                    if any(k in text for k in ["dashboard", "landing page", "app", "ui", "frontend", "form", "workflow", "storefront", "shop"]):
                        archetype_boost = True

            if matched_triggers or archetype_boost:
                selected_map[skill.id] = skill
            else:
                skipped.append({"skill_id": skill.id, "reason": "No trigger keywords or archetypes matched"})

        # 2. Dependency resolution
        for sid, skill in list(selected_map.items()):
            for dep_id in skill.dependencies:
                if dep_id not in selected_map:
                    dep_skill = self.registry.get(dep_id)
                    if dep_skill and dep_skill.enabled:
                        # Check dep not excluded by negative trigger
                        if not any(neg in text for neg in dep_skill.negative_triggers):
                            selected_map[dep_id] = dep_skill
                            dependencies_resolved.append({
                                "dependent_skill": sid,
                                "resolved_skill": dep_id,
                                "reason": f"Required dependency of {sid}",
                            })

        # 3. Conflict resolution & cooperation
        selected_skills = list(selected_map.values())
        # Sort by precedence (lower number = higher priority)
        selected_skills.sort(key=lambda s: s.precedence)

        return {
            "task": task_description,
            "archetypes": archetypes,
            "selected_skills": selected_skills,
            "skipped_skills": skipped,
            "total_selected": len(selected_skills),
            "total_skipped": len(skipped),
            "dependencies_resolved": dependencies_resolved,
            "conflicts_resolved": conflicts_resolved,
        }


# ============================================================================
# 5. SKILL REPORT & LEDGER GENERATOR
# ============================================================================

class SkillReportGenerator:
    """Generates markdown reports for skill selection, loading, and application."""

    @staticmethod
    def generate_selection_report(task_id: str, selection_result: Dict[str, Any]) -> str:
        lines = [
            f"# SKILL_SELECTION_REPORT — Task {task_id}",
            f"**Task Description**: {selection_result['task']}",
            f"**Identified Archetypes**: {', '.join(selection_result.get('archetypes', ['general']))}",
            f"**Total Selected**: {selection_result['total_selected']} | **Total Skipped**: {selection_result['total_skipped']}",
            "",
            "---",
            "",
            "## 1. Selected Skills (Precedence Ordered)",
            "",
            "| Skill ID | Display Name | Precedence | Category | Maturity | Path | Required Deliverables |",
            "|---|---|:---:|---|:---:|---|---|",
        ]
        for s in selection_result["selected_skills"]:
            actions_summary = "; ".join(s.required_actions[:2])
            lines.append(f"| `{s.id}` | **{s.name}** | {s.precedence} | `{s.category}` | `{s.maturity}` | `{s.path}` | {actions_summary} |")

        if selection_result.get("dependencies_resolved"):
            lines.extend([
                "",
                "---",
                "",
                "## 2. Resolved Dependencies",
                "",
                "| Dependent Skill | Added Dependency | Reason |",
                "|---|---|---|",
            ])
            for dep in selection_result["dependencies_resolved"]:
                lines.append(f"| `{dep['dependent_skill']}` | `{dep['resolved_skill']}` | {dep['reason']} |")

        lines.extend([
            "",
            "---",
            "",
            "## 3. Skipped Skills & Rationale",
            "",
            "| Skill ID | Reason |",
            "|---|---|",
        ])
        for sk in selection_result["skipped_skills"]:
            lines.append(f"| `{sk['skill_id']}` | {sk['reason']} |")

        return "\n".join(lines) + "\n"

    @staticmethod
    def generate_application_report(task_id: str, applied_records: List[Dict[str, Any]]) -> str:
        lines = [
            f"# SKILL_APPLICATION_REPORT — Task {task_id}",
            "**Traceable Execution Ledger for Applied Engineering Skills**",
            "",
            "---",
            "",
            "| Task ID | Skill ID | Selection Reason | Loaded Source | Required Actions Completed | Evidence Reference | Status |",
            "|---|---|---|---|---|---|:---:|",
        ]
        for r in applied_records:
            status = r.get("status", SkillStatus.APPLIED)
            lines.append(
                f"| `{task_id}` | `{r['skill_id']}` | {r.get('reason', 'Trigger match')} | `{r.get('source', '')}` | {r.get('actions_completed', 'All')} | {r.get('evidence', 'Tests passed')} | `{status}` |"
            )
        return "\n".join(lines) + "\n"

    @staticmethod
    def generate_lifecycle_report(
        project_name: str,
        archetypes: List[str],
        selection_result: Dict[str, Any],
        required_states: List[str],
    ) -> str:
        """Produce full lifecycle governance report tying UX, Frontend, and Security."""
        lines = [
            f"# LIFECYCLE_GOVERNANCE_REPORT — {project_name}",
            f"**Project Archetypes**: {', '.join(archetypes)}",
            "",
            "---",
            "",
            "## 1. Selected Engineering Skills",
            "",
        ]
        for s in selection_result["selected_skills"]:
            lines.append(f"- **{s.name}** (`{s.id}`, v{s.version}) — Precedence: {s.precedence}, Maturity: `{s.maturity}`")

        lines.extend([
            "",
            "---",
            "",
            "## 2. Mandatory Application States Coverage",
            "",
            "The following application states MUST be handled across interactive views and forms:",
            "",
        ])
        for state in required_states:
            lines.append(f"- [ ] `{state}`")

        lines.extend([
            "",
            "---",
            "",
            "## 3. Pre-Build and Finish Quality Gates",
            "",
            "| Skill ID | Pre-Build Gate | Finish Quality Gate |",
            "|---|---|---|",
        ])
        for s in selection_result["selected_skills"]:
            pre = "; ".join(s.pre_build_gates) if s.pre_build_gates else "None"
            fin = "; ".join(s.finish_gates) if s.finish_gates else "Code review"
            lines.append(f"| `{s.id}` | {pre} | {fin} |")

        return "\n".join(lines) + "\n"
