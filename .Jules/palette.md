
## 2026-04-12 - Adding ARIA labels to dynamically generated elements
**Learning:** In vanilla JavaScript without a framework like React, dynamically created DOM elements (e.g., via `document.createElement`) bypass static HTML parsing. ARIA attributes such as `aria-label` must be explicitly assigned using `setAttribute()` to ensure accessibility for screen readers.
**Action:** When creating UI elements dynamically in vanilla JS, specifically icon-only buttons or interactive elements, always use `setAttribute('aria-label', '...')` to ensure they remain accessible.
