# /root/.hermes commit/push pitfall

Observed during session:

- `cd /root/.hermes && git status --porcelain` can be clean even when the embedded `hermes-agent` checkout has local dirt.
- In this repo layout, `hermes-agent` is a nested git checkout/submodule-like dependency that must be inspected separately.
- The nested checkout can be in detached HEAD while the parent repo stays on `master`; that is not itself a problem, but it means changes may live only inside the nested repo.

Recommended checks before declaring "nothing to commit":

```bash
cd /root/.hermes
git status --porcelain
git submodule status --recursive || true

git -C hermes-agent status --porcelain
git -C hermes-agent branch --show-current
git -C hermes-agent rev-parse --abbrev-ref HEAD
```

If `git -C hermes-agent status` shows untracked or modified files, inspect whether they belong to the nested repo or are runtime artifacts before deciding whether to commit, ignore, or revert them.

If the parent repo is clean but the nested repo is dirty, do not assume the outer repo needs a commit; the actual source of truth may be inside `hermes-agent`.
