# Noisy session-root discovery checklist

Use this when working in a session-root checkout like `/root/.hermes/hermes-agent` where the outer tree may be ambient runtime noise and the real publish target may be a nested repo.

## Discovery sequence

1. Identify the owning repo for the path you plan to publish:
   ```bash
   git rev-parse --show-toplevel
   git status --porcelain --ignore-submodules=none
   ```

2. If the root contains a nested repo, inspect it directly:
   ```bash
   git -C <nested> rev-parse --show-toplevel
   git -C <nested> status --porcelain --ignore-submodules=none
   git -C <nested> branch --show-current
   git -C <nested> remote -v
   ```

3. Compare local HEAD to the intended remote branch before deciding to push:
   ```bash
   git -C <nested> fetch <remote>
   git -C <nested> rev-list --left-right --count <remote>/<branch>...HEAD
   git -C <nested> ls-remote <remote> refs/heads/<branch>
   ```

4. If the local branch is behind or equal to the remote, do not assume a push is needed:
   - `0\t0` means the branch already matches the remote.
   - `N\t0` means local commits exist and can be pushed fast-forward.
   - `0\tN` means the remote has newer work; rebase/merge first.

5. Push the exact repo/branch pair you verified:
   ```bash
   git -C <nested> push <remote> HEAD:<branch>
   ```

## Notes

- This is a discovery checklist, not a replacement for `git-working-tree-safety`.
- Use it when a top-level checkout and a nested repo both exist under the same session root.
- Prefer the nested repo as the publish target unless you explicitly intend to update the parent gitlink pointer.