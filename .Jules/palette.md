## 2024-03-24 - Accessibility for Dynamically Generated UI Elements
**Learning:** In applications relying heavily on vanilla JS DOM manipulation (like this app), dynamically created interactive elements (buttons, toggles) often omit crucial accessibility attributes like `aria-label` and `title`, making them unusable for screen readers. This is especially problematic for icon-only buttons (like 'X' for delete).
**Action:** Always use `.setAttribute('aria-label', ...)` and `.title` immediately after `document.createElement` for interactive elements.
