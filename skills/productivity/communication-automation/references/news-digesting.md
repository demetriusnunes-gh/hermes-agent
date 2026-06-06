# News digesting recipe

Use this as a compact fallback when a dedicated daily-news skill is unavailable.

## Goal
Produce a terse morning digest with only the most consequential items for:
- world
- Brazil
- São Paulo
- Rio de Janeiro
- DoorDash/DASH only if materially relevant

## Recommended source pattern

1. Pull general/world headlines from a high-signal RSS or news search source.
2. Pull Brazil-local candidates with country-specific query terms.
3. Pull São Paulo and Rio candidates separately.
4. Pull DoorDash/DASH separately and include only if it is a material update.

## Practical query set

- World: `Iran Reuters`, `Ukraine Reuters`, `ceasefire Reuters`, or the current top world issue
- Brazil: `Brazil Reuters`, `Brazil tariffs Reuters`, `Lula Reuters`
- São Paulo: `São Paulo G1`, `São Paulo Reuters`, `Guarulhos fire G1`
- Rio: `Rio de Janeiro G1`, `Rio Reuters`, `Rio investment Reuters`
- DoorDash: `DoorDash Reuters earnings`, `DASH Reuters`

## Selection rules

- Keep at most three news lines total unless the spec explicitly allows more.
- Pick the newest, highest-impact item in each bucket.
- Prefer Reuters for global/business and G1 for Brazilian/local coverage.
- Do not include low-signal lifestyle, event, or sports items in a market/news briefing.
- Include a company/stock line only when the move or event is clearly material.

## Output rules

- Header: date only.
- Bullets: one short line per story.
- No URLs unless identification would otherwise be unclear.
- No summary sentences, commentary, or category labels beyond the bullet emoji if desired.
- If there is nothing materially relevant, return `[SILENT]`.
