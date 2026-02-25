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

## 2026-10-24 - [CSP Tightening for Static Specs]
**Vulnerability:** Static HTML specifications often use `base-uri 'self'` and `form-action 'self'` by default, which can be overly permissive if the document is compromised via XSS (e.g., `<base>` injection).
**Learning:** Even without backend processing, static files benefit from "least privilege" CSP directives. `base-uri 'none'` prevents hijacking relative links, and `form-action 'none'` prevents exfiltration via form submission.
**Prevention:** For standalone documentation files, restrict `base-uri` and `form-action` to `'none'` unless explicitly needed.
