## 2026-04-02 - ARIA labels for dynamic vanilla JS elements
**Learning:** When dynamically creating DOM elements in vanilla JavaScript (e.g., via document.createElement), ARIA attributes such as aria-label must be explicitly assigned using setAttribute().
**Action:** Always use setAttribute() when adding ARIA attributes to dynamically created icon-only buttons to ensure they remain accessible.
