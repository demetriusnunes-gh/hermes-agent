# Nested repo pitfall inside /root/.hermes

Observed during a commit review on `/root/.hermes`:

- The top-level repo reported `M hermes-agent`.
- `git -C hermes-agent status --porcelain --ignore-submodules=none` showed `?? tinker-atropos/`.
- `tinker-atropos/` itself is a nested git checkout (`.git` file points to `../.git/modules/tinker-atropos`).
- The nested checkout can be on detached HEAD and still be the real source of dirt.
- A dirty or merely untracked nested checkout can make the outer `hermes-agent` entry look modified even when there is no intended source change to commit at `/root/.hermes`.

Recommended inspection sequence:

```bash
cd /root/.hermes

git status --porcelain --untracked-files=all --ignore-submodules=none
git -C hermes-agent status --porcelain --ignore-submodules=none
find hermes-agent -name .git -type f -maxdepth 2 -print -exec cat {} \;
```

If the nested checkout is intentionally present but not versioned by the parent repo, do not force a parent commit just to clear the outer status. Inspect whether the nested tree is itself a separate repo that should be committed on its own branch, ignored locally, or left untouched.