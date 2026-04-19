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

In this final module you learn advanced patterns for scaling your workflow.

> **New terms this module uses:**
> - **Worktree** -- a Git feature that lets you check out multiple branches in separate directories at the same time. Great for running parallel experiments without stashing and switching.
> - **Plugin (Claude Code)** -- a bundled set of extensions (skills, hooks, agents, MCP servers) that others can install in their projects. Installed with `/plugin`.
> - **Evaluation framework** -- a setup for running your agents/skills against a fixed set of inputs to measure quality over time. Like unit tests, but for AI behavior.
>
> See the [glossary](../../../GLOSSARY.md) for related terms.

### 10.1 Git Worktrees

**Why this step:** Git worktrees let you have multiple working copies of the same repo *without cloning it again*. Each worktree shares the same git history but has its own working directory and branch. Combined with Claude Code, this means you can have two or three Claude instances building different features in parallel on the same project -- true concurrent development.

Git worktrees let you have multiple working copies of the same repo. Each worktree can have its own Claude Code session working on a different feature simultaneously. Use the manual approach or the `--worktree` (`-w`) shortcut:

```
# Manual approach -- `-b` creates the branch at the same time as the worktree:
! git worktree add -b feature/coverage-html ../sentinel-coverage-html
! git worktree add -b feature/rule-import ../sentinel-rule-import

# Or the shortcut -- launches Claude in a new worktree automatically:
claude -w
```

Hook into `WorktreeCreate` and `WorktreeRemove` events to automate setup and teardown (installing deps, copying env files, cleaning up).

Now you have three working copies:
- `sentinel/` -- main development
- `sentinel-coverage-html/` -- HTML coverage reports
- `sentinel-rule-import/` -- importing rules from external files

**STOP -- What you just did:** You created two git worktrees -- separate working directories that share the same repository. Each one is on its own feature branch. This is the infrastructure for parallel development: you now have three separate directories where Claude Code sessions can work independently without merge conflicts until you are ready to combine the work.

Ready to spin up parallel Claude Code sessions?

### 10.2 Multiple Claude Code Instances With Shared Tasks

**Why this step:** This is where everything comes together -- worktrees for isolation, shared task lists for coordination, and multiple Claude instances for speed. Each instance picks up a different task and works on it independently. This is how you multiply your throughput on large features.

Open separate terminal windows and start Claude Code in each worktree:

Terminal 1:
```
cd sentinel-coverage-html
CLAUDE_CODE_TASK_LIST_ID=sentinel-parallel claude
```

Terminal 2:
```
cd sentinel-rule-import
CLAUDE_CODE_TASK_LIST_ID=sentinel-parallel claude
```

Create tasks in one session. Describe two independent features that can be built in parallel:

Try something like:

```
Create two independent tasks: 1) Add HTML coverage report with charts and drill-down, 2) Add rule import from YAML/JSON files. No dependencies between them.
```

Each session picks up a different task. They work in parallel on separate branches, sharing task status.

**STOP -- What you just did:** You ran two Claude Code instances simultaneously, each in its own worktree with its own branch, sharing a single task list. Session 1 works on HTML coverage reports while Session 2 works on rule import -- neither blocks the other. When both are done, you merge their branches. This is the most advanced Claude Code workflow: parallel, coordinated, independent development.

**Quick check before continuing:**
- [ ] You have two (or more) worktrees created from the sentinel repo
- [ ] Each worktree has its own Claude Code session running
- [ ] Both sessions share the same task list via CLAUDE_CODE_TASK_LIST_ID

### 10.3 Agent Teams

Agent teams are experimental. Enable them:

```
! claude config set experiments.agentTeams true
```

Tell Claude to create a team:

Try something like:

```
Create an agent team to harden Sentinel. One teammate adds new analysis rules for common vulnerabilities, another writes test fixtures with planted bugs, and a third improves the HTML report output. They share findings and coordinate.
```

Observe: Claude spawns teammates, assigns tasks, and they message each other directly. This automates the manual `CLAUDE_CODE_TASK_LIST_ID` coordination from Step 2. Use `Shift+Down` to navigate between teammates.

Agent Teams also works on Bedrock, Vertex, and Foundry API providers -- not just the direct Anthropic API.

**Subagents vs agent teams:** Subagents report back to you only. Agent teams communicate peer-to-peer through shared tasks and direct messages. Use subagents for focused delegation, agent teams for collaborative parallel work.

**STOP -- What you just did:** You used agent teams to coordinate multiple Claude instances automatically. Instead of managing separate terminals yourself, Claude handled the orchestration. This is experimental: no session resume for teams, no nested teams, and best suited for tasks with genuine interdependencies rather than simple parallelism.

### 10.4 Build a Plugin

Ask Claude to bundle everything you have built into a distributable plugin. Describe what you want packaged -- skills, agents, hooks, and MCP config -- and the directory structure.

Try something like:

```
Create a plugin called 'quality-tools' that packages all our skills, agents, hooks, and the SQLite MCP config into a single distributable directory. It needs a manifest at .claude-plugin/plugin.json with name, description, and version.
```

Claude will create the plugin structure. Plugins can also ship a `settings.json` for default configuration and can be distributed via the npm registry.

```
quality-tools/
  .claude-plugin/plugin.json    # manifest (name, description, version)
  skills/                       # all SKILL.md dirs
  agents/                       # all agent .md files
  hooks/hooks.json              # guard rail hooks
  .mcp.json                     # SQLite MCP server
```

**Why this step:** Plugins are how you distribute Claude Code customizations. Everything you built in Modules 4-8 -- skills, agents, hooks, MCP configs -- gets bundled into a single directory that anyone can load with `--plugin-dir`. This is how you share your work with teammates or the community.

### 10.5 Test the Plugin

```
claude --plugin-dir ./quality-tools
```

Verify that skills are available under the `quality-tools:` namespace:

```
/quality-tools:analyze src/
```

**STOP -- What you just did:** You bundled all of Sentinel's Claude Code customizations into a portable plugin and loaded it in a fresh Claude instance. Notice the namespace prefix (`quality-tools:analyze` instead of just `analyze`) -- this prevents naming conflicts when multiple plugins are loaded. Your skills, agents, hooks, and MCP configs all travel together as a single distributable unit.

Want to build an evaluation framework for Sentinel?

### 10.6 Build an Evaluation Framework

**Why this step:** Evaluation measures how well Sentinel actually works. Without it, you are guessing whether your analyzer catches real issues or produces false positives. By creating fixtures with planted bugs and comparing Sentinel's output to expected results, you get concrete accuracy metrics. This is the same approach used to evaluate AI models -- ground truth comparison.

Ask Claude to build an evaluation framework for Sentinel. Describe what you need -- fixture files with planted bugs, expected outputs, a runner that scores accuracy, and a summary report.

Try something like:

```
Build an evaluation framework for Sentinel. I need fixture source files with planted bugs in eval/fixtures/, expected analysis output in eval/expected/, and a runner script that compares Sentinel's output to the expected results and scores true positive rate, false positive rate, false negative rate, and severity accuracy. Run the eval and show me the results.
```

Claude might ask about how many fixtures you want or what kinds of bugs to plant. Tell it to start with a few representative examples and you will add more over time.

**STOP -- What you just did:** You built a scoring framework that measures Sentinel's accuracy with real metrics: true positive rate (how many real issues it catches), false positive rate (how often it flags clean code), false negative rate (how many real issues it misses), and severity accuracy. These numbers tell you exactly where Sentinel needs improvement. Every time you add a new rule or change the analyzer, re-running the eval tells you whether you made things better or worse.

Shall we set up PermissionRequest hooks for auto-approvals?

### 10.7 PermissionRequest Hooks

Ask Claude to create a PermissionRequest hook that auto-approves safe operations but still prompts for risky ones.

Try something like:

```
Add a PermissionRequest hook that auto-approves running tests and sentinel scan, but still prompts me for writes to config files, git push, and destructive commands. Create the script at .claude/scripts/auto-approve.sh.
```

The hook matches on "Bash" and runs your approval script. The script outputs JSON with `{"hookSpecificOutput": {"hookEventName": "PermissionRequest", "decision": {"behavior": "allow"}}}` for safe commands.

**STOP -- What you just did:** You built a programmable permission system. Instead of clicking "approve" every time Claude wants to run tests or scan code, the PermissionRequest hook auto-approves safe operations while still prompting for risky ones like git push or config changes. This dramatically speeds up your workflow -- Claude can run tests dozens of times without you clicking "yes" each time, but it still asks before doing anything destructive.

**Quick check before continuing:**
- [ ] Your evaluation framework has fixture files with planted bugs
- [ ] Running the eval produces accuracy metrics (TP rate, FP rate, etc.)
- [ ] The PermissionRequest hook auto-approves test runs and sentinel scans
- [ ] The PermissionRequest hook still prompts for writes to config files and git push

### 10.8 Continuous Learning

**Why this step:** This is the capstone pattern -- a feedback loop where Sentinel improves itself over time. Misclassifications from the eval are logged, loaded into Claude's context at session start, and used to guide future fixes. After each fix, the eval runs again to confirm the fix worked and check for regressions. This is how production ML systems improve, and you are applying the same principle to your code analyzer.

Ask Claude to build a feedback loop where eval results drive improvements. Describe the cycle you want -- log misclassifications, load them at session start, fix them, re-run eval, and record lessons learned.

Try something like:

```
Create a continuous learning loop: log false positives and negatives from the eval to eval/learning/misclassifications.jsonl. Add a SessionStart hook that loads recent misclassifications into context. After fixing one, re-run the eval to confirm and check for regressions. Then update CLAUDE.md with the lesson learned.
```

**STOP -- What you just did:** You closed the loop: eval finds problems, you fix them, eval confirms the fix, and CLAUDE.md records the lesson. This means every future session starts with the accumulated knowledge of past mistakes. Over time, Sentinel gets more accurate and Claude gets better at working with it. This continuous learning pattern is the most sophisticated workflow in the entire curriculum -- it combines hooks (SessionStart), memory (CLAUDE.md), evaluation (scoring framework), and iterative improvement into a single self-reinforcing system.

Claude also saves useful context automatically across sessions via **auto-memory**. Use `/memory` to review what has been captured. Auto-memory complements CLAUDE.md by catching things you might forget to write down.

Ready to clean up the worktrees and wrap up?

### 10.9 Clean Up Worktrees

After finishing parallel work:

```
! git worktree remove ../sentinel-coverage-html
! git worktree remove ../sentinel-rule-import
```

Merge the feature branches back to main.

### 10.10 Plugin Ecosystem Updates

The plugin system has expanded significantly. Explore these additions:

- **`source: 'settings'`** (v2.1.80) — declare plugin entries inline in settings.json
- **`${CLAUDE_PLUGIN_DATA}`** (v2.1.78) — persistent state directory that survives plugin updates
- **`/reload-plugins`** (v2.1.69) — activate plugin changes without restarting
- **`claude plugin validate`** (v2.1.77) — validates skill, agent, and command frontmatter plus hooks.json
- **`git-subdir`** (v2.1.69) — plugin source type pointing to a subdirectory within a git repo
- **`pluginTrustMessage`** (v2.1.69) — managed setting for org-specific plugin trust context
- **`CLAUDE_CODE_PLUGIN_SEED_DIR`** (v2.1.79) — now supports multiple directories

You've got this — try `claude plugin validate` on your project's plugin configuration.

### 10.11 Worktrees, IDE & Remote Control

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

### Checkpoint

You made it. A working code analyzer with plugins, evaluation, and a continuous learning loop -- built using every major Claude Code feature.

- [ ] You created and used git worktrees for parallel development
- [ ] You ran multiple Claude Code instances sharing a task list
- [ ] (Experimental) Created an agent team with 2-3 teammates
- [ ] Teammates communicated and coordinated through shared tasks
- [ ] `quality-tools` plugin is built with skills, agents, hooks, and MCP config
- [ ] Plugin works when loaded with `--plugin-dir`
- [ ] Evaluation framework exists with fixtures, expected output, and scoring
- [ ] PermissionRequest hook auto-approves safe operations
- [ ] Continuous learning loop logs misclassifications and feeds them back
- [ ] Explored plugin ecosystem updates (validate, reload, settings source)
- [ ] Reviewed worktree and IDE/Remote Control additions
- [ ] Tested plugin `userConfig` with a sensitive field

---

## What Is Next

Take a second to appreciate what you just did. You built a code analyzer and test generator from scratch — static analysis rules, automatic test generation, coverage tracking, a quality dashboard — and along the way, you mastered every major Claude Code feature: CLAUDE.md, plan mode, rules, skills, hooks, MCP servers, guard rails, subagents, tasks, worktrees, plugins, and evaluation. That's not a tutorial you followed. That's a real tool you built.

You're not a beginner anymore. You know how to make Claude Code work for you.

Here are paths forward:

- **Keep extending Sentinel.** Add more analysis rules, support additional languages, build IDE integration, add trend tracking to the quality dashboard. The analyzer is yours now.
- **Try another project.** Canvas, Forge, and Nexus cover the same features through different domains — and you'll move through them faster this time.
- **Share your plugin.** If your quality-tools plugin is useful, distribute it to your team or the community.
- **Build something new.** Take a project idea you've been putting off and build it with Claude Code. You have the full toolkit now — go use it.
- **Come back for updates.** This curriculum is actively maintained — `git pull` to get updated modules, new feature coverage, and refined exercises. Check the [changelog](../../../CHANGELOG.md) to see what's new.
