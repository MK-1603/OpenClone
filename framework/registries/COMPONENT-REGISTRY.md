# OpenClone Component Intelligence Registry
**Canonical Registry of Verified, Accessible, Open-Source Component Primitives**  
*OpenClone DIEE Domain 05 | Managed by Design Systems & Frontend Engineering*

---

## 1. Registry Architecture & Governance

The **Component Intelligence Registry** maps production-ready, open-source UI primitives across the **20 Standard Component Families**. It guarantees:
1. **Copy-Paste Ownership:** Prefers direct source integration in `components/ui/` (shadcn/ui model) over bloated runtime npm packages.
2. **Accessibility-First:** Every primitive is grounded in headless accessible foundations (Radix UI / WAI-ARIA 1.2) with verified keyboard navigation, focus management, and screen reader announcements.
3. **WCAG 2.2 AAA Alignment:** Enhanced 7:1 text contrast and 44px tap targets.
4. **Resilient 6-State Handling:** Every component defines `INITIAL`, `LOADING` (matched skeleton shimmer), `EMPTY`, `SUCCESS`, `ERROR`, and `PARTIAL`.

---

## 2. Master Component Families Catalog (150+ Primitives)

### Family 01: Navigation & Application Headers
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-0101` | Sticky Navbar with Scrim | `@radix-ui/react-navigation-menu` | shadcn `NavigationMenu` | MIT | AAA | ~6 kB |
| `C-0102` | Mobile Navigation Drawer | `@radix-ui/react-dialog` | shadcn `Sheet` | MIT | AAA | ~5 kB |
| `C-0103` | User Profile Dropdown | `@radix-ui/react-dropdown-menu` | shadcn `DropdownMenu` | MIT | AA | ~4 kB |
| `C-0104` | Workspace Switcher | `@radix-ui/react-popover` | shadcn `Popover` | MIT | AAA | ~5 kB |
| `C-0105` | Breadcrumb Trail | HTML5 `<nav aria-label="Breadcrumb">` | shadcn `Breadcrumb` | MIT | AAA | <2 kB |
| `C-0106` | Glassmorphic Top Bar | CSS Backdrop Filter Scrim | Dark Luxury Top Bar | MIT | AAA | <1 kB |
| `C-0107` | Side Navigation Bar | Radix Primitives | shadcn `Sidebar` | MIT | AAA | ~8 kB |

### Family 02: Hero Sections & Value Propositions
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-0201` | Centered Headline Hero | Semantic `<header>` | Tailwind Spatial Hero | MIT | AAA | <3 kB |
| `C-0202` | Split Interactive Hero | CSS Grid 12-Col | Dark Luxury Specular Hero | MIT | AAA | <4 kB |
| `C-0203` | Animated Text Gradient Hero | Framer Motion (reduced-motion guard) | Magic UI `AnimatedGradientText` | MIT | AA | ~6 kB |
| `C-0204` | Terminal / CLI Code Hero | Semantic `<pre><code>` | Dark Luxury Obsidian Console | MIT | AAA | <2 kB |
| `C-0205` | Video / Canvas Backdrop Hero | HTML5 `<video>` / Three.js | Aceternity `HeroHighlight` | MIT | AA (Scrim) | ~15 kB |
| `C-0206` | Metric Counter Hero | CSS Tabular Numbers | Specular Metric Hero | MIT | AAA | <2 kB |

### Family 03: Feature Grids & Bento Layouts
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-0301` | 3-Column Bento Grid | CSS Grid `@container` | Magic UI `BentoGrid` | MIT | AAA | <3 kB |
| `C-0302` | Asymmetric 5-Card Bento | CSS Grid Specular Cards | Dark Luxury Bento Layout | MIT | AAA | <4 kB |
| `C-0303` | Interactive Hover-Card Grid | `@radix-ui/react-hover-card` | shadcn `HoverCard` | MIT | AA | ~4 kB |
| `C-0304` | Feature Comparison Matrix | HTML5 `<table>` | TanStack Comparison Grid | MIT | AAA | ~8 kB |
| `C-0305` | Icon-Driven Feature List | Lucide Icons | Minimalist Swiss Feature Tile | MIT | AAA | <2 kB |

### Family 04: Data Presentation & Complex Tables
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-0401` | High-Density Data Grid | `@tanstack/react-table` | shadcn `DataTable` | MIT | AAA | ~14 kB |
| `C-0402` | Paginated Server Table | `@tanstack/react-table` | Server-Action TanStack Grid | MIT | AAA | ~14 kB |
| `C-0403` | Column Visibility & Filter Bar | `@radix-ui/react-dropdown-menu` | TanStack Column Controller | MIT | AAA | ~4 kB |
| `C-0404` | Expandable Row Master-Detail | `@tanstack/react-table` | Hierarchical Sub-Table | MIT | AAA | ~16 kB |
| `C-0405` | Virtualized Infinite Table | `@tanstack/react-virtual` | Virtualized TanStack Table | MIT | AA | ~18 kB |
| `C-0406` | Data Table Skeleton Shimmer | CSS Shimmer Animation | Matched 5-Row Shimmer Grid | MIT | AAA | <1 kB |

### Family 05: Metrics & Analytics Dashboards
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-0501` | KPI Metric Card with Sparkline | SVG Sparkline | Specular Metric Tile | MIT | AAA | <3 kB |
| `C-0502` | Delta Trend Badge | Lucide Trend Icons | Micro-Step Delta Chip | MIT | AAA | <1 kB |
| `C-0503` | Multi-Metric Overview Bar | CSS Flexbox | Linear-Style Telemetry Bar | MIT | AAA | <2 kB |
| `C-0504` | Real-time Heartbeat Indicator | Dual-Ring CSS Pulse | Emerald Status Heartbeat | MIT | AAA | <1 kB |
| `C-0505` | Time-Series Area Chart | Recharts / SVG | Dark Luxury Frosted Chart | MIT | AA | ~25 kB |

### Family 06: Forms, Inputs & Multi-Step Wizards
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-0601` | Floating Label Text Input | HTML5 `<input>` | shadcn `Input` | MIT | AAA | <1 kB |
| `C-0602` | Schema-Validated Form Wrapper | `react-hook-form` + `zod` | shadcn `Form` | MIT | AAA | ~12 kB |
| `C-0603` | Accessible Select / Combobox | `@radix-ui/react-select` | shadcn `Select` | MIT | AAA | ~6 kB |
| `C-0604` | Multi-Step Wizard Progress | Radix Progress Primitive | Step Stepper with Indicators | MIT | AAA | ~3 kB |
| `C-0605` | Password Input with Strength Meter | HTML5 `<input type="password">` | Secure Password Field | MIT | AAA | <2 kB |
| `C-0606` | Tag / Token Multi-Input | Radix Popover | Tag Multi-Select Chip Input | MIT | AA | ~5 kB |

### Family 07: Modals, Drawers & Dialogs
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-0701` | Accessible Modal Dialog | `@radix-ui/react-dialog` | shadcn `Dialog` | MIT | AAA | ~5 kB |
| `C-0702` | Destructive Action Alert Dialog | `@radix-ui/react-alert-dialog` | shadcn `AlertDialog` | MIT | AAA | ~5 kB |
| `C-0703` | Mobile-Optimized Slide Drawer | `vaul` / Radix Dialog | shadcn `Drawer` | MIT | AAA | ~7 kB |
| `C-0704` | Full-Screen Focus Modal | `@radix-ui/react-dialog` | Canvas Focus Workspace | MIT | AAA | ~5 kB |

### Family 08: Feedback, Alerts & Toasts
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-0801` | Stacked Toast Notification | `sonner` | shadcn `Sonner` | MIT | AAA | ~6 kB |
| `C-0802` | Inline Contextual Alert | HTML5 `<div role="alert">` | shadcn `Alert` | MIT | AAA | <2 kB |
| `C-0803` | Floating Status Banner | CSS Sticky Top Bar | Frosted Warning Banner | MIT | AAA | <2 kB |

### Family 09: Command Palettes & Global Search
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-0901` | Global Command Bar (⌘K) | `cmdk` | shadcn `Command` | MIT | AAA | ~8 kB |
| `C-0902` | Keyboard Shortcut Badge | HTML5 `<kbd>` | Machined Specular Kbd Badge | MIT | AAA | <1 kB |
| `C-0903` | Scoped Filter Search Bar | HTML5 `<input type="search">` | Quick Filter Input with Chip | MIT | AAA | <2 kB |

### Family 10: Navigation Menus & Mega-Menus
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-1001` | Multi-Column Mega-Menu | `@radix-ui/react-navigation-menu`| shadcn `NavigationMenu` | MIT | AAA | ~6 kB |
| `C-1002` | Contextual Right-Click Menu | `@radix-ui/react-context-menu` | shadcn `ContextMenu` | MIT | AAA | ~4 kB |
| `C-1003` | Floating Dock Navigation | Framer Motion (spring tokens) | Magic UI `Dock` | MIT | AA | ~8 kB |

### Family 11: Pricing Tables & Feature Tiers
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-1101` | 3-Tier Pricing Card Grid | HTML5 Semantic Cards | Dark Luxury Specular Pricing | MIT | AAA | <4 kB |
| `C-1102` | Monthly/Annual Billing Toggle | `@radix-ui/react-switch` | shadcn `Switch` | MIT | AAA | ~3 kB |
| `C-1103` | Feature Comparison Accordion | `@radix-ui/react-accordion` | shadcn `Accordion` | MIT | AAA | ~4 kB |

### Family 12: Testimonials & Social Proof
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-1201` | Marquee Logo Cloud | CSS Keyframe Infinite Scroll | Magic UI `Marquee` | MIT | AAA (pause on hover)| ~2 kB |
| `C-1202` | Verified Customer Review Card | Semantic `<blockquote>` | Dark Luxury Quote Tile | MIT | AAA | <2 kB |
| `C-1203` | Trust Badge / Security Pill | Lucide Shield | Verified Security Chip | MIT | AAA | <1 kB |

### Family 13: Footers & Sitemap Links
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-1301` | 4-Column Enterprise Footer | HTML5 `<footer>` | Dark Luxury Sitemap Footer | MIT | AAA | <3 kB |
| `C-1302` | Minimalist One-Line Footer | HTML5 `<footer>` | Swiss Monospace Copyright Bar | MIT | AAA | <1 kB |
| `C-1303` | Theme Selector Control | `@radix-ui/react-dropdown-menu` | Dark/Light/System Toggle | MIT | AAA | ~3 kB |

### Family 14: AI Chat, Prompts & Streaming Interfaces
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-1401` | Auto-Expanding Prompt Textarea | HTML5 `<textarea>` | Expandable Omnibar | MIT | AAA | <2 kB |
| `C-1402` | Streaming Message Bubble | Semantic `<div>` + Markdown | Markdown Chat Bubble with Copy | MIT | AAA | ~10 kB |
| `C-1403` | AI Thought Process Accordion | `@radix-ui/react-collapsible` | shadcn `Collapsible` | MIT | AAA | ~3 kB |
| `C-1404` | Token Velocity & Cost Badge | Monospace Badge | Real-time Token Counter | MIT | AAA | <1 kB |

### Family 15: Media Players & Lightboxes
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-1501` | Responsive Video Frame | HTML5 `<video>` / iframe | Aspect-Ratio 16:9 Frame | MIT | AAA | <2 kB |
| `C-1502` | Accessible Image Lightbox | `@radix-ui/react-dialog` | Frosted Image Zoom Modal | MIT | AAA | ~5 kB |
| `C-1503` | Audio / Podcast Waveform Bar | HTML5 `<audio>` | SVG Mini Waveform Player | MIT | AAA | <4 kB |

### Family 16: Drag-and-Drop & Canvas Workspaces
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-1601` | Sortable List Container | `@dnd-kit/core` + `@dnd-kit/sortable` | Accessible Kanban Column | MIT | AAA (Keyboard DnD) | ~18 kB |
| `C-1602` | File Drag-and-Drop Dropzone | HTML5 Drag & Drop API | Frosted Dashed Dropzone | MIT | AAA | <3 kB |
| `C-1603` | Resizable Panel Splitter | `react-resizable-panels` | shadcn `Resizable` | MIT | AAA | ~8 kB |

### Family 17: Calendars, Schedulers & Timelines
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-1701` | Date Picker & Range Selector | `react-day-picker` | shadcn `Calendar` | MIT | AAA | ~16 kB |
| `C-1702` | Vertical Activity Timeline | Semantic `<ol>` | Specular Audit Trail Timeline | MIT | AAA | <2 kB |
| `C-1703` | Event Scheduler Grid | CSS Grid `@container` | Multi-Track Schedule Grid | MIT | AA | ~14 kB |

### Family 18: E-Commerce Product Grids & Checkouts
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-1801` | Product Card with Quick-Add | Semantic `<article>` | Specular Product Tile | MIT | AAA | <3 kB |
| `C-1802` | Flyout Shopping Cart Sheet | `@radix-ui/react-dialog` | shadcn `Sheet` Cart Drawer | MIT | AAA | ~6 kB |
| `C-1803` | Quantity Stepper Input | HTML5 `<input type="number">` | Tactile Button Incrementer | MIT | AAA | <1 kB |
| `C-1804` | Order Summary Order Breakdown | HTML5 `<dl>` | High-Contrast Checkout Reciept | MIT | AAA | <2 kB |

### Family 19: Settings & Organization Management
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-1901` | Settings Tabbed Navigation | `@radix-ui/react-tabs` | shadcn `Tabs` | MIT | AAA | ~4 kB |
| `C-1902` | Role-Based Permission Matrix | HTML5 Table + Radix Checkbox | RBAC Security Access Grid | MIT | AAA | ~6 kB |
| `C-1903` | API Key Masked Revealer | HTML5 Input + Copy Button | Secure Key Concealer | MIT | AAA | <2 kB |

### Family 20: Error Pages & Empty States
| Component ID | Display Name | Headless Primitive | Styled Pattern | License | WCAG Rating | Bundle Weight |
|---|---|---|---|:---:|:---:|:---:|
| `C-2001` | 404 / 500 Glitch Error Screen | Semantic `<main>` | Dark Luxury Error Landmark | MIT | AAA | <3 kB |
| `C-2002` | Zero-Data Empty State with CTA | Lucide Icons + Radix Button | Informative Action Empty Tile | MIT | AAA | <2 kB |
| `C-2003` | Network Disconnect Offline Banner | HTML5 `<div role="status">` | Pulsing Offline Alert Bar | MIT | AAA | <2 kB |

---

## 3. Integration Guidelines for Agents

When scaffolding or composing components:
1. Always reference the Component ID (`C-XXXX`).
2. Implement using the corresponding Headless Primitive for accessibility logic.
3. Apply OpenClone 2026 design tokens (Dark Luxury obsidian backgrounds, specular top borders, frosted glass scrims).
4. Export the matching layout skeleton loader for all data-fetching components.
