# Google Workspace monitor implementation notes

Use this reference with the inbound monitoring section when a scheduled job scans Gmail and Calendar through the Google Workspace wrapper.

## Safe scan/commit boundary

1. Read and strictly parse the state file before any API scan. If it is missing, initialize it; if malformed, fail closed rather than scanning from an empty suppression set.
2. Check auth first. If `setup.py --check` succeeds but the optional `gws` backend returns an OAuth/invalid-credentials error, retry through the bundled Python backend before reporting auth failure.
3. Search a bounded inbox window and the relevant calendar range. Apply sender-class exclusions before broad keyword matching.
4. Re-fetch only high-confidence candidates whose snippets are generic, HTML-heavy, or control-character polluted. Preserve the richer search record (`from`, labels, thread context) separately; a `gmail get` result may normalize away sender metadata needed by hard exclusions.
5. Freeze one final candidate list. For each Gmail alert, retain the message ID and a stable hash; for a collapsed thread, retain every observed sibling message ID. For each Calendar alert, retain event ID and a stable hash from summary/start/end/location/description.
6. Suppress a candidate when either its ID or normalized hash is already in state. Normalize legacy `sha:` and `sha:event:` prefixes before comparison.
7. Apply a final deterministic exclusion pass immediately before persistence, then write state exactly once and render the report from the persisted candidate list. Never run a second committing scan to verify; verify membership in the state file or use a non-mutating dry run.

## Relevance defaults

Prefer concrete personal action or impact: billing/payment failure, shipping/order status, school/assessment logistics, appointment confirmation, account access/removal, service suspension, security, or explicit deadlines. Suppress newsletters, promotions, generic verification codes, calendar reminder emails, and routine agenda digests. Calendar events are not automatically relevant merely because they are upcoming; apply the same high-confidence standard unless the job explicitly asks for all events.

## Operational pitfall

Do not hand-rewrite the final report after updating state. A manually trimmed report can diverge from the exact IDs/hashes committed and either omit a new alert or reintroduce a duplicate on a later run.
