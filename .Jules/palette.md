## 2024-04-14 - Dynamic DOM Element ARIA Labels
**Learning:** In this application, elements created via vanilla JS `document.createElement()` bypass static HTML parsing. ARIA attributes must be explicitly assigned using `.setAttribute('aria-label', ...)` rather than property assignment to ensure they are picked up by screen readers.
**Action:** Always verify dynamic DOM creation scripts and append explicit `.setAttribute()` calls for accessibility attributes on icon-only interactive controls.
