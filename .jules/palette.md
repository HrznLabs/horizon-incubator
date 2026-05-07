## 2024-05-14 - Prevent Redundant Screen Reader Announcements in Decorative Buttons
**Learning:** Decorative emojis/symbols within interactive elements like "Back to top" buttons or generated anchor links are read aloud by screen readers alongside any assigned `aria-label`s. This can cause redundant and confusing auditory feedback. In this specific app's context, small decorative icons in vanilla HTML specs were polluting the a11y experience.
**Action:** Always wrap decorative symbols or text characters in icon-only buttons with `<span aria-hidden="true">` to explicitly hide them from assistive technologies, ensuring only the intended `aria-label` is announced.
## 2024-05-15 - Global Toast for Accessible Clipboard Confirmation
**Learning:** Relying solely on inline `aria-label` swaps or icon changes for clipboard copy confirmations is insufficiently accessible, as screen readers may not reliably announce dynamic attribute changes.
**Action:** Always implement a global `aria-live="polite"` toast notification container to ensure robust, reliable screen reader announcements for asynchronous user feedback actions like copying to clipboard.
## 2026-04-19 - Visual Fallbacks for Deferred Visualizations
**Learning:** When complex visualization libraries like Mermaid are deferred or lazy-loaded for performance, the raw syntax text is briefly visible to the user before the library initializes and renders the final graphic. This creates a jarring flash of unstyled content.
**Action:** Always provide a pure CSS loading state targeting the un-processed container (e.g., `:not([data-processed="true"])`) to hide the raw text and display a clean loading indicator during asynchronous rendering.
## 2025-02-27 - Enhance TOC Hit Areas and Text Selection Highlighting
**Learning:** Dense Table of Contents links with default inline boundaries limit the clickable area (Fitts's Law violation), making navigation harder. Also, default OS text selection styles can clash with dark neon themes, leading to poor contrast when users highlight content.
**Action:** Always pad interactive inline text elements (`display: inline-block; padding: 4px 8px; margin-left: -8px;`) to expand their hit area seamlessly, and provide a custom `::selection` style (`background: rgba(brand-color, 0.3)`) to maintain brand contrast and visual coherence.
## 2025-05-02 - Extract Active State to CSS using `aria-current`
**Learning:** Relying on JavaScript inline styles (e.g., `element.style.color`) to indicate active states can cause maintainability issues and override hover/focus states unintentionally. It's better to manage visual states via CSS using semantic attributes.
**Action:** Define active state styling in CSS using the `[aria-current="true"]` selector and remove inline style assignments from JavaScript logic.

## 2024-05-24 - Visual Cue for Internal Anchor Links
**Learning:** When navigating long documents via Table of Contents links, users can lose track of the exact target section, especially if the scroll position isn't perfect.
**Action:** Implemented a pure CSS keyframe animation paired with the `:target` pseudo-class to create a temporary visual pulse effect on the navigated section. This provides clear feedback without requiring any JavaScript.
