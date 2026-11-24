# OpenClone Skill Registry
**Canonical Registry of Verified Engineering, Design, Backend & Communication Skills**  
*OpenClone Global Standards | Managed by `src/openclone/skills/engine.py`*

---

## 1. Registered Skills Master Index

| Skill ID | Display Name | Version | Category | Precedence | Location | Pre-Build Gate | Finish Gate | Maturity Status |
|---|---|---|---|:---:|---|---|---|:---:|
| `saas-security-baseline` | **SaaS Security Baseline Skill** | `v1.0.0` | `security` | 5 | [`docs/security/saas-security-baseline.md`](file:///docs/security/saas-security-baseline.md) | Security architecture review | 19-Point Checklist Pass | `L5_VERIFIED` |
| `ux-pro` | **UX Pro Skill** | `v1.0.0` | `ux` | 8 | [`framework/skills/ux-pro/SKILL.md`](file:///framework/skills/ux-pro/SKILL.md) | Journey mapping / IA approval | Usability walkthrough pass | `L5_VERIFIED` |
| `taste-skill` | **Taste Skill** | `v2.6.0` | `design` | 10 | [`framework/skills/taste-skill/SKILL.md`](file:///framework/skills/taste-skill/SKILL.md) | `plan-check.mjs` (`GATE: READY`) | `gate.mjs` (`GATE: PASS`) | `L5_VERIFIED` |
| `design-system-engineering` | **Design System Engineering Skill** | `v1.0.0` | `design` | 12 | [`framework/skills/design-system-engineering/SKILL.md`](file:///framework/skills/design-system-engineering/SKILL.md) | Token contract definition | Token & variant test pass | `L5_VERIFIED` |
| `responsive-engineering` | **Responsive Engineering Skill** | `v1.0.0` | `frontend` | 14 | [`framework/skills/responsive-engineering/SKILL.md`](file:///framework/skills/responsive-engineering/SKILL.md) | Viewport breakpoint plan | 11-Tier Matrix / 0 Overflow | `L5_VERIFIED` |
| `strix-pentest-adapter` | **Strix Dynamic Pentest Adapter** | `v1.0.0` | `security` | 15 | [`docs/integrations/strix-dynamic-testing.md`](file:///docs/integrations/strix-dynamic-testing.md) | Written Target Authorization | Retest Finding Closure | `L5_VERIFIED` |
| `accessibility-engineering` | **Accessibility Engineering Skill** | `v1.0.0` | `accessibility` | 16 | [`framework/skills/accessibility-engineering/SKILL.md`](file:///framework/skills/accessibility-engineering/SKILL.md) | Semantic structure & contrast check | WCAG 2.2 AA / Keyboard walkthrough | `L5_VERIFIED` |
| `frontend-engineering` | **Frontend Engineering Skill** | `v1.0.0` | `frontend` | 18 | [`framework/skills/frontend-engineering/SKILL.md`](file:///framework/skills/frontend-engineering/SKILL.md) | Component architecture spec | 0 lint/type errors & build clean | `L5_VERIFIED` |
| `typography-standards` | **Typography Standards Skill** | `v1.0.0` | `design` | 20 | [`framework/domains/05-UX-UI-ENGINEERING/HUMAN-CRAFTED-DESIGN-SYSTEM.md`](file:///framework/domains/05-UX-UI-ENGINEERING/HUMAN-CRAFTED-DESIGN-SYSTEM.md) | Type Scale Validation | Optical Contrast / Line-length | `L5_VERIFIED` |
| `backend-architecture` | **Backend System Architecture Skill** | `v1.0.0` | `backend` | 20 | [`framework/skills/backend-architecture/SKILL.md`](file:///framework/skills/backend-architecture/SKILL.md) | Monolith-First Rule Check | Migration Rollback Verification | `L5_VERIFIED` |
| `database-engineering` | **Database & Data Modeling Skill** | `v1.0.0` | `database` | 21 | [`framework/skills/database-engineering/SKILL.md`](file:///framework/skills/database-engineering/SKILL.md) | Schema Normalization & Index Audit | Expand-and-Contract Migration Check | `L5_VERIFIED` |
| `api-engineering` | **API & Integration Engineering Skill** | `v1.0.0` | `backend` | 22 | [`framework/skills/api-engineering/SKILL.md`](file:///framework/skills/api-engineering/SKILL.md) | OpenAPI Contract & Error Schema | Pagination & Idempotency Key Check | `L5_VERIFIED` |
| `rate-limit-engineering` | **Traffic & Rate Limiting Skill** | `v1.0.0` | `backend` | 23 | [`framework/skills/rate-limit-engineering/SKILL.md`](file:///framework/skills/rate-limit-engineering/SKILL.md) | Tiered Limit Policy Spec | HTTP 429 Header Conformance | `L5_VERIFIED` |
| `caching-engineering` | **Caching Topologies Skill** | `v1.0.0` | `backend` | 24 | [`framework/skills/caching-engineering/SKILL.md`](file:///framework/skills/caching-engineering/SKILL.md) | Cache-Aside & TTL Spec | Stampede Prevention (XFetch) | `L5_VERIFIED` |
| `async-processing-engineering` | **Asynchronous Messaging Skill** | `v1.0.0` | `backend` | 25 | [`framework/skills/async-processing-engineering/SKILL.md`](file:///framework/skills/async-processing-engineering/SKILL.md) | Queue Topology & Worker Sizing | DLQ & Poison Message Alerting | `L5_VERIFIED` |
| `distributed-systems-engineering` | **Distributed Systems Skill** | `v1.0.0` | `backend` | 26 | [`framework/skills/distributed-systems-engineering/SKILL.md`](file:///framework/skills/distributed-systems-engineering/SKILL.md) | CAP/PACELC Trade-off Model | Saga Compensation & Leases | `L5_VERIFIED` |
| `reliability-engineering` | **Reliability & Resilience Skill** | `v1.0.0` | `reliability` | 27 | [`framework/skills/reliability-engineering/SKILL.md`](file:///framework/skills/reliability-engineering/SKILL.md) | Timeout & Breaker Thresholds | Jittered Retry Storm Prevention | `L5_VERIFIED` |
| `backend-observability-engineering` | **Backend Observability Skill** | `v1.0.0` | `backend` | 28 | [`framework/skills/backend-observability-engineering/SKILL.md`](file:///framework/skills/backend-observability-engineering/SKILL.md) | Structured JSON & OTel Schema | Golden Signals & Zero Secret Logs | `L5_VERIFIED` |
| `multi-tenant-engineering` | **Multi-Tenant SaaS Skill** | `v1.0.0` | `security` | 29 | [`framework/skills/multi-tenant-engineering/SKILL.md`](file:///framework/skills/multi-tenant-engineering/SKILL.md) | Tenant Context Propagation Spec | Database RLS & Leakage Audit | `L5_VERIFIED` |
| `system-design-engineering` | **System Design & Capacity Skill** | `v1.0.0` | `architecture` | 30 | [`framework/skills/system-design-engineering/SKILL.md`](file:///framework/skills/system-design-engineering/SKILL.md) | Capacity & SLA/SLO Boundaries | Formal ADR & Mermaid C4 Diagrams | `L5_VERIFIED` |
| `communication-infrastructure` | **Communication Infrastructure Skill** | `v1.0.0` | `backend` | 31 | [`framework/skills/communication-infrastructure/SKILL.md`](file:///framework/skills/communication-infrastructure/SKILL.md) | Priority Routing Tier Spec | Provider Failover & Ledger Audit | `L5_VERIFIED` |
| `email-engineering` | **Email & Deliverability Skill** | `v1.0.0` | `backend` | 32 | [`framework/skills/email-engineering/SKILL.md`](file:///framework/skills/email-engineering/SKILL.md) | SPF/DKIM/DMARC & Header Injection | Bounce/Complaint Suppression List | `L5_VERIFIED` |
| `sms-engineering` | **SMS & Verification Skill** | `v1.0.0` | `backend` | 33 | [`framework/skills/sms-engineering/SKILL.md`](file:///framework/skills/sms-engineering/SKILL.md) | E.164 & OTP Attempt Limits | GSM-7/UCS-2 Segmentation Check | `L5_VERIFIED` |
| `push-notification-engineering` | **Push Notification Skill** | `v1.0.0` | `backend` | 34 | [`framework/skills/push-notification-engineering/SKILL.md`](file:///framework/skills/push-notification-engineering/SKILL.md) | Device Token & VAPID Keys | Invalid Token Pruning Verification | `L5_VERIFIED` |
| `realtime-systems-engineering` | **Real-Time & WebSocket Skill** | `v1.0.0` | `backend` | 35 | [`framework/skills/realtime-systems-engineering/SKILL.md`](file:///framework/skills/realtime-systems-engineering/SKILL.md) | Handshake Auth & Keepalives | Room Broadcast Isolation Check | `L5_VERIFIED` |
| `notification-platform` | **Unified Notification Platform Skill** | `v1.0.0` | `backend` | 36 | [`framework/skills/notification-platform/SKILL.md`](file:///framework/skills/notification-platform/SKILL.md) | Preference Matrix & Security Bypass | Quiet-Hours & Idempotent Dedup | `L5_VERIFIED` |
| `ai-context-engineering` | **AI & Context Engineering Skill** | `v1.0.0` | `ai` | 20 | [`docs/reference/guidance/ai-engineering-catalogue.md`](file:///docs/reference/guidance/ai-engineering-catalogue.md) | Schema Output Validation | Token Budget / Rate Limit | `L5_VERIFIED` |
| `motion-design` | **Motion & Animation Skill** | `v1.0.0` | `design` | 25 | [`docs/reference/guidance/motion-and-animation.md`](file:///docs/reference/guidance/motion-and-animation.md) | Compositor Property Check | `prefers-reduced-motion` | `L5_VERIFIED` |

---

## 2. Precedence and Conflict Resolution Hierarchy

When tasks touch multiple engineering layers, skills operate under strict deterministic precedence (lower number = higher authority):

1. **User Requirements (`PROJECT.md`)**: Human owner constraints are authoritative and cannot be silently overridden.
2. **Security & Data Safety (`saas-security-baseline`, `strix-pentest-adapter`, `multi-tenant-engineering` — Precedence 5-15, 29)**: Mandatory zero-trust boundaries, private API authorization, and secret hygiene. Design cannot bypass security.
3. **UX & Architecture (`ux-pro` — Precedence 8)**: User problem definition, navigation hierarchy, task flows, and application states.
4. **Art Direction & Anti-Slop (`taste-skill` — Precedence 10)**: Eliminates clichés, enforces visual rhythm, and mandates pre-build gate verification.
5. **Design System & Components (`design-system-engineering` — Precedence 12)**: Reusable semantic tokens, theme architecture, and component primitives.
6. **Responsive Layout (`responsive-engineering` — Precedence 14)**: Mobile-first development, 11-tier viewport matrix, 44px tap targets, zero horizontal overflow.
7. **Accessibility (`accessibility-engineering` — Precedence 16)**: Semantic HTML, WCAG 2.2 AA contrast, keyboard navigation, focus trapping, screen reader landmarks.
8. **Frontend Implementation (`frontend-engineering` — Precedence 18)**: Type-safe architecture, state synchronization, form validation, error boundaries.
9. **Backend, Database & Distributed Systems (`backend-architecture`, `database-engineering`, `api-engineering`, `rate-limit-engineering`, `caching-engineering`, `async-processing-engineering`, `distributed-systems-engineering`, `reliability-engineering`, `backend-observability-engineering` — Precedence 20-28)**: Expand-and-contract migrations, token bucket rate limits, cache-aside, sagas, circuit breakers.
10. **System Design & Capacity (`system-design-engineering` — Precedence 30)**: Capacity estimation, Monolith-First Rule, C4 architecture diagrams, ADR generation, and 20 real-world case studies.
11. **Communication Infrastructure & Notifications (`communication-infrastructure`, `email-engineering`, `sms-engineering`, `push-notification-engineering`, `realtime-systems-engineering`, `notification-platform` — Precedence 31-36)**: Multi-channel messaging, SPF/DKIM/DMARC deliverability, GSM-7/UCS-2 SMS, FCM/APNs push tokens, WebSockets, quiet hours, and cryptographic delivery ledgers.

---

## 3. Project Archetype to Skill Selection Matrix

Skill selection adapts to the specific project archetype rather than forcing generic design rules onto every workload:

| Project Archetype | Primary Focus | Mandatory Selected Skills |
|---|---|---|
| **Marketing Website / Landing Page** | Visual storytelling, conversion, zero slop | `ux-pro`, `taste-skill`, `design-system-engineering`, `responsive-engineering`, `accessibility-engineering`, `frontend-engineering` |
| **SaaS Dashboard / Command Center** | Information density, workflows, navigation, security | `saas-security-baseline`, `ux-pro`, `design-system-engineering`, `responsive-engineering`, `accessibility-engineering`, `frontend-engineering`, `multi-tenant-engineering` |
| **High-Throughput Distributed Platform** | Concurrency, data volume, low latency, fault tolerance | `system-design-engineering`, `backend-architecture`, `database-engineering`, `api-engineering`, `rate-limit-engineering`, `caching-engineering`, `async-processing-engineering`, `distributed-systems-engineering`, `reliability-engineering`, `backend-observability-engineering` |
| **Communication & Notification System** | Multi-channel routing, quiet hours, deliverability | `communication-infrastructure`, `email-engineering`, `sms-engineering`, `push-notification-engineering`, `realtime-systems-engineering`, `notification-platform` |
| **Admin / Analytics Console** | Complex tables, data visualization, filtering, speed | `ux-pro`, `design-system-engineering`, `responsive-engineering`, `accessibility-engineering`, `frontend-engineering`, `database-engineering` |
| **Mobile-First PWA / Cross-Platform** | Touch ergonomics, offline states, drawer navigation | `ux-pro`, `responsive-engineering`, `accessibility-engineering`, `frontend-engineering`, `design-system-engineering`, `push-notification-engineering` |
| **Enterprise ERP / Operations Tool** | High-density forms, multi-step transactions, permissions | `saas-security-baseline`, `ux-pro`, `design-system-engineering`, `accessibility-engineering`, `frontend-engineering`, `multi-tenant-engineering`, `database-engineering` |
| **Developer Tool / CLI / Headless API** | Command ergonomics, contract stability, low latency | `system-design-engineering`, `backend-architecture`, `api-engineering`, `database-engineering`, `saas-security-baseline` (UI skills skipped via negative triggers) |

---

## 4. Mandatory Application States Coverage

For every user-facing view, form, and table, the engineering team must implement and verify:
- [ ] `INITIAL` — Clean resting state before user input.
- [ ] `EMPTY` — First-run zero state with guidance and primary call to action.
- [ ] `LOADING` — Contextual skeleton or pulse indicator preserving spatial layout.
- [ ] `SUCCESS` — Crisp completion indicator, dismissible banner, or immediate data update.
- [ ] `ERROR` — Clear recovery path, field-level feedback, and actionable remediation.
- [ ] `PARTIAL` — Offline indicator, progressive rendering, or degraded data banner.
