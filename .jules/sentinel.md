## 2026-02-11 - [Standalone HTML Specification Security]
**Vulnerability:** HTML specifications were loading external libraries (Mermaid.js) without a Content Security Policy (CSP) or version pinning, creating potential XSS and supply chain risks.
**Learning:** Standalone documentation files often bypass standard security checks (like CSP headers) because they are not served by a traditional backend. They require embedded `<meta>` tags for security.
**Prevention:** All standalone HTML files must include a strict CSP meta tag and pin all external dependencies (e.g., `mermaid@10.9.5`) to prevent unauthorized script execution and version drift.

## 2026-02-11 - [Subresource Integrity (SRI) in Standalone Specs]
**Vulnerability:** External scripts in HTML specifications lacked Subresource Integrity (SRI) hashes, leaving them vulnerable to CDN compromises or tampering.
**Learning:** Trusting a CDN URL (even with version pinning) is insufficient for high-security documentation. Browser-level verification via SRI is required to guarantee code integrity.
**Prevention:** Enforce SRI (`integrity` attribute) for all external resources (scripts/styles) in standalone HTML files, in addition to CSP.
