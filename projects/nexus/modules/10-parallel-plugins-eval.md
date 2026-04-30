# Module 10 -- Parallel Dev, Plugins & Evaluation

<!-- progress:start -->
**Progress:** Module 10 of 10 `[██████████]` 100%

**Estimated time:** ~90-120 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** Worktrees, agent teams (experimental), plugins, eval, PermissionRequest hooks, continuous learning

**Persona -- Launcher:** State the goal, step back. Only help if stuck after multiple tries. "You've got this", "Go build it."

</details>

<!-- guide-only -->
**Why this step:** Until now, you have worked on one feature at a time. Git worktrees create separate working directories that share the same repository, so you can have two Claude Code instances building two features simultaneously. This is how teams work on multiple features in parallel without merge conflicts blocking progress.
<!-- /guide-only -->

> **New terms this module uses:**
> - **Worktree** -- a Git feature that lets you check out multiple branches in separate directories at the same time. Great for running parallel experiments without stashing and switching.
> - **Plugin (Claude Code)** -- a bundled set of extensions (skills, hooks, agents, MCP servers) that others can install in their projects. Installed with `/plugin`.
> - **Evaluation framework** -- a setup for running your agents/skills against a fixed set of inputs to measure quality over time. Like unit tests, but for AI behavior.
>
> See the [glossary](../../../GLOSSARY.md) for related terms.

### 10.1 Git Worktrees for Parallel Development

Git worktrees give you multiple working directories for the same repo, enabling two Claude Code instances on different features simultaneously. Create two worktrees manually or use the `--worktree` (`-w`) shortcut:

```
# Manual approach -- `-b` creates the branch at the same time as the worktree:
! git worktree add -b feature/metrics ../nexus-gateway-metrics
! git worktree add -b feature/websocket ../nexus-gateway-websocket

# Or the shortcut -- launches Claude in a new worktree automatically:
claude -w
```

Hook into `WorktreeCreate` and `WorktreeRemove` events to automate setup and teardown (installing deps, copying env files, cleaning up).

### 10.2 Multiple CC Instances with Shared Tasks

Open two terminals with shared tasks:
- **Terminal 1:** `cd ../nexus-gateway-metrics && CLAUDE_CODE_TASK_LIST_ID=nexus-parallel claude`
- **Terminal 2:** `cd ../nexus-gateway-websocket && CLAUDE_CODE_TASK_LIST_ID=nexus-parallel claude`

In Terminal 1, describe the metrics feature and ask Claude to create tasks for it:

```
I want to add a metrics system to the gateway. Create tasks for: a request counter per route, a response time histogram, a /metrics endpoint, and tests for metrics collection. Start on the first task.
```

In Terminal 2, describe the websocket feature:

```
I want to add websocket support to the gateway. Create tasks for: websocket upgrade handling in the router, proxying websocket connections to upstreams, websocket health checks, and tests. Start on the first task.
```

Both instances share the task list. When one completes a task, the other sees the update. This is the parallel development workflow.

**STOP -- What you just did:** You ran two Claude Code instances simultaneously, each building a different feature in its own worktree, while sharing a task list. This is the most advanced development pattern in Claude Code: parallel autonomous development with coordination. In a real team setting, each worktree could be a different developer's Claude instance, all contributing to the same backlog.

**Quick check before continuing:**
- [ ] Two worktrees exist (nexus-gateway-metrics and nexus-gateway-websocket)
- [ ] Two Claude Code instances are running with `CLAUDE_CODE_TASK_LIST_ID=nexus-parallel`
- [ ] Tasks created in one terminal appear in the other
- [ ] Both instances are making progress on their respective features

### 10.3 Agent Teams

Agent teams are experimental. Enable them:

```
! claude config set experiments.agentTeams true
```

Tell Claude to create a team:

```
Create an agent team for the gateway. One teammate builds a health dashboard endpoint, another adds request logging middleware, and a third writes load tests. They share a task list and coordinate.
```

Watch the team work: Claude spawns teammates, assigns tasks, and they message each other directly. This automates the manual `CLAUDE_CODE_TASK_LIST_ID` pattern from Step 2. Use `Shift+Down` to navigate between teammates.

Agent Teams also works on Bedrock, Vertex, and Foundry API providers -- not just the direct Anthropic API.

**Subagents vs agent teams:** Subagents report back to you only. Agent teams communicate peer-to-peer through shared tasks and direct messages. Use subagents for focused delegation, agent teams for collaborative parallel work.

**STOP -- What you just did:** You used agent teams to automate multi-instance coordination. Instead of managing separate terminals with a shared `CLAUDE_CODE_TASK_LIST_ID`, Claude handled the orchestration -- creating teammates, assigning work, and letting them communicate. This is experimental: no session resume for teams, no nested teams, and best suited for tasks with genuine interdependencies.

### 10.4 Create a Plugin -- "gateway-plugin"

<!-- guide-only -->
**Why this step:** Everything you have built -- skills, agents, hooks -- lives inside your project's `.claude/` directory. A plugin packages all of that into a portable bundle that can be shared, versioned, and reused across projects. If you build another gateway next month, you bring the plugin instead of recreating everything from scratch.
<!-- /guide-only -->

Ask Claude to bundle your skills, agents, and hooks into a distributable plugin. Describe what you want packaged.

```
Package all my skills, agents, and hooks into a plugin called gateway-plugin. Create the plugin directory structure with a plugin.json, copy the skills and agents from .claude/, and include the hook configuration. Version 1.0.0.
```

Claude will create the plugin structure with `.claude-plugin/plugin.json`, a `skills/` directory, an `agents/` directory, and a `hooks/hooks.json` file. Plugins can also ship a `settings.json` for default configuration and can be distributed via the npm registry.

Test: `claude --plugin-dir ./gateway-plugin`, then try `/gateway-plugin:add-route` and `/gateway-plugin:status-report`. Skills appear with the namespace prefix.

**STOP -- What you just did:** You packaged your skills, agents, and hooks into a distributable plugin. Notice the namespace prefix (`/gateway-plugin:add-route`) -- this prevents naming collisions when multiple plugins are loaded. The plugin is a self-contained directory that anyone can use with `--plugin-dir`. You have gone from "tools that help me" to "tools I can share."

Ready to build an evaluation and scoring system?

### 10.5 Evaluation -- Test Specs and Scoring

<!-- guide-only -->
**Why this step:** Evaluation is how you measure Claude's work against objective criteria. Instead of manually checking "does the gateway work?", you define test specs with pass/fail criteria and a scoring system. This pattern is essential for CI/CD pipelines where Claude runs headlessly via `claude -p` and you need automated quality assessment.
<!-- /guide-only -->

Describe the evaluation criteria you want for your gateway and ask Claude to build a scoring script. Think about what matters -- health checks, route matching, rate limiting, caching, middleware, and error handling.

```
Create an evaluation script that scores the gateway out of 10. I want to check: health endpoint responds within 2 seconds, route matching works for at least 5 scenarios, rate limiting returns 429 when exceeded, caching works for GET requests, middleware chain executes in order, and error handling returns proper status codes for upstream failures and bad requests. Run the evaluation and show me the score.
```

Claude will build the evaluation script and run it. This is a basic evaluation framework. In production, you would use this pattern to score Claude's work against specifications.

**STOP -- What you just did:** You created a scoring rubric for your gateway and ran it as an automated evaluation. This is the foundation for continuous evaluation: every time you make changes, you can re-run the eval to check for regressions. In production workflows, this pattern runs in CI to score Claude's output against specifications before merging.

**Quick check before continuing:**
- [ ] The evaluation script runs and reports a score out of 10
- [ ] The plugin works with `--plugin-dir` and skills have the namespace prefix
- [ ] Both worktree features are progressing (or completed)

### 10.6 PermissionRequest Hooks

<!-- guide-only -->
**Why this step:** PermissionRequest hooks control the permission dialogs Claude shows you. Instead of clicking "allow" every time Claude wants to run tests, you auto-approve known-safe commands. And instead of trusting yourself to remember "do not edit the database directly," you auto-deny dangerous patterns. This is the final layer of automation: even the permission system is programmable.
<!-- /guide-only -->

PermissionRequest hooks fire when Claude would show a permission dialog. Add to `.claude/settings.json`:

- **Auto-approve tests**: matcher `"Bash(npm test*)"` (adjust for your test runner), decision `"behavior": "allow"`
- **Block direct DB edits**: matcher `"Bash(sqlite3 cache.db*)"`, decision `"behavior": "deny"` with message `"Use the cache-agent or cache-inspect skill instead."`

The JSON output format for PermissionRequest hooks uses `hookSpecificOutput.decision.behavior` set to `"allow"` or `"deny"`. Ask Claude to generate the full settings.json entries for your language's test command.

**STOP -- What you just did:** You automated the permission system itself. PermissionRequest hooks are the final piece of the hook lifecycle: SessionStart (context at launch), PreToolUse (guard before actions), PostToolUse (validate after actions), Stop (quality gate at completion), SubagentStop (quality gate for agents), and now PermissionRequest (control the permission dialogs). Every interaction point between you and Claude is now programmable.

Shall we capture what you learned in your project knowledge layer?

### 10.7 Continuous Learning

<!-- guide-only -->
**Why this step:** This is not just a cleanup step -- it is the most important habit you will take from this course. Every project improves Claude's effectiveness by capturing what you learned: architecture decisions in CLAUDE.md, coding patterns in rules files, workflows in skills, specialized analysis in agents. The project you just built is not just a gateway -- it is a knowledge base that makes your next project faster.
<!-- /guide-only -->

Update CLAUDE.md with architecture decisions, common commands, known issues, coding conventions, and performance characteristics. Also update `.claude/rules/` with new rules from your work.

The key insight: CLAUDE.md + rules + skills + agents + hooks form a complete "knowledge layer" that makes Claude more effective over time. Claude also saves useful context automatically across sessions via **auto-memory** -- use `/memory` to review what has been captured. Auto-memory complements CLAUDE.md by catching things you might forget to write down.

### 10.8 Plugin Ecosystem Updates

The plugin system has expanded significantly. Explore these additions:

- **`source: 'settings'`** (v2.1.80) — declare plugin entries inline in settings.json
- **`${CLAUDE_PLUGIN_DATA}`** (v2.1.78) — persistent state directory that survives plugin updates
- **`/reload-plugins`** (v2.1.69) — activate plugin changes without restarting
- **`claude plugin validate`** (v2.1.77) — validates skill, agent, and command frontmatter plus hooks.json
- **`git-subdir`** (v2.1.69) — plugin source type pointing to a subdirectory within a git repo
- **`pluginTrustMessage`** (v2.1.69) — managed setting for org-specific plugin trust context
- **`CLAUDE_CODE_PLUGIN_SEED_DIR`** (v2.1.79) — now supports multiple directories

You've got this — try `claude plugin validate` on your project's plugin configuration.

### 10.9 Worktrees, IDE & Remote Control

Final batch of updates spanning worktrees and IDE integration:

- **`ExitWorktree`** tool (v2.1.72) — leave an `EnterWorktree` session cleanly
- **`worktree.sparsePaths`** (v2.1.76) — check out only the directories you need in large monorepos
- **VS Code `/remote-control`** (v2.1.79) — bridge your session to claude.ai/code for browser/phone access
- **`vscode://anthropic.claude-code/open`** (v2.1.72) — URI handler to open Claude Code tabs programmatically
- **Native MCP dialog** (v2.1.70) — manage MCP servers from the VS Code chat panel
- **Spark icon** (v2.1.70) — activity bar icon listing all sessions
- **Deprecated `/output-style`** (v2.1.73) — use `/config` instead

No hints needed — explore what's relevant to your workflow. Go build it.

### 10.13 Plugin Configuration & Sensitive Storage

Plugins can now define user-facing configuration schemas in their manifest using `userConfig`. When a user enables the plugin, they are prompted for configuration values. Fields marked with `sensitive: true` are stored securely -- in the macOS keychain or a protected credentials file on other platforms.

If you created a plugin earlier in this module, try adding a `userConfig` section to its manifest with at least one sensitive field (like an API key or token). Enable the plugin and observe how it prompts for configuration. Check that the sensitive value is not visible in the manifest file itself.

### 10.14 /ultrareview cloud multi-agent review (v2.1.111)

New: `/ultrareview` runs a comprehensive multi-agent code review in the cloud. It invokes multiple specialized reviewers in parallel (security, types, tests, architecture, etc.), aggregates their findings, and returns a structured report.

**When to reach for it:** before shipping a major PR or touching a sensitive area (auth, payments, webhooks). Slower and costlier than a local review — reserve for high-stakes changes.

**When to skip:** routine work, or anywhere your `code-reviewer` / `security-reviewer` subagents already do the job locally.

Try it on one of your worktree branches. Compare the findings to what your local review flow caught.

### 10.15 Plugin ecosystem updates (v2.1.115 – v2.1.119)

A burst of plugin-layer polish worth skimming:

- **Themes ship via plugins.** A plugin can include a `themes/` directory; every theme in there shows up in `/theme` once the plugin is enabled (v2.1.115). Brand palettes become a plugin, not a settings snippet.
- **`claude plugin tag`.** Plugin authors: this command creates a git tag for the plugin's declared version so downstream marketplaces that pin by tag can find it (v2.1.115).
- **Auto-install missing dependencies.** `/reload-plugins` (v2.1.116), `plugin install` (v2.1.117), and `claude plugin marketplace add` (v2.1.117) all now auto-resolve missing deps instead of erroring. Dependency errors distinguish "declared but not installed" from other failure modes. Plugins pinned by another plugin's version constraint auto-update when that constraint changes (v2.1.119).
- **Plugin skip reasons in `/doctor`** (v2.1.115). If a plugin is disabled, incompatible, or waiting on an unmet dep, `/doctor` now tells you which.
- **`prUrlTemplate` setting** (v2.1.119). Custom code-review URLs for internal forges. Example: `"prUrlTemplate": "https://code.mycorp.internal/{repo}/mr/{n}"` rewrites `owner/repo#42` shorthand links to open your internal GitLab instead of github.com.
- **Managed-settings enforcement.** `blockedMarketplaces` and `strictKnownMarketplaces` are enforced at plugin install time (v2.1.117); `blockedMarketplaces` now correctly honors both `hostPattern` and `pathPattern` (v2.1.119).
- **`DISABLE_UPDATES`** (v2.1.115). Env var that blocks *every* update path — `claude update`, background checks, plugin auto-updates. Stricter than `CLAUDE_CODE_DISABLE_AUTOUPDATER` (which only blocks automatic upgrades).

None of this requires action. Surface-level awareness so when you hit a weird plugin state, you know where to look.

### 10.16 New CLI subcommands: `claude ultrareview` and `claude plugin prune` (v2.1.120, v2.1.121)

Two non-interactive CLI subcommands worth knowing for scripted workflows.

**`claude ultrareview [target]`** (v2.1.120). Runs `/ultrareview` from the shell -- useful in CI, pre-merge scripts, or wrapper tools. `[target]` defaults to the current branch's diff against the default branch; pass a PR number (`1234`) or a branch (`origin/main`) to scope the review elsewhere. `--json` prints the raw findings payload for downstream tooling. Exit codes: `0` = completed, `1` = failed or timed out, `130` = Ctrl-C.

**`claude plugin prune`** (v2.1.121). Removes auto-installed plugin dependencies that no other plugin requires -- useful after uninstalling a plugin or refactoring your plugin set. Pair with `--dry-run` first to preview, then re-run to apply. The companion `plugin uninstall <name> --prune` cascades cleanup in one command instead of two.

Skim the changelog for both -- you'll find them when you need them.

### Checkpoint

You made it. A production-style gateway, built from scratch, using every major Claude Code feature.

- [ ] Two git worktrees created for parallel feature development
- [ ] Two Claude Code instances sharing a task list
- [ ] (Experimental) Created an agent team with 2-3 teammates
- [ ] Teammates communicated and coordinated through shared tasks
- [ ] gateway-plugin created with skills, agents, and hooks
- [ ] Plugin tested with `--plugin-dir` flag
- [ ] Evaluation script runs and produces a score
- [ ] PermissionRequest hooks auto-approve tests and block direct DB modification
- [ ] CLAUDE.md updated with comprehensive project knowledge
- [ ] All worktree branches merged back to main
- [ ] Final commit on main with all features integrated
- [ ] Explored plugin ecosystem updates (validate, reload, settings source)
- [ ] Reviewed worktree and IDE/Remote Control additions
- [ ] Tested plugin `userConfig` with a sensitive field

---

## Final Verification Checklist

Go through this list to confirm you have covered every major CC feature:

**Foundation (Modules 1-2)**
- [ ] CLAUDE.md exists with comprehensive project documentation
- [ ] You have used Plan mode to design before building
- [ ] At least 10 meaningful git commits across the project
- [ ] The gateway starts, routes requests, and serves /health

**Context Management (Module 3)**
- [ ] .claude/rules/ has path-scoped rules for routing, config, and testing
- [ ] CLAUDE.local.md exists for personal preferences
- [ ] CLAUDE.md uses @imports for documentation files
- [ ] You have used /context, /compact, /stats or /cost, and /statusline

**Skills (Module 4)**
- [ ] At least 4 skills in .claude/skills/
- [ ] At least one skill uses $ARGUMENTS or $0 substitution
- [ ] At least one skill has disable-model-invocation: true
- [ ] Skills are invokable via /skill-name

**Hooks (Modules 5 + 7)**
- [ ] SessionStart hook injects gateway status
- [ ] PostToolUse hook validates config after writes
- [ ] Stop hook runs tests before allowing completion
- [ ] PreToolUse hook with permissionDecision (deny)
- [ ] PreToolUse hook with additionalContext
- [ ] Prompt-based hook for security checking
- [ ] All hooks configured in .claude/settings.json

**MCP (Module 6)**
- [ ] SQLite MCP server connected
- [ ] .mcp.json exists at project root
- [ ] Cache layer uses SQLite through MCP
- [ ] A skill orchestrates MCP tools (cache-inspect)

**Subagents (Module 8)**
- [ ] At least 3 subagents in .claude/agents/
- [ ] Subagents have been invoked, chained, and run in background
- [ ] Subagent frontmatter includes tools and model restrictions

**Tasks & TDD (Module 9)**
- [ ] Task list with dependencies created and completed
- [ ] TDD cycles committed separately (red-green-refactor)
- [ ] SubagentStop hook validates subagent output

**Advanced (Module 10)**
- [ ] Git worktrees used for parallel development
- [ ] Agent teams (experimental) -- created a team, observed messaging and task coordination
- [ ] Plugin created and tested
- [ ] Evaluation script produces a score
- [ ] PermissionRequest hooks configured
- [ ] Skimmed the plugin-ecosystem updates (themes via plugins, `prUrlTemplate`, `DISABLE_UPDATES`, deps auto-install)
- [ ] Know that `claude ultrareview` and `claude plugin prune` exist for scripted workflows

---

## Tips

**Context management is the most important skill.** Use `/compact` aggressively, use subagents to isolate verbose work, and keep CLAUDE.md concise with @imports for details.

**Commit often.** Small, focused commits with `Esc Esc` (rewind) give easy rollback points.

**Use Plan mode before Act mode.** Design in Plan mode first. Thinking up front prevents costly rework.

**Skills encode workflow; subagents encode expertise.** Repeated processes become skills. Specialized perspectives (security, performance) become subagents.

**Hooks eliminate friction.** Any manual step you repeat is a candidate. Start with SessionStart and PostToolUse, then add more as friction points emerge.

**Test through the gateway.** Always test through HTTP, not by calling functions directly. This validates routing, middleware, caching, and rate limiting end-to-end.

**Read the context/ directory.** The cc-self-train repository has detailed CC feature reference docs in `context/`.

---

## What's Next?

Take a second to appreciate what you just did. You built a full-featured local API gateway from scratch -- routing, rate limiting, caching, health checks, middleware -- and along the way, you mastered every major Claude Code feature: CLAUDE.md, plan mode, rules, skills, hooks, MCP servers, guard rails, subagents, tasks, worktrees, plugins, and evaluation. That's not a walkthrough you followed. That's real infrastructure you built.

You're not a beginner anymore. You know how to make Claude Code work for you.

Here are paths forward:

**Extend the gateway.** WebSocket proxying, gRPC support, circuit breaker patterns, distributed rate limiting, request/response transformation middleware, OpenAPI spec generation from route configs.

**Go deeper with Claude Code.** Explore the `context/` directory in cc-self-train for advanced patterns. Build your own MCP server. Create and distribute plugins. Set up CI/CD pipelines using `claude -p` (headless mode).

**Try another project.** [Forge](../forge/) if you want to build a personal dev toolkit, or [Sentinel](../sentinel/) if you want to build a code analyzer and test generator. Both cover the same features through different domains -- and you'll move through them faster this time.

**Come back for updates.** This curriculum is actively maintained -- `git pull` to get updated modules, new feature coverage, and refined exercises. Check the [changelog](../../../CHANGELOG.md) to see what's new.
