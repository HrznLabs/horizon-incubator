## 2026-02-10 - [HTML Specification Security Hardening]
**Vulnerability:** Standalone HTML specification files (e.g., `Verticals/ridesDAO/RidesVertical_Complete_Spec.html`) lacked Content Security Policy (CSP) headers, exposing users to potential XSS if malicious scripts were injected or loaded via compromised CDNs.
**Learning:** Documentation-focused repositories with standalone HTML artifacts often overlook browser-side security headers because they execute in a local or static context where traditional server-side headers are absent.
**Prevention:** Mandate the inclusion of strict `<meta>` CSP tags in all standalone HTML deliverables. Use a standardized policy that whitelists only necessary CDNs (e.g., jsDelivr for Mermaid.js) and disables object/embed sources.
