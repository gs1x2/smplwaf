## 2026-03-27 - Keyboard Accessibility for Hover-Reveal Actions
**Learning:** Using `display: none` for hover-reveal actions (like file controls) completely removes them from the tab order, trapping keyboard users.
**Action:** Use `opacity: 0` and `pointer-events: none` combined with `:focus-within` and `:hover` to keep interactive elements in the accessibility tree while hiding them visually until needed.
