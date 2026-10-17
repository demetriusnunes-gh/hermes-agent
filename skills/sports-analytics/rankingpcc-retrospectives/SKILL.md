---
name: rankingpcc-retrospectives
description: Prepare accurate monthly retrospectives of RankingPCC matches and ranking movement, with WhatsApp-ready formatting.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [rankingpcc, tennis, monthly-report, whatsapp, sports-analytics]
    related_skills: [rankingpcc-rating-analysis, rankingpcc-app-maintenance]
---

# RankingPCC Monthly Retrospectives

## When to use

Use this skill when the user asks for a monthly recap, retrospective, summary, or WhatsApp post about RankingPCC matches, player performance, rating movement, or ranking movement.

## Required workflow

1. **Use the freshest authoritative data available.** Prefer the live app data or the newest local database backup, not an older month-end snapshot. A later backup may contain games entered retroactively or games played near the end of the month.
2. Inspect the match schema and player names before calculating. Confirm that match dates come from `played_at`, teams are represented by player IDs, and parsed scores contain winner, format, actual games, and Elo games.
3. Filter by the calendar month requested, using the event's recorded `played_at` date. State the date range or data cutoff when useful.
4. Count and verify:
   - matches;
   - distinct players;
   - sets;
   - wins and losses by player;
   - game differential, clearly distinguishing actual games from Elo-weighted games when relevant;
   - format distribution if it adds value.
5. Reproduce the production RankingPCC ranking logic when reporting rating or position changes. Replay all matches chronologically; do not infer rating changes by subtracting arbitrary current totals.
6. Compare the ranking immediately before the month with the ranking at the end of the month. Report position movement only when the baseline is clear.
7. Cross-check the match count against the database before drafting. If the user corrects a count, re-query the newest data source and regenerate all dependent statistics; do not merely edit the prose.
8. Produce a WhatsApp-ready message in Portuguese when the user is writing Portuguese. Use short paragraphs, bullets, bold/italic emphasis, emojis sparingly, and no Markdown tables.
9. Include the complete list of monthly matches with date, winning pair, losing pair, and score, followed by concise highlights.
10. Distinguish facts from interpretation. Labels such as “destaque do mês” should be supported by activity, W-L record, rating movement, or ranking movement.

## Recommended report structure

- Title: `*Retrospectiva de [mês] — Ranking PCC 🎾*`
- Verified totals: matches, players, sets.
- Chronological match list.
- Highlights: most active player, unbeaten players, rating rises/falls, ranking-position movement.
- Closing sentence suitable for the club WhatsApp group.

## Data freshness and correction pitfalls

- Do not assume a backup named for the previous month contains every match played in that month. Later backups can add records for the prior month.
- Do not call a player “invicto” unless the monthly W-L record is explicitly 100% wins.
- Do not call the player with the largest rating rise the player with the best monthly record without checking both metrics.
- In doubles, count one match for each participating player and one team result for each side; avoid counting player appearances as matches.
- Super-tiebreak reporting may use actual points/games for the readable score but Elo-weighted games for ranking calculations. Label the metric when showing aggregates.
- If a correction changes the number of matches, recalculate totals, player records, highlights, and ranking movement from scratch.

## Validation checklist

Before sending the post:

- Match total equals the number of listed matches.
- Every listed player name exists in the player table.
- Every score matches the stored record and winner.
- Monthly W-L totals reconcile with player appearances.
- Unbeaten and most-active claims match the computed records.
- Ranking movement is based on the same cutoff and ranking formula for both snapshots.
- No stale or duplicate match from an older backup is included.
- The final text is directly copyable into WhatsApp.

## Supporting reference

See `references/monthly-retrospective-data-check.md` for the data-freshness and recalculation pattern learned from a prior month-end correction.
