## 2026-01-26 - Static Asset Optimization in Documentation
**Learning:** Even in repositories without application code, performance optimization is possible by targeting large static assets in documentation (like Mermaid.js in HTML specs). Blocking scripts in `<head>` delay First Contentful Paint.
**Action:** Always check HTML specifications for render-blocking scripts and move them to the footer or use `defer`.

## 2026-02-05 - Resource Hint Optimization for CDNs
**Learning:** For standalone HTML specifications relying on external CDNs (like jsDelivr), using `<link rel="preconnect">` and `<link rel="dns-prefetch">` can significantly reduce connection latency and improve Time to First Byte (TTFB). This is a low-effort, high-impact optimization for documentation sites.
**Action:** Always include resource hints for critical external domains in the `<head>` of HTML documentation.
