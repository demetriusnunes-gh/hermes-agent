# Commit / Push Playbook for a Writable Fork

Use this when working in a live Hermes checkout that may already contain generated files, user changes, or a pre-existing fork remote.

## Checklist

1. Inspect the working tree before staging:
   ```bash
   git status --porcelain --ignore-submodules=none
   ```
2. Verify remotes and pick the writable target explicitly:
   ```bash
   git remote -v
   git ls-remote fork refs/heads/<branch>
   ```
3. Review the exact delta you intend to ship:
   ```bash
   git diff --name-status
   ```
4. Stage, commit, and push to the fork/branch you verified:
   ```bash
   git add -A
   git commit -m "<message>"
   git push fork HEAD:<branch>
   ```

## Push-protection pitfall

If GitHub rejects the push for secret scanning or push protection, treat that as a tree hygiene problem, not a networking problem:

- identify the secret-bearing path in the rejected commit
- remove it from the commit or rewrite the commit
- push again only after the sensitive file is gone

## Notes

- `git ls-remote fork refs/heads/<branch>` is a quick, low-noise way to confirm the writable fork branch exists before pushing.
- In Hermes-home checkouts, the working tree may be very noisy; prefer targeted inspection of the intended commit over assuming a clean repo.
