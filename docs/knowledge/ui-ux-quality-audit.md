# UI/UX Quality Audit Protocol
**11-Dimension Weighted Quality Scoring System & AI-Slop Elimination Guide**  
*OpenClone Global Design Intelligence | Target: Bridging the 80–90% Quality Gap to Production Grade*

---

## 1. Why AI-Generated UI Stalls at 80–90%

Many AI-assisted development projects produce interfaces that initially seem acceptable but stall at an unpolished "80–90%" feel. The root causes are systematically identifiable:

1. **Generic Aesthetic Convergence**: Defaulting to clichéd purple/indigo gradients, floating blur blobs, and repetitive rounded cards across unrelated products.
2. **Missing Component States**: Implementing the default "happy path" while neglecting hover, focus-visible, active-press, disabled, empty, loading, error, and offline states.
3. **Mobile Viewport Neglect**: Treating mobile responsiveness as simply squeezing desktop 3-column grids into a single narrow column, resulting in awkward whitespace and unreachable controls.
4. **Weak Information Hierarchy**: Headings are oversized, secondary text is too small or faint, and key user actions lack visual prominence.
5. **Lack of Motion Purpose**: Adding animations as decorative afterthoughts rather than using motion to communicate state transitions, feedback, and spatial continuity.
6. **Inaccessible Contrast & Touch**: Low contrast grey-on-dark text and touch targets smaller than 44x44px.

---

## 2. The 11-Dimension Weighted Quality Audit (100 Points Total)

Every user interface is audited across 11 dimensions scored from 0 to 5.
Weighted Score = $\sum (\text{Dimension Score} / 5) \times \text{Weight}$.

| Dimension | Weight | What to Inspect | Scoring Rubric (0–5) |
|---|:---:|---|---|
| **1. Product Identity & Art Direction** | **12** | Does the interface possess a deliberate, product-specific identity tailored to its domain (DevTools, Healthcare, Fintech)? | 0 = Generic template<br/>3 = Competent baseline<br/>5 = Distinctive, bespoke, purposeful |
| **2. Layout & Information Hierarchy** | **12** | Is information scannable? Are primary actions immediately obvious? Are reading widths constrained to 65ch? | 0 = Cluttered/disorganized<br/>3 = Clear sections<br/>5 = Flawless visual hierarchy |
| **3. Typography** | **10** | Consistent type scale (Major Third/Perfect Fourth), strict line lengths, readable line-heights, optical weight pairings. | 0 = Chaotic font sizes<br/>3 = Standard scale<br/>5 = Editorial-grade typography |
| **4. Color & Contrast** | **8** | Semantic color system (Primary, Neutral, Success, Warning, Danger), WCAG 2.2 AA contrast (4.5:1 min), restraint. | 0 = Unreadable / clownish<br/>3 = Brand aligned<br/>5 = Harmonious, accessible palette |
| **5. Spacing & Composition** | **8** | Strict 8-point spatial grid, consistent inner card padding, balanced negative space, zero crowded collisions. | 0 = Arbitrary spacing<br/>3 = Grid aligned<br/>5 = Rhythmic spatial perfection |
| **6. Components & States** | **10** | Complete interactive states: Default, Hover, Active, Focus, Disabled, Loading (skeleton), Empty, Error, Success. | 0 = Missing states<br/>3 = Basic hover/focus<br/>5 = Complete, tactile states |
| **7. Responsive Behavior** | **10** | Deliberately designed layouts across 390px (Mobile), 768px (Tablet), 1024px (Laptop), 1440px+ (Desktop). | 0 = Broken overflow<br/>3 = Responsive stacking<br/>5 = Native-feeling responsive adaptations |
| **8. Interaction & Usability** | **8** | Intuitive navigation, clear error recovery, immediate user feedback, keyboard focus traps in modals. | 0 = Confusing UX<br/>3 = Predictable workflows<br/>5 = Frictionless, joyful interaction |
| **9. Motion & Transitions** | **6** | Microinteractions (<250ms), view transitions, spring physics, `@media (prefers-reduced-motion: reduce)` support. | 0 = Jarring or absent<br/>3 = Smooth basic fades<br/>5 = Cinematic, performant continuity |
| **10. Accessibility (a11y)** | **8** | Keyboard navigable, screen-reader landmarks (`<main>`, `<nav>`), ARIA labels, 44x44px minimum touch targets. | 0 = Inaccessible<br/>3 = Standard a11y<br/>5 = WCAG 2.2 AAA compliant |
| **11. Craft & Visual Polish** | **8** | High-resolution assets, pixel-aligned SVG icons, crisp borders, subtle elevation layering, zero layout shift. | 0 = Rough rough-edges<br/>3 = Clean assembly<br/>5 = Master craftsmanship |
| **Total** | **100** | | |

### Score Interpretation
- **95–100**: Exceptional; studio-grade engineering. Ready for premier production release.
- **90–94**: Premium and robust; surpasses standard commercial benchmarks.
- **80–89**: Competent but contains noticeable AI slop or unpolished edges (requires refinement).
- **70–79**: Inconsistent; another full design iteration is mandatory.
- **Below 70**: Reject and re-engineer.

---

## 3. The 6-Stage Premium Design Execution Protocol

To close the quality gap from 85% to 95%+, coding agents must follow this sequential protocol:

```text
Stage A: UNDERSTAND INTENT & CONSTRAINTS (Domain, Users, Business Goal)
                       ↓
Stage B: ESTABLISH ART DIRECTION (Personality, Color Restraint, Density)
                       ↓
Stage C: DEFINE DESIGN TOKENS (Type Scale, 8pt Grid, 5-Tier Surfaces)
                       ↓
Stage D: BUILD VERTICAL SLICE (Representative screen with ALL 9 states)
                       ↓
Stage E: MULTI-VIEWPORT CRITIQUE (390px, 768px, 1024px, 1440px + a11y)
                       ↓
Stage F: POLISH & RETEST (Audit against 11-dimension matrix -> Score >= 92)
```

### Mandatory AI-Slop Checklist Before Completion
- [ ] Does this interface avoid generic purple/blue background glows?
- [ ] Are cards used only where semantic grouping is necessary (not wrapping everything in identical cards)?
- [ ] Are real, domain-specific text and numbers used instead of generic "Lorem Ipsum" or fake "99.9% uptime" stats?
- [ ] Does the mobile view feel deliberately designed rather than a crushed desktop view?
- [ ] Are all buttons and interactive controls at least 44x44px?
- [ ] Does every animation support `prefers-reduced-motion`?
