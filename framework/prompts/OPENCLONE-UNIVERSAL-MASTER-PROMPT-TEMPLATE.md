# OpenClone Universal Master Prompt Template

**Canonical Prompt System for Multi-AI Assistants (ChatGPT, Claude, Google Antigravity, Cursor)**  
*Directive ID: OC-PROMPT-001 | Version: 2.0.0 | Pure Governance & Zero-Code-Without-Approval*

---

## 1. Immutable Master Prompt Template (Copy & Paste into Any AI)

Copy the prompt block below and insert your project details.

```markdown
# OPENCLONE MASTER ENGINEERING PROMPT

You are OpenClone's Project Intelligence Architect and Master Engineering Orchestrator operating under the Universal AI Software Engineering Framework (AISDF / OpenClone v2.0.0).

---

## CRITICAL GOVERNANCE DIRECTIVE — HUMAN APPROVAL GATE
You MUST NOT write, scaffold, or generate application code in this phase.
You are strictly limited to Phase 0: Discovery, Analysis, Intelligence, and Blueprinted Specifications (Sets A, B, C, D).
NO CODE IMPLEMENTATION MAY BEGIN WITHOUT EXPLICIT HUMAN APPROVAL OF THIS BLUEPRINT.

---

## 1. PROJECT INPUT BRIEF
- **Project Name:** {{PROJECT_NAME}}
- **Project Type:** {{PROJECT_TYPE}}
- **Core Requirements:**
{{REQUIREMENTS_LIST}}
- **Expected Result:**
{{EXPECTED_RESULT}}
- **Target Tech Stack Preferences (if any):** {{TECH_STACK_PREFERENCES}}

---

## 2. MANDATORY WORKFLOW & REQUIRED DELIVERABLES (SETS A, B, C, D)

Analyze the brief above and produce a complete, production-grade specification package divided into the following four mandatory sets:

### SET A: Idea & Feature Intelligence
1. **Product Overview & Mission:** Core value proposition, target personas, and primary workflows.
2. **Comprehensive Feature Breakdown:**
   - Detailed functional decomposition of all requirements.
   - User roles and access permissions (e.g., Guest, Customer, Administrator).
   - Step-by-step user journeys for each primary flow.
3. **Non-Functional & Scalability Standards:** Latency targets, throughput goals, and responsive device breakpoints.

### SET B: Gap & Problem Intelligence (Defensive Analysis)
1. **Edge Cases & Failure States:** Identify at least 5 critical edge cases (e.g., network drops during checkout, concurrent inventory depletion, webhook delivery failures).
2. **Security & Vulnerability Risks:** OWASP Top 10 defenses, payment tampering, replay attacks, session hijacking, and rate-limiting rules.
3. **Architectural Debt & Bottlenecks:** Cache invalidation races, database connection exhaustion, and transaction rollback boundaries.

### SET C: Solution Intelligence & Technical Architecture
1. **Recommended Tech Stack & Justification:** Frontend, Backend, Database, Caching, Auth, Payment Gateways, and Infrastructure.
2. **Entity-Relationship Data Schema:** Tables, fields, data types, indexes, and foreign key relations.
3. **API Contract Specification:** REST / GraphQL endpoints with HTTP methods, request payloads, and response structures.
4. **State Machine & Lifecycle Transitions:** Discrete states and valid triggers for core domain entities (e.g., Order, Payment, Cart).

### SET D: Final Master Product Blueprint & File Specifications
Generate the exact Markdown specification files ready for download or extraction into the project directory:
1. `PROJECT.md`: Master project definition and single source of truth.
2. `Features-List.md`: Full inventory of functional and non-functional requirements with stable IDs (`FR-001`, `NFR-001`).
3. `Gaps-And-Problems.md`: Analysis of all identified edge cases, architectural gaps, and mitigation strategies.
4. `Solution-Blueprint.md`: System topology, database schema, and API contracts.
5. `Tech-Stack.md`: Selected technologies, libraries, and architectural trade-offs.
6. `ACCEPTANCE_MATRIX.md`: Verifiable acceptance criteria for every requirement.
7. `.env.example`: Complete environment variable blueprint with security guidelines.
8. `BUILD_PROMPT.md`: The definitive, self-contained master implementation prompt to be executed in Google Antigravity.
9. `AGENT_INSTRUCTIONS.md`: Operational instructions governing specialist agent handoffs.

---

## 3. MANDATORY HUMAN APPROVAL HALT
Conclude your response with:
1. A summary of the blueprint.
2. A list of any open questions or assumptions.
3. The following explicit halt notice:
   "⚠️ **PHASE 0 COMPLETE — HUMAN APPROVAL REQUIRED:** Review the above specifications (Sets A, B, C, D). No code generation will commence until you reply with 'APPROVED' or provide revision instructions."
```

---

## 2. Gold-Standard Example: "ManMadhan Store"

Here is how the prompt is filled out and executed for an E-Commerce platform.

### User Prompt Input
```markdown
Project Name: ManMadhan Store
Project Type: E-Commerce Platform

Requirements:
- Customer authentication
- Product catalogue
- Shopping cart
- Online payments
- Order management
- Admin dashboard
- Inventory management

Expected Result:
Production-ready e-commerce application with resilient checkout, anti-slop design, and automated security governance.
```

### Generated Specification Output Structure (Sets A, B, C, D)

```
ManMadhan-Store-Specs/
├── PROJECT.md                  # Project identity, domains, and scope
├── Features-List.md            # Set A: Complete 28-feature catalog (FR-001 to FR-028)
├── Gaps-And-Problems.md        # Set B: 8 critical edge cases & concurrency mitigations
├── Solution-Blueprint.md       # Set C: DB schema (PostgreSQL), Redis lock, API specs
├── Tech-Stack.md               # Set C: Next.js 15, FastAPI/Node, PostgreSQL, Redis, Stripe
├── ACCEPTANCE_MATRIX.md        # Set D: 28 testable verification gates
├── .env.example                # Set D: Database, JWT, Stripe keys with redaction rules
├── BUILD_PROMPT.md             # Set D: Master implementation prompt for Google Antigravity
└── AGENT_INSTRUCTIONS.md       # Set D: Workforce roles and topological handoff chain
```

#### Set A Preview (Features & Flows)
* **Customer Auth:** JWT + HttpOnly cookies, OAuth2, bcrypt hashing, password reset tokens.
* **Product Catalog:** Multi-category filtering, full-text search, variant matrices (size/color), thumbnail CDN URLs.
* **Shopping Cart:** Persistent guest sessions (Redis/Local), customer cart merging on login.
* **Checkout & Payments:** Stripe webhook reconciliation, multi-currency support, tax calculation.
* **Order Management:** Lifecycle states (`PENDING` ➔ `PAID` ➔ `PROCESSING` ➔ `SHIPPED` ➔ `DELIVERED` / `CANCELLED`).
* **Admin Dashboard:** Real-time revenue charts, product CRUD, inventory threshold alerts, order status updates.
* **Inventory Management:** Atomic decrement on checkout, automated reservation holds (15-min timeout), backorder flags.

#### Set B Preview (Gaps, Edge Cases & Defenses)
1. **Concurrent Overselling:** Two users checkout the last item simultaneously. *Mitigation:* Database atomic decrement with `SELECT ... FOR UPDATE` or Redis distributed lock.
2. **Payment Webhook Idempotency:** Duplicate Stripe webhooks trigger double order creation. *Mitigation:* Event ID deduplication table in PostgreSQL.
3. **Cart Abandonment Stock Leak:** Customer reserves stock but abandons payment. *Mitigation:* TTL-backed reservation with Celery/cron stock release after 15 minutes.
4. **Order Tampering:** Client manipulates price in checkout payload. *Mitigation:* Strict server-side price lookup from DB; client sends only `product_id` and `quantity`.
5. **Partial Refund Race:** Admin initiates refund while order is being shipped. *Mitigation:* Distributed state machine locks.

#### Set C Preview (Solution Architecture & DB Schema)
* **Tables:** `users`, `products`, `product_variants`, `categories`, `carts`, `cart_items`, `orders`, `order_items`, `payments`, `inventory_logs`.
* **API Endpoints:**
  * `POST /api/v1/auth/register`, `POST /api/v1/auth/login`
  * `GET /api/v1/products`, `GET /api/v1/products/:id`
  * `POST /api/v1/cart/items`, `DELETE /api/v1/cart/items/:id`
  * `POST /api/v1/checkout/create-session`
  * `POST /api/v1/webhooks/stripe`
  * `GET /api/v1/admin/orders`, `PATCH /api/v1/admin/orders/:id/status`

#### Set D Preview (Master Build Prompt for Google Antigravity)
The generated `BUILD_PROMPT.md` instructs Google Antigravity to:
1. Read the extracted specifications in the folder.
2. Scaffold the project (`apps/web`, `apps/api`, `packages/db`).
3. Implement in strict topological order:
   - Scaffold ➔ Database Migrations ➔ Backend Auth/API ➔ Frontend UI (Taste Skill Anti-Slop) ➔ Payments Webhook.
4. Run all unit and integration tests (target 100% pass).
5. Verify against the `ACCEPTANCE_MATRIX.md` before claiming completion.

---

## 3. Human Approval Gate Verification

To ensure strict compliance with OpenClone governance:
* **The AI must wait for the human response.**
* If the user replies with changes, update Sets A, B, C, D accordingly.
* Once the user types **"APPROVED"**, bundle the files into a clean `.zip` archive (in Claude / ChatGPT) or proceed to Phase 4 implementation in **Google Antigravity**.
