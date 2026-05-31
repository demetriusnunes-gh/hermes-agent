# Push protection remediation

Use this when GitHub rejects a push because a secret is present in reachable history.

## Decision rule

- Do **not** keep retrying the same ref.
- Rewrite a sanitized branch that removes the secret-bearing path/blob from history.
- Verify the rewritten branch no longer contains the sensitive path before pushing.

## Minimal recipe

```bash
# Start from the branch you want to publish
BRANCH=master-sanitized

# Option 1: remove a whole path from the branch history
GIT_SEQUENCE_EDITOR=: git filter-branch --force \
  --index-filter 'git rm --cached --ignore-unmatch .env.backup' \
  --prune-empty "$BRANCH"

# Verify the secret path is gone from reachable history
git rev-list "$BRANCH" -- .env.backup

# Push the sanitized ref explicitly
git push fork "$BRANCH:master"
```

## Notes

- Prefer a clean sanitized branch over force-pushing the original ref.
- If the secret lives in a different path or blob, adjust the `git rm --cached --ignore-unmatch <path>` filter accordingly.
- After push, confirm the remote ref points at the rewritten commit with `git ls-remote <remote> refs/heads/<branch>`.
