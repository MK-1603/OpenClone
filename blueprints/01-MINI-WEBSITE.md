# Blueprint 01: Mini Website & Landing Page

**Project Family:** `web_engineering`  
**Primary Project Type:** `mini_website`  
**Maturity Status:** `OPERATIONAL`  
**Complexity Level:** `MINI`  
**Default Delivery Targets:** `web_browser`

---

## 1. Goals & Scope
- High-converting, fast-loading marketing websites, documentation sites, product launch landing pages, or portfolios.
- Scope emphasizes Core Web Vitals (LCP < 2.5s, CLS < 0.1), WCAG 2.2 AA accessibility, SEO metadata, and responsive typography.
- Explicit non-goals: complex multi-tenant databases, server-side background job workers, user account sessions, or payment subscription recurring billing.

## 2. Classification Rules
- Matched if requirements describe static content, single-page presentation, product landing page, or documentation site without user accounts.
- If dynamic authentication, multi-tenancy, or user databases are required, classify up to `saas_web_app`.

## 3. Intake Questions & Required Information
1. Target audience and key conversion action (e.g. newsletter signup, app download, documentation exploration).
2. Content structure: hero section, value propositions, feature highlights, testimonials, pricing cards, FAQ, footer.
3. Brand guidelines: color palette, typography, logo SVG, dark/light theme requirements.
4. Deployment destination: Cloudflare Pages, Vercel, Netlify, or static S3 bucket.

## 4. Conditional Requirements
- If lead capture form exists: integrate serverless API endpoint or form provider (e.g., Formspree, Resend) with CSRF and rate limiting.
- If analytics required: privacy-first analytics (Plausible, Fathom) without intrusive tracking cookies.

## 5. Domain & Capability Mapping
- **Mandatory Domains:** `01-SPECIFICATION`, `05-DESIGN-SYSTEMS`, `06-UX-RESEARCH`, `07-ACCESSIBILITY-AND-INCLUSION`, `14-PERFORMANCE-ENGINEERING`.
- **Mandatory Engines:** `E-001` (Specification), `E-007` (Accessibility), `E-008` (API Contracts / Form Endpoints), `E-014` (Performance), `E-056` (Taste Skill).
- **Excluded Domains:** `11-PERMISSIONS-AND-ACCESS-CONTROL`, `17-INCIDENT-RESPONSE`, `21-DATA-MIGRATION-AND-ROLLBACK`.

## 6. Specialist Workforce (Minimum Effective Team)
- `frontend-engineer`: Implements semantic HTML5, responsive layout, CSS/Tailwind styling, and client state.
- `ui-designer`: Establishes design tokens, component spacing, typography scale, and visual hierarchy.
- `accessibility-specialist`: Audits WCAG 2.2 AA compliance, color contrast, keyboard navigation, and screen reader labels.

## 7. Tool & Model Allocation
- **Primary Model:** `gpt-6.2-sol` (efficient, high-fidelity UI generation).
- **Visual Audit Model:** `gpt-6.1-terra` (computer vision validation of layout and responsive screenshots).

## 8. Workflow Stages
1. `WF-001`: Project Discovery & Baseline Initialization.
2. `WF-002`: Content specification & wireframe structure.
3. `WF-009`: Human approval of layout blueprint and copy.
4. `WF-004`: Implementation of responsive component hierarchy.
5. `WF-008`: Taste Skill visual review & WCAG 2.2 AA accessibility audit.
6. `WF-006`: Automated build and link verification.

## 9. Verification & Delivery Artifacts
- Static build output in `dist/` or `out/`.
- Lighthouse Performance score > 95, Accessibility score = 100.
- Zero broken links verified by `check_links.py`.
- Evidence of responsive rendering across mobile (375px), tablet (768px), and desktop (1440px).
