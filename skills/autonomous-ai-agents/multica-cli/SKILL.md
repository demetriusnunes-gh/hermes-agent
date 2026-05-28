---
name: multica-cli
description: Live-reference skill for using the Multica CLI to authenticate, inspect workspaces/projects/issues, create issues, manage agents, and understand how "boards" map to projects/issues.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Multica, CLI, Issues, Projects, Agents, Workspace, Boards]
    related_skills: [multica-vps-oauth-localhost-tunnel]
---

# Multica CLI

Use this skill whenever the user asks about Multica CLI commands, creating/updating issues, projects, agents, authentication, or anything like "add this to the Multica board".

This skill is based on live `multica --help` output from this VPS, not memory.

## Important mental model

There is **no `multica board` command** in the installed CLI.

If the user says "board", the practical CLI mapping is usually:
- workspace -> container for everything
- project -> likely the closest CLI concept to a board/grouping
- issue -> item/task/card on that board/project
- issue status -> column/state movement

So the default interpretation of "add to board" is:
1. identify the target project
2. create the issue with `--project <project-id>`
3. optionally set `--status`, `--priority`, `--assignee`

## Core command groups

```bash
multica --help
```

Top-level command groups observed:
- `agent`
- `autopilot`
- `issue`
- `project`
- `repo`
- `skill`
- `workspace`
- `daemon`
- `runtime`
- `attachment`
- `auth`
- `config`
- `login`
- `setup`
- `update`
- `version`

Global flags:
- `--profile`
- `--server-url`
- `--workspace-id`

Environment variables:
- `MULTICA_SERVER_URL`
- `MULTICA_WORKSPACE_ID`

## Authentication and health checks

### Check auth
```bash
multica auth status
```

### Log in
```bash
multica login
multica login --token
```

If `multica login` is run on a VPS and the hosted login callback targets `localhost`, load the related skill:
- `multica-vps-oauth-localhost-tunnel`

### Check and manage daemon
```bash
multica daemon status   # Check if daemon is running
multica daemon start    # Start the daemon
multica daemon stop     # Stop the daemon
multica daemon restart  # Restart the daemon
```

## Workspace commands

### List workspaces
```bash
multica workspace list
```

### Get workspace details
```bash
multica workspace get <workspace-id> --output json
```

### List workspace members
```bash
multica workspace members <workspace-id> --output json
```

## Project commands

### List projects
```bash
multica project list --output json
multica project list --status active --output json
```

### Get project
```bash
multica project get <project-id> --output json
```

### Create project
```bash
multica project create \
  --title "Brazil Launch" \
  --description "Track Brazil localization work" \
  --status active \
  --output json
```

Useful flags from live help:
- `--title` required
- `--description`
- `--icon`
- `--lead`
- `--status`
- `--output`

### Update project
```bash
multica project update <project-id> --title "New title" --output json
```

### Change project status
```bash
multica project status <project-id> <status>
```

## Issue commands

### List issues
```bash
multica issue list --output json
multica issue list --project <project-id> --output json
multica issue list --status todo --output json
multica issue list --assignee <name> --output json
```

Useful filters from live help:
- `--assignee`
- `--limit`
- `--offset`
- `--priority`
- `--project`
- `--status`

### Get issue details
```bash
multica issue get <issue-id> --output json
```

### Create issue
```bash
multica issue create \
  --title "Add Pix-aware billing flow" \
  --description "Support Brazil-first payment flow for the product" \
  --project <project-id> \
  --status todo \
  --priority medium \
  --assignee <member-or-agent-name> \
  --output json
```

Live flags observed:
- `--title` required
- `--description`
- `--assignee`
- `--attachment` (repeatable)
- `--due-date` (RFC3339)
- `--parent`
- `--priority`
- `--project`
- `--status`
- `--output`

### Update issue
```bash
multica issue update <issue-id> \
  --title "Updated title" \
  --description "Updated description" \
  --project <project-id> \
  --status in_progress \
  --priority high \
  --assignee <member-or-agent-name> \
  --output json
```

### Change issue status
```bash
multica issue status <issue-id> done --output json
```

### Assign/unassign issue
```bash
multica issue assign <issue-id> --to <member-or-agent-name> --output json
multica issue assign <issue-id> --unassign --output json
```

### Search issues
```bash
multica issue search "Brazil localization" --output json
```

### Comment on issue
Prefer stdin for long comments to avoid shell escaping problems:

```bash
printf '%s
' "Investigation complete. Recommend shipping MVP with Pix + boleto first." \
  | multica issue comment add <issue-id> --content-stdin --output json
```

Or simple content flag:
```bash
multica issue comment add <issue-id> --content "Done" --output json
```

Comment flags observed:
- `--content`
- `--content-stdin`
- `--attachment` (repeatable)
- `--parent` (reply to comment)
- `--output`

## Agent commands

### List agents
```bash
multica agent list --output json
```

### Get agent
```bash
multica agent get <agent-id> --output json
```

### Create agent
```bash
multica agent create \
  --name "Researcher" \
  --description "Brazil market researcher" \
  --runtime-id <runtime-id> \
  --instructions "Research, synthesize, and report findings clearly." \
  --visibility workspace \
  --max-concurrent-tasks 3 \
  --output json
```

Live flags observed:
- `--name` required
- `--runtime-id` required
- `--description`
- `--instructions`
- `--max-concurrent-tasks`
- `--visibility private|workspace`
- `--custom-args` JSON array string
- `--runtime-config` JSON string
- `--output`

### Update agent
```bash
multica agent update <agent-id> --instructions "New instructions" --output json
```

### Agent skills/tasks
```bash
multica agent skills --help
multica agent tasks <agent-id> --output json
```

## Default workflows

### Workflow: add a new issue to a "board"
When the user says "add an issue to the Multica board":

1. Confirm or discover workspace/project context:
```bash
multica workspace list
multica project list --output json
```

2. If the board corresponds to a project, create the issue there:
```bash
multica issue create \
  --title "<title>" \
  --description "<description>" \
  --project <project-id> \
  --status todo \
  --priority medium \
  --output json
```

3. If needed, move/update later with:
```bash
multica issue update <issue-id> --project <project-id> --status in_progress --output json
```

### Workflow: inspect an assigned issue before doing work
```bash
multica issue get <issue-id> --output json
multica issue comment list <issue-id> --output json
multica issue runs <issue-id> --output json
```

### Workflow: close out work
```bash
multica issue comment add <issue-id> --content "Completed. See summary above." --output json
multica issue status <issue-id> done --output json
```

## Practical tips

- Prefer `--output json` whenever the output will be parsed or reused.
- If the user mentions a board, do not assume there is a `board` command — map it to projects/issues.
- If creating a project/board with `multica project create ...` fails with a server-side 500 like `POST /api/projects returned 500: {"error":"failed to create project"}`, do not block the task. Fall back to creating the requested issues directly in the workspace with no `--project`, then clearly tell Demetrius the project creation failed and the issues were created workspace-level instead.
- For anything on a remote VPS using hosted Multica login, use the SSH localhost-callback tunnel skill.
- For long comments, prefer `--content-stdin`.
- If workspace context is unclear, start with:
  - `multica workspace list`
  - `multica project list --output json`
- Default behavior for Demetrius:
  - assign new Multica issues to `Roger Hermes` unless he explicitly says otherwise
  - do not attach a project unless he explicitly asks for one
- If the user wants a specific issue created, gather at least:
  - title
  - description
  - optional assignee/priority/status
  - only ask for project/board target if the user explicitly wants project placement

## Known-good commands verified live on this VPS

These were checked directly via `--help` or live status commands:
- `multica --help`
- `multica issue --help`
- `multica issue create --help`
- `multica issue update --help`
- `multica issue status --help`
- `multica issue assign --help`
- `multica issue comment --help`
- `multica issue comment add --help`
- `multica project --help`
- `multica project create --help`
- `multica project list --help`
- `multica workspace --help`
- `multica workspace list --help`
- `multica agent --help`
- `multica agent create --help`
- `multica login --help`
- `multica auth --help`
- `multica auth status`
- `multica daemon status`

## What to say when asked "how do I add a new issue to the Multica board?"

Short answer:

```bash
multica project list --output json
multica issue create --title "..." --description "..." --project <project-id> --status todo --priority medium --output json
```

And note explicitly: there is no `multica board` command in this CLI; the board concept appears to be represented through projects + issue status.
