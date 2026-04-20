## 2026-04-20 - Dynamic DOM Element Accessibility
**Learning:** Dynamically created DOM elements (e.g., via `document.createElement`) bypass static HTML parsing, meaning standard attributes won't automatically apply.
**Action:** Explicitly assign ARIA attributes like `aria-label` using `setAttribute()` to ensure icon-only buttons remain accessible to screen readers.
