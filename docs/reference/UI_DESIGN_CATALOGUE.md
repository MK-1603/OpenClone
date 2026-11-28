# OpenClone — Complete UI Design & Architecture Catalogue
**Version:** 1.0.0  
**Scope:** Canonical taxonomy of 86 visual styles and 232 user interface architecture patterns.

---

## 1. The 86 Visual Design Styles

The 86 visual directions are indexed across 6 core aesthetic families:

### Family A: Contemporary Minimalist & Tech Clean (Styles 1–15)
1. **Linear Clean:** High information density, subtle borders (`border-neutral-800`), deep dark background (`#090d16`), monospaced badge accents.
2. **Vercel Monochrome:** High-contrast black and white, zero decorative blur, sharp 4px corners, Geist Sans typography.
3. **Stripe Corporate:** Sophisticated pastel accents, layered cards, clean tabular figures, subtle drop shadows (`0 4px 12px rgba(0,0,0,0.05)`).
4. **GitHub Modern:** Functional gray surfaces (`#161b22`), rounded pill badges, high-contrast text hierarchies, clear git-diff state styling.
5. **Raycast Keyboard-First:** Compact vertical rhythm, command palette focus, prominent shortcut badges (`kbd`), dark graphite backgrounds.
6. **Supabase Neon-Accent:** Dark obsidian canvas (`#121212`) paired with singular vibrant emerald green CTA accents (`#24b47e`).
7. **Apple Human Interface:** Generous whitespace, San Francisco typography, subtle depth, high legibility, accessible focus rings.
8. **Material Design 3:** Tonal palettes, dynamic color extraction, rounded surface containers (16px), floating action buttons.
9. **Radix Primitives Clean:** Functional, unopinionated accessible base with custom token overrides and focus-visible outlines.
10. **Tailwind Default:** Balanced utility-driven zinc palette, responsive grid layouts, standard 6-level typography scale.
11. **Figma Canvas Style:** Dark neutral toolbar framing a stark high-contrast interactive workspace with precise pixel grids.
12. **Notion Editorial:** Off-white canvas, serif headline pairings, inline drag-and-drop handles, distraction-free document layout.
13. **Sublime Text High-Contrast:** Pitch-black background (`#000000`) with vibrant syntax-highlighted data chips.
14. **Graphite Monolith:** Deep slate monochrome (`#1e293b`) with crisp 1px borders and understated silver typography.
15. **Nordic Frost:** Cool blue-gray undertones (`#eceff4`), crisp typography, minimal iconography, high-contrast status pills.

### Family B: Tactile & Skeuomorphic Transitions (Styles 16–30)
16. **Neumorphism Soft:** Dual-source soft bevel lighting (`box-shadow: 6px 6px 12px #d1d5db, -6px -6px 12px #ffffff`) with inset active states.
17. **Frosted Glassmorphism:** Translucent surfaces (`backdrop-filter: blur(16px)`), high-contrast backing scrim (`rgba(15,23,42,0.85)`).
18. **Skeuomorphic Modern:** Tactile buttons with subtle top highlight borders, inset shadows, realistic physical switch toggles.
19. **Claymorphism:** Puffy, rounded pastel shapes with inner glow shadows and soft 3D elevations.
20. **Paper & Ink:** Textured off-white card backgrounds, drop shadows resembling real physical paper layers, serif accents.
21. **Embossed Tech:** Raised surface bevels on dark brushed metal textures with crisp engraved typographic labels.
22. **Brushed Titanium:** Subtle metallic linear gradients with high-contrast chrome divider lines.
23. **Leather & Stitch:** Dark luxury upholstery tones, textured borders, gold/brass accent typography.
24. **Enamel Gloss:** High-gloss reflective surface badges with subtle convex curvature.
25. **Ceramic Smooth:** Ultra-matte porcelain white surfaces with diffused ambient occlusion shadows.
26. **Architectural Blueprint:** Deep cyan background (`#0c4a6e`) with white gridlines, technical crosshairs, and monospaced notes.
27. **Woodcraft Warm:** Organic warm oak and walnut backgrounds, dark chocolate typography, rounded container cards.
28. **Vellum Translucent:** Layered parchment opacity with dark ink calligraphy and traditional book margins.
29. **Rubberized Industrial:** Matte black textured surfaces with high-grip tactile knurling patterns on sliders.
30. **Carbon Fiber:** Textured diagonal twill patterns on dark performance automotive dashboard panels.

### Family C: Brutalist & Monospaced Developer Styles (Styles 31–45)
31. **Neo-Brutalism:** Thick black borders (`3px solid #000000`), hard drop shadows (`4px 4px 0px #000000`), unrounded corners, bold primary fills.
32. **Industrial Brutalism:** Stark geometry, exposed mechanical gridlines, zero decorative fluff, monospaced typography.
33. **Terminal CRT:** Phosphor green (`#22c55e`) or amber (`#f59e0b`) on black canvas with scanlines and blinking block cursors.
34. **Raw Wireframe:** Pure black-and-white structural outlines with placeholder cross boxes and label tags.
35. **Swiss International:** Asymmetric mathematical grid layout, Inter/Akzidenz-Grotesk typography, stark black-and-white contrast.
36. **Bauhaus Functional:** Primary geometric forms (circles, squares, triangles) with red, yellow, and blue primary color blocks.
37. **Constructivist Bold:** Dynamic diagonal layout axes, heavy typographic contrast, stark black and crimson palettes.
38. **ASCII Art Interface:** Text-only user interfaces constructed entirely from ASCII characters and box-drawing glyphs (`┌─┐│└─┘`).
39. **Hacker Console:** Monospaced data tables, hex dumps, green status indicators, zero mouse-dependent interactions.
40. **Xerox Monolith:** High-contrast photocopier aesthetic, halftone stipple patterns, rough black-and-white textures.
41. **Tape Labeler:** Embossed Dymo label tape badges with white capital letters on textured black plastic strips.
42. **Engineering Ledger:** Dual-column accounting rule lines, red margin dividers, serif tabular digits.
43. **Tabular Monospace:** Data-dense tables where every digit and character aligns to a fixed font pitch.
44. **Microfiche Reader:** High-contrast negative microfilm styling with inverted white text on dark navy ground.
45. **Punchcard Punch:** Perforated card patterns, fixed column grids, vintage IBM 7090 computer aesthetics.

### Family D: Expressive, Editorial & Luxury (Styles 46–60)
46. **Editorial Magazine:** Multi-column text flow, large serif pull-quotes, elegant drop capitals, generous white margins.
47. **Luxury Haute:** Midnight black with fine hairline gold rules, Playfair Display typography, understated micro-interactions.
48. **Art Deco Geometric:** Symmetrical chevron patterns, bronze and gold foil borders, tall condensed serif headers.
49. **Cyberpunk Neon:** High-contrast dark violet canvas with electric cyan and magenta wireframe accents.
50. **Vaporwave Nostalgia:** Pastel pink and turquoise gradients, retro 1980s computer icons, grid horizon backgrounds.
51. **Y2K Futuristic:** Metallic bubble typography, translucent frosted plastic accessories, glossy chrome buttons.
52. **Psychedelic Bold:** Fluid organic curves, high-saturation contrasting hues, expressive distorted display typefaces.
53. **Memphis Modern:** Playful squiggles, polka dot patterns, pastel background containers, asymmetric card placement.
54. **Pop Art Comic:** Halftone Ben-Day dots, bold comic ink outlines, bright primary yellow and red speech bubble alerts.
55. **Gothic Victorian:** Dark ornate filigree borders, antique serif typefaces, deep burgundy velvet accents.
56. **Nordic Hygge:** Cozy warm neutral beige canvas, soft sage green pills, natural textured imagery cards.
57. **Japanese Wabi-Sabi:** Asymmetrical natural layouts, earthy unbleached linen tones, calm generous negative space.
58. **Mid-Century Modern:** Warm teak wood accents, olive and mustard yellow containers, atomic era starburst icons.
59. **Solarpunk Organic:** Warm sunlight yellow and leaf green palettes, natural solar motif icons, clean sustainable tech UI.
60. **Vintage Botanist:** Delicate hand-drawn floral line borders, sepia ink tones, traditional specimen label tags.

### Family E: High-Density Enterprise & Data UI (Styles 61–75)
61. **Bloomberg Terminal:** Dark charcoal background, compact orange and amber monospace tabular figures, zero dead margin space.
62. **Data-Dense SaaS:** 32px table row heights, compact status badges, sticky headers, multi-sortable tabular columns.
63. **Developer Console:** Collapsible sidebar tree, unified command palette, integrated log output drawer with filter tabs.
64. **Cockpit Aviation:** Circular flight instrument gauges, high-contrast artificial horizon displays, annunciator warning lights.
65. **Medical Monitor:** High-contrast real-time waveform sweeps, critical alert color bands, large glanceable vital numbers.
66. **Trading Desk Matrix:** Multi-window draggable panels, real-time depth-of-market ladder, red/green price ticker flashes.
67. **Network Topology Map:** Force-directed node-link graph visualization with interactive zoom, pan, and cluster badges.
68. **Telemetry Dashboard:** Live scrolling time-series charts with threshold trigger lines and anomaly markers.
69. **Kubernetes Cluster Monitor:** Grid of hexagonal node cards color-coded by CPU and memory saturation metrics.
70. **CI/CD Pipeline Waterfall:** Sequential stage blocks connected by status lines with real-time streaming step logs.
71. **Database Schema Diagram:** Entity-relationship table cards with foreign-key connector paths and indexed column badges.
72. **Audio DAW Mixing Board:** Vertical volume faders, decibel peak-meter bars, rotary pan knobs, mute/solo toggle buttons.
73. **3D CAD Viewport:** 3-axis coordinate gizmo, wireframe/shaded rendering toggles, hierarchical component tree.
74. **GIS Geospatial Map:** Layered satellite imagery with vector polygon overlays, contour lines, and coordinate HUD.
75. **Security SIEM Matrix:** Threat severity heatmap grid, incident timeline waterfall, correlated IP address links.

### Family F: Specialized & Emerging Interaction Interfaces (Styles 76–86)
76. **AI Chat Stream:** Message bubbles with streaming markdown text, copy-to-clipboard actions, and token metrics.
77. **Agent Canvas:** Infinite zooming canvas with floating agent task nodes, sticky notes, and execution wires.
78. **Spatial OS Windowing:** Translucent floating glass panes with realistic 3D depth, gaze highlights, and pinch targets.
79. **Voice HUD:** Pulsing audio visualizer orb with real-time speech transcription caption banners.
80. **Augmented Reality Overlay:** Contextual bounding boxes anchored to real-world camera feeds with distance telemetry.
81. **Smart Watch Complication:** Ultra-compact circular dial widgets showing battery, heart rate, and schedule rings.
82. **E-Ink Reader:** Pure 1-bit black and white layout, zero animation transitions, high-contrast serif typography.
83. **Automotive Infotainment:** Extra-large touch targets (64px minimum), high contrast for daylight glare, simple navigation tiles.
84. **Kiosk Touchscreen:** High-contrast self-service interactive tiles with large back buttons and session inactivity timers.
85. **Handheld Scanner UI:** High-contrast monospaced inventory lookup with prominent barcode scanner viewfinder.
86. **Head-Up Display (HUD):** Monochromatic green collimated projection graphics with horizon indicators and speed tape.

---

## 2. The 232 User Interface Architecture Taxonomy

The 232 architecture patterns are structured across 8 operational layers:

- **Layer 1: Layout & Spatial Containers (1–30):** Full-bleed canvas, sticky header, collapsible multi-tier sidebar, split-pane resizable layout, masonry grid, holy-grail layout, off-canvas drawer, modal overlay, floating command bar, dashboard multi-grid, infinite scroll viewport, tabbed workspace, floating action dock, card deck carousel, accordion vertical stack, fixed bottom nav, responsive fluid breakpoint shell, asymmetric hero container, bento box grid, full-screen takeover view, drawer sheet, sticky footer banner, dual-panel master-detail, timeline vertical track, stepped wizard frame, fixed sidebar with fluid main, centered content container, multi-column reading flow, canvas graph viewport, HUD frame.
- **Layer 2: Navigation & Wayfinding (31–60):** Top navigation bar, nested breadcrumbs, tab strip with active underline, vertical tree navigation, floating pill navbar, mega-menu dropdown, command palette (Cmd+K), keyboard shortcut quick-switcher, pagination controls, step indicator bar, table of contents sidebar, anchor scrollspy, bottom navigation bar, hamburger menu overlay, hierarchical drill-down menu, back navigation link with history, segmented pill controls, tag cloud filter bar, status badge filter bar, search bar with autocomplete dropdown, jumping quick-nav, multi-workspace switcher, global user avatar menu, project context breadcrumb, notification bell dropdown, flyout sub-menu, dot pagination indicator, swipeable carousel dots, infinite scroll trigger, footer site map.
- **Layer 3: Data Presentation & Visualization (61–95):** Sortable data table, virtualized list, key-value detail list, statistic metric card, time-series line chart, multi-bar chart, donut percentage chart, area trend chart, sparkline mini-graph, heatmap matrix, funnel conversion chart, bubble scatter plot, radar skill chart, tree map container, sankey flow diagram, candlestick financial chart, gauge speedometer, bullet progress graph, milestone timeline, kanban board column, gantt schedule chart, user activity calendar, entity relationship card, JSON code viewer, diff split-view viewer, markdown rendered prose, media gallery grid, file directory tree, tabular comparison matrix, badge chip cluster, avatar stack with count, real-time event log stream, summary stat banner, status annunciator pill, progress bar with percentage.
- **Layer 4: Forms & Input Controls (96–135):** Text input with floating label, password input with toggle show/hide, search input with clear button, multiline textarea with auto-grow, select dropdown with search, multi-select tag input, checkbox with label, radio button group, toggle switch button, range slider with tooltip, dual-thumb range slider, date picker calendar, date range picker, time picker wheel, file dropzone with preview, image crop uploader, color picker swatch, pin code input (OTP), rich text editor, markdown editor with preview, autocomplete combobox, transfer list, editable inline text, rating star bar, segmented button group, increment/decrement stepper, formula math input, currency input with prefix, telephone input with country flag, code editor with syntax highlighting, form validation error banner, inline field error message, field helper text, required field asterisk indicator, password strength meter, dirty form unsaved changes bar, multi-step form wizard, bulk action checkbox toolbar, drag-and-drop sortable list, reset form button.
- **Layer 5: Feedback & Status Indicators (136–165):** Toast notification banner, top alert callout, inline info note, confirmation modal dialog, full-screen loading spinner, skeleton placeholder card, circular progress ring, linear indeterminate progress bar, pinging live activity dot, status badge pill, empty state illustration with CTA, error state banner with retry button, 404 not found page, 500 server error view, offline connection banner, unsaved changes pill, auto-save status indicator, tooltip hover popover, interactive guided walkthrough tour, feature announcement banner, quota usage limit bar, success celebration screen, warning confirmation sheet, session timeout warning modal, destructive action double-confirm modal, copy to clipboard confirmation toast, sync in progress indicator, webhook delivery status pill, rate limit cooling banner, maintenance mode announcement.
- **Layer 6: Overlays, Menus & Dialogs (166–195):** Centered modal dialog, slide-over right sheet, slide-over bottom sheet, contextual right-click menu, dropdown menu from trigger, popover information card, hover preview card, command search dialog, image lightbox overlay, video player modal, cookie consent banner, onboarding welcome dialog, multi-level action sheet, dropdown date selector, user profile flyout, notification drawer, floating action button menu, sticky bottom filter bar, confirmation popover, tool shortcut cheat sheet modal, fullscreen presentation mode, mobile bottom sheet with snap points, multi-select bulk actions bar, quick edit flyout, export format picker dialog, import file review modal, print preview dialog, feedback submission modal, invite team member modal, subscription upgrade paywall modal.
- **Layer 7: Micro-Interactions & Motion Behavior (196–215):** Button press scale down (`active:scale-95`), hover elevation lift (`hover:-translate-y-0.5`), card border glow on hover, accordion smooth expansion, tab indicator sliding glide, toast slide-in from bottom right, modal fade-in and scale-up, skeleton shimmer wave, ripple click effect, toggle switch spring slide, drag-and-drop ghost element, drag over highlight border, smooth height auto-transition, dropdown scale-down entry, tooltip fade-in with delay, number counter animation, page transition crossfade, pull-to-refresh spinner, swipe to delete revealing red action, progress bar filling animation.
- **Layer 8: Accessibility & Ergonomics (216–232):** Skip to main content link, high-contrast focus visible ring (`focus-visible:ring-2`), ARIA live region for dynamic alerts, screen reader only text (`sr-only`), keyboard navigation tab order, accessible name on icon buttons, contrast-compliant text ratio (4.5:1), reduced-motion media query override, large touch target bounds (44px minimum), zoom scaling layout safety (up to 200%), dark mode color inversion token, colorblind-safe status palette, readable line length constraints (60–80ch), dyslexic font alternative option, clear visual link underline, sticky header accessible collapse, text resizing support without horizontal scroll.
