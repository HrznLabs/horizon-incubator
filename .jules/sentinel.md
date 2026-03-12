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

## 2026-02-24 - [Dependency Upgrade & CSP Maintenance]
**Vulnerability:** Static HTML documentation relied on `mermaid@11.12.2`, preventing access to latest security patches in `v11.12.3`.
**Learning:** Upgrading dependencies in static files requires a synchronized update of the `<script>` tag, the `integrity` attribute (SRI), and the Content Security Policy (CSP) `script-src` directive.
**Prevention:** Establish a process to check for dependency updates in static files and automate the recalculation of SRI and CSP hashes.

## 2026-02-27 - [CSP Tightening for Static HTML]
**Vulnerability:** Standalone HTML specifications, even without forms, often default to `form-action 'self'` or similar permissive CSP directives, which is unnecessary and potentially risky if forms are introduced later.
**Learning:** When a static page has no interactive forms, the principle of least privilege dictates explicitly disabling form submissions.
**Prevention:** Set `form-action 'none'` in the Content Security Policy for all static HTML files that do not require form submission capabilities.

## 2026-03-05 - [Detecting CSP violations in Playwright]
**Vulnerability:** Not a direct vulnerability, but a testing blind spot where CSP violations were missed during automated verification because they don't throw standard JS errors.
**Learning:** CSP violations in headless browsers (like Chromium via Playwright) often surface exclusively as `console` events with type `error` containing the text "Content-Security-Policy", rather than causing the page to crash or throwing catchable exceptions.
**Prevention:** To detect Content Security Policy (CSP) violations in Playwright tests, explicitly listen to `page.on('console')` events and check if the message text (lowercased) contains 'content security policy' or 'csp', as these violations surface as console messages rather than standard page errors.

## 2025-03-03 - Enforce strict securityLevel in Mermaid.js Configuration
**Vulnerability:** Mermaid.js diagrams embedded in HTML specifications configured with `securityLevel: 'antiscript'` are susceptible to DOM-based XSS if the diagram definitions are ever manipulated or supplied by untrusted sources, as it still allows certain HTML tags.
**Learning:** While `antiscript` is a step above default settings, it does not fully mitigate HTML injection risks. When integrating third-party diagramming libraries that generate complex SVGs and allow DOM manipulation, the strictest possible security level should be enforced unless dynamic HTML/click events are explicitly required and rigorously sanitized.
**Prevention:** Always configure `mermaid.initialize` with `securityLevel: 'strict'` to completely disable HTML rendering and click events within diagram nodes. Any changes to the initialization block must also ensure the Content Security Policy (CSP) inline script hashes are correctly recalculated and updated to prevent the script from being blocked.

## 2025-03-06 - Enforce Strict Security Level in Mermaid.js
**Vulnerability:** Mermaid diagrams instantiated with `securityLevel: 'antiscript'` or weaker are susceptible to DOM XSS, especially when rendering user-controlled or dynamically generated markdown.
**Learning:** `antiscript` attempts to sanitize specific scripts but has known bypasses in older or complex diagram versions. Only `securityLevel: 'strict'` securely strips all potentially malicious HTML tags and scripts from Mermaid diagrams before rendering.
**Prevention:** To prevent DOM XSS vulnerabilities when using Mermaid.js, always initialize it with `securityLevel: 'strict'`. Ensure any resulting changes to inline scripts are accurately reflected in CSP `script-src` hashes.

## 2026-03-09 - [Malformed Base64 CSP Hashes]
**Vulnerability:** Content Security Policy (CSP) inline script hashes were improperly padded with `==` instead of `=`, rendering them invalid base64. The browser silently ignored these malformed hashes, causing the inline scripts (which were otherwise correct) to be blocked and failing to execute critical components (like Mermaid.js initialization).
**Learning:** Base64 padding must strictly adhere to valid multiples. A SHA-256 hash output is 32 bytes (256 bits). When base64 encoded, this translates to 43 characters of data plus a single `=` padding character (44 characters total). Appending `==` creates an invalid 45-character string which browsers (like Chrome) will reject as a syntax error in the CSP header.
**Prevention:** When generating or updating CSP hashes for inline scripts, strictly ensure the base64 encoding utilizes the correct padding length. A SHA-256 base64 hash will always end in exactly one `=` character.

## 2025-03-01 - CSP script-src Hash Padding
**Vulnerability:** Inline scripts were blocked by the browser because their SHA-256 hashes in the Content Security Policy `script-src` directive were padded with two equals signs (`==`) instead of one (`=`).
**Learning:** A 32-byte SHA-256 base64-encoded hash must end with exactly one padding character (44 characters total). The browser will consider a hash with two equals signs as invalid and silently block the script.
**Prevention:** Ensure correct padding when generating Base64-encoded SHA-256 hashes for CSP `script-src` directives.

## 2024-05-24 - CSP Base64 Padding Requirement
**Vulnerability:** Inline scripts were blocked despite being in the CSP `script-src` because their base64-encoded SHA-256 hashes were incorrectly padded with `==` instead of `=`.
**Learning:** A 32-byte SHA-256 hash encodes to exactly 43 Base64 characters, requiring a single `=` padding character to reach a length of 44. Browsers enforce strict Base64 validation for CSP hashes and will silently reject improperly padded ones, blocking the scripts.
**Prevention:** When generating or verifying SHA-256 hashes for CSP `script-src`, ensure correct Base64 padding. A 32-byte hash must end with exactly one `=`. Do not blindly append `==`.
