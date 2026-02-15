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
