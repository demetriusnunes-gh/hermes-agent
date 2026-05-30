# Ranking PCC tie-break example

This session surfaced a small but reusable pattern:

- records had `playedAt` for the match date/time
- records also had `createdAt` for save time
- replay/ranking order was correct for normal cases, but ties on `playedAt` were only broken by `id`
- UI "latest results" used the same fragile fallback

## Fix applied

Use `createdAt` as the secondary comparator in both places:

- replay / ranking calculation: ascending by `playedAt`, then ascending by `createdAt`
- "latest results" UI: descending by `playedAt`, then descending by `createdAt`

## Regression test shape

Create two matches with the same `playedAt` but different `createdAt`:

```js
const earlyWinLateLoss = [
  { id: 'z', playedAt: '2026-01-01T12:00:00Z', createdAt: '2026-01-01T10:00:00Z', ... },
  { id: 'a', playedAt: '2026-01-01T12:00:00Z', createdAt: '2026-01-01T11:00:00Z', ... },
];
```

Then reverse the input order and assert the final ranking still reflects `createdAt`, not array order.

## Why this matters

If the user edits or imports a historical match, two records can share the same date. A stable tie-breaker prevents:

- inconsistent ranking results
- different output between local and remote stores
- UI order drifting from replay order

## Implementation note

Keep `createdAt` in the normalized record shape everywhere. If one store path omits it, the comparator falls back to `id` and the deterministic order is lost.