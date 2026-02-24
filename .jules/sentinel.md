## 2026-02-11 - [Standalone HTML Specification Security]
**Vulnerability:** HTML specifications were loading external libraries (Mermaid.js) without a Content Security Policy (CSP) or version pinning, creating potential XSS and supply chain risks.
**Learning:** Standalone documentation files often bypass standard security checks (like CSP headers) because they are not served by a traditional backend. They require embedded `<meta>` tags for security.
**Prevention:** All standalone HTML files must include a strict CSP meta tag and pin all external dependencies (e.g., `mermaid@10.9.5`) to prevent unauthorized script execution and version drift.

## 2026-02-12 - [Subresource Integrity for External Scripts]
**Vulnerability:** External scripts loaded from CDNs lacked Subresource Integrity (SRI) hashes, making the application vulnerable to supply chain attacks if the CDN is compromised.
**Learning:** Even pinned versions on CDNs can be tampered with. SRI ensures that the browser only executes the script if it matches the expected cryptographic hash.
**Prevention:** Always generate and include `integrity` attributes (SHA-384 preferred) for all external scripts and stylesheets, along with `crossorigin="anonymous"`.

## 2026-02-13 - [CSP Hash Fragility and Path Restriction]
**Vulnerability:** A mismatched CSP hash silently blocked the Mermaid.js initialization script, while a loose CDN wildcard (`.../npm/mermaid@10.9.5/`) allowed loading unnecessary files.
**Learning:** CSP hashes are brittle; whitespace changes invalidate them, leading to silent failures where libraries load but don't initialize. Directory wildcards on CDNs are wider than necessary.
**Prevention:** Always verify inline script execution (not just file loading) after CSP changes. Restrict CDN sources to exact file paths (`dist/mermaid.min.js`) to minimize the attack surface.

## 2026-02-21 - [Dependency Upgrade for Static HTML Security]
**Vulnerability:** Static HTML documentation relied on an older version of Mermaid.js (v10.9.5) which had known security vulnerabilities (e.g., XSS sinks in diagram rendering).
**Learning:** Static files are often overlooked in dependency audits. Even documentation files can be vectors for XSS if they load vulnerable libraries and are viewed in a trusted context.
**Prevention:** Regularly audit and upgrade dependencies in static HTML files, ensuring SRI hashes and CSP directives are updated to match the new versions.

## 2026-02-24 - [CSP Maintenance for Performance Refactors]
**Vulnerability:** Inline scripts modified for performance optimization (e.g., deferring execution via `requestIdleCallback`) were blocked by the strict Content Security Policy (CSP) due to hash mismatch.
**Learning:** Performance enhancements that alter script content invalidate existing CSP hashes, causing silent failures. Security and performance refactors are coupled in CSP-protected files.
**Prevention:** Always recalculate and update the SHA-256 hash in the CSP `script-src` directive whenever inline script content changes, ensuring functionality is preserved alongside security.
