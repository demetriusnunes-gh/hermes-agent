# Agent Marketplace Research Signals - 2026-05-27

## Key Learnings from Today's Research Session

### AgentMRR as a Research Source
When researching AI agent business ideas, agent marketplaces and revenue leaderboards (like AgentMRR) are valuable sources for traction validation. Key extraction patterns:

1. **Revenue Figures as Traction Proof**: 
   - MRR (Monthly Recurring Revenue) and all-time revenue figures provide concrete traction evidence
   - Examples observed: ProspectZero ($2,176 MRR, $12,694 all-time), act101 ($57 MRR, $147 all-time)
   - These figures indicate real market validation beyond speculative ideas

2. **Agent Descriptions Reveal Business Models**:
   - Detailed descriptions in marketplace listings expose the actual value proposition
   - Look for specific mechanisms, not just vague claims (e.g., "signal-based LinkedIn outreach" vs "AI for sales")
   - Technical specifics (MCP servers, grammars, AST operations) indicate defensibility

3. **Founder Cross-Referencing**:
   - Founder names allow verification through LinkedIn, Twitter, or other sources
   - Repeat founders in multiple listings may indicate studio models or serial entrepreneurs
   - Enables background checks on execution capability

4. **Tags/Categories for Market Focus**:
   - Platform tags help categorize the agent's target market (dev tools, sales, marketing, etc.)
   - Helps identify patterns in what types of AI agents are gaining traction

### Extraction Technique for Agent Marketplaces
When browser snapshots show agent listings:
- Use browser snapshot to extract structured data from tables/lists
- For paginated results, check multiple pages or adjust filters (e.g., different time windows: ALL TIME vs MONTHLY)
- Focus on extracting: agent name, description, founder, revenue metrics, and tags
- Validate unusual claims by cross-referencing with the agent's own website or documentation

### Brazil-Gap Validation Workflow Refinement
Added explicit step for incumbent checking:
1. After identifying US proof point, search for Brazilian equivalents using:
   - Direct Google/Bing searches in Portuguese
   - Brazilian tech directories (ComoFazer, GuiaDoEmpreendedor, etc.)
   - Product Hunt Brazil, BRStartups, etc.
   - App stores (Apple App Store Brazil, Google Play Brazil) for mobile solutions
2. If strong incumbent exists (>50k users, established pricing, clear value prop):
   - Narrow the idea to a specific sub-workflow or niche
   - Focus on underserved segments (SMB vs enterprise, specific industry verticals)
   - Consider differentiation via localization, pricing, or specific feature gaps
3. Only proceed if clear differentiation path exists

### Source Citation Format
When citing sources in the digest:
- Primary source: Direct link to the product/service
- Secondary source: Link to discovery platform (HN post, Product Hunt, etc.) in parentheses
- Format: `Source: https://product.com (HN: https://news.ycombinator.com/item?id=12345)`
- This provides both the direct proof and the discovery context

## Actionable Takeaways for Future Digests
1. Always check agent marketplaces (AgentMRR, similar platforms) for AI business ideas with traction proof
2. Extract concrete metrics (MRR, user counts) rather than relying on vague claims
3. Validate Brazil gap through direct incumbent research, not assumptions
4. Use consistent source citation format for reproducibility
5. When HN Algolia returns sparse results, broaden to adjacent monetized classes (pricing, workflow automation, etc.)