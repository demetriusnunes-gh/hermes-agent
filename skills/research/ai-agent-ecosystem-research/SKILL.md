---
name: ai-agent-ecosystem-research
description: "Research AI-agent ecosystem developments to improve agent skills, tooling awareness, workflows, and source discovery. Use for recurring scans, landscape reviews, and evidence-backed recommendations about agent frameworks, skills, protocols, registries, and orchestration patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ai-agents, agent-skills, agent-tools, workflows, MCP, A2A, research, source-discovery]
    category: research
---

# AI-Agent Ecosystem Research

Use this class-level workflow for recurring, read-only research scans focused on improving an agent framework such as Hermes. The goal is not to collect news; it is to identify durable practices, emerging interfaces, and high-value sources that can improve skills, tooling awareness, workflows, or discovery.

## Scan priorities

Cover these four lenses, weighting the user's stated priority:

1. **Skill quality** — portable skill formats, trigger metadata, examples, executable helpers, verification, safety boundaries, reuse signals, and evaluation practices.
2. **AI tooling awareness** — MCP servers, registries, SDKs, browser/computer-use tools, memory systems, evaluation/observability tools, and provider/platform changes.
3. **Workflows** — delegation, handoffs, long-running tasks, planning/execution loops, agent-to-agent collaboration, structured outputs, and recovery patterns.
4. **Source discovery** — official registries, standards/specifications, release feeds, ecosystem directories, and repositories with live activity.

## Read-only procedure

1. Establish the scan date and the exact improvement lenses; do not modify files, skills, code, configuration, or cron jobs.
2. Start with primary sources: official specifications, registries, maintained repositories, release notes, and authoritative project documentation.
3. Prefer live directories and registries over static lists. For skills, inspect standards and multi-agent directories; for tools, inspect official registries and maintained reference repositories; for protocols, inspect the protocol project and specification.
4. Cross-check important claims across at least two independent primary or near-primary sources. Treat install counts, stars, and activity as adoption signals—not proof of quality.
5. Separate observations from recommendations. Record the source, date, signal, likely Hermes relevance, confidence, and any security or compatibility caveat.
6. Rank findings by likely leverage and durability. Ignore one-off announcements unless they reveal a reusable workflow or interface.
7. Deliver a compact report: at most three top findings and at most two follow-ups, with one line per bullet when the caller requests a short summary.

## Source strategy and fallback

- **Skills:** use the Agent Skills specification and maintained skill directories such as `skills.sh`; inspect representative skills for structure, portability, and verification patterns.
- **Tooling:** use the official MCP Registry for discoverable servers and the MCP project repository/docs for protocol and reference-server status; distinguish reference implementations from production-ready offerings.
- **Agent interoperability:** use the A2A specification/project for capability discovery, modality negotiation, task collaboration, and agent-vs-tool boundaries.
- **Current project state:** use repository pages, commit history, releases, and official changelogs rather than relying on model memory.
- If a configured web search/extraction backend is unavailable, diagnose once and switch to browser navigation or direct official pages. Do not infer that the ecosystem is unavailable from a provider setup failure.

## Evidence discipline

Apply the `grounded-citations` skill when available: register retrieved URLs at retrieval time, cite claims close to the relevant bullet, and avoid presenting search snippets as if they were full-page evidence. For a very short scheduled report, compact source URLs may be attached inline rather than expanding the prose.

## Quality and security checks

For every proposed follow-up, ask:

- Does it improve capability discovery, skill reuse, workflow reliability, or source coverage?
- Is it compatible with Hermes' provider-agnostic, profile-aware, read-only/approval-aware design?
- Does it introduce untrusted code, prompt injection, credential exposure, or supply-chain risk?
- Can it be evaluated with a small repeatable test or quality scorecard?

Do not recommend installing or executing a newly discovered skill/server solely because it is popular. Recommend inspection, sandboxing, provenance checks, permissions review, and evaluation first.

## Related reference

See `references/scan-source-map.md` for the source classes and evidence notes from the initial ecosystem scan.
