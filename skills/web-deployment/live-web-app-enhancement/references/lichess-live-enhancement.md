# Lichess live enhancement reference

## Visual assets

The Lichess-hosted Cburnett SVG endpoints use these paths:

```text
https://lichess1.org/assets/piece/cburnett/wK.svg
https://lichess1.org/assets/piece/cburnett/bK.svg
```

The pattern covers both colors (`w`/`b`) and all six piece letters (`K`, `Q`, `R`, `B`, `N`, `P`). For a self-hosted site, copy the 12 files into a local `pieces/cburnett/` directory and verify them through the site's public hostname.

## Terminal rating lookup

The board stream's final `gameState` can identify the result without including rating changes. Request the final game export after the terminal state:

```http
GET https://lichess.org/game/export/{gameId}?clocks=0&eval=0&literate=0
Authorization: Bearer ***
Accept: application/json
```

Read `players.white.rating`, `players.white.ratingDiff`, and the corresponding black fields. The post-game rating can be shown as `rating + ratingDiff`. Treat absent deltas and non-2xx responses as a normal unavailable state, not as a fatal game-result error.

## Verification recipe

1. Extract inline JavaScript and run `node --check`.
2. Request the public HTML with a cache-busting query string.
3. Request all new SVGs over the public HTTPS hostname and expect HTTP 200.
4. Navigate with a browser and use a screenshot/vision check for percentage-width and aspect-ratio requirements.
5. Remove any backup artifact from the document root before final verification.
