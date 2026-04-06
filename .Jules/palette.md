## 2026-04-05 - Dynamic Element ARIA Labels
**Learning:** When dynamically creating DOM elements in vanilla JavaScript (e.g., via `document.createElement`), ARIA attributes such as `aria-label` must be explicitly assigned using `setAttribute()`. This ensures icon-only buttons remain accessible to screen readers, as they bypass static HTML parsing.
**Action:** Always verify dynamically created interactive elements and use `setAttribute()` to assign required accessibility attributes.
