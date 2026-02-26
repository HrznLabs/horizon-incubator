## 2026-01-26 - Static Asset Optimization in Documentation
**Learning:** Even in repositories without application code, performance optimization is possible by targeting large static assets in documentation (like Mermaid.js in HTML specs). Blocking scripts in `<head>` delay First Contentful Paint.
**Action:** Always check HTML specifications for render-blocking scripts and move them to the footer or use `defer`.

## 2026-02-10 - Resource Hints for Documentation Assets
**Learning:** Large external libraries (like Mermaid.js via CDN) can block the critical rendering path. Adding preconnect and dns-prefetch hints improves perceived performance by paralleling connection setup.
**Action:** Audit all HTML specs for external script tags and ensure corresponding resource hints are present.

## 2026-02-12 - Scroll Event Throttling in Single-Page Specs
**Learning:** Single-page HTML specifications with "Back to Top" functionality often use unthrottled scroll event listeners, which can degrade scrolling performance on lower-end devices.
**Action:** Always wrap scroll event listeners in `requestAnimationFrame` to decouple the handler execution from the scroll event rate.

## 2026-02-14 - Preconnect Crossorigin Attribute
**Learning:** For resources fetched via CORS (like scripts from CDNs), the `<link rel="preconnect">` tag must include the `crossorigin` attribute to be effective. Without it, the browser opens a connection without credentials, which cannot be reused for the CORS request.
**Action:** Always verify that `preconnect` tags for external scripts/fonts include `crossorigin` (or `crossorigin="anonymous"`).

## 2026-03-05 - Lazy Loading Mermaid Diagrams
**Learning:** Initializing all Mermaid diagrams on load can cause significant main thread blocking and delay interactivity, especially in long documents. Using `IntersectionObserver` to render diagrams only when they approach the viewport drastically reduces Total Blocking Time (TBT).
**Action:** Implement lazy loading for Mermaid diagrams using `IntersectionObserver` and `mermaid.run({ nodes: [...] })`.

## 2026-03-07 - Printing Dark-Themed Diagrams
**Learning:** Dark-themed Mermaid.js diagrams (common in specs) render with heavy black backgrounds in print media, wasting ink and reducing legibility on paper.
**Action:** Use CSS filters (`invert(1) hue-rotate(180deg)`) inside `@media print` blocks to force diagrams into a light/high-contrast mode without requiring JavaScript theme switching.

## 2026-03-15 - Deferred Progressive Enhancement in Static Specs
**Learning:** For static documentation with client-side enhancements (like anchor links), delaying execution until idle time (`requestIdleCallback`) significantly improves initial paint metrics without user-visible degradation.
**Action:** Identify non-critical DOM manipulation scripts in HTML specs and wrap them in `requestIdleCallback` or `setTimeout` to unblock the main thread.

## 2026-03-20 - Batching Heavy Rendering in IntersectionObserver
**Learning:** Triggering heavy rendering logic (like `mermaid.run`) individually for every intersecting element can cause multiple layout recalculations per frame. Batching these requests within the `IntersectionObserver` callback significantly reduces main thread work.
**Action:** Accumulate targets in `IntersectionObserver` callbacks and process them in a single batch whenever possible.
