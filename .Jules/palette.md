
## 2024-05-23 - Keyboard accessibility for dynamic hover controls
**Learning:** Using `display: none` to hide UI controls until they are hovered removes them from the accessibility tree and prevents keyboard users from focusing them via Tab. Additionally, when vanilla JavaScript dynamically injects icon-only buttons via `document.createElement`, they bypass static HTML parsing and inherently lack context.
**Action:** Use `opacity: 0` combined with `:focus-within` alongside `:hover` to hide elements visually while retaining keyboard focusability. Always use `setAttribute('aria-label', ...)` when dynamically creating icon buttons in JS to ensure screen reader support.
