# Module 8 -- Subagents

**CC features:** .claude/agents/, subagent frontmatter, chaining, parallel, background (Ctrl+B), resuming, `claude agents` CLI

> **Persona — Peer:** Terse guidance, point to docs, let them debug first. "Your call", "What would you do here?"

In this module you create specialized AI agents that handle specific tasks within Sentinel.

### Step 1: What are subagents

> **Why this step:** Up to now, everything has happened in a single Claude conversation. Subagents let you spin up specialized Claude instances -- each with their own system prompt, tool access, and context window. Think of it as delegation: instead of doing everything yourself, you assign specific jobs to specialists. This keeps your main conversation clean and lets you parallelize work.

Ask Claude what subagents are and when you should use them instead of the main conversation.

> "What are Claude Code subagents? How are they different from this main conversation, and when should I use one?"

Key points: subagents run in their own context window with a custom system prompt and specific tool access. They keep verbose output out of your main conversation. They cannot spawn other subagents.

### Step 2: Create the analyzer agent

Ask Claude to create a specialized analyzer agent. Describe its role -- deep code analysis, running the scanner, evaluating whether issues are true or false positives, and suggesting fixes. Tell Claude to give it read-only tools (no Write or Edit) since it should find issues, not fix them. Suggest using the `sonnet` model to save tokens.

> "Create an analyzer agent at .claude/agents/analyzer-agent.md. It should be a deep analysis specialist -- runs the scanner, evaluates each issue for true/false positive, assesses severity, and suggests fixes. Give it only Read, Grep, Glob, and Bash tools (no Write). Use model: sonnet."

> **STOP -- What you just did:** You created a specialized analyzer agent with limited tool access (Read, Grep, Glob, Bash -- no Write or Edit). This is intentional: the analyzer agent should *find* issues, not *fix* them. Restricting tools prevents subagents from doing things outside their role. The `model: sonnet` setting means this agent uses a cheaper model -- since analysis does not require the most powerful model, this saves tokens.

Shall we create the test writer agent next?

### Step 3: Create the test writer agent

Now create a test writer agent. This one needs Write and Edit tools since it creates test files. Describe its job -- read source files, identify public functions, generate comprehensive tests, run them, and fix failures.

> "Create a test writer agent at .claude/agents/test-writer-agent.md. It should read source files, identify all public functions, generate tests covering happy paths, edge cases, and error cases, then run them and fix any failures. Give it Read, Write, Edit, Bash, Grep, and Glob tools. Use model: sonnet. It should follow our .claude/rules/tests.md conventions."

### Step 4: Create the reporter agent

Finally, create a reporter agent. Since formatting is a simpler task, this one can use `model: haiku` to save tokens. Describe its job -- gather analysis data and format it as text, JSON, or HTML.

> "Create a reporter agent at .claude/agents/reporter-agent.md. It should gather analysis data and format it as text, JSON, or HTML reports. HTML reports should include summary metrics, issue distribution tables, and severity color coding. Save to reports/. Use model: haiku since formatting doesn't need the most powerful model. Give it Read, Write, Bash, and Glob tools."

> **STOP -- What you just did:** You created three agents with deliberately different configurations. The analyzer has read-only tools and uses sonnet. The test writer has write tools (it needs to create test files) and uses sonnet. The reporter uses haiku because formatting is a simpler task. This is the key design principle for subagents: match the model and tools to the job. Expensive models for hard reasoning, cheap models for mechanical work.

> **Quick check before continuing:**
> - [ ] `.claude/agents/` has three agent files: analyzer, test-writer, reporter
> - [ ] Each agent has different tool access appropriate to its role
> - [ ] You understand why different agents use different models

### Step 5: Understand frontmatter options

Ask Claude to walk you through all the available frontmatter fields for subagents.

> "What frontmatter fields can I use in subagent files? Walk me through name, description, tools, disallowedTools, model, permissionMode, skills, hooks, maxTurns, mcpServers, and memory."

Two additional frontmatter fields worth knowing: `isolation: worktree` runs the agent in its own git worktree so its changes stay isolated from your working tree, and `background: true` always runs the agent in the background (useful for long-running tasks that should not block). You can verify your agents from the command line with `claude agents` -- it lists all configured agents and their metadata.

> **What about agents that talk to each other?** Subagents report back to your main conversation only -- they cannot communicate with each other. In Module 10 you will learn about **agent teams**, where multiple Claude instances share a task list and message each other directly. Subagents are for focused delegation; agent teams are for collaborative parallel work.

### Step 6: Chain agents

> **Why this step:** Chaining is when the output of one agent feeds into the input of the next. This is a pipeline pattern -- the analyzer finds problems, then the test writer generates tests for exactly those problems. Neither agent needs to know about the other; Claude orchestrates the handoff in your main conversation.

Ask Claude to chain the two agents -- have the analyzer find issues first, then pass those findings to the test writer to generate targeted tests.

> "Use the analyzer-agent to analyze src/rules/. Then use the test-writer-agent to generate tests for any files the analyzer flagged."

Claude will run the analyzer agent first, receive its findings, then pass relevant context to the test writer agent. This is **chaining**: the output of one agent feeds into the next.

> **STOP -- What you just did:** You chained two subagents -- the analyzer found issues, and the test writer generated tests targeting those specific issues. This pipeline pattern is how you build complex workflows from simple, focused agents. In real projects, you might chain: analyzer -> fixer -> reviewer, or scanner -> reporter -> notifier.

Want to try running agents in parallel?

### Step 7: Run agents in parallel and background

Ask Claude to fan out analysis across multiple directories using parallel subagents. Tell it to run them in the background so you can keep working.

> "In parallel, use separate subagents to analyze src/scanner/, src/rules/, and src/reporters/ for code quality. Run them in the background so I can keep working."

Press `Ctrl+B` if Claude starts a foreground agent and you want to move it to the background. Press `Ctrl+F` to kill background agents (press twice to confirm). Use `/tasks` to see running background tasks.

> **STOP -- What you just did:** You ran three subagents in parallel, each analyzing a different directory simultaneously. This is the key advantage of subagents for large codebases -- instead of analyzing directories one by one, you fan out the work. Background mode (`Ctrl+B`) lets you continue working in your main conversation while agents crunch away. You will use this pattern whenever you have independent tasks that can run concurrently.

How about we try resuming a completed subagent?

### Step 8: Resume a subagent

After a subagent completes, you can resume it to continue its work. Try extending the analyzer agent's previous run:

> "Continue the analyzer-agent from the previous analysis and now also check for security issues in the same files."

Claude resumes the agent with its full conversation history intact.

### Checkpoint

Three agents that decompose your analyzer's workflow. Chain them for pipelines, parallel them for speed.

- [ ] `.claude/agents/` directory has analyzer-agent.md, test-writer-agent.md, reporter-agent.md
- [ ] Each agent has appropriate frontmatter (name, description, tools, model)
- [ ] You chained analyzer -> test-writer successfully
- [ ] You ran agents in parallel or background
- [ ] You resumed a completed agent to continue its work
- [ ] You understand when to use subagents vs the main conversation
