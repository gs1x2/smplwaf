## 2024-03-22 - Dynamic DOM Icon-only Buttons
**Learning:** When dynamically creating DOM elements in vanilla JavaScript (e.g., via `document.createElement`), ARIA attributes such as `aria-label` must be explicitly assigned using `setAttribute()`. This ensures icon-only buttons remain accessible to screen readers, as they bypass static HTML parsing.
**Action:** Always verify that dynamically created icon-only elements have an explicit `aria-label` assigned.
