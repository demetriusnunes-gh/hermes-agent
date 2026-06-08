# Legacy skill name mismatch in cron jobs

## Symptom

A cron job prints a warning like:

- `Skill(s) not found and skipped: <name> (OR the name equivalent)`

but the underlying scheduled prompt still executes.

## What it means

The cron scheduler resolves the job's `skills` list by exact active skill name. If a listed skill cannot be loaded, the scheduler skips that skill layer and continues with the rest of the job.

This is usually a *name drift* problem, not a total job failure:

- the skill was renamed or archived
- the job still references the old skill name
- the prompt body remains valid enough to run without the skill layer

## How to confirm

1. Inspect the job definition in `cron/jobs.json`.
2. Compare the listed skill names with the current active skills.
3. Check whether the needed behavior now lives in a broader umbrella skill instead of the old narrow skill.

## Fix options

- Update the cron job to reference the current skill name.
- Add a compatibility alias/wrapper skill if the old name must keep working.
- If the prompt already contains the full behavior, remove the stale `skills` entry and let the job run prompt-only.

## Practical guidance for monitoring jobs

For email/calendar monitoring, prefer one class-level umbrella skill plus a small set of references for state, deduplication, and legacy-name notes. Do not keep one-off skill names alive in cron metadata unless they are intentionally maintained as aliases.

## Related files

- `references/monitoring-workflow.md`
- `references/email-calendar-state-hygiene.md`
