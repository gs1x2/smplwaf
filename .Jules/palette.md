## 2024-05-15 - Dynamic DOM and Dark Theme A11y
**Learning:** Vanilla JS apps generating DOM elements often lack `aria-label` for icon-only buttons, making them inaccessible to screen readers. Additionally, dark themes frequently swallow default browser focus rings, severely hurting keyboard navigation visibility.
**Action:** Always verify keyboard focus visibility (`:focus-visible`) in dark modes and ensure dynamically created icon-only buttons receive descriptive `aria-label` attributes.
