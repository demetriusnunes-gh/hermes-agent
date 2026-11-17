# Historical ranking replay

## Define independent parameters

1. **Elo history:** all stored matches by default; filter only if the user explicitly wants a period-only Elo simulation. Preserve each player's configured `initialRating`.
2. **Observation window:** when best positions may be recorded. Apply a year/day cutoff in the user's BRT timezone, not implicit UTC.
3. **Player eligibility:** official snapshots require `gamesPlayed >= 20`; no-minimum snapshots require `gamesPlayed > 0`. Counts belong to the historical prefix used for that snapshot.
4. **Field-size gate:** optionally require at least N eligible players before recording peaks. Do not reset Elo when the gate opens.

Do not conflate these parameters: keeping all historical games while observing peaks only after a cutoff differs from rebuilding Elo using only games after that cutoff.

## Read and replay

1. GET `/players` and `/matches` from the production API. Retain a single snapshot for all variants being directly compared; if re-fetching, report that the snapshot changed rather than attributing all differences to the new parameters. Exclude base64 profile photos from printed output.
2. Normalize API fields: `initial_rating` to `initialRating`; `team_a`, `team_b`, `score_text`, `played_at`, `created_at` to their camelCase names. Keep IDs unchanged.
3. Inspect the current `src/ranking.js` comparator and the UI eligibility logic before calculating. Import `calculateRanking` and `normalizeDateString` with Node ES modules from the app directory; pass JSON through stdin. Preserve the app's event-time, creation-time, ID ordering and its ranking tie-breakers instead of sorting only by Elo.
4. Sort matches chronologically using normalized dates. For all-history Elo with a reporting cutoff, calculate the prefix strictly before the cutoff and record its ranking as the opening snapshot at the cutoff. This captures positions already held at the beginning of the reporting period.
5. Extend the prefix one match at a time. Call `calculateRanking(players, prefix)`, filter historical eligibility, then check the field-size gate. Enumerate positions only after filtering; guests must not create gaps in official positions.
6. For every eligible player, update the saved peak only when the ordinal position is strictly smaller. Save the snapshot timestamp, triggering match ID, and eligible field size. Strict improvement preserves the first occurrence; evaluate all players, not just the four participants.
7. Preserve each distinct match, even when date, teams, and score repeat. Final and qualifying matches may legitimately be identical. Same-day peak dates can refer to different intermediate snapshots, so do not imply tied positions.
8. Save the report JSON in the active profile's scratch workspace. Repeated prefix calculation is simple and adequate for a small club history; do not introduce a separate Elo formula merely to optimize it.

## Verify before reporting

- Account for every player: a peak record or an explicit unranked result.
- Check each peak date lies within the observation window and satisfies the historical eligibility and field-size gates.
- Check peak position is no worse than the current position when the current snapshot qualifies.
- Check full-history match count equals pre-cutoff plus in-window match counts.
- Compare the final replay with `calculateRanking` over the complete selected history; filtering eligibility changes position numbering, not Elo.
- Explain that a peak dated at the reporting cutoff can be an inherited position, not a match played that day.
- State that results are reconstructed with the current formula and stored match ordering when discussing historical accuracy; this is not proof of exactly what an older deployed formula displayed.

## Output

Use a short scenario statement, then bullets of `Name: best position — first date`. List zero-game players separately. Add field-size context only when early peaks are misleading. Keep simulations read-only and distinguish calculation results from implemented website features.
