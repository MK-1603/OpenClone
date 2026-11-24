---
id: frontend-engineering
name: Frontend Engineering Skill
version: 1.0.0
category: frontend
description: Production frontend architecture, state management, API integration, routing, forms, rendering (CSR/SSR/SSG), XSS prevention, and observability.
maturity: L5_VERIFIED
status: VERIFIED_IMPLEMENTED
path: framework/skills/frontend-engineering/SKILL.md
triggers:
  - frontend
  - ui
  - react
  - next.js
  - nextjs
  - vue
  - nuxt
  - svelte
  - sveltekit
  - astro
  - angular
  - component
  - tailwind
  - css
  - html
  - web app
  - state management
  - client-side
  - routing
negative_triggers:
  - backend-only
  - cli-only
  - no-ui
  - headless
precedence: 18
dependencies:
  - responsive-engineering
  - accessibility-engineering
conflicts: []
supported_environments:
  - antigravity
  - claude-code
  - cursor
  - codex
pre_build_gates:
  - Component architecture & folder structure specified
  - State management & API contract integration strategy defined
  - Form schema validation rules established
finish_gates:
  - Zero TypeScript compiler errors & zero linter errors
  - Production build succeeds without warnings
  - Critical error boundaries & API retry flows verified
verification:
  - Automated component & unit test suite pass
  - End-to-end integration test pass
---

# Frontend Engineering — Specialist Skill
**Version:** `1.0.0` | **Category:** `frontend` | **Maturity:** `L5_VERIFIED`  
**Governing Standard:** OpenClone UX & Frontend Engineering Intelligence  
**Workforce Alignment:** `frontend-architect`, `frontend-engineer`, `web-performance-engineer`

---

## 1. PURPOSE & BOUNDARIES

### Purpose
Build robust, maintainable, performant, and production-grade client-side applications. Frontend Engineering translates UX designs and architectural contracts into clean, type-safe, resilient code across web frameworks, ensuring deterministic state management, secure data handling, and seamless user experiences.

### Boundaries
- **In Scope:** Application architecture, modular component design, state management (local, global, server, URL), API data integration, routing and layouts, form schema validation, rendering strategies (CSR, SSR, SSG, ISR), frontend security (XSS, CSP, secret hygiene), testing, SEO metadata, PWA capabilities, and client runtime observability.
- **Out of Scope:** Server-side database migrations and cloud infrastructure management.

---

## 2. REQUIRED EXPERTISE DOMAINS

### A. Frontend Architecture & Modular Boundaries
1. **Feature-Based Folder Structure:**
   ```text
   src/
     app/            # Routes, pages, layouts (App Router / Pages)
     components/     # Shared UI primitives and composite widgets
       ui/           # Headless primitives (Button, Input, Modal, Badge)
       layout/       # AppShell, Sidebar, Header, Navigation
       modals/       # Contextual dialogs and overlay workflows
       views/        # Top-level screen assemblies
     hooks/          # Reusable custom hooks
     lib/            # Utility functions, API clients, formatters
     styles/         # Global CSS, theme definitions, tokens
     types/          # Domain contracts and TypeScript models
   ```
2. **Separation of Concerns:** Keep presentation components decoupled from side effects and backend calls. Use custom hooks or service modules for API fetching.

### B. Component Engineering & Contracts
1. **Composition Over Inheritance:** Build small, single-purpose components composed into higher-level views.
2. **Explicit Props Typing:** Every component must export a strict TypeScript interface for props. Never use `any` or loose untyped objects.
3. **State Isolation:** Localize state to the lowest common ancestor in the component hierarchy to prevent unnecessary re-renders.

### C. State Management
1. **State Tiering:**
   - **Local Component State:** Input values, accordion toggle, temporary UI flags (`useState`).
   - **URL State:** Search queries, pagination page, active tabs, filters (`useSearchParams` / router state).
   - **Server / Cache State:** Server data, caching, invalidation (`TanStack Query`, SWR, or React Server Components).
   - **Global Client State:** User session, theme, global notification drawer (`zustand`, React Context, or Jotai).

### D. API Integration & Resilience
1. **Contract Validation:** Validate server responses at runtime using Zod or Valibot schemas before rendering to catch API drift early.
2. **Graceful Failure Handling:** Every network request must provide:
   - Loading indicator (skeleton or scoped spinner).
   - Explicit retry mechanism.
   - User-friendly error message.
   - Cancellation token / AbortController support on unmount.
3. **Optimistic Updates:** Apply optimistic local UI updates where appropriate (e.g. toggling task status), with automatic rollback on server error.

### E. Routing & Navigation
1. **Route Architecture:** Clean nested routing with persistent layouts to avoid unmounting global shells between page transitions.
2. **Protected Routes & Guards:** Client-side route guards for authentication, paired with server-side authorization enforcement.
3. **404 & Error Boundaries:** Scoped React Error Boundaries around major views to prevent single-component crashes from taking down the entire application.

### F. Forms & Validation
1. **Schema Validation:** Define forms using schema-first validation (Zod, Valibot, React Hook Form).
2. **Validation Timing:** Validate on blur or change once the user has touched the field; avoid aggressive errors before initial input.
3. **Accessible Form Feedback:** Associate error messages using `aria-invalid` and `aria-describedby`.

### G. Rendering Strategies & Trade-offs
- **CSR (Client-Side Rendering):** Highly interactive private dashboards with dense local state.
- **SSR (Server-Side Rendering):** Dynamic content requiring SEO and fast initial server render.
- **SSG (Static Site Generation):** Documentation, blogs, and public marketing sites.
- **ISR (Incremental Static Regeneration):** Large e-commerce or content catalogs updating periodically.

### H. Frontend Security & Zero-Leak Policy
1. **Zero Client Secrets:** NEVER include API secrets, private keys, database credentials, or auth tokens in client bundles. Only public environment variables (`NEXT_PUBLIC_*`, `VITE_*`) may enter client code.
2. **XSS Prevention:** Never use `dangerouslySetInnerHTML` with unsanitized user inputs. Use DOMPurify if HTML rendering is strictly necessary.
3. **Safe Navigation:** Sanitize all dynamic links to prevent `javascript:` URI execution.

### I. Frontend Testing & Observability
1. **Unit & Component Testing:** Test utility functions, hooks, and isolated UI components with Vitest/Jest and Testing Library.
2. **Error Logging:** Capture uncaught client exceptions via structured client logger (redacting any user PII/tokens before transmission).

---

## 3. TECHNOLOGY NEUTRALITY

This skill supports modern frontend ecosystems without imposing an arbitrary framework:
- **React / Next.js** (App Router & Pages)
- **Vue / Nuxt**
- **Svelte / SvelteKit**
- **Astro**
- **Angular**
- **Vanilla HTML / CSS / TypeScript**
- **Flutter Web / Cross-Platform**
