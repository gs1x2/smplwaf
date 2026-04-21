## 2024-05-24 - Dynamic DOM Element ARIA Attributes
**Learning:** Dynamically created DOM elements in vanilla JavaScript (e.g., via `document.createElement`) bypass static HTML parsing. ARIA attributes such as `aria-label` cannot simply be set as properties and must be explicitly assigned using `setAttribute()`. This is critical to ensure screen readers announce icon-only buttons correctly.
**Action:** Always use `setAttribute('aria-label', '...')` when creating icon-only buttons dynamically via JavaScript, rather than relying on direct property assignment or omitting the label entirely.
