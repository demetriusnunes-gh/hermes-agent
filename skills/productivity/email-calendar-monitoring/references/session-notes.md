# Session notes: monitoring implementation

Concise implementation notes discovered while running the scheduled inbox/calendar monitor.

## Parsing Gmail search output

- Gmail search output can contain raw control characters or HTML-heavy snippets.
- Use a tolerant JSON parser (`json.loads(..., strict=False)` or equivalent) when loading search results.
- If the search payload is still messy, re-fetch only the small final candidate set with `gmail get` before final relevance or dedup decisions.

## Deduplication

- Normalize legacy hash formats before comparison:
  - treat bare SHA-256 digests and prefixed forms like `sha:` / `sha:event:` / `sha:thread:` as equivalent.
- For Gmail monitoring, canonicalize to one alert per thread after relevance filtering.
- For Calendar monitoring, hash stable visible fields such as summary + start + end + location + description.
- Treat repeated alerts for the same visible item as a bug, not as harmless noise.

## Output discipline

- If no new relevant items survive deduplication, output exactly `[SILENT]`.
- If auth fails, report the auth failure once concisely rather than replaying old alerts.
