
## 2024-03-28 - Dynamic Element Accessibility
**Learning:** In dynamically constructed DOM elements like tables, missing `aria-label` attributes on icon-only buttons (`btnDel`) make them entirely opaque to screen readers because they fall outside static HTML parsing.
**Action:** Always map programmatic dynamic element creation (e.g., `document.createElement('button')`) to require explicit `setAttribute('aria-label')` alongside standard text content assignment when the content is purely symbolic (e.g., 'X').
