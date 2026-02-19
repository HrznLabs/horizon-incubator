## 2026-02-11 - [Standalone HTML Specification Security]
**Vulnerability:** HTML specifications were loading external libraries (Mermaid.js) without a Content Security Policy (CSP) or version pinning, creating potential XSS and supply chain risks.
**Learning:** Standalone documentation files often bypass standard security checks (like CSP headers) because they are not served by a traditional backend. They require embedded `<meta>` tags for security.
**Prevention:** All standalone HTML files must include a strict CSP meta tag and pin all external dependencies (e.g., `mermaid@10.9.5`) to prevent unauthorized script execution and version drift.

## 2026-02-12 - [Subresource Integrity for External Scripts]
**Vulnerability:** External scripts loaded from CDNs lacked Subresource Integrity (SRI) hashes, making the application vulnerable to supply chain attacks if the CDN is compromised.
**Learning:** Even pinned versions on CDNs can be tampered with. SRI ensures that the browser only executes the script if it matches the expected cryptographic hash.
**Prevention:** Always generate and include `integrity` attributes (SHA-384 preferred) for all external scripts and stylesheets, along with `crossorigin="anonymous"`.

## 2026-02-18 - [CSP Path Specificity vs Wildcards]
**Vulnerability:** CSP `script-src` allowed an entire directory (e.g., `.../mermaid@10.9.5/`) instead of a specific file, potentially allowing execution of other scripts (like unminified versions or additional modules) if an attacker could inject a script tag.
**Learning:** Directory-based CSP rules increase attack surface unnecessarily when only a single file is needed.
**Prevention:** Restrict `script-src` to the exact file path (e.g., `.../dist/mermaid.min.js`) whenever possible to adhere to the principle of least privilege.
