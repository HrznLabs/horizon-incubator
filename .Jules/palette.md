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
