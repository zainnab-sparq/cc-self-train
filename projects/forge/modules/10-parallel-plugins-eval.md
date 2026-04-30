# Module 10 -- Parallel Dev, Plugins, and Evaluation

<!-- progress:start -->
**Progress:** Module 10 of 10 `[██████████]` 100%

**Estimated time:** ~90-120 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** Git worktrees, agent teams (experimental), plugins, evaluation,
PermissionRequest hooks, continuous learning

**Persona -- Launcher:** State the goal, step back. Only help if stuck after multiple tries. "You've got this", "Go build it."

</details>

> **New terms this module uses:**
> - **Worktree** -- a Git feature that lets you check out multiple branches in separate directories at the same time. Great for running parallel experiments without stashing and switching.
> - **Plugin (Claude Code)** -- a bundled set of extensions (skills, hooks, agents, MCP servers) that others can install in their projects. Installed with `/plugin`.
> - **Evaluation framework** -- a setup for running your agents/skills against a fixed set of inputs to measure quality over time. Like unit tests, but for AI behavior.
>
> See the [glossary](../../../GLOSSARY.md) for related terms.

### 10.1 Git Worktrees for Parallel Development

<!-- guide-only -->
**Why this step:** Until now, you have worked on one feature at a time: create a branch, build, merge, repeat. Git worktrees let you work on multiple features *simultaneously* in separate directories, each with its own Claude Code session. This is parallel development -- two features being built at the same time by two Claude instances, coordinating through a shared task list.
<!-- /guide-only -->

Git worktrees let you work on multiple branches simultaneously without
switching. Each worktree is a separate directory pointing to the same repo.

Create two worktrees for parallel feature development. You can use the manual approach or the `--worktree` (`-w`) shortcut:

```
# Manual approach -- `-b` creates the branch at the same time as the worktree:
! git worktree add -b feature/api ../forge-api
! git worktree add -b feature/export ../forge-export

# Or the shortcut -- launches Claude in a new worktree automatically:
claude -w
```

Hook into `WorktreeCreate` and `WorktreeRemove` events to automate setup and teardown (installing deps, copying env files, cleaning up).

Now you have three directories:
- `forge-toolkit/` -- main branch
- `../forge-api/` -- feature/api branch
- `../forge-export/` -- feature/export branch

### 10.2 Run Parallel Claude Instances

Open separate terminals. Share a task list across both:

```
# Terminal 1:
cd ../forge-api && CLAUDE_CODE_TASK_LIST_ID=forge-parallel claude

# Terminal 2:
cd ../forge-export && CLAUDE_CODE_TASK_LIST_ID=forge-parallel claude
```

In Terminal 1, create tasks for the API feature (design routes, implement
server, write tests -- with dependencies). In Terminal 2, create tasks for
the export feature (design formats, implement exporters, write tests).

Both sessions see all tasks. When one completes a task, the other is notified.

**STOP -- What you just did:** You set up parallel development with two Claude instances sharing a task list via `CLAUDE_CODE_TASK_LIST_ID`. Each instance works in its own worktree on its own feature branch, but they can see each other's task progress. This is the most advanced workflow pattern in Claude Code -- it lets you multiply your throughput by running independent features in parallel. When one session completes a task that unblocks work in the other session, both see the update.

**Quick check before continuing:**
- [ ] Two worktree directories exist (`forge-api/` and `forge-export/`)
- [ ] Each has its own Claude Code session running
- [ ] Both sessions see the same shared task list
- [ ] Tasks created in one session appear in the other

### 10.3 Agent Teams

<!-- guide-only -->
**Why this step:** You just coordinated two Claude instances manually -- separate terminals, shared task list, you switching between them. Agent teams automate this: Claude spawns teammates, assigns tasks, and they message each other directly. Same coordination pattern, but Claude manages it instead of you.
<!-- /guide-only -->

Agent teams are experimental. Enable them:

```
! claude config set experiments.agentTeams true
```

Tell Claude to create a team:

"Create an agent team to improve the forge toolkit. One teammate reviews the search system for edge cases, another adds missing export formats, and a third writes integration tests. They should coordinate through shared tasks."

Observe the team in action: Claude creates teammates, they pick up tasks, message each other, and report back. You can watch via the task list and message notifications. Use `Shift+Down` to navigate between teammates.

Agent Teams also works on Bedrock, Vertex, and Foundry API providers -- not just the direct Anthropic API.

**Subagents vs agent teams:** Subagents report back to you only -- they cannot communicate with each other. Agent teams message peer-to-peer and share a task list. Use subagents for focused delegation, agent teams for collaborative work requiring coordination.

**STOP -- What you just did:** You let Claude orchestrate a team of agents instead of managing parallel sessions yourself. Agent teams automate the `CLAUDE_CODE_TASK_LIST_ID` pattern you used in 10.2 -- same idea, but Claude handles the spawning, assignment, and messaging. This is experimental: no session resume for teams, no nested teams, and coordination overhead makes it best for tasks with real interdependencies.

### 10.4 Plugin Creation

<!-- guide-only -->
**Why this step:** Everything you have built -- skills, agents, hooks -- lives inside your project. A plugin packages these components into a portable, reusable bundle that can be shared with other projects or other people. Think of it as turning your project-specific customizations into a distributable tool.
<!-- /guide-only -->

Package everything you have built into a reusable plugin. Describe to Claude what you want to include and let it figure out the plugin structure.

"Package my forge toolkit into a reusable plugin called knowledge-base-plugin. Include the add-item, search, daily-summary, and backup skills, the search, format, and review agents, and extract the relevant hooks into plugin format. Create a plugin.json manifest with name and version."

Plugins can also ship a `settings.json` for default configuration (hooks, permissions, etc.) and can be distributed via the npm registry for easy sharing.

Claude may ask about which hooks to include or how to handle project-specific paths. The directory layout must be:

```
knowledge-base-plugin/
  .claude-plugin/plugin.json    <-- manifest (required)
  skills/                       <-- at root, NOT inside .claude-plugin/
  agents/
  hooks/hooks.json
```

### 10.5 Test the Plugin

Test your plugin locally:

```
claude --plugin-dir ./knowledge-base-plugin
```

Verify everything works:
- Skills invoke correctly: `/knowledge-base:add-item`, `/knowledge-base:search`
- Agents appear in `/agents`
- Hooks fire as expected

Note the namespacing: plugin skills are prefixed with the plugin name to
prevent conflicts.

**STOP -- What you just did:** You packaged your forge toolkit's skills, agents, and hooks into a standalone plugin with a manifest file. The plugin can be loaded into any project with `--plugin-dir`, and all skills are automatically namespaced (e.g., `/knowledge-base:add-item`) to prevent conflicts with the host project's own skills. This is how you share Claude Code customizations across projects and teams.

Ready to build an evaluation suite for your skills and agents?

### 10.6 Evaluation

<!-- guide-only -->
**Why this step:** How do you know your skills and agents actually work well? Evaluation gives you a systematic way to test them with defined inputs, expected outputs, and scoring criteria. This is not the same as unit testing your code -- it is testing your *Claude Code configuration*: do skills produce the right output? Do agents make good decisions?
<!-- /guide-only -->

Describe to Claude the test cases you want for each skill and agent. Think about what "correct behavior" looks like for each one -- both the happy path and the failure cases.

"Create an evaluation suite for the forge toolkit. I want test cases for each skill and agent with defined inputs, expected outputs, and scoring criteria. For add-item: test with a valid note, an empty title, and missing fields. For the search agent: test exact title match, tag search, and no-results behavior. For the review agent: test with an incomplete item and duplicates. Write a script that runs each test and reports pass/fail."

Claude may ask about how strict the scoring should be or what counts as "close enough." These are your standards -- discuss them.

**STOP -- What you just did:** You created an evaluation suite that tests your Claude Code configuration the same way you would test code. Each test case specifies what to input, what output to expect, and how to score the result. This closes the feedback loop: you built skills and agents in earlier modules, and now you have a way to measure whether they work correctly. In real projects, run evaluations after any change to skills, agents, or hooks to catch regressions.

Shall we set up auto-approval hooks for eval runs?

### 10.7 PermissionRequest Hooks for Eval Automation

<!-- guide-only -->
**Why this step:** Running evaluations means invoking many tool calls in rapid succession. Without auto-approval, you would have to manually confirm every Read, Grep, and Bash command -- dozens of permission prompts that slow everything down. PermissionRequest hooks let you auto-approve safe operations during eval while keeping the safety prompts during normal development.
<!-- /guide-only -->

During evaluation, auto-approve safe operations to avoid prompt fatigue. Ask Claude to set up the auto-approval hook in your local settings (not the shared project settings).

"Add a PermissionRequest hook to .claude/settings.local.json that auto-approves Read, Grep, Glob, and forge commands during evaluation. Use a matcher for those specific tools and output a decision with behavior: allow. Keep it in settings.local.json since this is a personal workflow choice."

**STOP -- What you just did:** You used a PermissionRequest hook to auto-approve safe operations (Read, Grep, Glob, and forge commands) during evaluation. Notice this hook lives in `settings.local.json` -- not committed to version control -- because auto-approval is a personal workflow choice, not a team policy. This is a good example of the local vs. project settings distinction: safety-reducing configurations stay local.

**Quick check before continuing:**
- [ ] Your plugin loads with `--plugin-dir` and skills work with namespace prefix
- [ ] Evaluation suite exists with test cases for skills and agents
- [ ] PermissionRequest hook auto-approves safe operations during eval
- [ ] The auto-approval hook is in `settings.local.json`, not `settings.json`

### 10.8 Continuous Learning

<!-- guide-only -->
**Why this step:** This is the most important habit you can build. Claude Code's effectiveness comes from its configuration -- CLAUDE.md, rules, skills, agents, hooks. Every time you discover a pattern that works or a mistake to avoid, capturing it in your configuration makes every future session better. This is compound learning: each session builds on everything that came before.
<!-- /guide-only -->

Reflect on the full project and have a conversation with Claude about what you have learned. Ask it to review your configuration and suggest improvements based on how things actually worked.

"Review our CLAUDE.md, rules, skills, agents, and hooks. What patterns worked well? What should we refine? Are there edge cases we missed or descriptions that could be clearer? Help me update everything based on what we've learned building this project."

This is the continuous learning cycle: build, reflect, refine, repeat.

Claude also saves useful context automatically across sessions via **auto-memory**. Use `/memory` to review what has been saved and verify it matches your understanding. Auto-memory complements CLAUDE.md -- it captures things you might forget to write down.

**STOP -- What you just did:** You completed the full learning loop. Over 10 modules, you built a personal dev toolkit while systematically learning every major Claude Code feature. This final step -- reviewing and refining your configuration -- is what separates people who use Claude Code from people who master it. Your CLAUDE.md, rules, skills, agents, and hooks are a living system that gets better with every session. Keep updating them.

### 10.9 Plugin Ecosystem Updates

The plugin system has expanded significantly. Explore these additions:

- **`source: 'settings'`** (v2.1.80) — declare plugin entries inline in settings.json
- **`${CLAUDE_PLUGIN_DATA}`** (v2.1.78) — persistent state directory that survives plugin updates
- **`/reload-plugins`** (v2.1.69) — activate plugin changes without restarting
- **`claude plugin validate`** (v2.1.77) — validates skill, agent, and command frontmatter plus hooks.json
- **`git-subdir`** (v2.1.69) — plugin source type pointing to a subdirectory within a git repo
- **`pluginTrustMessage`** (v2.1.69) — managed setting for org-specific plugin trust context
- **`CLAUDE_CODE_PLUGIN_SEED_DIR`** (v2.1.79) — now supports multiple directories

You've got this — try `claude plugin validate` on your project's plugin configuration.

### 10.10 Worktrees, IDE & Remote Control

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

You made it. A complete toolkit, built from scratch, using every major Claude Code feature.

- [ ] Created git worktrees for parallel feature development
- [ ] Ran two Claude instances with a shared task list
- [ ] Both instances could see and update the same tasks
- [ ] (Experimental) Created an agent team with 2-3 teammates
- [ ] Teammates communicated and coordinated through shared tasks
- [ ] Plugin created with manifest, skills, agents, and hooks
- [ ] Plugin tested with `--plugin-dir` and skills work with namespace prefix
- [ ] Evaluation suite exists with test specs for skills and agents
- [ ] PermissionRequest hook auto-approves safe operations during eval
- [ ] CLAUDE.md and rules updated with lessons learned from the project
- [ ] Explored plugin ecosystem updates (validate, reload, settings source)
- [ ] Reviewed worktree and IDE/Remote Control additions
- [ ] Tested plugin `userConfig` with a sensitive field

---

## Final Verification Checklist

Confirm you have touched every major Claude Code feature across all 10 modules:

- [ ] `/init`, `/memory`, `CLAUDE.md` -- project memory and configuration
- [ ] Keyboard shortcuts -- Tab, Shift+Tab, Ctrl+C, Ctrl+L, @, !, Esc Esc, Ctrl+O, Ctrl+B
- [ ] Plan mode -- designed architecture before building
- [ ] Git integration -- branches, commits, merges through Claude
- [ ] `.claude/rules/` -- path-scoped rules with YAML frontmatter
- [ ] `CLAUDE.local.md` -- personal, non-committed preferences
- [ ] `@imports` -- modular CLAUDE.md referencing external docs
- [ ] `/context`, `/compact`, `/stats` or `/cost`, `/statusline` -- context and usage management
- [ ] Custom skills -- `SKILL.md` with frontmatter, `$ARGUMENTS`, hot-reload
- [ ] `disable-model-invocation` -- manual-only skills
- [ ] Hooks -- SessionStart, PostToolUse, PreToolUse, Stop in `.claude/settings.json`
- [ ] Hook decision control -- `permissionDecision`, `additionalContext`, `updatedInput`
- [ ] Prompt-based hooks -- `type: "prompt"` for LLM-powered quality gates
- [ ] MCP servers -- `claude mcp add`, `/mcp`, `.mcp.json`, scopes
- [ ] Skills + MCP -- skill orchestrating MCP tools
- [ ] Subagents -- `.claude/agents/` with frontmatter, chaining, parallel, resume
- [ ] Tasks -- TaskCreate, dependencies, `CLAUDE_CODE_TASK_LIST_ID`
- [ ] TDD -- test-first development cycle
- [ ] SubagentStop hooks -- verification of subagent output
- [ ] Git worktrees -- parallel development with multiple Claude instances
- [ ] Agent teams (experimental) -- created a team, observed messaging and task coordination
- [ ] Plugins -- manifest, skills, agents, hooks, `--plugin-dir`
- [ ] Evaluation -- test specs for skills and agents
- [ ] PermissionRequest hooks -- auto-approval for eval automation
- [ ] Continuous learning -- updated CLAUDE.md with project insights
- [ ] Skimmed the plugin-ecosystem updates (themes via plugins, `prUrlTemplate`, `DISABLE_UPDATES`, deps auto-install)
- [ ] Know that `claude ultrareview` and `claude plugin prune` exist for scripted workflows

---

## Tips

**Start small, then expand.** Do not try to build everything at once. Each
module builds on the last. If you get stuck, go back and make sure the
previous module's checkpoint is complete.

**Use plan mode liberally.** Before any significant change, switch to plan
mode and think it through. This is cheaper than fixing mistakes.

**Read the context files.** The `cc-self-train/context/` directory has detailed
reference docs for every CC feature: `claudemd.txt`, `skillsmd.txt`,
`hooks.txt`, `configure-hooks.txt`, `mcp.txt`, `skills-plus-mcp.txt`,
`subagents.txt`, `agent-teams.txt`, `tasks.txt`, `plugins.txt`,
`interactive-mode.txt`, `common-workflows.txt`, `when-to-use-features.txt`,
`boris-workflow.txt`.

**Commit often.** Small, focused commits make it easy to revert mistakes and
track progress.

**Use `/compact` strategically.** Context management is a skill. When your
session gets long, use `/compact` with a focus argument to preserve what matters.
Check `/stats` or `/cost` periodically to understand your usage patterns.

**Keep CLAUDE.md up to date.** Every time you discover a pattern, convention,
or lesson, add it to your project memory. Future sessions benefit immediately.

**Test your hooks locally first.** Before adding a hook to settings.json, run
the script manually with sample JSON input to make sure it works. A broken
hook can block your workflow.

**Use `Ctrl+O` for debugging.** Verbose mode shows hook execution, tool calls,
and other details that are hidden by default. Toggle it when troubleshooting.

**Background tasks are powerful.** Use `Ctrl+B` to background long-running
operations (tests, builds, agents) and keep working on something else.

---

## What Is Next

Take a second to appreciate what you just did. You built a personal dev toolkit from scratch — one you'll actually use — and along the way, you mastered every major Claude Code feature: CLAUDE.md, plan mode, rules, skills, hooks, MCP servers, guard rails, subagents, tasks, worktrees, plugins, and evaluation. That's not a tutorial you followed. That's a real tool you built.

You're not a beginner anymore. You know how to make Claude Code work for you.

Here are paths forward:

- **Keep extending your toolkit.** Add full-text search with stemming, a web UI, import from Notion or Obsidian. The forge is yours now.
- **Try another project.** Canvas, Nexus, and Sentinel cover the same features through different domains — and you'll move through them faster this time.
- **Share your plugin.** If your knowledge-base plugin is useful, distribute it to your team or the community.
- **Build something new.** Take a project idea you've been putting off and build it with Claude Code. You have the full toolkit now — go use it.
- **Come back for updates.** This curriculum is actively maintained — `git pull` to get updated modules, new feature coverage, and refined exercises. Check the [changelog](../../../CHANGELOG.md) to see what's new.
