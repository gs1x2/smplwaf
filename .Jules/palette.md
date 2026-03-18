## 2026-03-17 - Adding Accessible Controls to Rule Tree Items
**Learning:** The rule tree view had buttons ('ВКЛ'/'ВЫКЛ' and 'X') that lacked clear context for screen reader users and tooltip context for mouse users. These controls are critical for managing the system's rules.
**Action:** Updated `app/web/static/index.html` to dynamically attach `aria-label` and `title` attributes to the toggle and delete buttons within the rules tree based on their state.
