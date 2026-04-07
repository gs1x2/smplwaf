## 2024-04-07 - Add ARIA label to dynamically created element
**Learning:** When dynamically creating DOM elements in vanilla JavaScript, ARIA attributes such as `aria-label` must be explicitly assigned using `setAttribute()` to ensure screen reader accessibility, because they bypass static HTML parsing.
**Action:** Always use `.setAttribute('aria-label', '...')` for dynamically created icon-only buttons in vanilla JS.
