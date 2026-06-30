---
name: deployed-webapp-recovery
description: Recover, relocate, and safely redeploy a live VPS webapp whose source tree is missing, damaged, or partially deleted, using runtime inspection and Hermes session history before touching traffic.
tags:
  - deployment
  - recovery
  - systemd
  - caddy
  - vite
  - node
  - session-history
---

# Deployed Webapp Recovery

Use this when a deployed webapp is still live but its source tree, package metadata, server entrypoint, or local changes appear missing, deleted, or damaged. The goal is to recover source safely, validate it, and only then repoint service traffic.

## Core workflow

1. **Preserve the live process first**
   - Do not restart the app service until the source entrypoint and build/runtime path are confirmed recoverable.
   - Treat a live process as fragile: it may still be running from files that have since been deleted.

2. **Capture runtime facts without disrupting traffic**
   - Inspect systemd unit fields: `WorkingDirectory`, `ExecStart`, `MainPID`, `ActiveState`.
   - Inspect the process cwd/cmdline when available.
   - Confirm the local port and health endpoint.
   - Check reverse proxy configuration and public URL, but keep these as read-only checks until source is validated.

3. **Restore into a clean canonical path**
   - Prefer `/root/.www/<app>` for VPS webapp source trees.
   - Back up any existing target directory before replacing it.
   - Copy live `dist/` artifacts as a fallback/reference, but rebuild from source whenever possible.

4. **Recover local changes from durable traces**
   - If GitHub/source archive access is unavailable or incomplete, search Hermes session JSON for prior tool calls and file contents.
   - Reconstruct files from saved `read_file` outputs, then replay saved `write_file`, `patch`, and deterministic code transformations with old paths replaced by the new target path.
   - See `references/source-recovery-from-session-history.md` for the detailed reconstruction pattern.

5. **Validate before switching service paths**
   - Install dependencies from the restored path.
   - Run project tests, app-specific scoring/check scripts, and production build.
   - Fix syntax/duplication issues caused by replayed patches before touching systemd.

6. **Switch traffic only after validation**
   - Back up the current systemd unit.
   - Update `WorkingDirectory` or path references to the restored source path.
   - Run `systemctl daemon-reload`, restart the service, and verify local health.
   - Verify public HTTPS root, health endpoint, frontend assets, and representative API calls last.

## Pitfalls

- **Do not restart too early.** A deleted entrypoint can leave the current app live but unrestartable.
- **GitHub access may not be enough.** Private repos, missing auth, or local hackathon changes may require session-history reconstruction.
- **Patch replay can duplicate code.** If build errors point to repeated components or malformed JSX, inspect around the line and remove duplicated replay fragments.
- **Avoid credential persistence.** Redact tokens, `.env` values, connection strings, and API keys from recovered notes and summaries.

## Verification checklist

- Restored source exists in the target path.
- Dependency install succeeds.
- Tests/scorers pass.
- Production build succeeds.
- Service runs from the restored path.
- Local health endpoint succeeds.
- Public HTTPS root and API endpoints succeed.
