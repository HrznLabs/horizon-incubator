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

## 2026-03-10 - [CSP Hash Drift for Utility Scripts]
**Vulnerability:** An inline script block providing utility functions (anchor links and clipboard copy) was silently blocked because its SHA-256 hash was omitted from the `script-src` directive in the Content Security Policy (CSP).
**Learning:** When modifying inline scripts, or when refactoring/adding new inline script blocks in a document with a strict CSP, the corresponding hashes in the `script-src` directive often drift out of sync if not manually updated. This results in completely broken functionality for those specific scripts.
**Prevention:** Always recount inline scripts and recalculate their base64-encoded SHA-256 hashes against the actual file content when making structural or logic changes to HTML specifications. Ensure every single inline `<script>` block has a corresponding hash in the CSP header.

## 2026-03-12 - [Orphaned CSP Hash Removal]
**Vulnerability:** A static HTML specification retained an unused CSP inline script hash from a prior version or removed script. While not directly exploitable, it violates the principle of least privilege by artificially widening the `script-src` attack surface.
**Learning:** When cleaning up or refactoring HTML, CSP tags must also be audited to remove hashes of scripts that no longer exist, preventing attackers from injecting those exact scripts if a bypass is found.
**Prevention:** Periodically re-evaluate all CSP `script-src` hashes against the actual inline scripts present in the document. Automating the comparison can quickly identify orphaned hashes that need removal.

## 2026-03-24 - [CSP style-src and Mermaid.js Compatibility]
**Vulnerability:** Attempting to harden Content Security Policy (CSP) by removing `'unsafe-inline'` from `style-src` in static HTML specifications.
**Learning:** Mermaid.js dynamically generates SVG diagrams that heavily rely on injecting inline styles. Removing `'unsafe-inline'` from the `style-src` directive without a robust nonce-based architecture breaks the rendering of all diagrams. In a static HTML context without a server to generate nonces, retaining `'unsafe-inline'` for `style-src` is a necessary tradeoff.
**Prevention:** Do not remove `'unsafe-inline'` from `style-src` in static HTML files that utilize Mermaid.js unless transitioning to a server-rendered or build-step architecture capable of injecting nonces into all dynamically generated SVG elements.

## 2025-04-10 - Refactoring innerHTML to Prevent DOM-Based XSS in Anchor Links
**Vulnerability:** The JavaScript responsible for adding anchor links (`.anchor-link`) and updating their content on click used `btn.innerHTML` to inject HTML strings (`<span aria-hidden="true">🔗</span>` and `<span aria-hidden="true">✅</span>`). While the current injected values were static strings, using `innerHTML` for DOM manipulation is a dangerous practice that can lead to DOM-based Cross-Site Scripting (XSS) if the input ever becomes dynamic or is influenced by user data.
**Learning:** Even in static HTML specification documents, defense-in-depth principles require avoiding sinks like `innerHTML` when safer alternatives exist. It's crucial to establish secure coding habits across the entire codebase to prevent future vulnerabilities during maintenance or expansion.
**Prevention:** Replace `innerHTML` assignments with safer DOM manipulation methods, such as `document.createElement`, `setAttribute`, and `textContent` or `appendChild`. This ensures that any injected content is treated strictly as text or DOM nodes, eliminating the risk of HTML parsing and script execution.

## 2026-03-26 - [CSP Hash Drift for Security Script Execution]
**Vulnerability:** Inline scripts, particularly those configuring critical security settings like Mermaid's `securityLevel: 'strict'`, were silently blocked by the browser. This occurred because a previous edit to the HTML specification caused a mismatch (hash drift) between the actual script content and the SHA-256 hashes defined in the `Content-Security-Policy` header.
**Learning:** Any modification to an inline `<script>` block—or any structural change in a static HTML file that accidentally alters whitespace within a script—invalidates its CSP hash. If the hashes are not kept synchronized, the browser blocks the script. This is especially dangerous when the blocked script is responsible for enforcing security boundaries (like disabling `unsafe-eval` or sanitizing XSS sinks in diagramming libraries).
**Prevention:** Establish a rigorous process (ideally automated) to recalculate and update all base64-encoded SHA-256 hashes in the CSP `script-src` directive whenever inline scripts are added, removed, or modified in static HTML files.

## 2025-05-24 - Removing Raw Error Logs in Client-Side Scripts
**Vulnerability:** The application was catching and logging raw error objects (`console.error(err)`) to the browser console when Mermaid.js diagram rendering failed.
**Learning:** Logging raw, unhandled error objects in production can expose sensitive stack traces, internal implementation details, and potentially sensitive data variables to end-users or attackers inspecting the console. This violates the principle of failing securely and avoiding information leakage.
**Prevention:** Always replace raw error object logging with generic, safe error messages (e.g., `console.error('Failed to render diagram.')`) on the client side, especially for third-party library errors that might include unpredictable internal state.
