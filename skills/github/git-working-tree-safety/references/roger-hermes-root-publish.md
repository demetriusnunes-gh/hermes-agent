# `/root/.hermes` publish checklist

Use this checklist for recurring cron jobs that need to publish the outer Hermes home or verify that nothing publishable changed.

## What to inspect

1. Check the outer root first.
   - `git status --porcelain=v2 --ignore-submodules=none`
   - Summarize untracked files by top-level directory when the tree is noisy.
2. Check any nested repos separately.
   - `git -C <nested> rev-parse --show-toplevel`
   - `git -C <nested> status --porcelain --ignore-submodules=none`
3. Verify the intended remote/branch explicitly.
   - `git remote -v`
   - `git ls-remote <remote> refs/heads/<branch>`
   - `git rev-list --left-right --count <remote>/<branch>...HEAD`
4. Stage only the intended durable files.
   - Prefer allowlist staging in noisy roots.
   - Keep runtime caches, auth material, session databases, and lockfiles out unless explicitly requested.
5. Push with an explicit refspec.
   - `git push <remote> HEAD:<branch>`
6. Confirm the remote tip matches the commit you meant to publish.
   - `git rev-parse HEAD`
   - `git ls-remote <remote> refs/heads/<branch>`

## Useful noise triage

If the outer root is full of generated or runtime paths, group the untracked set before deciding whether anything needs publishing:

```bash
git ls-files --others --exclude-standard | cut -d/ -f1 | sort | uniq -c | sort -nr
```

That makes it easier to spot the few durable paths that deserve review.

## Reminder

A clean nested repo does not imply the outer root is clean. Check both layers before returning `[SILENT]`.