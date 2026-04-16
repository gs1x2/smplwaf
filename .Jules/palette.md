## 2024-04-17 - Dynamic DOM Elements and Accessibility
**Learning:** In vanilla JavaScript without a framework, dynamically creating UI elements (e.g., `document.createElement('button')`) bypasses static HTML parsing. Consequently, ARIA attributes like `aria-label` for icon-only buttons must be explicitly assigned using `setAttribute()` since they are not present in standard markup.
**Action:** Always ensure dynamically generated icon-only buttons (like the rule deletion 'X' button) have their `aria-label` set via JavaScript to maintain screen reader accessibility.
