# Fork Remote Verification and Push Recovery

Use this when creating a fork for a repo you do not own and you need a reliable remote for pushing branches.

## Checklist

1. Confirm the fork exists on GitHub.
   ```bash
   gh repo view <your-user>/<repo>
   ```
   If it returns the fork URL/metadata, the fork exists.

2. Do not assume `gh repo fork --remote` updated the local checkout.
   Always inspect local remotes immediately after the command:
   ```bash
   git remote -v
   ```

3. If the expected fork remote is missing, add it explicitly.
   ```bash
   git remote add fork git@github.com:<your-user>/<repo>.git
   # or HTTPS
   git remote add fork https://github.com/<your-user>/<repo>.git
   ```

4. Push to the verified fork remote explicitly.
   ```bash
   git push -u fork <branch>
   ```

5. Verify the remote ref after push.
   ```bash
   git ls-remote fork refs/heads/<branch>
   ```

## Common failure modes

- `Permission denied` or `403` while pushing to `origin` usually means `origin` still points at the upstream repo, not your fork.
- `gh repo fork` can create the fork on GitHub without leaving a usable local remote behind in the current checkout; treat the local remote as untrusted until `git remote -v` confirms it.
- A detached HEAD is not a blocker for pushing, but you should create or switch to a branch before pushing if you want a stable branch name.
