# Module 8 -- Subagents

**CC features:** `.claude/agents/`, subagent frontmatter, chaining, parallel,
background (`Ctrl+B`), resuming, `claude agents` CLI

**Persona -- Peer:** Terse guidance, point to docs, let them debug first. "Your call", "What would you do here?"

> **New term this module uses:**
> - **Subagent** -- a separate, focused instance of Claude with its own context window, spawned to handle a specific task (code review, research, refactoring). Subagents keep heavy work out of your main conversation so your main context stays clean. You define them in `.claude/agents/`.
>
> See the [glossary](../../../GLOSSARY.md) for related terms.

### 8.1 What Are Subagents

**Why this step:** Up to now, your main Claude session does everything -- planning, coding, testing, searching. Subagents let you delegate specialized tasks to focused assistants that have their own context windows and tool restrictions. This keeps your main conversation clean and lets you route tasks to cheaper, faster models (like Haiku for search) while reserving the more capable model for complex work.

Subagents are specialized AI assistants with their own context windows, system
prompts, tool access, and permissions. When Claude encounters a task matching
a subagent's description, it delegates to that subagent. The subagent works
independently and returns results.

Benefits:
- **Preserve context:** heavy work stays out of your main conversation
- **Enforce constraints:** limit which tools a subagent can use
- **Specialize behavior:** focused system prompts for specific domains
- **Control costs:** route tasks to faster, cheaper models

### 8.2 Create the Agents Directory

```
! mkdir -p .claude/agents
```

### 8.3 Create: search-agent

Describe your search agent to Claude. It should be a specialist that parses queries, searches across all data types, ranks results by relevance, and suggests alternatives when nothing matches. Since search is a focused task, use a fast, cheap model.

"Create a search-agent in .claude/agents/search-agent.md. It should be a search specialist that parses queries, searches all data types, ranks results by relevance (exact title matches first, then tags, then body text), and suggests related searches if no results. Use model: haiku and restrict tools to Read, Grep, Glob, and Bash."

### 8.4 Create: format-agent

Create a format conversion agent. Describe the formats you want it to handle and what "good output" looks like for each one.

"Create a format-agent in .claude/agents/format-agent.md. It should convert forge items to Markdown, JSON, HTML, or CSV with proper formatting for each output type. It should handle edge cases like special characters and report a summary of what it exported. Use model: haiku and restrict tools to Read, Write, and Bash."

**STOP -- What you just did:** You created two subagents with different models and tool sets. The search-agent uses Haiku (fast, cheap) because search is a focused task that does not require complex reasoning. The format-agent also uses Haiku because format conversion is mechanical. By choosing the right model for each agent, you control both cost and speed. You will use this pattern whenever a task is well-defined enough that a smaller model can handle it.

**Engineering value:**
- *Entry-level:* Subagents are specialists — instead of one generalist trying to do everything, you have focused experts that each do one thing well.
- *Mid-level:* Model selection matters for cost. A haiku-powered lint agent costs ~10x less than opus. Running 50 accessibility scans a day with haiku vs opus is the difference between $5/month and $50/month.
- *Senior+:* This is the microservices pattern applied to AI: decompose a monolithic conversation into specialized, independently scalable agents with defined interfaces and resource constraints.

**No restart needed.** New agents are available immediately — just invoke them. If Claude doesn't see your agent, mention the file with `@` or run `/compact` to refresh context.

Shall we create a review agent with read-only permissions?

### 8.5 Create: review-agent

Create a review agent for quality-checking your knowledge base. This one needs better reasoning than search or format conversion, so use a more capable model. And since a reviewer should never modify anything, make it read-only.

"Create a review-agent in .claude/agents/review-agent.md. It should check items for completeness, clarity, tag consistency, and duplicates, then score them (Good/Needs Improvement/Poor) with specific suggestions. Use model: sonnet, permissionMode: plan (read-only), and restrict tools to Read, Grep, and Glob."

Note `permissionMode: plan` -- this agent can only read and analyze, never modify files.

**STOP -- What you just did:** You created a review agent with `permissionMode: plan`, which means it can only *read* and *analyze* -- it cannot write files or run commands that modify anything. This is the principle of least privilege applied to AI agents: give each agent only the permissions it needs. A reviewer should never accidentally edit the code it is reviewing.

**Quick check before continuing:**
- [ ] Three agent files exist in `.claude/agents/`
- [ ] search-agent and format-agent use `model: haiku`
- [ ] review-agent uses `model: sonnet` and `permissionMode: plan`
- [ ] Each agent has a focused description and restricted tool list

### 8.6 Subagent Frontmatter Reference

| Field | Required | Description |
|-------|---------|-------------|
| `name` | Yes | Unique identifier (lowercase, hyphens) |
| `description` | Yes | When Claude should use this agent |
| `tools` | No | Tools the agent can use (inherits all if omitted) |
| `disallowedTools` | No | Tools to explicitly deny |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` (default: `inherit`) |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `skills` | No | Skills to preload into the agent's context |
| `hooks` | No | Lifecycle hooks scoped to this agent |
| `maxTurns` | No | Maximum number of agentic turns before the subagent stops |
| `mcpServers` | No | MCP servers available to this subagent (named reference or inline config) |
| `memory` | No | Persistent memory scope: `user`, `project`, or `local`. Enables cross-session learning |
| `isolation` | No | Set to `worktree` to run the agent in its own git worktree. Changes stay isolated from your working tree |
| `background` | No | Set to `true` to always run the agent in the background. Good for long-running tasks that should not block |

To verify your agents from the command line without starting a session, run `claude agents`. It lists all configured agents and their metadata.

**What about agents that talk to each other?** Subagents report back to your main conversation only -- they cannot communicate with each other. In Module 10 you will learn about **agent teams**, where multiple Claude instances share a task list and message each other directly. Subagents are for focused delegation; agent teams are for collaborative parallel work.

### 8.7 Invoke Subagents

Try invoking your subagents. You can be explicit about which agent to use, or just describe a task and let Claude decide whether to delegate.

Explicit invocation:

"Use the search-agent to find all items tagged with 'reference'"

"Use the format-agent to export all notes as Markdown to exports/notes.md"

Automatic delegation -- just describe what you want and see if Claude routes it:

"Find items related to API design in my knowledge base"

Claude may route this to the search-agent on its own, based on the agent's description.

**Why this step:** Subagents can be invoked explicitly ("Use the search-agent to...") or automatically by Claude when the task matches the agent's description. Automatic delegation is powerful but requires good descriptions in your agent frontmatter -- Claude uses the description to decide when to delegate.

Want to learn how to chain and parallelize agents?

### 8.8 Patterns: Chain, Parallel, Resume

**Chaining:** Connect agents in sequence -- the output of one feeds into the next:

"Use the search-agent to find all poorly-tagged items, then use the review-agent to suggest better tags for each one."

**Parallel (background):** Press `Ctrl+B` to background a running agent, then start another task:

"Use the review-agent to review all my notes"

While it runs, press `Ctrl+B`, then:

"Use the format-agent to export all bookmarks as HTML"

Both agents work simultaneously. To kill background agents, press `Ctrl+F` (press twice to confirm).

**Resuming:** After an agent completes, continue its work:

"Continue that review and now also check snippets for quality"

Claude resumes the previous agent with its full context preserved.

**STOP -- What you just did:** You practiced three subagent patterns: chaining (output of one feeds into the next), parallel (multiple agents working simultaneously via `Ctrl+B`), and resuming (continuing a completed agent's work). These patterns compose -- you can chain two agents, background both, and resume whichever finishes first. In real projects, you will use chaining for pipelines (search then format), parallel for independent tasks (review notes while exporting bookmarks), and resuming for iterative refinement.

**Engineering value:**
- *Entry-level:* Running agents in parallel means a full code review (accessibility + design + content) takes the same time as one scan, not three.
- *Mid-level:* Chaining agents creates automated review pipelines: find issues → suggest fixes → verify fixes. This is the same find-fix-verify pattern used in CI/CD.

### 8.9 SendMessage & Agent Frontmatter

Breaking change and new capabilities for subagents:

**`resume` parameter removed** (v2.1.77) — the Agent tool no longer accepts `resume`. Use `SendMessage({to: agentId})` to continue a previously spawned agent. `SendMessage` auto-resumes stopped agents in the background.

**`model` parameter restored** (v2.1.72) — per-invocation model overrides on the Agent tool work again. Full model IDs (e.g., `claude-opus-4-5`) are now accepted in agent frontmatter `model:` field (v2.1.74).

**New agent frontmatter fields** (v2.1.78) — plugin-shipped agents support `effort`, `maxTurns`, and `disallowedTools` in frontmatter.

**Partial results preserved** (v2.1.76) — killing a background agent now preserves its partial results in the conversation context instead of losing them.

Update any agents that use `resume` to use `SendMessage` instead.

### 8.10 Agent Auto-Start with `initialPrompt`

Agents can now declare `initialPrompt` in their frontmatter to auto-submit a first turn when spawned. Instead of the agent waiting for instructions, it starts working immediately.

Try adding `initialPrompt` to one of your existing agents. For example, add `initialPrompt: "Scan all HTML files for accessibility issues and report findings"` to your accessibility agent's frontmatter. Then invoke the agent and compare: with `initialPrompt`, it starts scanning immediately without you having to type anything. Without it, it waits.

When would you want this? Think about agents that always do the same thing -- linters, scanners, formatters. They do not need a prompt; they need a trigger.

### Checkpoint

Three agents that know your toolkit inside and out. Chain them, parallel them, resume them -- they are yours to orchestrate.

- [ ] `.claude/agents/` contains `search-agent.md`, `format-agent.md`, `review-agent.md`
- [ ] Each agent has correct frontmatter (name, description, tools, model)
- [ ] You invoked each agent manually and it produced results
- [ ] You chained two agents (search then format, or search then review)
- [ ] You backgrounded an agent with `Ctrl+B` and started another task
- [ ] You resumed a completed agent to continue its work
- [ ] Understand SendMessage replaces Agent resume parameter
- [ ] Tested `initialPrompt` frontmatter on an agent
