## 2024-05-18 - Empty States in Real-time Dashboards
**Learning:** Real-time monitoring dashboards that wait for active traffic (like CTF firewalls) can cause confusion if they just show an empty table. Users might think the system is broken rather than simply waiting for events.
**Action:** Always include an explicit empty state ("No active sessions", "Waiting for traffic...") in dynamic tables to reassure the user that the system is functioning correctly but currently lacks data.

## 2024-05-18 - Context-Dependent Buttons
**Learning:** Having an enabled action button (like "Block IP") that just alerts the user to "select something first" is a frustrating experience.
**Action:** Buttons that depend on a selected state should be visually and functionally disabled by default (`disabled` attribute, `cursor: not-allowed`, lower opacity) and only enabled dynamically when the required context is provided.
