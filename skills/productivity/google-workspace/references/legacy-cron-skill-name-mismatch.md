# Legacy cron skill-name mismatch

## Symptom

Cron output includes a warning such as:

- `Skill(s) not found and skipped: <name> (OR the name equivalent)`

while the scheduled prompt still appears to run.

## Meaning

The scheduler resolves the job's `skills` field by active skill name. If the listed name is missing, the skill layer is skipped and the remaining job still runs.

This usually means the job metadata is stale, not that Gmail/Calendar access is broken.

## Common causes

- the skill was renamed, archived, or split into a broader umbrella skill
- cron metadata still references the old narrow skill name
- the prompt body contains enough logic to run even without the skill layer

## Fix options

- update the job to the current umbrella skill name
- add a compatibility alias/wrapper skill if backward compatibility matters
- remove the stale `skills` entry when the prompt already carries the full workflow

## Verification

- inspect `cron/jobs.json`
- compare the listed skill names to the current active skill library
- confirm that any warning is coming from skill resolution, not from the underlying Gmail/Calendar backend
