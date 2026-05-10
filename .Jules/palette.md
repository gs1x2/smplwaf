## 2024-05-14 - Dynamic Icon-only Buttons Accessibility
**Learning:** When dynamically creating DOM elements in vanilla JavaScript (e.g., via `document.createElement`), ARIA attributes such as `aria-label` must be explicitly assigned using `setAttribute()`. This ensures icon-only buttons remain accessible to screen readers, as they bypass static HTML parsing.
**Action:** Always check dynamically injected UI controls in `app/web/static/index.html` (like rule controls) to ensure they have appropriate ARIA attributes set programmatically.
