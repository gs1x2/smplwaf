## 2024-05-24 - Dynamic DOM ARIA Labels
**Learning:** When dynamically creating DOM elements with `document.createElement` in vanilla JS, ARIA labels for icon-only buttons bypass static HTML parsers and must be explicitly added using `setAttribute('aria-label', ...)`.
**Action:** Always manually invoke `setAttribute` when creating interactive icon-only elements dynamically to ensure they are accessible to screen readers.
