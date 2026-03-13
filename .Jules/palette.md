## 2024-05-22 - Documentation as UX
**Learning:** In non-code repos, the "interface" is the documentation structure. Adding TOCs and proper semantics directly improves the user journey.
**Action:** Always check for long markdown files without TOCs as a quick win.

## 2025-05-22 - [Respecting Reduced Motion in JS Animations]
**Learning:** Pure CSS `scroll-behavior: smooth` isn't enough when triggering scrolls via JavaScript (e.g., Back to Top buttons). JS `window.scrollTo` defaults to instant or the passed behavior, ignoring the CSS preference unless explicitly checked.
**Action:** Always check `window.matchMedia('(prefers-reduced-motion: reduce)').matches` before applying `{ behavior: 'smooth' }` in JS.

## 2025-05-23 - Performance as UX in Specs
**Learning:** Performance optimizations (e.g., `<link rel="preconnect">`, throttled scroll listeners) in standalone HTML specifications are critical UX improvements, especially when heavy libraries like Mermaid.js are involved.
**Action:** When auditing static documentation, check for and implement resource hints and event throttling to improve perceived responsiveness.

## 2025-05-24 - [Visual Consistency in Dark Mode Docs]
**Learning:** Hardcoded white backgrounds in diagrams (like Mermaid) create jarring "flashbang" effects in dark-themed documentation, breaking immersion and causing eye strain.
**Action:** Always check diagram configurations (`theme: 'dark'`) and container styles when auditing dark-mode documentation.

## 2025-05-24 - [Print Styles as Accessibility]
**Learning:** Documentation is often "printed" (Print-to-PDF) for offline reading or archival. Dark mode interfaces fail catastrophically here, wasting ink and reducing readability.
**Action:** When creating standalone documentation, always include a `@media print` block that forces high-contrast (black-on-white), hides interactive elements, and expands collapsibles.

## 2025-06-15 - [Dynamic Scroll Progress]
**Learning:** In specs with lazy-loaded content (e.g., diagrams), `document.scrollHeight` increases as elements render, causing reading progress bars to shrink unexpectedly, which can confuse users about their true progress.
**Action:** When implementing progress bars for dynamic pages, consider binding the max value to a stable metric (like section count) or use a `ResizeObserver` to smoothly animate the change in total height, signaling to the user that new content has appeared.

## 2025-06-16 - [Contextual Navigation in Long Specs]
**Learning:** In long documentation with a fixed Table of Contents, users lose context of their current position as they scroll, reducing the utility of the TOC as a mental map.
**Action:** Use `IntersectionObserver` with an asymmetric `rootMargin` (e.g., `-10% 0px -70% 0px`) to efficiently highlight the currently active section in the TOC and apply `aria-current="true"`, providing both visual orientation and accessibility benefits without the performance cost of scroll listeners.

## 2025-06-16 - [Complex Diagram Accessibility]
**Learning:** Complex diagrams in HTML (e.g., Mermaid.js outputs) often lack accessibility features, leaving screen reader users without context about the diagram's content and purpose. Adding scripts to modify DOM for UX improvements can conflict with strict Content Security Policies (CSP) and be hard to maintain if they require inline script hashing.
**Action:** Use native HTML accessibility attributes (`role="region"`, `aria-labelledby`, `aria-describedby`) on diagram containers to associate them with their visible headings and descriptions. Additionally, wrap decorative emojis in headings with `<span aria-hidden="true">` to prevent assistive tech from reading them out loud, providing a better screen reader UX using pure HTML without introducing JS/CSP complexities.

## 2023-10-27 - Dynamic Table of Contents Orientation and CSP Handling
**Learning:** For long, single-page HTML specifications, static Table of Contents links can leave users disoriented about their current position in the document. Using `aria-current="true"` on the active TOC link is a crucial accessibility enhancement for screen reader users to understand their context. Furthermore, when implementing this via JS in files with a strict Content Security Policy (CSP), altering script blocks requires extremely careful recalculation of SHA-256 hashes to prevent breaking unrelated functionality on the page. Adding custom CSS should also be avoided per repo constraints, preferring inline styles set by the JS directly.
**Action:** When building static HTML specifications with a Table of Contents, use `IntersectionObserver` on the section headers to dynamically update inline styles (for visual users) and `aria-current="true"` (for screen readers) on the corresponding TOC links. When adding the JS logic, ensure it's merged into an existing script if possible, and explicitly recalculate only the modified script's hash to update the CSP, preserving other script hashes identically.
## 2025-03-09 - Accessible Icon-Only Buttons
**Learning:** Decorative emojis or symbols (like `↑`, `🔗`, or `✅`) inside interactive icon-only buttons that already have an `aria-label` must be explicitly wrapped in `<span aria-hidden="true">`. Otherwise, screen readers may read the symbol redundantly alongside the label, creating a confusing or cluttered experience. Additionally, when injecting these HTML elements dynamically via JavaScript, `innerHTML` must be used instead of `textContent` or `innerText` to ensure the wrappers are parsed as HTML.
**Action:** When creating or modifying icon-only buttons or interactive elements containing raw symbols, always verify if they have an `aria-label`. If they do, wrap the decorative symbol in an `aria-hidden="true"` span. Use `innerHTML` when applying this pattern dynamically.

## 2025-06-16 - Accessible Feedback for Icon-Only Actions
**Learning:** Visual-only feedback (like temporarily swapping an icon to a `✅` after copying a link) provides zero audible confirmation for screen reader users, who have just triggered an action. However, dynamically setting and reverting an `aria-label` requires careful state handling: if the element originally had no `aria-label`, restoring it by setting the value to `null` coerces it to the string `"null"`, confusing users.
**Action:** When implementing temporary state changes for accessibility (like "Link copied!"), always cache the original attribute value. When reverting, check if the cached value is truthy: if it is, restore it using `setAttribute`; if it is null or undefined, completely remove the attribute using `removeAttribute`.
