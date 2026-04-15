## 2025-01-20 - Accessible Vanilla JS UI Buttons
**Learning:** Dynamically generated icon-only buttons in vanilla JS bypass static HTML parsing. They require explicit `setAttribute('aria-label', ...)` assignment to be accessible to screen readers, rather than just using a text character like "X".
**Action:** Always use `setAttribute('aria-label', ...)` and add a `title` property when dynamically generating icon-only buttons using `document.createElement`.
