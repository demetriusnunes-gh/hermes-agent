# Skill discovery, source ordering, and session recall

Condensed notes from a research pass on Hermes agentic workflows.

## Skill discovery
- `skills_list` is metadata-first: name, description, category; `skill_view` is the step for full instructions and linked files.
- Hub search is lexical/textual, not semantic: it searches name/description/tags and then merges source hits.
- `unified_search()` fans out in parallel and deduplicates by skill name, preferring higher trust in this order: `builtin` > `trusted` > `community`.
- Source order currently includes official optional skills, skills.sh, well-known, GitHub, ClawHub, Claude Marketplace, and LobeHub adapters.

## Trust and filtering
- GitHub skills from `openai/skills` and `anthropics/skills` are treated as trusted; other GitHub repos are community.
- Platform compatibility and user-disabled skills are filtered before display/load.
- For AI-agent workflows, discovery should prefer official/trusted sources first, then broaden if needed.

## Session recall
- `session_search` is for past conversations, not the current turn.
- It hides `tool`-sourced sessions and avoids surfacing the active lineage/root session in browsing results.
- Transcript formatting truncates long tool output and preserves tool-call names so the recap emphasizes actions, outcomes, and unresolved items.
- Use it to recover delegation/cronned work and other agent workflow history before asking the user to repeat context.