# PULSE — Project Command Center
## OpenClone Frontend Engineering Demonstration

> **Positioning:** "Everything in Motion. One Clear Direction."  
> **Framework:** OpenClone Universal AI Engineering Platform  
> **Scope:** High-fidelity interactive SaaS frontend application  
> **Tech Stack:** Next.js 15, React 19, TypeScript, Tailwind CSS, Lucide Icons, Local State Persistence

---

## 1. Overview

**PULSE** is a commercial-grade project command center designed for engineering leads, startup founders, product managers, and agile software development teams. It unifies project management, sprint execution, burndown metrics, and team capacity into a focused, low-cognitive-overhead command console.

Built in strict compliance with the **OpenClone Taste Skill & Anti-Slop Design Guidelines**, PULSE replaces generic AI dashboard aesthetics (neon gradients, purple blur blobs, excessive glassmorphism) with a restrained deep charcoal (`#0A0A0A`) and restrained gold (`#D6B36A`) design system.

---

## 2. Architecture & Directory Structure

```
examples/pulse/
├── package.json                   # Next.js 15, React 19, Tailwind, Lucide React
├── tsconfig.json                  # Strict TypeScript configuration
├── tailwind.config.js             # Semantic design tokens & color system
├── next.config.js                 # Next.js configuration
├── src/
│   ├── app/
│   │   ├── layout.tsx             # Root layout with dark theme & metadata
│   │   └── page.tsx               # App entrypoint wrapping PulseProvider & AppShell
│   ├── components/
│   │   ├── layout/
│   │   │   ├── AppShell.tsx       # Global application shell & view coordinator
│   │   │   ├── Header.tsx         # Breadcrumbs, search, quick create, alerts, profile
│   │   │   └── Sidebar.tsx        # Collapsible navigation, workspaces, governance pill
│   │   ├── modals/
│   │   │   ├── CreateProjectModal.tsx  # Project creation with category & owner assignment
│   │   │   ├── CreateTaskModal.tsx     # Task creation with column selection & tags
│   │   │   ├── QuickCreateModal.tsx    # Multi-action quick create dialog
│   │   │   └── ConfirmDeleteModal.tsx  # Safe deletion confirmation dialog
│   │   └── views/
│   │       ├── DashboardView.tsx       # Overview, KPIs, SVG productivity chart, health
│   │       ├── ProjectsView.tsx        # Portfolio with grid/list toggles, search, filters
│   │       ├── TasksView.tsx           # 5-column interactive Kanban board & list view
│   │       ├── CalendarView.tsx        # Monthly & weekly schedule grid with task agenda
│   │       ├── AnalyticsView.tsx       # Sprint velocity, burndown rate, workload distribution
│   │       ├── TeamView.tsx            # Member roster, avatars, workload capacity bars
│   │       ├── ActivityView.tsx        # Chronological audit timeline with event filters
│   │       └── SettingsView.tsx        # Preferences, theme toggles, local persistence
│   ├── context/
│   │   └── PulseContext.tsx       # Centralized state management with localStorage sync
│   ├── data/
│   │   ├── mock-projects.ts       # 6 realistic engineering projects
│   │   ├── mock-tasks.ts          # 10 deliverables with priorities & tags
│   │   ├── mock-team.ts           # 6 cross-functional team members
│   │   └── mock-activities.ts     # Chronological execution audit events
│   ├── styles/
│   │   └── globals.css            # Base styles, dark surfaces, custom scrollbar
│   └── types/
│       └── index.ts               # Complete TypeScript interfaces & union types
└── README.md
```

---

## 3. Design System & Tokens

### Color Palette
- **Primary Background (Deep Charcoal):** `#0A0A0A`
- **Secondary Surface:** `#111111`
- **Elevated Surface:** `#181818`
- **Primary Text:** `#F5F5F5`
- **Secondary Text:** `#A1A1AA`
- **Muted Text:** `#71717A`
- **Accent (Restrained Gold):** `#D6B36A` (Hover: `#E0C58A`, Border: `rgba(214, 179, 106, 0.3)`)
- **Supporting Semantics:**
  - Success: `#10B981` (Muted: `#064E3B`, Text: `#34D399`)
  - Warning: `#F59E0B` (Muted: `#78350F`, Text: `#FBBF24`)
  - Error: `#EF4444` (Muted: `#281515`, Text: `#F87171`)
  - Information: `#3B82F6` (Muted: `#1E3A8A`, Text: `#60A5FA`)

---

## 4. Key Functional Capabilities

### A. Dashboard Overview
- Executive welcome banner with date and urgent action counter.
- 4 top-level KPI cards: Active Projects, Task Completion Rate, Pending Deliverables, and Velocity.
- Weekly productivity SVG bar chart displaying engineering committed hours.
- Real-time project health radar and recent activity stream.

### B. Project Portfolio
- Grid and list view toggles.
- Real-time search across names, descriptions, and categories.
- Filtering by status (`In Progress`, `Planning`, `Review`, `Completed`) and categories.
- Interactive project creation modal and safe deletion confirmation.

### C. Sprint Task Board (Kanban & List)
- 5 status columns: `Backlog` → `Todo` → `In Progress` → `Review` → `Completed`.
- Task card actions: Move left/right between sprint columns or delete.
- Priority tagging: `Urgent` (red), `High` (amber), `Medium` (gold), `Low` (blue).
- Fast filter by project association or priority level.

### D. Schedule & Calendar
- Full 30-day interactive month grid with daily scheduled event chips.
- Selected day agenda pane showing assigned deliverables, owners, and due dates.
- Previous/next month navigation controls.

### E. Analytics & Performance
- Sprint velocity chart comparing Planned vs Delivered story points across 6 sprints.
- Resource workload distribution across Engineering, Product, Design, and DevOps.
- Key metrics: Burndown rate (96.6%), cycle time (2.4 days), health distribution.

### F. Team Roster & Capacity
- Member cards with avatars, roles, departments, active tasks, and shipped items.
- Workload capacity progress bars indicating team bandwidth and burn.
- Direct email contact links and real-time status indicators (`Active`, `In Meeting`, `Offline`).

### G. Audit Activity Stream
- Date-grouped chronological timeline of task transitions, project allocations, and milestones.
- Filter by event type (`Tasks`, `Projects`, `Milestones`).

### H. Settings & Persistence
- User profile overview (Elena Rostova - Principal Product Architect).
- Theme selection (Charcoal Dark, Midnight Dark, Pure OLED).
- Notification toggles (Critical Task Alerts, Weekly Digest Email).
- All changes automatically synchronized with browser `localStorage`.

---

## 5. Getting Started

### Installation
```bash
cd examples/pulse
npm install
```

### Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build
```bash
npm run build
npm run start
```
Verified production build output:
```
Route (app)                                 Size  First Load JS
┌ ○ /                                    21.1 kB         124 kB
└ ○ /_not-found                            994 B         104 kB
+ First Load JS shared by all             103 kB
```
Zero linting errors, strict TypeScript conformance, 100% static pre-render.
