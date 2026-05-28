# Nested checkout and gitlink notes

Use this when a parent checkout contains another repository, a gitlink, or runtime-generated nested directories that make `git status` noisy.

## Quick checks

```bash
git rev-parse --show-toplevel
git status --porcelain --ignore-submodules=none
git ls-files -s <path>
```

## What to verify

- The current directory is the repository root you intend to modify.
- A reported nested path is actually part of the repo you want to push, not an unrelated checkout living inside it.
- If the parent repo tracks the path as mode `160000`, you are updating a gitlink pointer, not the nested repo's files.
- If the nested directory is itself a repo, run `git status` and `git rev-parse --show-toplevel` inside it before deciding whether to stage anything in the parent.

## Safe interpretation patterns

- `git status` shows `M <path>` where `<path>` is a gitlink: inspect whether the subrepo HEAD moved intentionally.
- `git status` shows `?? <path>/`: that usually means the parent is seeing untracked files in a nested checkout or generated output.
- `git status` in the nested repo is clean but the parent is dirty: the parent probably tracks the nested path as a gitlink and needs a pointer update, not file edits.

## Recommended sequence

1. Confirm the top-level repo.
2. Check whether the path is a gitlink with `git ls-files -s`.
3. Inspect the nested repo separately if it exists.
4. Stage only the level you intend to change.
5. Re-run `git status` in both repos before commit and push.
