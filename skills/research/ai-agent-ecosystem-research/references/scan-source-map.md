# Initial AI-Agent Ecosystem Scan: Source Map

This reference records durable source-selection lessons from the first scan. It is intentionally a compact knowledge bank, not a transcript.

## Primary source classes

| Area | Preferred source | What it is good for | Caveat |
|---|---|---|---|
| Agent skills | [Agent Skills](https://github.com/anthropics/skills), [Agent Skills directory](https://skills.sh/) | Portable `SKILL.md` packaging, metadata, examples, cross-agent compatibility, install/activity signals | Directory popularity is an adoption signal, not a quality or safety guarantee |
| MCP tooling | [Official MCP Registry](https://registry.modelcontextprotocol.io/), [MCP servers repository](https://github.com/modelcontextprotocol/servers) | Current server discovery, versions, descriptions, reference implementations, SDK coverage | The reference-server repository explicitly distinguishes educational/reference code from production-ready solutions |
| Agent interoperability | [A2A project](https://github.com/a2aproject/A2A) | Agent capability discovery, modality negotiation, long-running collaboration, and the boundary between agents and tools | Protocol adoption and implementation maturity require separate verification |

## Observed durable signals

- Skills are increasingly treated as self-contained packages of instructions, scripts, and resources loaded dynamically for specialized work; a rich skill should therefore include operational guidance and validation, not only prose.
- Tool discovery is moving toward registries rather than static repository lists; a recurring scan should inspect registry freshness, versioning, descriptions, and provenance.
- MCP and A2A solve different layers: MCP exposes tools/data to an agent, while A2A enables opaque agents to discover and collaborate with other agents. Avoid collapsing them into one interoperability category.
- Cross-agent compatibility is now a useful discovery dimension: directories may show support for Claude Code, Codex, Copilot, Gemini, Nous Research, OpenCode, and others. Treat compatibility claims as a lead to verify, not as certification.

## Retrieval fallback

If web search or extraction backends are not configured, a read-only scan can still proceed by navigating official GitHub pages, registry pages, and documentation pages in a browser. Record the provider limitation only as an operational note; do not turn it into a durable claim that a source or tool is unavailable.
