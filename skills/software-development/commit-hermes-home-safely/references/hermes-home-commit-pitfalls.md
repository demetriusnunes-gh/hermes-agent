# ~/.hermes commit pitfalls observed in session

## New local-only artifacts seen during a commit workflow
- `profiles/` directories can appear under the repo root when profile work is active. These are runtime/env-specific and should not be committed as code changes.
- `ollama_cloud_models_cache.json` can appear as a local cache artifact and should be ignored or cleaned up before committing.
- `kanban.db` may show up as noisy tracked state during agent sessions; verify whether it is meaningful before staging.

## Cleanup pattern
1. `git status --porcelain`
2. Inspect `git diff` for tracked files.
3. Revert true runtime artifacts if they are tracked and not intended for commit.
4. Extend `.gitignore` for untracked runtime/cache artifacts that are clearly local-only.
5. Re-run `git status --porcelain` before staging.

## Verification gotcha
`git diff --cached --check` can be clean even when token-like strings in docs are legitimate examples. Treat the grep-based secret scan as advisory and verify context before stripping or reverting docs.