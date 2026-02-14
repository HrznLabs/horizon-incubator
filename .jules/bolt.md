## 2026-01-26 - Static Asset Optimization in Documentation
**Learning:** Even in repositories without application code, performance optimization is possible by targeting large static assets in documentation (like Mermaid.js in HTML specs). Blocking scripts in `<head>` delay First Contentful Paint.
**Action:** Always check HTML specifications for render-blocking scripts and move them to the footer or use `defer`.

## 2026-02-10 - Resource Hints for Documentation Assets
**Learning:** Large external libraries (like Mermaid.js via CDN) can block the critical rendering path. Adding preconnect and dns-prefetch hints improves perceived performance by paralleling connection setup.
**Action:** Audit all HTML specs for external script tags and ensure corresponding resource hints are present.

## 2026-02-12 - Scroll Performance in Static Docs
**Learning:** Simple UI interactions like "Back to Top" buttons in static HTML documentation can degrade performance if scroll event listeners are not throttled, especially on mobile devices where `scroll` fires frequently.
**Action:** Always throttle scroll event listeners using `requestAnimationFrame` in standalone HTML specifications.
