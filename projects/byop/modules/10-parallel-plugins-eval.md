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
**Why this step:** Until now, you have worked on one feature at a time. Git worktrees let you have multiple branches checked out simultaneously in different directories -- each with its own Claude Code session. This is how you do true parallel development: two features being built at the same time by two Claude instances that can even share a task list.
<!-- /guide-only -->

Git worktrees let you work on multiple branches simultaneously without
switching. Each worktree is a separate directory pointing to the same repo.

Pick two features you want to build for your project. Create worktrees for each:

```
# Manual approach -- `-b` creates the branch alongside the worktree.
# Replace with your project and feature names:
! git worktree add -b feature/feature-a ../my-project-feature-a
! git worktree add -b feature/feature-b ../my-project-feature-b

# Or the shortcut -- launches Claude in a new worktree automatically:
claude -w
```

You can hook into worktree lifecycle with `WorktreeCreate` and `WorktreeRemove` hook events -- use them to automate setup (installing deps, copying env files) and teardown (cleaning up temp files).

Now you have three directories:
- Your main project directory -- main branch
- `../my-project-feature-a/` -- feature/feature-a branch
- `../my-project-feature-b/` -- feature/feature-b branch

**STOP -- What you just did:** You created two separate working directories from the same git repository. Each worktree is a full checkout of a different branch. They share the same git history, but files in one worktree do not affect the other. This is fundamentally different from `git stash` or `git checkout` -- you do not lose any work when switching between features because they live in separate directories.

Want to start building your first feature?

### 10.2 Feature 1 (Worktree 1)

In the first worktree, tell Claude to build your first feature. Describe the behavior you want:

```
Build [your feature A -- describe what it should do, how it should behave, what the inputs and outputs are]. [Add any constraints or design preferences.]
```

Discuss implementation details with Claude -- architecture, edge cases, how it integrates with existing code. These design decisions are yours to make.

### 10.3 Feature 2 (Worktree 2)

In the second worktree, describe your second feature to Claude:

```
Build [your feature B -- describe what it should do, how it should behave, what the inputs and outputs are]. [Add any constraints or design preferences.]
```

Work through the implementation. Both features are being developed independently in their own branches.

**Quick check before continuing:**
- [ ] First worktree directory exists with the feature branch checked out
- [ ] Second worktree directory exists with the feature branch checked out
- [ ] You can open files in each worktree independently without affecting the other
- [ ] Both features are defined and at least partially built

### 10.4 Run Parallel Claude Instances

Open separate terminals. Share a task list across both:

```
# Terminal 1:
cd ../my-project-feature-a && CLAUDE_CODE_TASK_LIST_ID=my-project-parallel claude

# Terminal 2:
cd ../my-project-feature-b && CLAUDE_CODE_TASK_LIST_ID=my-project-parallel claude
```

In Terminal 1, tell Claude to create tasks for feature A with dependencies between them. In Terminal 2, do the same for feature B.

Both sessions see all tasks. When one completes a task, the other is notified.

**STOP -- What you just did:** You ran two Claude Code instances simultaneously, each in its own worktree with its own branch, sharing a single task list via `CLAUDE_CODE_TASK_LIST_ID`. This is the most powerful development pattern in Claude Code: parallel feature development with coordination. Each instance works independently but can see the other's progress. In a real team workflow, you might have three or four worktrees running simultaneously -- one per feature.

### 10.5 Agent Teams

<!-- guide-only -->
**Why this step:** You just coordinated two Claude instances manually -- separate terminals, shared task list, you managing both. Agent teams automate this: Claude spawns teammates, assigns tasks, and they message each other directly. It is the difference between you being the coordinator and Claude being the coordinator.
<!-- /guide-only -->

Agent teams are an experimental feature. Enable them first:

```
! claude config set experiments.agentTeams true
```

Now tell Claude to create a team for a multi-agent task relevant to your project:

```
Create an agent team to [your task -- e.g., "refactor the authentication module", "audit the codebase for security issues", "add comprehensive error handling"]. One teammate [first role], another [second role], and a third [third role]. They should share findings and coordinate fixes.
```

Watch what happens: Claude creates a team, spawns teammates, assigns tasks, and the teammates message each other directly. You can observe the task list updating and messages flowing between agents. Use `Shift+Down` to navigate between teammates.

Agent Teams also works on Bedrock, Vertex, and Foundry API providers -- not just the direct Anthropic API.

**Subagents vs agent teams:** Subagents report back to your main conversation only -- they cannot talk to each other. Agent teams communicate peer-to-peer through a shared task list and direct messages. Use subagents for focused delegation ("scan these files"), agent teams for collaborative work ("three specialists coordinating a review").

**STOP -- What you just did:** You used agent teams to coordinate multiple Claude instances automatically. Instead of managing separate terminals and a shared task list yourself, Claude handled the orchestration -- creating teammates, assigning work, and letting them communicate. This is an experimental feature with limitations: no session resume for teams, no nested teams, and the coordination overhead means it is best suited for tasks with genuine interdependencies, not simple parallelism.

Ready to package everything into a reusable plugin?

### 10.6 Plugin Creation

<!-- guide-only -->
**Why this step:** Plugins let you package everything you have built -- skills, agents, hooks -- into a single distributable unit. Instead of every new project needing to recreate these tools from scratch, you bundle them once and reuse them anywhere. This is how you go from "project-specific tooling" to "reusable toolkit."
<!-- /guide-only -->

Package everything you have built into a reusable plugin. Think about what would be useful across projects of the same type:

```
Create a plugin called '[your-project-type]-plugin' (e.g., 'python-api-plugin', 'react-app-plugin', 'go-service-plugin') that packages the skills, agents, and hooks we have built. It needs a .claude-plugin/plugin.json manifest, the skills and agents directories at the root level, and the hooks extracted into a hooks/hooks.json file.
```

Claude will handle the file copying and manifest creation. Review the structure it creates against the expected layout:

The directory layout must be:

```
your-plugin/
  .claude-plugin/plugin.json    <-- manifest (required)
  skills/                       <-- at root, NOT inside .claude-plugin/
  agents/
  hooks/hooks.json
```

Plugins can also ship a `settings.json` for default configuration (hooks, permissions, etc.) and can be distributed via the npm registry for easy sharing.

### 10.7 Test the Plugin

Test your plugin locally:

```
claude --plugin-dir ./your-plugin
```

Verify everything works:
- Skills invoke correctly with the plugin namespace prefix
- Agents appear in `/agents`
- Hooks fire as expected

Note the namespacing: plugin skills are prefixed with the plugin name to
prevent conflicts.

**STOP -- What you just did:** You packaged your skills, agents, and hooks into a plugin and tested it with `--plugin-dir`. Notice the namespacing: when loaded as a plugin, your skills get a namespace prefix. This prevents conflicts when multiple plugins provide skills with similar names. The plugin directory structure (`.claude-plugin/plugin.json` at root, `skills/` and `agents/` alongside it) is the standard layout Claude Code expects.

**Quick check before continuing:**
- [ ] Your plugin directory has `.claude-plugin/plugin.json` with name and version
- [ ] `skills/` directory contains your skills (not nested inside `.claude-plugin/`)
- [ ] `agents/` directory contains your agents
- [ ] `--plugin-dir` loaded the plugin and skills work with the namespace prefix

### 10.8 Evaluation

<!-- guide-only -->
**Why this step:** Building skills and agents is only half the job -- you need to verify they work correctly across different inputs. Evaluation suites test your tools systematically: does a skill handle edge cases gracefully? Does an agent catch the issues it is supposed to catch? This is how you catch regressions and build confidence in your toolkit.
<!-- /guide-only -->

Ask Claude to help you build an evaluation suite for your toolkit. Describe the kinds of test cases you want:

```
Create an evaluation suite for our skills and agents. I want test cases for [your skills -- e.g., "the scaffolding skill (valid input, empty input, duplicate names)"], [your agents -- e.g., "code-review-agent (code with issues, clean code)", "test-coverage-agent (files with tests, files without tests)"]. Each test should define input, expected output, and scoring criteria. Write a script that runs everything and reports pass/fail.
```

Discuss with Claude which edge cases matter most to you and whether the scoring criteria make sense.

**STOP -- What you just did:** You wrote evaluation test specs for your skills and agents. Each test case defines an input, expected output, and scoring criteria. This is the same pattern used in professional software testing -- define expectations, run the tool, compare results. The evaluation script gives you a pass/fail report you can run any time you change a skill or agent.

Want to automate eval permissions with a PermissionRequest hook?

### 10.9 PermissionRequest Hooks for Eval Automation

During evaluation, auto-approve safe operations to avoid prompt fatigue. Tell Claude what you need:

```
Add a PermissionRequest hook to settings.local.json (not the committed settings file) that auto-approves Read, Grep, and Glob operations. Use a matcher of 'Read|Grep|Glob' and output hookSpecificOutput.decision.behavior 'allow'.
```

Keep this in `settings.local.json` (not committed) and use only during eval.

**STOP -- What you just did:** You created a PermissionRequest hook that auto-approves safe, read-only operations during evaluation runs. Without this, every `Read` and `Grep` call would prompt you for permission -- making automated evaluation tedious and slow. The key safety decision: this lives in `settings.local.json` (not committed to git) and only covers read-only tools. You would never auto-approve `Write` or `Bash` in production.

Shall we wrap up with continuous learning and a final review?

### 10.10 Continuous Learning

Reflect on the full project and update your configuration. Ask Claude to help you review what you have built:

```
Review our CLAUDE.md, rules, skills, agents, and hooks. What worked well? What should we refine? Update each one based on what we learned -- better descriptions, missing edge cases, patterns to avoid, hook interaction notes.
```

This is a conversation about your own tooling. Tell Claude what surprised you, what felt clunky, and what you would do differently. Then update the configuration together.

This is the continuous learning cycle: build, reflect, refine, repeat.

Claude also saves useful context automatically across sessions via **auto-memory**. Use `/memory` to review what has been saved and verify it matches your understanding. Auto-memory complements CLAUDE.md -- it captures things you might forget to write down.

**STOP -- What you just did:** You completed the full loop: build tools, use them, evaluate them, then refine them based on what you learned. This is the most important pattern in all of Claude Code -- your CLAUDE.md, rules, skills, agents, and hooks are living documents. Every project teaches you something, and updating your configuration captures that knowledge for future sessions. The best Claude Code users are the ones who continuously refine their setup.

### 10.11 Plugin Ecosystem Updates

The plugin system has expanded significantly. Explore these additions:

- **`source: 'settings'`** (v2.1.80) — declare plugin entries inline in settings.json
- **`${CLAUDE_PLUGIN_DATA}`** (v2.1.78) — persistent state directory that survives plugin updates
- **`/reload-plugins`** (v2.1.69) — activate plugin changes without restarting
- **`claude plugin validate`** (v2.1.77) — validates skill, agent, and command frontmatter plus hooks.json
- **`git-subdir`** (v2.1.69) — plugin source type pointing to a subdirectory within a git repo
- **`pluginTrustMessage`** (v2.1.69) — managed setting for org-specific plugin trust context
- **`CLAUDE_CODE_PLUGIN_SEED_DIR`** (v2.1.79) — now supports multiple directories

You've got this — try `claude plugin validate` on your project's plugin configuration.

### 10.12 Worktrees, IDE & Remote Control

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

None of this requires action for your project. Surface-level awareness so when you hit a weird plugin state, you know where to look.

### 10.16 New CLI subcommands: `claude ultrareview` and `claude plugin prune` (v2.1.120, v2.1.121)

Two non-interactive CLI subcommands worth knowing for scripted workflows.

**`claude ultrareview [target]`** (v2.1.120). Runs `/ultrareview` from the shell -- useful in CI, pre-merge scripts, or wrapper tools. `[target]` defaults to the current branch's diff against the default branch; pass a PR number (`1234`) or a branch (`origin/main`) to scope the review elsewhere. `--json` prints the raw findings payload for downstream tooling. Exit codes: `0` = completed, `1` = failed or timed out, `130` = Ctrl-C.

**`claude plugin prune`** (v2.1.121). Removes auto-installed plugin dependencies that no other plugin requires -- useful after uninstalling a plugin or refactoring your plugin set. Pair with `--dry-run` first to preview, then re-run to apply. The companion `plugin uninstall <name> --prune` cascades cleanup in one command instead of two.

Skim the changelog for both -- you'll find them when you need them.

### Checkpoint

You made it. Every major Claude Code feature, applied to your own project.

- [ ] Created git worktrees for parallel feature development
- [ ] Feature A works in its own worktree and branch
- [ ] Feature B works in its own worktree and branch
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
- [ ] Tested plugin `userConfig` with a sensitive field
- [ ] Reviewed worktree and IDE/Remote Control additions

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

**Run your tests frequently.** After every change, run your project's test
suite to catch regressions early. Use `Ctrl+B` to background long test runs
and keep working.

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

Take a second to appreciate what you just did. You took your own project -- not a tutorial, not a toy example -- and layered every major Claude Code feature on top of it: CLAUDE.md, plan mode, rules, skills, hooks, MCP servers, guard rails, subagents, tasks, worktrees, plugins, and evaluation. You learned these tools by applying them to real problems in a codebase you care about.

You are not a beginner anymore. You know how to make Claude Code work for you.

Here are paths forward:

- **Keep building.** You have the full toolkit now. Use it on your project every day and refine your setup as you learn what works.
- **Share your plugin.** If your plugin is useful for your project type, distribute it to your team or the community.
- **Try a tutorial project.** Canvas, Forge, Nexus, and Sentinel cover the same features through guided, domain-specific builds -- and you will move through them fast now that you know the concepts.
- **Build something new.** Take a project idea you have been putting off and build it with Claude Code from scratch. You have the full toolkit now -- go use it.
- **Come back for updates.** This curriculum is actively maintained -- `git pull` to get updated modules, new feature coverage, and refined exercises. Check the [changelog](../../../CHANGELOG.md) to see what's new.
