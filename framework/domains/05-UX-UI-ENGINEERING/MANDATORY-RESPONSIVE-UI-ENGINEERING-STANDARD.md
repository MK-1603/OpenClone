# Mandatory Responsive UI Engineering Standard
## OpenClone Quality Gate & Mobile-First Interaction Contract

---

## 1. Principle & Scope

Every user-facing application built with or deployed under OpenClone must adhere to a **responsive, mobile-first design and development standard**.

Mobile responsiveness is not an optional polish phase or a post-launch optimization; it is a fundamental architectural requirement. Applications must be designed, structured, and implemented for mobile viewports concurrently with desktop viewports.

---

## 2. The 10 Non-Negotiable Core Rules

1. **Concurrent Mobile-First Implementation:** Design and implement mobile layouts alongside desktop layouts from the initial sprint. Never defer mobile adaptation to later refactors.
2. **Comprehensive Breakpoint Coverage:** The application must cleanly support:
   - Small mobile: **320px**
   - Standard mobile: **375px**
   - Large mobile: **430px**
   - Tablet / Hybrid: **768px**
   - Laptop: **1024px** and **1280px**
   - Desktop / Ultra-wide: **1440px+**
3. **Fluid Layouts & Adaptive Spacing:** Use flexible containers (`max-w-7xl`, `w-full`), fluid typography, and proportional spacing (`gap-3 sm:gap-6`, `p-3 sm:p-6`). Never use fixed pixel container widths exceeding viewport dimensions.
4. **Zero Horizontal Overflow:** Eliminate unintended horizontal scrolling (`overflow-x-hidden` on root bodies; wrap tables in momentum-scrolling touch containers `overflow-x-auto`).
5. **Adaptive Navigation Systems:** Desktop sidebars and persistent navigation bars must transform into touch-friendly off-canvas drawers, modal sheets, or bottom navigation bars on screens `< 768px`.
6. **Touch-Target Sizing:** All interactive elements (buttons, nav links, icon toggles, dropdowns, inputs) must maintain a minimum touch target size of **44x44 CSS pixels** to prevent accidental input on mobile devices.
7. **Component Transformation Over Mere Shrinking:** Complex desktop components (e.g. multi-column data tables, kanban boards) must adapt into mobile-tailored card views, collapsed accordions, or horizontally swipeable tabs rather than illegibly scaling down desktop layouts.
8. **Responsive Media & Data Visualizations:** Images, SVG charts, and metric displays must adapt gracefully using responsive viewBox parameters, SVG preserveAspectRatio rules, and responsive grid wrappers (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`).
9. **Dynamic Viewport & Keyboard Handling:** Interfaces must withstand virtual keyboard appearance, dynamic mobile browser address bars (`dvh` / `svh` units), and device orientation shifts without clipping modals or interactive controls.
10. **A11y, Contrast & Visual Hierarchy:** Maintain WCAG 2.2 AA contrast ratios, fluid readable typography (minimum 14px body text on mobile), and prominent visual hierarchies regardless of device screen size.

---

## 3. Responsive Breakpoint Matrix & Verification Targets

| Device Category | Target Viewport Width | Required Adaptation Pattern | Primary Acceptance Criteria |
|---|---|---|---|
| **Small Mobile** | **320px** | Single-column stack, collapsed drawer, full-width modals | Zero horizontal overflow; text legible; 44px tap targets |
| **Standard Mobile** | **375px** | Single-column layout, bottom/off-canvas drawer navigation | Search & filters accessible; modals bounded to `90vh` |
| **Large Mobile** | **430px** | Enhanced 1-col or 2-col metric cards | Smooth touch scrolling; touchable action menus |
| **Tablet** | **768px** | 2-column grids, collapsible desktop sidebar or top nav | Balanced layout density; accessible side panels |
| **Laptop** | **1024px – 1280px** | Full multi-column dashboard, persistent sidebar | Fluid main content container (`max-w-7xl mx-auto`) |
| **Desktop / Wide** | **1440px+** | Centered high-density layout, secondary utility drawers | Optimal reading line-lengths; zero stretched full-bleed text |

---

## 4. Complex Component Adaptation Guidelines

### A. Sidebars and Global Navigation
- **Desktop (`>= 768px`):** Persistent or collapsible side rail (`w-64` or `w-20`).
- **Mobile (`< 768px`):** Off-canvas slide-out drawer with a darkened backdrop (`bg-black/60`). Clicking outside or selecting a navigation target automatically closes the drawer. Accessible via a header hamburger button.

### B. Data Tables vs Mobile Cards
- **Desktop:** Multi-column grid with sorting, pagination, and inline controls.
- **Mobile:** Render table rows as independent summary cards with key metadata badges, or wrap table in an `overflow-x-auto` container with visual fade indicators indicating horizontal scrollability.

### C. Modals and Dialog Windows
- **Desktop:** Centered floating dialogs (`max-w-lg mx-auto`).
- **Mobile:** Responsive bottom sheet or centered card constrained to `w-[calc(100vw-24px)]` and `max-h-[90vh]` with internal vertical scrolling so action buttons never get clipped beneath the mobile keyboard.

---

## 5. Responsive Verification & Completion Gate

A user-facing application must **never** be marked complete based solely on desktop appearance.

Before sign-off:
1. Verify small mobile (320px), standard mobile (375px), tablet (768px), and desktop (1440px).
2. Validate zero unintended horizontal scrolling across all views.
3. Verify touch navigation toggles, modals, and forms open and close properly.
4. Verify automated responsive tests (`pytest tests/test_responsive_ui.py`) pass with 100% success.
