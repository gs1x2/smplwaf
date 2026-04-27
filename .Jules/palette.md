## 2024-04-28 - Icon Buttons Missing ARIA Labels
**Learning:** Icon-only buttons created dynamically via JavaScript in vanilla JS projects (like the "X" delete rule button) bypass static HTML parsing and often miss critical accessibility attributes like `aria-label`, making them unusable for screen readers.
**Action:** Always verify `setAttribute('aria-label', '...')` is explicitly called when creating icon-only elements dynamically via `document.createElement`.
