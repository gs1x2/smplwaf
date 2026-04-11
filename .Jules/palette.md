## 2024-04-12 - ARIA Labels on Dynamically Created Elements
**Learning:** When dynamically creating DOM elements in vanilla JavaScript (e.g., via `document.createElement`), ARIA attributes such as `aria-label` must be explicitly assigned using `setAttribute()`. This ensures icon-only buttons remain accessible to screen readers, as they bypass static HTML parsing.
**Action:** Use `setAttribute('aria-label', ...)` when dynamically creating UI elements instead of just setting text content or properties, to ensure proper accessibility for screen readers.
