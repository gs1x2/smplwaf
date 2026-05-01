## 2024-05-01 - Hidden Action Accessibility
**Learning:** Hidden controls (like file actions) that rely solely on `display: none` and `:hover` are completely inaccessible to keyboard users, breaking the ability to manage rules without a mouse.
**Action:** Always prefer `opacity: 0` with `pointer-events: none` and reveal on `:focus-within` to maintain spatial layout and enable keyboard tab navigation.
