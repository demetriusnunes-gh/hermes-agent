---
name: live-web-app-enhancement
description: "Safely enhance an already-public web app while preserving hosting, validating browser behavior, and verifying the live result."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
tags: [web, deployment, frontend, static-site, caddy, verification, browser]
metadata:
  hermes:
    related_skills: [web-deployment]
---

# Live Web App Enhancement

Use this skill when a user asks to improve a site that is already publicly hosted. The goal is to make the smallest correct change, preserve the existing runtime and reverse proxy, and verify the public rendering rather than stopping after editing files.

## Workflow

1. **Identify the serving path before editing.** Locate the public hostname's document root or application process, inspect the reverse-proxy route, and determine whether the site is static or backed by a runtime. Do not assume the current repository is the deployed source.
2. **Inspect the existing implementation.** Find the exact render path, CSS constraints, and state transition that owns the requested behavior. Prefer a targeted patch over a rewrite.
3. **Keep public assets local and deterministic.** For visual assets, use a stable upstream source only during acquisition, then store the required files under the site's public asset directory. Verify every referenced asset returns 200 through the public hostname. Do not leave backup files, editor swaps, or temporary artifacts in the web root.
4. **Preserve compatibility.** Keep existing no-dependency and device-specific constraints unless the user explicitly asks to remove them. When changing a board or other responsive component, update both width and height/aspect rules so the element remains usable and square where appropriate.
5. **Implement state-dependent features at the authoritative transition.** For a game result, order completion, or similar terminal state, update the UI from the final event/state handler. If the event omits secondary data, make a follow-up request to the authoritative export/detail endpoint and provide a graceful unavailable state.
6. **Validate before announcing completion.** Run a syntax check appropriate to the changed code. Fetch the public HTML/assets with a cache-busting query. Use a browser navigation and, when visual layout matters, a screenshot/vision check at the real viewport. Verify both the requested change and that existing primary controls remain present.
7. **Report accurately.** Distinguish code deployed and publicly verified from behavior requiring an authenticated or real user flow. If an end-to-end authenticated action was not possible, say so plainly instead of claiming it was tested.

## Reusable patterns

### Lichess-style SVG chess pieces

For Lichess-compatible board visuals, the Cburnett piece set is available at `https://lichess1.org/assets/piece/cburnett/{w|b}{K|Q|R|B|N|P}.svg`. Download the 12 required files into a local `pieces/cburnett/` directory and render them as `<img>` elements. This avoids inconsistent Unicode glyph shapes and reproduces the familiar outlined white / shaded black appearance.

Use an asset helper rather than duplicating paths:

```js
function getPieceAsset(piece) {
    var color = piece === piece.toUpperCase() ? 'w' : 'b';
    return 'pieces/cburnett/' + color + piece.toUpperCase() + '.svg';
}
```

### Lichess rating changes after game end

The board game stream's terminal state may provide status and winner but not rating deltas. After the terminal state is displayed, request:

```text
/game/export/{gameId}?clocks=0&eval=0&literate=0
```

with the user's bearer token and `Accept: application/json`. Read `players.white.rating`, `players.white.ratingDiff`, and the corresponding black fields. Display the old rating, new rating (`rating + ratingDiff`), and signed delta. Handle missing deltas and request failures with text such as “Rating changes are not available yet.”

For the Lichess-specific asset/API details and verification recipe, see `references/lichess-live-enhancement.md`.

## Pitfalls

- A local file edit is not proof that the public host serves the new version; always request the exact public URL.
- A desktop screenshot can expose an unintended max-width cap; if the user asks for a percentage-width element, inspect the rendered pixel width and remove or revise the cap rather than trusting CSS alone.
- A follow-up API request can be delayed or unavailable immediately after game completion; show a loading state and a non-error fallback.
- Avoid putting `.bak`, temporary, or debug files in a public document root.
- Do not alter the reverse proxy or restart unrelated services for a static-file-only change.

## Verification checklist

- [ ] Exact deployed file and serving route identified.
- [ ] Targeted implementation patch applied.
- [ ] Syntax check passes.
- [ ] All new public assets return 200.
- [ ] Public HTML contains the new markers after cache busting.
- [ ] Browser screenshot confirms the visual requirement at the actual viewport.
- [ ] Authenticated/terminal behavior is either end-to-end tested or explicitly marked unverified.
- [ ] No temporary artifacts remain in the web root.
