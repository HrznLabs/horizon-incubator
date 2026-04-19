## 2024-05-14 - Prevent Redundant Screen Reader Announcements in Decorative Buttons
**Learning:** Decorative emojis/symbols within interactive elements like "Back to top" buttons or generated anchor links are read aloud by screen readers alongside any assigned `aria-label`s. This can cause redundant and confusing auditory feedback. In this specific app's context, small decorative icons in vanilla HTML specs were polluting the a11y experience.
**Action:** Always wrap decorative symbols or text characters in icon-only buttons with `<span aria-hidden="true">` to explicitly hide them from assistive technologies, ensuring only the intended `aria-label` is announced.
## 2024-05-15 - Global Toast for Accessible Clipboard Confirmation
**Learning:** Relying solely on inline `aria-label` swaps or icon changes for clipboard copy confirmations is insufficiently accessible, as screen readers may not reliably announce dynamic attribute changes.
**Action:** Always implement a global `aria-live="polite"` toast notification container to ensure robust, reliable screen reader announcements for asynchronous user feedback actions like copying to clipboard.
## 2026-04-19 - Visual Fallbacks for Deferred Visualizations
**Learning:** When complex visualization libraries like Mermaid are deferred or lazy-loaded for performance, the raw syntax text is briefly visible to the user before the library initializes and renders the final graphic. This creates a jarring flash of unstyled content.
**Action:** Always provide a pure CSS loading state targeting the un-processed container (e.g., `:not([data-processed="true"])`) to hide the raw text and display a clean loading indicator during asynchronous rendering.
