# RankingPCC inactivity penalty implementation notes

Use this reference when adjusting RankingPCC's activity/decay rule.

## Current rule added in this session

- Activity is calculated as a rolling 52-week window.
- A week counts as active when a player appears in at least one match during that week.
- Players get 12 inactive weeks of grace per year, so 40 active weeks avoids penalty.
- Penalty is 5 points per inactive week beyond the 12-week grace.
  - 40 active weeks / 12 inactive weeks => 0 penalty.
  - 39 active weeks / 13 inactive weeks => -5 points.
  - 38 active weeks / 14 inactive weeks => -10 points.
- The penalty is derived dynamically in `calculateRanking(...)`; do not store fake penalty matches or mutate historical ratings.
- Keep both `baseRating` and penalized `rating` so the UI/tests can distinguish Elo movement from inactivity decay.

## Implementation shape

Primary file: `src/ranking.js`

Recommended exports/constants:

```js
export const INACTIVITY_PENALTY_PER_WEEK = 5;
export const INACTIVITY_GRACE_WEEKS_PER_YEAR = 12;
export const RANKING_ACTIVITY_WINDOW_WEEKS = 52;
```

`calculateRanking(players, matches, options = {})` should accept an `asOf` option for deterministic tests and compute activity from the rolling window. Do not rely on the real current date in tests.

UI transparency added in `src/main.jsx`:

- Ranking row: show `inatividade -X` only when `row.inactivityPenalty > 0`.
- Player card: show `Inatividade: -X pts · Y/52 semanas ativas` only when penalized.
- Rules page: document the 52-week window, 12-week grace, and 5-point penalty.

## Testing notes

- Add/update tests in `src/ranking.test.js` before changing behavior.
- Use deterministic dates with `asOf`.
- For activity tests, generate one match per week with `Date.UTC(...)` to avoid timezone drift.
- Existing tests that assert rating movement may need to assert `baseRating` instead of penalized `rating`, because a single match in a 52-week window triggers inactivity penalty by design.

Suggested verification:

```bash
npm test -- --run src/ranking.test.js src/main.test.jsx
npm run build
```

Then deploy static assets:

```bash
cp -a dist/. /var/www/rankingpcc/
```

Browser-verify `/calculo` includes the inactivity rule text.
