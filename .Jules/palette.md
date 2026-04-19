## 2024-04-18 - Missing ARIA Labels on Icon Buttons
**Learning:** Dynamically created icon-only buttons (like the delete "X" and toggle "ВКЛ/ВЫКЛ" buttons) in vanilla JS bypass static HTML parsing, so screen readers rely entirely on their text content, which is unhelpful for symbols like "X".
**Action:** When dynamically creating DOM elements via `document.createElement`, explicitly assign ARIA attributes like `aria-label` using `setAttribute()` to ensure accessibility.
