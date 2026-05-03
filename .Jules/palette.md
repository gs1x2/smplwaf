## 2024-05-04 - Hidden Controls Accessibility
**Learning:** Using `display: none` paired with `:hover` to show file controls completely removes them from the tab order, making them entirely inaccessible to keyboard navigation and screen readers.
**Action:** Always prefer `opacity: 0` alongside `opacity: 1` on `:focus-within` (and ensure they remain focusable elements via `display` properties) to ensure components remain accessible while hidden.

## 2024-05-04 - Dynamically Rendered ARIA Labels
**Learning:** In vanilla JavaScript, dynamically generating icon buttons without explicit text leaves screen readers without context because static HTML parsers cannot infer the button's purpose post-render.
**Action:** When building elements via `document.createElement`, ensure `setAttribute('aria-label', ...)` is added for icon-only or shortened buttons, keeping localization context in mind.
