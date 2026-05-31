---
name: secure-git-publication
description: Safely publish Git history when direct pushes are blocked by permissions or secret-scanning rules.
---

# Secure Git Publication

Use this skill when a repository is ready to publish, but a push fails because of one of these classes of problems:
- insufficient remote permissions
- GitHub push protection / secret scanning
- contamination in commit history from a sensitive file or value
- confusion between sibling repositories that share a parent directory

## Goals
- Publish only clean history.
- Preserve the working repository unless an explicit rewrite is required there.
- Prefer a fork or disposable clone for history surgery.
- Verify the sanitized branch before attempting another push.

## Workflow
1. **Identify the exact repo and remote.**
   - Confirm `git rev-parse --show-toplevel`, current branch, and `git remote -v`.
   - If there are sibling repositories under the same parent path, treat them as distinct repos.

2. **Classify the push failure.**
   - `403` / permission denied: the destination remote is not writable by the current account.
   - `GH013` / push protection: GitHub detected a secret somewhere in the branch history.

3. **If history is contaminated, rewrite it in a disposable clone.**
   - Prefer `git filter-repo` when available.
   - If not available, use `git filter-branch` only in a temporary clone/worktree, never in the only clean working copy.
   - Remove the sensitive path or value from *all* commits, not just the tip.

4. **Verify the sanitized history before pushing.**
   - Confirm the sensitive path is absent from history (`git log --all -- <path>` should be empty).
   - Confirm the new branch tip is the expected sanitized commit.
   - Re-check the remote URL you intend to push to.

5. **Publish the sanitized branch.**
   - Push the cleaned branch to a writable remote or fork.
   - Use a fresh branch name if the original ref is blocked.
   - If the main remote is protected or unwritable, stop at the fork/PR stage.

## Pitfalls
- Do not force-push contaminated history to a protected remote.
- Do not assume two directories with similar names are the same repository.
- Do not leave secret values in logs, notes, or commit messages; redact them.
- Do not rewrite the only working copy unless that is explicitly intended.
- Expect rewritten SHAs; any downstream branches or PRs need to be rebased onto the sanitized branch.

## Verification checklist
- `git status` is clean in the repo you intend to publish.
- The target remote is correct and writable.
- The sensitive file/value is absent from all reachable commits on the branch to be pushed.
- The pushed remote branch tip matches the sanitized local tip.

## Related notes
- See `references/push-protection-remediation.md` for a compact remediation pattern and verification notes.