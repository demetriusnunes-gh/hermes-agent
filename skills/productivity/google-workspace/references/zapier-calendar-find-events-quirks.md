# Zapier Google Calendar find-events quirks

Session note:
- The `google_calendar_find_events` action may prompt for a `Calendar` value if it is omitted.
- In this environment, explicitly pass the calendar ID/email (for example, the primary Gmail address) to avoid the follow-up prompt.
- The `ordering` enum is case-sensitive; use `startTime` for start-time sorting.
- If the result set is empty after a valid query, that may simply mean there are no upcoming events in the requested window.
