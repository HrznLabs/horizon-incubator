# Sentinel Journal 🛡️

This journal tracks CRITICAL security learnings, vulnerabilities, and patterns discovered in the codebase.

---

## 2026-02-06 - [Insecure Documentation Configuration]
**Vulnerability:** The Mermaid.js initialization in `RidesVertical_Complete_Spec.html` was set to `securityLevel: 'loose'`, which allows HTML tags in diagrams to execute scripts (XSS risk).
**Learning:** Even static documentation files can harbor security risks if they include client-side rendering libraries with insecure defaults.
**Prevention:** Always use `securityLevel: 'strict'` or `securityLevel: 'antiscript'` for Mermaid.js unless there is a specific, vetted need for HTML. Additionally, use Content-Security-Policy (CSP) to restrict allowed sources.
