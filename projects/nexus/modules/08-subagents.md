# Module 8 -- Subagents

**CC features:** .claude/agents/, subagent frontmatter, chaining, parallel, background (Ctrl+B), resuming, `claude agents` CLI

> **Persona — Peer:** Terse guidance, point to docs, let them debug first. "Your call", "What would you do here?"

### Step 1: What Are Subagents

Subagents are specialized AI assistants running in their own context window with custom system prompts, specific tool access, and independent permissions. Benefits: preserve main conversation context, enforce tool constraints, specialize behavior, control costs by routing to faster models.

> **Why this step:** Your main Claude session handles everything -- routing, caching, security, testing. Subagents let you split that into specialists. A routing expert agent does not need write access or knowledge of caching. A security agent does not need to edit files. By restricting each agent's tools and focus, you get better results and preserve your main conversation's context window.

### Step 2: Create the "router-agent"

Ask Claude to create a subagent that specializes in route analysis. Describe its focus area and what tools it should have access to.

> "Create a router-agent subagent that specializes in route matching, conflict detection, and optimization. It should be able to read files and search the codebase but use the Sonnet model to save costs. When invoked, it should analyze the route config for conflicts, unreachable routes, and ordering issues, and present findings as a table."

Claude will create `.claude/agents/router-agent.md` with the appropriate frontmatter, including `tools:` to restrict what the agent can do and `model: sonnet` for cost efficiency.

### Step 3: Create the "cache-agent"

Now create a caching specialist. Describe what it should analyze and what tools it needs.

> "Create a cache-agent subagent that manages the SQLite cache layer. It should be able to query cache.db, analyze hit/miss rates and entry ages, suggest TTL adjustments and eviction strategies, and debug stale or oversized entries. Sonnet model, with Read, Bash, Grep, and Glob tools."

> **STOP -- What you just did:** You created two specialist agents with different tool sets. The router-agent has `Read, Grep, Glob, Bash` because it needs to analyze code and configs. The cache-agent also has `Bash` so it can query the database. Notice the `model: sonnet` field -- this routes these agents to a faster, cheaper model since they are doing analysis, not complex reasoning. You will use Opus for design decisions and Sonnet for routine analysis.

Ready to create a read-only security auditor agent?

### Step 4: Create the "security-agent"

Create a security auditor agent. This one should have read-only access -- no Bash, no Write -- because a security auditor should not be able to modify code.

> "Create a security-agent subagent that audits the gateway for security issues. It should check route configs for exposed admin endpoints and missing rate limits, review code for missing input validation and header injection risks, and check for missing auth and security headers. Give it only Read, Grep, and Glob tools -- no Bash or Write. Sonnet model. Output should be an audit report with severity levels."

Notice that the security-agent only has `Read, Grep, Glob` -- no `Bash`, no `Write`. This is intentional: a security auditor should analyze, not modify.

> **Quick check before continuing:**
> - [ ] `.claude/agents/` has three agent files: router-agent, cache-agent, security-agent
> - [ ] Each agent has a `tools:` field limiting what it can do
> - [ ] Each agent has `model: sonnet` (or another appropriate model)
> - [ ] You can explain why the security-agent only has `Read, Grep, Glob` (no Bash, no Write)

### Step 5: Subagent Frontmatter Details

Review the key frontmatter fields:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase, hyphens) |
| `description` | Yes | When to delegate to this agent |
| `tools` | No | Allowed tools (inherits all if omitted) |
| `disallowedTools` | No | Tools to deny |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | No | `default`, `plan`, `acceptEdits`, `dontAsk`, `bypassPermissions` |
| `skills` | No | Skills to preload into context |
| `hooks` | No | Hooks scoped to this agent's lifecycle |
| `maxTurns` | No | Maximum number of agentic turns before the subagent stops |
| `mcpServers` | No | MCP servers available to this subagent (named reference or inline config) |
| `memory` | No | Persistent memory scope: `user`, `project`, or `local`. Enables cross-session learning |
| `isolation` | No | Set to `worktree` to run the agent in its own git worktree. Changes stay isolated from your working tree |
| `background` | No | Set to `true` to always run the agent in the background. Good for long-running tasks that should not block |

To verify your agents from the command line without starting a session, run `claude agents`. It lists all configured agents and their metadata.

> **What about agents that talk to each other?** Subagents report back to your main conversation only -- they cannot communicate with each other. In Module 10 you will learn about **agent teams**, where multiple Claude instances share a task list and message each other directly. Subagents are for focused delegation; agent teams are for collaborative parallel work.

### Step 6: Invoke, Chain, Parallel, and Background

**Direct invocation:** Ask Claude to delegate to a specific agent.

> "Use the security-agent to audit the current gateway configuration."

**Chaining** (sequential delegation): Ask Claude to run agents in sequence, where each feeds into the next.

> "First use the router-agent to check for route conflicts, then pass any issues to the security-agent for a security audit, then have the cache-agent verify caching is correct for the affected routes."

**Parallel** (simultaneous delegation): Ask for two agents to work at the same time.

> "In parallel, have the router-agent analyze route performance and the cache-agent analyze cache hit rates. Combine the findings into one optimization report."

> **STOP -- What you just did:** You chained subagents -- one agent's output feeds into the next. This is powerful for multi-stage analysis: first check for route conflicts, then audit the conflicts for security issues, then verify caching is correct for the affected routes. Each agent brings its specialized perspective, and the chain builds a complete picture that no single agent would produce alone.

**Background** (non-blocking):

> **Why this step:** Long-running analyses (like a full security audit) can block your workflow. Background execution with `Ctrl+B` lets you keep working while the agent runs. You will use this pattern whenever an agent's work is not blocking your next step.

While Claude is running a subagent, press `Ctrl+B` to send it to the background. You can continue working and Claude will notify you when it finishes. To kill background agents, press `Ctrl+F` (press twice to confirm).

> "Run the security-agent in the background to audit the full codebase. I'll keep working on the rate limiter."

**Resuming:** When the background agent finishes, you can resume and extend its work.

> "Resume the security-agent and have it also check the new middleware code."

### Checkpoint

Three specialized agents for your gateway. Routing, caching, and security -- each one focused on what it does best.

- [ ] `.claude/agents/router-agent.md` exists and responds when invoked
- [ ] `.claude/agents/cache-agent.md` exists and can query the cache database
- [ ] `.claude/agents/security-agent.md` exists and produces an audit report
- [ ] You successfully chained two subagents in sequence
- [ ] You ran a subagent in parallel or in the background
- [ ] You understand the frontmatter fields: name, description, tools, model
- [ ] Subagent files committed to git
