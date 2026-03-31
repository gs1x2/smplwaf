# Palette UX Journal

## 2024-04-01 - Dynamic DOM Elements Need Explicit ARIA
**Learning:** When dynamically creating UI elements like icon-only buttons via `document.createElement()` in vanilla JavaScript, their ARIA attributes (such as `aria-label`) must be explicitly set via `setAttribute()`. Standard static HTML parsers or linters miss these elements, making them functionally invisible to screen readers if neglected.
**Action:** Always verify that any interactive element generated via vanilla JS dynamically has an explicitly assigned ARIA label using `setAttribute()`.