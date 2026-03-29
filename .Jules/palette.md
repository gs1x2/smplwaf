## 2026-03-29 - ARIA labels for dynamically created DOM elements
**Learning:** When dynamically creating DOM elements in vanilla JavaScript (e.g., via `document.createElement`), standard assignments or attributes are not always sufficient. ARIA attributes such as `aria-label` must be explicitly assigned using `setAttribute()` to ensure icon-only buttons remain accessible to screen readers, as they bypass static HTML parsing.
**Action:** Always use `setAttribute('aria-label', '...')` when creating icon-only interactive elements dynamically to maintain accessibility compliance.
