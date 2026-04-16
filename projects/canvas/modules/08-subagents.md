# Module 8 -- Subagents

**CC features:** `.claude/agents/`, subagent frontmatter, chaining, parallel,
background (`Ctrl+B`), resuming, `claude agents` CLI

**Persona -- Peer:** Terse guidance, point to docs, let them debug first. "Your call", "What would you do here?"

> **New term this module uses:**
> - **Subagent** -- a separate, focused instance of Claude with its own context window, spawned to handle a specific task (code review, research, refactoring). Subagents keep heavy work out of your main conversation so your main context stays clean. You define them in `.claude/agents/`.
>
> See the [glossary](../../../GLOSSARY.md) for related terms.

### 8.1 What Are Subagents

**Why this step:** Until now, everything has happened in your main Claude Code conversation. Subagents are separate AI assistants that work in their own context windows. This is important because your main conversation has limited context space -- heavy analysis (like scanning every HTML file for accessibility issues) fills it up fast. Subagents do the heavy lifting in their own space and return just the results.

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

### 8.3 Create: accessibility-agent

Tell Claude to create an accessibility scanning agent. Describe what you want it to check and how you want the output formatted:

```
Create an accessibility-agent in .claude/agents/. It should scan all HTML files for WCAG issues -- missing alt text, missing form labels, skipped heading levels, missing ARIA landmarks, and anything else you think is important. Use haiku model since it only needs to read and report, and limit its tools to Read, Grep, and Glob. Output should be a report grouped by severity.
```

Claude will create the agent file. Notice it only has read-only tools -- this agent cannot modify your files, which is intentional.

**STOP -- What you just did:** You created a subagent with constrained tools (`Read, Grep, Glob` -- no `Write` or `Edit`) and a cheaper model (`haiku`). This is intentional: the accessibility agent only needs to *read and report*, not modify files. Using haiku instead of the default model saves tokens on a task that does not need the most powerful reasoning. Matching the model to the task complexity is a key cost optimization pattern.

**Engineering value:**
- *Entry-level:* Subagents are specialists — instead of one generalist trying to do everything, you have focused experts that each do one thing well.
- *Mid-level:* Model selection matters for cost. A haiku-powered lint agent costs ~10x less than opus. Running 50 accessibility scans a day with haiku vs opus is the difference between $5/month and $50/month.
- *Senior+:* This is the microservices pattern applied to AI: decompose a monolithic conversation into specialized, independently scalable agents with defined interfaces and resource constraints.

**No restart needed.** New agents are available immediately — just invoke them. If Claude doesn't see your agent, mention the file with `@` or run `/compact` to refresh context.

Shall we create the design review agent next?

### 8.4 Create: design-agent

Create a design review agent focused on CSS consistency. Describe the kinds of issues you want it to catch:

```
Create a design-agent that reviews CSS for consistency issues -- hardcoded values that should use custom properties, missing responsive breakpoints, spacing inconsistencies, missing hover/focus states. Use haiku model and read-only tools. It should output specific suggestions with code fixes.
```

### 8.5 Create: content-agent

Create a content quality reviewer that checks for real-world issues like leftover placeholder text and missing SEO basics:

```
Create a content-agent that reviews page content for quality -- leftover lorem ipsum, inconsistent tone, missing calls-to-action, SEO issues like missing meta descriptions, broken links, and placeholder images. Use sonnet model since it needs stronger reasoning for content quality, and set permissionMode to plan so it is read-only.
```

Note `permissionMode: plan` -- this agent is read-only.

**STOP -- What you just did:** You created three agents with different specializations, tool access, and models. Notice the design: accessibility-agent uses haiku (cheap, fast scans), design-agent uses haiku (CSS analysis does not need heavy reasoning), and content-agent uses sonnet with `permissionMode: plan` (it needs stronger reasoning for content quality but should not modify files). Each agent is tuned for its specific job.

**Quick check before continuing:**
- [ ] `.claude/agents/` contains three agent files
- [ ] Each agent has `name`, `description`, `tools`, and `model` in frontmatter
- [ ] content-agent has `permissionMode: plan` (read-only)
- [ ] accessibility-agent and design-agent use `haiku` model

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

Try invoking your subagents. You can be explicit:

```
Use the accessibility-agent to scan all HTML pages for WCAG issues.
```

Or you can just describe what you want and let Claude figure out which agent to use:

```
Check my portfolio for accessibility problems.
```

Claude reads the agent's `description` field and matches it to your request. Try both approaches and notice whether Claude delegates automatically or handles it directly.

**Why this step:** You can invoke subagents explicitly ("Use the accessibility-agent") or let Claude auto-delegate based on the task description. Auto-delegation works because Claude reads the agent's `description` field and matches it to your request. Writing clear, specific descriptions in your agent frontmatter makes auto-delegation more reliable.

### 8.8 Patterns: Chain, Parallel, Resume

**Chaining:** Connect agents in sequence. Ask Claude to run one agent and then feed its results into another:

```
Use the accessibility-agent to find all issues, then use the design-agent to suggest CSS fixes for the visual problems it found.
```

**Parallel (background):** Press `Ctrl+B` to background a running agent,
then start another task. Ask for one scan:

```
Use the accessibility-agent to scan all pages.
```

While it runs, press `Ctrl+B`, then start another:

```
Use the content-agent to review all page content.
```

Both agents work simultaneously. To kill background agents, press `Ctrl+F` (press twice to confirm).

**Resuming:** After an agent completes, continue its work by asking a follow-up:

```
Continue that accessibility review and now also check the contact form for keyboard navigation issues.
```

Claude resumes the previous agent with its full context preserved.

**STOP -- What you just did:** You learned the three core subagent patterns. Chaining connects agents in sequence (accessibility finds issues, then design suggests fixes). Parallel runs agents simultaneously with `Ctrl+B` -- both work at the same time without blocking each other. Resuming continues a completed agent's work without losing its context. In real projects, you will use parallel agents for comprehensive code reviews (run accessibility + design + content checks simultaneously) and chaining for multi-step workflows.

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

Three specialized agents, all yours. You can chain them, run them in parallel, and resume where they left off.

- [ ] `.claude/agents/` contains `accessibility-agent.md`, `design-agent.md`, `content-agent.md`
- [ ] Each agent has correct frontmatter (name, description, tools, model)
- [ ] You invoked each agent manually and it produced results
- [ ] You chained two agents (accessibility then design)
- [ ] You backgrounded an agent with `Ctrl+B` and started another task
- [ ] You resumed a completed agent to continue its work
- [ ] Understand SendMessage replaces Agent resume parameter
- [ ] Tested `initialPrompt` frontmatter on an agent
