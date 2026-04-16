## 2024-05-14 - Prevent Redundant Screen Reader Announcements in Decorative Buttons
**Learning:** Decorative emojis/symbols within interactive elements like "Back to top" buttons or generated anchor links are read aloud by screen readers alongside any assigned `aria-label`s. This can cause redundant and confusing auditory feedback. In this specific app's context, small decorative icons in vanilla HTML specs were polluting the a11y experience.
**Action:** Always wrap decorative symbols or text characters in icon-only buttons with `<span aria-hidden="true">` to explicitly hide them from assistive technologies, ensuring only the intended `aria-label` is announced.

## 2024-05-15 - Global Toast Notifications for Accessible Feedback
**Learning:** For critical UI actions like copying to clipboard, relying solely on inline icon swaps or label changes for feedback is insufficient, particularly for accessibility. Screen readers may not consistently announce localized changes without proper ARIA live region configuration.
**Action:** Implement a global toast notification container with `aria-live="polite"` and `aria-atomic="true"` to ensure robust screen reader confirmation and consistent visual feedback across the application.
