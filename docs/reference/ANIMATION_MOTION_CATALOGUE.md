# OpenClone — Complete Animation & Motion Design Catalogue
**Version:** 1.0.0  
**Scope:** Canonical taxonomy of 365 animation, physics easing, micro-interaction, and motion engineering concepts.

---

## 1. Executive Summary & Design Principles

Motion in software interfaces serves **comprehension, feedback, and spatial orientation**—never mere decoration. OpenClone mandates the following non-negotiable motion rules:
1. **Compositor Only:** Animations must animate strictly GPU-composited properties (`transform`, `opacity`). Never animate `width`, `height`, `top`, `margin`, or `padding` to prevent layout thrashing and dropped frames.
2. **60 FPS Baseline:** All transitions must hit 60 frames per second (16.6ms per frame budget).
3. **Respect Reduced Motion:** Every animation MUST provide an immediate zero-duration or gentle opacity-only fallback under `@media (prefers-reduced-motion: reduce)`.
4. **Physical Easing:** Interfaces must use physics-based spring curves (cubic-bezier) rather than linear or mechanical transitions.

---

## 2. Standardized Timing & Duration Tokens

```css
:root {
  /* Micro-interactions & instant feedback */
  --duration-instant: 50ms;
  --duration-fast: 100ms;
  --duration-normal: 150ms;

  /* State transitions, menus, tooltips */
  --duration-moderate: 200ms;
  --duration-smooth: 250ms;

  /* Dialogs, sheets, large surface transforms */
  --duration-deliberate: 300ms;
  --duration-extended: 400ms;
  --duration-page: 500ms;

  /* Physics-derived easing curves */
  --ease-standard: cubic-bezier(0.2, 0.0, 0, 1.0);
  --ease-decelerate: cubic-bezier(0.0, 0.0, 0.2, 1.0);
  --ease-accelerate: cubic-bezier(0.4, 0.0, 1.0, 1.0);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  --ease-smooth: cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## 3. The 365 Animation & Motion Concepts Taxonomy

The 365 motion concepts are structured across 10 functional domains:

### 1. Fundamental Principles & Timing (Concepts 1–35)
Duration scaling, frame budgeting (16.6ms), frame drops detection, easing curves, cubic-bezier math, linear vs non-linear acceleration, deceleration curve, anticipation principle, staging, follow-through, overlapping action, slow in and slow out, arcs of motion, secondary action, timing and rhythm, exaggeration threshold, solid drawing / depth, appeal, visual weight, momentum conservation, friction simulation, mass perception, spring stiffness, spring damping ratio, velocity inheritance, interruptibility, reversible transitions, frame-rate independence, hardware acceleration, layer promotion (`will-change`), repaint minimization, composite layer auditing, layout thrashing prevention, time dilation testing, motion sickness triggers.

### 2. Micro-Interactions & Button Feedback (Concepts 36–75)
Button tap press scale (`scale(0.97)`), button hover elevation lift, button focus pulse ring, tactile inset shadow transition, ripple click wave, border highlight shimmer, magnetic button cursor pull, button loading spinner morph, checkmark morph on success, shake on validation error, badge counter pop, icon rotation on toggle, icon morphing (hamburger to X), tooltip delayed fade-in, copy button checkmark swap, download progress fill, heart like bounce, bookmark ribbon fold, star rating fill cascade, toggle switch thumb glide, slider thumb expansion on drag, volume knob rotation, drag handle grip hover, stepper number flip, tag chip dismiss slide-out, segment switch slide underline, audio waveform bar bounce, status dot breathing pulse, unread indicator badge ping, clipboard paste flash, typing dots bounce, send message fly-up, delete trashcan lid open, undo banner countdown bar, file upload dropzone glow, hover glow follow, interactive card tilt (3D transform), subtle border color transition, active state dark tint.

### 3. Surface, Layout & Container Transitions (Concepts 76–115)
Accordion smooth height transition, tab content crossfade, sliding tab indicator, modal backdrop fade-in, modal surface scale-up (`scale(0.95)` to `scale(1)`), modal dismiss slide-down, slide-over right sheet enter, bottom sheet snap points, drawer bounce-back on edge, split-pane divider resize drag, cards reorder swap, bento box expansion, masonry grid reflow, hero image expand to full-screen view, sticky header compact transition on scroll, floating dock hide on scroll down / show on scroll up, sidebar collapse to icons, nested menu slide-in with back button, breadcrumb truncation expand, command palette backdrop blur fade, search bar expansion on focus, table row hover highlight, table sort arrow flip, table row deletion collapse, list item insertion slide-down, virtual list scrolling stability, infinite scroll loader appearance, empty state illustration fade, error callout unfold, notification toast slide from bottom-right, toast stack shift on dismiss, paywall modal curtain reveal, lightbox image zoom, full-screen takeover zoom from thumbnail, multi-column reading flow transition.

### 4. Navigation & Page Routing (Concepts 116–150)
Page crossfade, shared element transition (Morphing), drill-down push transition, hierarchical pop transition, sliding horizontal page transitions, vertical stack page reveal, tab bar icon active state spring, bottom nav hide on deep scroll, back swipe interactive gesture, breadcrumb hover expand, anchor scroll smooth jump, scrollspy indicator active tracking, step wizard forward slide, step wizard backward slide, multi-level dropdown flyout, mega-menu staggered column fade, contextual right-click menu scale, mobile navigation full-screen curtain, circular reveal page transition, split flap departure board transition, curtain wipe transition, diagonal slide transition, zoom out / zoom in navigation, card flip transition, cube 3D rotation transition, parallax page depth shift, scroll-driven header opacity, navbar blur on scroll trigger, floating pill nav center snap, footer reveal on bottom scroll.

### 5. Data Visualization & Chart Dynamics (Concepts 151–185)
Line chart path drawing (`stroke-dashoffset`), bar chart height grow from baseline, multi-bar chart staggered entrance, pie chart slice unroll from 12 o'clock, donut chart percentage sweep, area chart gradient fill reveal, scatter plot dot fade and scale, candlestick chart volume bar rise, gauge needle spring swing, sparkline path draw on hover, tooltip follow cursor along curve, crosshair line snapping to data point, active data point pulse ring, chart legend toggle fade, axis tick mark fade-in, gridline subtle reveal, chart zoom smooth scale, chart pan inertia, time-series window slide, treemap rectangle split, sankey flow particle animation, choropleth map color transition, node-link graph force simulation settle, cluster bubble pack expansion, heatmap cell color fade, funnel stage drop transition, radar polygon morph, metric number odometer roll, delta badge color flash (green/red), chart empty-to-data transition, live data point append slide, threshold line warning pulse, data brush selection box draw.

### 6. Scroll-Driven & Parallax Effects (Concepts 186–220)
Scroll-driven animation timeline, CSS `animation-timeline: scroll()`, CSS `animation-timeline: view()`, scrubbed video playback on scroll, multi-layer parallax background shift, horizontal scroll on vertical wheel, sticky section pin and unpin, text reveal on scroll entering viewport, image zoom inside container on scroll, scroll progress indicator bar, circular scroll percentage ring, section snap scrolling, momentum scrolling physics, overscroll bounce effect, rubber-band pull to refresh, scroll direction detection (up vs down), reading progress tracker, timeline path fill on scroll, card stacking on scroll, sticky element stacking effect, horizontal card carousel drag scroll, scroll velocity tracking, scroll-triggered counting numbers, background color morph on section change, subtle foreground element float, fixed background image reveal, scroll anchor smooth jump, scrollbar thumb hover expansion.

### 7. Gestures & Mobile Touch Dynamics (Concepts 221–255)
Touch start instant response, swipe-to-delete revealing red action, swipe-to-archive green action, pinch-to-zoom image scaling, double-tap zoom toggle, drag-and-drop item pickup lift, drag shadow elevation increase, drag item snapping into slot, drag collision avoidance reflow, edge swipe back gesture, pull-down to dismiss modal, bottom sheet drag down to close, long-press contextual menu pop, haptic feedback sync, pan gesture inertial fling, multi-touch rotation, touch target ripple expansion, touch cancel smooth revert, boundary collision resistance, spring back to bounds on over-drag, flick gesture velocity detection, touch tracking precision, floating button drag and dock, gesture interruption handling, swipeable card deck discard left/right, pull-to-refresh spinner tension curve.

### 8. Text, Typography & Content Transitions (Concepts 256–290)
Typing text typewriter effect, text scramble decode animation, letter stagger fade-in, word-by-word streaming reveal, headline line-by-line slide-up, gradient text shimmer sweep, counter odometer rolling digits, currency transition with separator roll, text highlight marker sweep, strikethrough animation on task completion, underline draw on link hover, text blur-to-sharp focus reveal, text size fluid responsive interpolate, font weight transition on hover, serif to monospace character morph, pull-quote drop cap reveal, inline code copy confirmation, alert text shake on error, tooltip text fade-up, caption slide over image on hover, markdown live rendering text flow, syntax highlight fade-in, truncated text clamp expansion, smooth text wrap reflow.

### 9. Loading, Skeletons & System State (Concepts 291–325)
Skeleton pulse shimmer wave (`linear-gradient` sweep), circular spinner rotation, linear progress bar fill, indeterminate progress bounce, pulsing brand logo loading, three dots sequential bounce, radial sweep loader, file upload radial progress ring, multi-step progress stepper checkmark fill, optimistic UI instant state update, optimistic UI revert shake on failure, background sync icon spin, connection reconnecting pulse, offline status banner drop, server ping indicator beacon, live streaming data wave, battery charging lightning pulse, cache invalidation refresh sweep, auto-save spinner to checkmark morph, rate limit countdown ring, maintenance countdown clock.

### 10. Performance, Compositing & Accessibility (Concepts 326–365)
GPU layer promotion with `translateZ(0)`, CSS `will-change` lifecycle cleanup, subpixel rendering optimization, layout recalculation elimination, paint area bounding, DOM tree depth reduction for animation, Web Workers for heavy physics computation, `requestAnimationFrame` synchronization, `requestIdleCallback` for non-critical animations, FPS meter HUD integration, Chrome DevTools performance profiling, memory leak prevention in JS animations, garbage collection pause avoidance, CSS `@media (prefers-reduced-motion: reduce)` enforcement, instant opacity crossfade for reduced motion, vestibular disorder prevention, zero continuous motion on idle, auto-play animation pause button, accessibility screen reader announcement timing, high contrast mode animation overrides, mobile low-power battery mode throttling, display refresh rate sync (60Hz, 120Hz ProMotion).
