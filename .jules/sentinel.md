# Sentinel Security Journal

## 2026-02-09 - [Standalone HTML CSP Requirement]
**Vulnerability:** Standalone HTML specifications lacked Content Security Policy (CSP), allowing unrestricted script execution if opened in a browser.
**Learning:** Even static documentation files can be vectors for XSS if they contain script tags (like Mermaid.js) without restrictions.
**Prevention:** Enforce strict CSP in all standalone HTML files: `default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;`
