# Nested repo without `.gitmodules`

Observed pattern from `/root/.hermes`:

- The parent checkout can track a child path as a gitlink (`mode 160000`) even when `.gitmodules` is absent.
- In that case, `git submodule status` may fail with: `fatal: no submodule mapping found in .gitmodules for path '<path>'`.
- Treat the child path as a real nested repository and inspect it directly.

## Verification sequence

1. Inspect the parent tree:
   ```bash
   git status --porcelain --ignore-submodules=none
   git ls-files -s <path>
   ```
2. Inspect the nested repo itself:
   ```bash
   git -C <path> rev-parse --show-toplevel
   git -C <path> status --porcelain --ignore-submodules=none
   git -C <path> branch --show-current
   ```
3. Verify the publish target explicitly:
   ```bash
   git -C <path> remote -v
   git -C <path> ls-remote <remote> refs/heads/<branch>
   ```
4. Push the intended branch/ref pair directly if needed:
   ```bash
   git -C <path> push <remote> HEAD:<branch>
   ```

## Pitfalls

- Do not assume the nested repo's current local branch is the branch that should be published.
- Do not use `git submodule status` as the sole probe when `.gitmodules` is absent.
- If the parent repo only tracks the gitlink pointer, a parent push and a nested repo push are separate operations and may target different branches.
