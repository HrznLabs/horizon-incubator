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

## 2025-05-25 - [Print-Friendly Documentation]
**Learning:** Standalone HTML specs often prioritize dark mode for screen reading but neglect printability. This creates poor UX when users need to save as PDF or print.
**Action:** Always verify `@media print` styles in standalone HTML docs to ensure high contrast (black on white) and remove interactive elements.
