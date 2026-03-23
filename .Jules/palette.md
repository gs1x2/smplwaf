## 2024-03-23 - Initialization

## 2024-03-23 - Focus States and ARIA labels
**Learning:** The app's custom UI entirely lacked visible focus states (`:focus-visible`), making keyboard navigation impossible to track. Dynamic elements (like rule toggle/delete buttons) were generated purely as functional buttons without semantic labels or tooltips.
**Action:** Implemented a global `:focus-visible` outline for all interactive elements to instantly enable keyboard accessibility across the entire app. Added `aria-label` and `title` attributes to dynamically generated icon/short-text buttons to support screen readers and provide hover context. Always remember to localize accessibility strings (Russian in this case) to match the app's primary language.