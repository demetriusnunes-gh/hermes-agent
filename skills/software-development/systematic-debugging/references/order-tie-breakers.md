# Ordering and tie-breakers

Use this note when a list or report sorts correctly on the primary key but still appears in the wrong order for tied items.

## Checklist
- Confirm the primary sort key matches the user-facing concept (e.g. `playedAt`).
- Inspect the secondary sort key: it should reflect the *business* ordering, not just a convenient unique field.
- Prefer a creation timestamp (`createdAt` / `created_at`) when the requirement is "order by registration order".
- Do **not** use an opaque identifier (`id`) as a proxy for registration order unless the ID is explicitly sequential and monotonic.
- If the data model stores both domain time and record time, document which one is used for sorting and why.

## Pattern
```js
function sortDesc(a, b) {
  return new Date(b.playedAt) - new Date(a.playedAt)
      || new Date(b.createdAt) - new Date(a.createdAt);
}
```

## Why this matters
- `id` usually only guarantees uniqueness, not creation order.
- UUIDs are especially bad as ordering keys because their lexical order is unrelated to when records were inserted.
- `createdAt` gives deterministic tie-breaking that matches how users think about "latest registered" entries.
