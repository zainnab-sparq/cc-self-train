# Module 8 -- Subagents

<!-- progress:start -->
**Progress:** Module 8 of 10 `[████████░░]` 80%

**Estimated time:** ~60-90 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** .claude/agents/, subagent frontmatter, chaining, parallel, background (Ctrl+B), resuming, `claude agents` CLI

**Persona -- Peer:** Terse guidance, point to docs, let them debug first. "Your call", "What would you do here?"

</details>

In this module you create specialized AI agents that handle specific tasks within Sentinel.

> **New term this module uses:**
> - **Subagent** -- a separate, focused instance of Claude with its own context window, spawned to handle a specific task (code review, research, refactoring). Subagents keep heavy work out of your main conversation so your main context stays clean. You define them in `.claude/agents/`.
>
> See the [glossary](../../../GLOSSARY.md) for related terms.

**Module pacing override:** Subagents are structurally novel — the mental model (subagents report to a main conversation vs. agent teams that peer-communicate) is non-obvious even for experienced engineers. If your persona for this module would normally be Peer ("terse guidance, point to docs"), prefer Collaborator-style explanations here anyway: define each concept before using it, give one worked example per feature, and pause to verify the mental model is landing. Terseness in Module 8 is premature. Module 10 goes back to Peer/Launcher.

### 8.1 What Are Subagents

**Why this step:** Up to now, everything has happened in a single Claude conversation. Subagents let you spin up specialized Claude instances -- each with their own system prompt, tool access, and context window. Think of it as delegation: instead of doing everything yourself, you assign specific jobs to specialists. This keeps your main conversation clean and lets you parallelize work.

Ask Claude what subagents are and when you should use them instead of the main conversation.

Try something like:

```
What are Claude Code subagents? How are they different from this main conversation, and when should I use one?
```

Key points: subagents run in their own context window with a custom system prompt and specific tool access. They keep verbose output out of your main conversation. They cannot spawn other subagents.

### 8.2 Create the Analyzer Agent

Ask Claude to create a specialized analyzer agent. Describe its role -- deep code analysis, running the scanner, evaluating whether issues are true or false positives, and suggesting fixes. Tell Claude to give it read-only tools (no Write or Edit) since it should find issues, not fix them. Suggest using the `sonnet` model to save tokens.

Try something like:

```
Create an analyzer agent at .claude/agents/analyzer-agent.md. It should be a deep analysis specialist -- runs the scanner, evaluates each issue for true/false positive, assesses severity, and suggests fixes. Give it only Read, Grep, Glob, and Bash tools (no Write). Use model: sonnet.
```

**STOP -- What you just did:** You created a specialized analyzer agent with limited tool access (Read, Grep, Glob, Bash -- no Write or Edit). This is intentional: the analyzer agent should *find* issues, not *fix* them. Restricting tools prevents subagents from doing things outside their role. The `model: sonnet` setting means this agent uses a cheaper model -- since analysis does not require the most powerful model, this saves tokens.

**Engineering value:**
- *Entry-level:* Subagents are specialists — instead of one generalist trying to do everything, you have focused experts that each do one thing well.
- *Mid-level:* Model selection matters for cost. A haiku-powered lint agent costs ~10x less than opus. Running 50 accessibility scans a day with haiku vs opus is the difference between $5/month and $50/month.
- *Senior+:* This is the microservices pattern applied to AI: decompose a monolithic conversation into specialized, independently scalable agents with defined interfaces and resource constraints.

**No restart needed.** New agents are available immediately — just invoke them. If Claude doesn't see your agent, mention the file with `@` or run `/compact` to refresh context.

Shall we create the test writer agent next?

### 8.3 Create the Test Writer Agent

Now create a test writer agent. This one needs Write and Edit tools since it creates test files. Describe its job -- read source files, identify public functions, generate comprehensive tests, run them, and fix failures.

Try something like:

```
Create a test writer agent at .claude/agents/test-writer-agent.md. It should read source files, identify all public functions, generate tests covering happy paths, edge cases, and error cases, then run them and fix any failures. Give it Read, Write, Edit, Bash, Grep, and Glob tools. Use model: sonnet. It should follow our .claude/rules/tests.md conventions.
```

### 8.4 Create the Reporter Agent

Finally, create a reporter agent. Since formatting is a simpler task, this one can use `model: haiku` to save tokens. Describe its job -- gather analysis data and format it as text, JSON, or HTML.

Try something like:

```
Create a reporter agent at .claude/agents/reporter-agent.md. It should gather analysis data and format it as text, JSON, or HTML reports. HTML reports should include summary metrics, issue distribution tables, and severity color coding. Save to reports/. Use model: haiku since formatting doesn't need the most powerful model. Give it Read, Write, Bash, and Glob tools.
```

**STOP -- What you just did:** You created three agents with deliberately different configurations. The analyzer has read-only tools and uses sonnet. The test writer has write tools (it needs to create test files) and uses sonnet. The reporter uses haiku because formatting is a simpler task. This is the key design principle for subagents: match the model and tools to the job. Expensive models for hard reasoning, cheap models for mechanical work.

**Quick check before continuing:**
- [ ] `.claude/agents/` has three agent files: analyzer, test-writer, reporter
- [ ] Each agent has different tool access appropriate to its role
- [ ] You understand why different agents use different models

### 8.5 Understand Frontmatter Options

Ask Claude to walk you through all the available frontmatter fields for subagents.

Try something like:

```
What frontmatter fields can I use in subagent files? Walk me through name, description, tools, disallowedTools, model, permissionMode, skills, hooks, maxTurns, mcpServers, and memory.
```

Two additional frontmatter fields worth knowing: `isolation: worktree` runs the agent in its own git worktree so its changes stay isolated from your working tree, and `background: true` always runs the agent in the background (useful for long-running tasks that should not block). You can verify your agents from the command line with `claude agents` -- it lists all configured agents and their metadata.

**What about agents that talk to each other?** Subagents report back to your main conversation only -- they cannot communicate with each other. In Module 10 you will learn about **agent teams**, where multiple Claude instances share a task list and message each other directly. Subagents are for focused delegation; agent teams are for collaborative parallel work.

### 8.6 Chain Agents

**Why this step:** Chaining is when the output of one agent feeds into the input of the next. This is a pipeline pattern -- the analyzer finds problems, then the test writer generates tests for exactly those problems. Neither agent needs to know about the other; Claude orchestrates the handoff in your main conversation.

Ask Claude to chain the two agents -- have the analyzer find issues first, then pass those findings to the test writer to generate targeted tests.

Try something like:

```
Use the analyzer-agent to analyze src/rules/. Then use the test-writer-agent to generate tests for any files the analyzer flagged.
```

Claude will run the analyzer agent first, receive its findings, then pass relevant context to the test writer agent. This is **chaining**: the output of one agent feeds into the next.

**STOP -- What you just did:** You chained two subagents -- the analyzer found issues, and the test writer generated tests targeting those specific issues. This pipeline pattern is how you build complex workflows from simple, focused agents. In real projects, you might chain: analyzer -> fixer -> reviewer, or scanner -> reporter -> notifier.

Want to try running agents in parallel?

### 8.7 Run Agents in Parallel and Background

Ask Claude to fan out analysis across multiple directories using parallel subagents. Tell it to run them in the background so you can keep working.

Try something like:

```
In parallel, use separate subagents to analyze src/scanner/, src/rules/, and src/reporters/ for code quality. Run them in the background so I can keep working.
```

Press `Ctrl+B` if Claude starts a foreground agent and you want to move it to the background. Press `Ctrl+F` to kill background agents (press twice to confirm). Use `/tasks` to see running background tasks.

**STOP -- What you just did:** You ran three subagents in parallel, each analyzing a different directory simultaneously. This is the key advantage of subagents for large codebases -- instead of analyzing directories one by one, you fan out the work. Background mode (`Ctrl+B`) lets you continue working in your main conversation while agents crunch away. You will use this pattern whenever you have independent tasks that can run concurrently.

**Engineering value:**
- *Entry-level:* Running agents in parallel means a full code review (accessibility + design + content) takes the same time as one scan, not three.
- *Mid-level:* Chaining agents creates automated review pipelines: find issues → suggest fixes → verify fixes. This is the same find-fix-verify pattern used in CI/CD.

How about we try resuming a completed subagent?

### 8.8 Resume a Subagent

After a subagent completes, you can resume it to continue its work. Try extending the analyzer agent's previous run:

Try something like:

```
Continue the analyzer-agent from the previous analysis and now also check for security issues in the same files.
```

Claude resumes the agent with its full conversation history intact.

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

Three agents that decompose your analyzer's workflow. Chain them for pipelines, parallel them for speed.

- [ ] `.claude/agents/` directory has analyzer-agent.md, test-writer-agent.md, reporter-agent.md
- [ ] Each agent has appropriate frontmatter (name, description, tools, model)
- [ ] You chained analyzer -> test-writer successfully
- [ ] You ran agents in parallel or background
- [ ] You resumed a completed agent to continue its work
- [ ] You understand when to use subagents vs the main conversation
- [ ] Understand SendMessage replaces Agent resume parameter
- [ ] Tested `initialPrompt` frontmatter on an agent
