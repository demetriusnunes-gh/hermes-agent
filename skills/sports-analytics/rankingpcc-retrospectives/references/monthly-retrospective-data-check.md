# Monthly retrospective data check

## Why freshness matters

A database snapshot labeled with a month-end date can be stale for that month. In the September 2026 retrospective, the September 30 snapshot showed four matches, while later daily backups contained a fifth match played on September 29. The latest backup was therefore the correct source for the retrospective.

## Reproduction pattern

1. Enumerate available backups by date.
2. Choose the newest backup whose data covers the requested month.
3. Query matches by `played_at` for the requested calendar month.
4. Print every matching match with its date, team IDs resolved to player names, winner, and score.
5. Recompute counts and player aggregates from those rows.
6. If ratings or positions are included, replay all matches chronologically up to the end-of-month cutoff using the production ranking implementation.
7. Validate that the number of listed matches equals the queried count before drafting the WhatsApp text.

## Correction protocol

If the user says the count is wrong, treat that as a data-quality signal. Do not patch only the sentence containing the count. Re-query the newest data and recalculate all totals, player records, highlights, ratings, and ranking movement. A corrected report should acknowledge the correction briefly and present the regenerated copy-ready message.

## Formatting notes

For WhatsApp, use chronological match bullets or date labels, bold/italic emphasis, no tables, and a compact closing. Include the complete score and winning pair so the group can audit the summary visually.
