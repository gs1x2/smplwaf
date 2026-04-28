## 2024-10-18 - Keyboard accessibility for hover-revealed UI controls

**Learning:** Hiding UI controls (like file action buttons) with `display: none` until a container is hovered breaks keyboard navigation, because `display: none` removes elements from the DOM and tab order. Furthermore, when creating DOM elements dynamically in vanilla JavaScript, attributes like `aria-label` are easily missed since they bypass static HTML linters.

**Action:** For UI elements meant to appear on interaction, always use `opacity: 0` alongside `pointer-events: none` and reveal them using both `:hover` and `:focus-within` to support both mouse and keyboard users. Additionally, always explicitly use `.setAttribute('aria-label', ...)` when instantiating icon-only buttons dynamically via `document.createElement()`.
