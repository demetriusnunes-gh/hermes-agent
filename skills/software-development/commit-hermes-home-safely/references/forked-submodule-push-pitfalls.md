# Forked submodule push pitfalls

Session lesson: when `/root/.hermes` contains a tracked submodule that points at an upstream repo you cannot push to, the parent repo can still be committed cleanly while the submodule itself must be pushed to your fork.

Observed pattern:
- Parent repo: `roger-hermes` on `master`
- Submodule: `hermes-agent`
- Upstream push failed with `Permission denied` on `NousResearch/hermes-agent.git`
- Fork existed at `demetriusnunes-gh/hermes-agent`

Safe sequence:
1. Inspect parent and submodule status with `git status --porcelain --ignore-submodules=none` and `git -C hermes-agent status --porcelain --ignore-submodules=none`.
2. Confirm the submodule commit you want to publish is local-only.
3. Create or verify a writable fork remote for the submodule.
4. If the fork already has newer commits, `git -C hermes-agent fetch fork` and `git -C hermes-agent rebase fork/main` before pushing.
5. Push the submodule to the fork remote.
6. Update the parent `.gitmodules` URL to the fork when the parent should stop tracking the upstream URL.
7. Stage the parent submodule pointer + `.gitmodules`, commit, and push the parent repo.
8. Re-run status checks for both repos to confirm cleanliness.

Pitfalls:
- A clean parent `git status` does not prove the nested submodule is publishable.
- Pushing to the upstream submodule remote may fail even if `gh auth status` is healthy, because repo-level write permissions are separate.
- If the fork already has work, a direct push may be rejected as non-fast-forward; rebase onto the fork remote first.
- Changing `.gitmodules` updates the tracked URL in the parent; it is not enough to push the submodule itself.
