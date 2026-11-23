# Anti-AI-Slop Governance & Visual Pattern Evaluation

**Operating Rule:** Stop generic AI-generated UI. Every visual decision must be functional, justifiable, and authentic.

---

## 1. Visual Slop Catalogue

AI coding agents habitually assemble pages using identical, clichéd visual tropes. The Anti-Slop Engine catalogs and evaluates these patterns:

| Pattern | Typical Manifestation | Assessment Strategy |
|---|---|---|
| **Unnecessary Glassmorphism** | `backdrop-filter: blur()`, translucent cards everywhere | Check contrast and surface hierarchy. Replace with solid elevated surfaces. |
| **Purple/Blue AI Palette** | Repetitive violet `#8b5cf6` + cyan `#06b6d4` gradients | Ban as default palette unless specifically part of verified client brand tokens. |
| **Floating Background Blobs** | Blurred colored circles (`blur-3xl`) drifting behind text | High severity slop. Remove unless product is generative AI art studio. |
| **Identical Rounded Card Grids** | 3x3 identical cards with centered icon, heading, short text | Monotonous layout. Replace with varied editorial sections or data tables. |
| **Meaningless Decorative Icons** | Lucide/Feather icons placed on every card as visual filler | Remove icons that do not provide functional orientation. |
| **Excessive Badges & Pills** | Every title preceded by "✨ The Future of Work" pill | Eliminate filler badges. Reserve badges strictly for dynamic system statuses. |
| **Unnecessary Glows & Drop Shadows** | `box-shadow: 0 0 40px rgba(...)` on static elements | Degrades visual clarity and performance. Clean surface borders win. |
| **Fabricated Metrics & Testimonials** | "99.9% Happier", quotes from "Sarah Jenkins, VP of Ideas" | Remove fake trust indicators. Use real customer case studies or omit. |

---

## 2. Decision Classification Matrix

Do not blindly prohibit visual elements; evaluate them in product context:

* **REQUIRED:** Critical functional UI (e.g. status badge on active server instance, monospace font on code block).
* **JUSTIFIED:** Visually enhances communication for the specific product domain (e.g. WebGL shader on 3D game studio landing page).
* **OPTIONAL:** Harmless micro-enhancement that does not impair readability or performance.
* **UNNECESSARY:** Purely decorative visual noise that clutters the composition without aiding comprehension. Must be REDUCED or REMOVED.
* **PROHIBITED:** Clichéd AI aesthetics, deceptive fabricated social proof, unreadable low-contrast layers. Must be REMOVED immediately.

---

## 3. Audit Output Format

Every slop audit finding generates an explicit action record:

```text
Pattern: Excessive glassmorphism
Severity: Medium
Evidence: 12 translucent cards across 3 sections with backdrop-filter: blur(16px)
Recommendation: Replace decorative glass panels with solid surface tokens.
Action: REMOVE
Reason: Improves readability, accessibility contrast, and scroll performance.
```
