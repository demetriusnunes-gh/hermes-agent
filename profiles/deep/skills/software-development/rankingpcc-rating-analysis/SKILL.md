---
name: rankingpcc-rating-analysis
description: Simulate, audit, and compare RankingPCC Elo/rating algorithms against current app data before changing production code.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [rankingpcc, elo, rating, simulation, supabase, tennis]
    related_skills: [rankingpcc-app-maintenance, spike, systematic-debugging]
---

# RankingPCC Rating Analysis

## When to use

Use this skill when the user asks to analyze, compare, simulate, or redesign the RankingPCC rating/ranking calculation before committing to app changes. This includes Elo formula comparisons, alternative K factors, inactivity penalties, scoring-format changes, and ranking output previews.

For full app editing/deployment workflows, also load `rankingpcc-app-maintenance`. This skill is specifically for **read-only rating experiments and analysis**.

## Core workflow

1. Treat rating experiments as read-only unless the user explicitly asks to implement.
2. Pull the current dataset from the same source as the app, usually Supabase via `.env` values:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
   - tables: `players`, `matches`
3. Do not print secrets or full `.env` contents.
4. Write throwaway simulation code outside the repo, e.g. under `/tmp`, unless the user asks for a reusable script.
5. Reimplement parser/ranking behavior inside the simulation when the proposed algorithm changes parsing semantics. Do not blindly import production `parseScore()` if the experiment changes match-format classification.
6. Output dataset sanity counts before the ranking:
   - players
   - matches
   - processed matches
   - parse errors
   - format counts under the simulated rules
7. Output a compact ranked table. Include enough columns to explain the movement, commonly:
   - rank, player, rating
   - games played, W-L, win rate
   - Elo delta from match outcomes
   - inactivity penalty or other experimental adjustment
   - game differential
8. State clearly whether any website/code/data changes were made. For simulations, say that none were made.
9. When comparing variants, compute each variant by replaying all matches chronologically rather than subtracting current totals. Removing participation bonus, removing inactivity penalties, or changing a format K changes intermediate ratings, which affects later Elo expected probabilities.
10. For user-facing comparison tables, compare the simulated ranking to `calculateRanking(players, matches)` from production code in the same script so rank/rating deltas use the live baseline.
11. For “unify best of 3” experiments, explicitly state whether both the Elo K and the inactivity penalty are unified. The user may mean only K=40, but a true single format likely also maps `best_of_3_full` penalty from 6 to 4.

## Current production baseline

RankingPCC’s production Elo logic lives in `src/ranking.js`.

Baseline shape:

- Default initial rating: `1000`
- Doubles team rating: average of the two partners
- Expected win probability:

  ```txt
  expectedA = 1 / (1 + 10 ^ ((teamRatingB - teamRatingA) / 400))
  ```

- Current production K factors:
  - short set: 10
  - single set: 20
  - best of 3 with super tiebreak: 40
  - best of 3 full: 60
- Current production format nuance:
  - `inferFormat()` still keeps `best_of_3_super` and `best_of_3_full` as separate internal formats for weighting.
  - 2 reported normal sets and 3 sets ending in super tiebreak => `best_of_3_super`.
  - 3 full normal sets => `best_of_3_full`.
  - `describeFormat()` displays both as `melhor de 3`, so the UI label is simplified even though the Elo weighting is not.
- Current production margin multiplier:

  ```txt
  marginMultiplier = min(1.5, 1 + margin / total)
  ```

- Current production delta:

  ```txt
  deltaA = round(k * marginMultiplier * (scoreA - expectedA))
  deltaB = -deltaA
  ```

## References

- `references/rating-simulation-inactivity-elo.md` — session-derived example for simulating Elo with inactivity penalties and changed K factors.

## Pitfalls

- The user may ask to “simulate here first”; do not edit `src/ranking.js`, tests, deployment files, or Supabase data for that request.
- Match-format interpretation can be part of the experiment. In one session, the requested rule was: exactly two reported sets should count as `best_of_3_super`, even though production behavior differed.
- Keep experimental outputs legible and concise; the user wants enough explanation to decide whether to change the website, not a code dump.
- If using the Supabase JS package from a standalone Node script, import from the installed package’s actual ESM entrypoint if bare/package-subpath imports fail.
