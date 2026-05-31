# Status vs diff discrepancy triage

Use this when `git status` shows tracked modifications but `git diff` is unexpectedly empty or unclear.

## Quick checks

1. Confirm the repo root you are actually operating in.
   ```bash
   git rev-parse --show-toplevel
   pwd
   ```

2. Inspect the precise state shape.
   ```bash
   git status --porcelain=v2 --ignore-submodules=none
   ```
   This separates index state from worktree state.

3. Compare the tracked object, index entry, and current worktree hash for the file.
   ```bash
   git rev-parse HEAD:<path>
   git ls-files -s <path>
   git hash-object <path>
   ```

4. If HEAD and index match but the worktree hash differs, the change is only in the working tree.

5. If the path is inside a nested repo or gitlink-style checkout, inspect that path directly with `git -C <path> status --porcelain=v2` before staging the parent.

## Why this helps

In noisy workspaces, `git status` can show the right file while a quick diff check is still misleading to the eye. Hash comparison makes the actual content delta unambiguous before you stage or commit.