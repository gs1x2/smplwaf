
## 2024-04-10 - Vanilla JS Dynamic Element A11y
**Learning:** When dynamically creating DOM elements via vanilla JS `document.createElement`, basic attributes like `textContent` and `style` properties are not enough for screen-reader accessibility. ARIA attributes must be explicitly assigned using `setAttribute('aria-label', ...)` because they bypass static HTML parsing. Icon-only buttons or state-toggling buttons dynamically created require this approach.
**Action:** Always verify that dynamically created interactive elements explicitly set `aria-label` using `setAttribute()`, especially if they use icons or terse state labels ("ON"/"OFF" or "X").
