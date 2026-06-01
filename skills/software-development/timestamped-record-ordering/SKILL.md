---
name: timestamped-record-ordering
description: Use when records are ordered by an event timestamp but creation order must break ties deterministically across calculations, rankings, and UI lists.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ordering, timestamps, ui, ranking, deterministic, supabase, react]
    related_skills: [test-driven-development, requesting-code-review]
---

# Timestamped Record Ordering

## Overview

Many apps store two different timestamps for a record:

- the *event time* (when the thing happened)
- the *creation time* (when the record was saved)

If the app sorts or replays records chronologically, event time is usually the primary key. But when multiple records share the same event time, you still need a stable, deterministic secondary order. Using `createdAt` as the next tie-breaker is a common fix because it preserves the order of registration without changing the meaning of the event timestamp.

This skill covers the end-to-end pattern: data model, normalization, sort helpers, derived calculations, UI lists, and regression tests.

See `references/rankingpcc-createdAt-tiebreak.md` for a compact real-world example and test shape.

## When to Use

Use this skill when:

- a UI shows "latest results", "recent activity", timelines, feeds, match history, logs, or audit-style records
- calculations depend on replaying records in chronological order
- two records can legitimately share the same primary timestamp
- the app stores or syncs records through multiple backends and you need the ordering to remain stable everywhere
- a local/demo store and a remote store should produce the same sort order

Do not use this skill for:

- random ordering or user-curated ordering
- records that already have an explicit manual sequence number
- one-off ad hoc sorting where ties do not matter

## Core Pattern

### 1) Preserve both timestamps in the model

Keep the event timestamp and creation timestamp on the record object everywhere:

- backend row
- API response
- local store payload
- frontend normalized shape

Typical naming:

- database: `played_at`, `created_at`
- app state: `playedAt`, `createdAt`

If the remote schema uses timestamps with automatic defaults, ensure the local store also populates `createdAt` when creating a new record so both environments stay comparable.

### 2) Use one comparator everywhere

Define a single comparator and reuse it for:

- ranking/replay calculations
- list views such as "latest results"
- player drill-downs or history modals
- any derived breakdown that depends on replay order

Recommended order:

1. event timestamp (`playedAt`) ascending for replay logic, descending for "latest first" views
2. creation timestamp (`createdAt`) as the secondary tie-breaker
3. stable fallback (`id`) only as a last resort

Example ascending comparator for history/replay:

```js
function compareChronological(a, b) {
  return new Date(a.playedAt) - new Date(b.playedAt)
    || new Date(a.createdAt || 0) - new Date(b.createdAt || 0)
    || String(a.id).localeCompare(String(b.id));
}
```

Example descending comparator for UI lists:

```js
function compareLatestFirst(a, b) {
  return new Date(b.playedAt) - new Date(a.playedAt)
    || new Date(b.createdAt || 0) - new Date(a.createdAt || 0)
    || String(b.id).localeCompare(String(a.id));
}
```

### 3) Keep the calculation order and the UI order aligned

A common bug is to sort the visible list one way while the calculation engine replays the data another way. That makes the app look correct in the feed but produce inconsistent derived values.

Rule of thumb:

- if the calculation uses `createdAt` as a tie-breaker, the UI should too
- if the UI uses `createdAt` as a tie-breaker, the replay/calculation layer should too

### 4) Test the tie case explicitly

The important regression is not the "normal" case. It is the tie case:

- two records with the same `playedAt`
- different `createdAt`
- input array order reversed
- the final output should still be deterministic

Write one test that proves the result changes when `createdAt` changes, not when the array order changes.

## Implementation Checklist

1. **Audit the schema**
   - confirm the record has an event timestamp and a creation timestamp
   - if the creation timestamp is missing in one storage path, add it there first

2. **Normalize the shape**
   - map remote snake_case to app camelCase
   - include both timestamps in the normalized object
   - avoid silently dropping `createdAt`

3. **Centralize the comparator**
   - use a shared helper instead of duplicating inline sort logic
   - keep the ascending and descending versions consistent

4. **Use the same ordering in derived logic**
   - ranking calculations
   - drill-down breakdowns
   - "latest results" cards
   - history modals

5. **Add regression tests**
   - same `playedAt`, different `createdAt`
   - reverse input order and assert the same output
   - verify both calculation and UI-facing ordering if both exist

6. **Verify the build**
   - run targeted tests for the calculation module
   - run the app build or UI test suite after the comparator change

## Common Pitfalls

1. **Using `id` as the second sort key.**
   IDs are arbitrary and usually encode creation order only by accident. They can diverge across syncs, imports, migrations, or test fixtures.

2. **Sorting the list but not the replay engine.**
   The feed looks right, but the calculated ranking or deltas change when the record order changes.

3. **Forgetting local/demo storage.**
   Remote rows may have `created_at`, but the local store may not populate `createdAt` unless you add it explicitly.

4. **Dropping `createdAt` during normalization.**
   If the frontend only keeps the event timestamp, there is nothing left to break ties with later.

5. **Assuming date-only input is enough.**
   The user may choose only a date in the UI, but the app still needs a timestamped canonical representation for deterministic replay.

6. **Writing tests that only cover one input order.**
   That misses the exact bug this pattern is meant to prevent.

## Verification Checklist

- [ ] event timestamp is preserved end-to-end
- [ ] creation timestamp is preserved end-to-end
- [ ] calculation/replay ordering and UI ordering use the same tie-break rule
- [ ] tie cases with identical event timestamps are deterministic
- [ ] tests cover reversed input order
- [ ] build or targeted test suite passes
- [ ] if the change is deployed behind a live site, verify the served bundle is current and inspect the rendered list order in the browser, not just the source code

## Supporting Reference

- `references/rankingpcc-createdAt-tiebreak.md` — compact case study with the ranking app fix, comparator shape, and the regression test that guards it.
- `references/live-ui-verification.md` — live-site validation notes: stale bundle detection, cachebust checks, and browser-level confirmation of the rendered order.
- `references/browser-dom-extraction.md` — DOM-query pattern for extracting rendered match rows and turning them into month-level analysis.
