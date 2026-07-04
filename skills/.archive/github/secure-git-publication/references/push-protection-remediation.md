# Push-protection remediation pattern

Use this pattern when a GitHub push is rejected with secret-scanning / repository rule violations.

## Observed pattern
- A direct push can fail for permissions (`403`) before any content check matters.
- A different destination may still reject the branch with `GH013` if the branch history contains a sensitive file or value.
- The fix is to remove the sensitive path from history, not just from the tip commit.

## Safe remediation loop
1. Clone or copy the repository into a disposable location.
2. Rewrite history to remove the sensitive file/path from all commits.
   - Prefer `git filter-repo`.
   - If unavailable, use `git filter-branch` only in the disposable clone.
3. Verify the path no longer appears in history:
   - `git log --all -- <path>` should return nothing.
   - Optionally inspect the resulting branch graph and tip SHA.
4. Push the sanitized branch to a writable fork or branch name.
5. Open a PR from the sanitized branch if the primary remote is protected.

## Reminders
- Redact secret values in any notes or reports.
- Keep the original contaminated repo unchanged unless you intentionally want to rewrite it too.
- Expect rewritten commits to diverge from the original history; this is normal.