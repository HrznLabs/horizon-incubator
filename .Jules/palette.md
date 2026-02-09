## 2024-05-22 - Documentation as UX
**Learning:** In non-code repos, the "interface" is the documentation structure. Adding TOCs and proper semantics directly improves the user journey.
**Action:** Always check for long markdown files without TOCs as a quick win.

## 2026-02-09 - [Mermaid Dark Mode Contrast]
**Learning:** Default Mermaid themes ('dark') handle standard elements well, but hardcoded `rect rgb(...)` backgrounds often break text contrast in dark mode diagrams.
**Action:** When enabling dark mode for Mermaid, always audit and manually adjust `rect` background colors to ensure white text remains readable.
