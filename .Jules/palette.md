
## 2026-05-06 - Keyboard Accessibility for Hover-Revealed Controls
**Learning:** Using `display: none` to hide controls until hover completely removes them from the accessibility tree, making keyboard navigation impossible. Additionally, when dynamically generating DOM elements (e.g., via `document.createElement`), native HTML parsing is bypassed, so ARIA attributes must be explicitly assigned using `.setAttribute()`.
**Action:** Use `opacity: 0` and `pointer-events: none` combined with `:focus-within` for hidden controls instead of `display: none`, and always apply `aria-label` attributes to dynamically created icon-only or status buttons via JavaScript.
