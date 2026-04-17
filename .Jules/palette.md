## 2026-04-17 - Dynamic DOM ARIA Accessibility
**Learning:** When dynamically creating DOM elements in vanilla JavaScript (e.g., via `document.createElement`), ARIA attributes such as `aria-label` must be explicitly assigned using `setAttribute()`. Direct property assignment for ARIA attributes doesn't work the same way as standard properties.
**Action:** Always use `setAttribute('aria-label', value)` and include a `title` property when creating icon-only buttons via JS to ensure screen reader accessibility and provide hover context.
