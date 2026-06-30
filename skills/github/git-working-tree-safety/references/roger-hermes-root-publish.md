# Roger Hermes /root/.hermes publish note

Session-specific reminder for recurring cron jobs that ask to "commit and push roger hermes code under /root/.hermes".

## What this session showed

- The nested repo at `/root/.hermes/hermes-agent` can be clean while the outer `/root/.hermes` tree still contains durable, publishable changes or root-level noise.
- A publish check should inspect the outer root and nested repos separately before returning `[SILENT]`.
- For the outer root, stage by allowlist rather than `git add -A` so runtime artifacts stay out of the commit.

## Minimal decision sequence

1. Check outer root status, remotes, and branch.
2. Check nested repos like `/root/.hermes/hermes-agent` separately.
3. If the outer root is the actual target, stage only durable files/directories and push with an explicit refspec.
4. Verify remote branch tips after push.
