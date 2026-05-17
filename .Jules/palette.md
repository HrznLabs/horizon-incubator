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

## 2025-10-24 - Screen Reader Feedback on Interactive Elements
**Learning:** Providing visual-only feedback (like changing an icon to a checkmark) during interactive states like "copy to clipboard" is insufficient for accessibility.
**Action:** Always dynamically update the element's `aria-label` to narrate state changes (e.g., 'Copied!') for screen readers, and remember to revert it when the visual state reverts.

## 2025-10-25 - [Hash Links and Keyboard Focus]
**Learning:** Pure CSS `#target` anchoring and standard HTML `<a>` behavior updates the scroll position but frequently fails to move programmatic keyboard focus into the target element across all browsers (like WebKit) unless the target is natively focusable or explicitly given a tabindex.
**Action:** When implementing Skip-to-content or Table of Contents (TOC) navigation, always ensure the destination container (e.g., `<section>`) has `tabindex="-1"` to guarantee the focus context moves seamlessly for keyboard users.

## 2025-04-04 - Programmatic Focus Management for Scroll-to-Top Actions
**Learning:** When a user activates a "Back to Top" button, visual focus moves to the top of the page, but keyboard/screen reader focus remains at the bottom on the now-hidden button. This creates a confusing experience when they resume navigation.
**Action:** Always programmatically manage focus by shifting it to a logical container at the top of the page (like `<header tabindex="-1">`) when scrolling to top, ensuring keyboard users can seamlessly resume reading.

## 2024-05-22 - [Anchor Link Context and Breathing Room]
**Learning:** When navigating via anchor links (like a Table of Contents) in long HTML documents, the browser scrolls the target element flush against the top of the viewport. This often hides context (like section headers) under fixed headers or progress bars, leading to a cramped and disorienting UX.
**Action:** Always add `scroll-margin-top` to target sections (`section[id]`) to provide visual breathing room and ensure headings remain clearly visible when linked to.
## 2024-04-07 - Ensure Touch Accessibility for Hover-Dependent Elements
**Learning:** Elements relying purely on `:hover` and `:focus-visible` (like `.anchor-link` for headings) become completely invisible and undiscoverable on touch devices, violating accessibility guidelines for mobile users.
**Action:** When creating hover-based interactive elements, always implement an `@media (hover: none)` or `@media (max-width: 768px)` fallback to ensure they are visible (e.g., permanent partial opacity) on touch devices where hover interactions are not supported.
## 2024-11-20 - Improved color contrast of critical badge for accessibility
**Learning:** The `.badge.critical` component on a dark background (`#1a1a2e`) combined with a translucent red background (`rgba(231,76,60,0.2)`) and red text (`#e74c3c`) resulted in a contrast ratio of 3.58:1, failing WCAG AA standards. This highlights the need to be cautious with dark themes and translucent backgrounds when calculating final foreground text color contrast.
**Action:** When working on dark mode UI with translucent background accents, explicitly verify the computed contrast ratio against the absolute background. In this case, adjusting the text color to `#ff6b6b` achieved a compliant 4.93:1 contrast ratio.
## 2025-04-11 - Table Semantics Accessibility Fix
**Learning:** Incorrectly using `<td scope="row">` instead of `<th scope="row">` creates invalid semantic HTML that screen readers may fail to interpret properly as row headers. When fixing this by replacing `<td>` with `<th>` inside a `<tbody>`, the new `<th>` elements might accidentally inherit global table header styles (often meant only for `<thead>`).
**Action:** When fixing table semantics by introducing row headers (`<th>` in `<tbody>`), always update the CSS selectors to explicitly differentiate styling between `.decisions thead th` and `.decisions tbody th` to prevent visual regressions while ensuring proper accessibility structure.

## 2025-10-25 - [Skip-to-Content Focus Outline Management]
**Learning:** When users activate a 'Skip to content' link targeting a `<main>` element with `tabindex="-1"`, browsers often apply a default focus ring around the entire main container. This creates a massive, visually distracting outline around the whole page body that confuses both keyboard and screen reader users.
**Action:** When managing programmatic focus for skip links or anchor targets, explicitly remove the default focus outline using `main[tabindex="-1"]:focus { outline: none; }` to maintain a clean visual experience while preserving the necessary focus context.
## 2025-01-20 - Dynamic ARIA labels for nested heading structures
**Learning:** When extracting text content from DOM elements (like headings) to generate dynamic ARIA labels via JavaScript, using `element.textContent` will extract the text of all nested elements, including those explicitly marked as `aria-hidden="true"` (like emojis or decorative badges). However, it might miss text if you only filter for direct `Node.TEXT_NODE` children if there are formatting tags like `<strong>`. A balanced approach is needed depending on the HTML structure.
**Action:** Before generating ARIA labels dynamically from DOM content, carefully inspect the target element's HTML structure. If it contains `aria-hidden` nodes, filtering logic is required to prevent screen readers from announcing decorative text.

## 2025-01-20 - Ensure Playwright tests account for async DOM injection via requestIdleCallback
**Learning:** When writing Playwright tests to verify the presence of DOM elements (like dynamically injected anchor links) that are added via asynchronous callbacks like `requestIdleCallback`, the script must include an explicit delay (e.g., `time.sleep(1)`) to allow the browser's idle period to execute the callback before the elements can be queried.
**Action:** Always include a brief `time.sleep()` or equivalent wait condition in Playwright test scripts when verifying elements injected by `requestIdleCallback` or `setTimeout` to ensure the DOM is fully populated before assertions are made.
