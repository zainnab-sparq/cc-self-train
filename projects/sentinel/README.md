# Sentinel -- Code Analyzer & Test Generator

You're going to build a tool that makes all your other code better — a code analysis engine that scans source files for issues, generates tests, tracks coverage, and produces quality reports. Along the way, you'll master every major Claude Code feature by putting each one to work on a real problem.

**Level:** Intermediate-Advanced
**Time:** 3-5 sessions (8-15 hours)
**Prerequisites:** Comfortable with at least one programming language, familiar with git basics. Prior Claude Code experience (e.g., Projects 1-3 from this curriculum) is helpful but not required.

## What You Will Build

Sentinel is a **code quality meta-tool** -- a tool that improves other code. When finished, it will:

- Recursively scan source files in any project directory
- Apply configurable analysis rules (complexity, naming, missing docs, unused imports)
- Report issues with severity, file location, and actionable messages
- Generate test cases for source files that lack coverage
- Track coverage over time and store historical data in SQLite
- Output reports in text, JSON, and HTML formats
- Expose all functionality through a CLI: `sentinel scan`, `sentinel rules`, `sentinel report`, `sentinel coverage`

## What You Will Learn (Claude Code Features)

| Module | CC Features |
|--------|------------|
| 1. Setup & First Contact | CLAUDE.md, /init, /memory, interactive mode, keyboard shortcuts |
| 2. Blueprint & Build | Plan mode, git integration, basic prompting |
| 3. Rules, Memory & Context | .claude/rules/, CLAUDE.local.md, @imports, /context, /compact, /stats, /cost |
| 4. Skills & Commands | SKILL.md, frontmatter, custom slash commands, hot-reload, disable-model-invocation |
| 5. Hooks | SessionStart, PostToolUse, Stop hooks, matchers, settings.json |
| 6. MCP Servers | MCP servers, .mcp.json, scopes, skills+MCP, claude mcp add |
| 7. Guard Rails | PreToolUse, hook decision control, permissionDecision, additionalContext, updatedInput |
| 8. Subagents | .claude/agents/, subagent frontmatter, chaining, parallel, background |
| 9. Tasks & TDD | Tasks, dependencies, cross-session, TDD loops, SubagentStop |
| 10. Parallel Dev, Plugins & Eval | Worktrees, plugins, eval, PermissionRequest hooks, continuous learning |

## What You'll Build — Milestones

Here's what your project looks like at key milestones:

### After Module 3 — Code Scanner

A CLI that recursively scans source files and reports issues — complexity warnings, naming violations, missing docs. `sentinel scan` and `sentinel rules list` work from your terminal.

```
sentinel/
├── src/
│   ├── main.*              # CLI entry point
│   ├── scanner.*           # File discovery and parsing
│   ├── rules/              # Configurable analysis rules
│   │   ├── complexity.*
│   │   ├── naming.*
│   │   └── docs.*
│   └── reporter.*          # Text/JSON output
├── .claude/rules/          # Your conventions
├── CLAUDE.md
└── CLAUDE.local.md
```

### After Module 6 — Test Generator and Coverage Tracker

Generates test stubs for uncovered files, tracks coverage over time in SQLite, and produces HTML quality reports. MCP integration lets Claude query your project's health.

```
sentinel/
├── src/
│   ├── generator.*         # Test stub generation
│   ├── coverage.*          # Coverage tracking
│   ├── reporter.*          # Text, JSON, and HTML reports
│   └── ...
├── data/
│   └── coverage.db         # Historical coverage data
├── .claude/
│   ├── skills/             # Custom commands
│   ├── settings.json       # Automation hooks
│   └── rules/
└── .mcp.json               # MCP server config
```

### After Module 10 — Full Quality Platform

A comprehensive code quality tool with custom rule authoring, cross-project analysis, trend dashboards, and CI integration. Subagents run parallel analyses, tasks track quality improvements, and a publishable plugin shares your rules with the community.

---

## Set Up Your Dev Environment

Before starting Module 1, make sure your language toolchain is ready. Sentinel works in **any language** -- pick whichever you are most comfortable with.

| Language | Requirements | Quick check |
|----------|-------------|-------------|
| **Python** | Python 3.10+, pip/conda/uv | `python --version` |
| **TypeScript** | Node.js 18+, npm/pnpm/yarn | `node --version` |
| **Go** | Go 1.21+ | `go version` |
| **Rust** | Rust 1.70+ via rustup | `rustc --version` |
| **Docker** | Optional -- any project works in a container | `docker --version` |

Install links: [Python](https://python.org) | [Node.js](https://nodejs.org) | [Go](https://go.dev/dl/) | [Rust](https://rustup.rs)

### Environment Isolation

**Environment isolation:** If you chose an environment during `/start` (venv, conda, or Docker), it's already set up in your project directory. If you skipped it and want to add one later, ask Claude: "Help me set up [venv/conda/Docker] for this project."

### Git

```
git --version
```

If missing: [git-scm.com/downloads](https://git-scm.com/downloads)

### Coverage tools (needed in Module 9)

| Language | Coverage Tool |
|----------|--------------|
| Python | `coverage` or `pytest-cov` |
| TypeScript | `c8`, `istanbul`, or built-in via `vitest --coverage` |
| Go | Built-in: `go test -cover` |
| Rust | `cargo-tarpaulin` or `cargo-llvm-cov` |

### Claude Code

```
npm install -g @anthropic-ai/claude-code
claude --version
```

You need an [Anthropic API key](https://console.anthropic.com/) or a Claude subscription (Pro, Max, or Team).

---

## Modules

| # | Module | Focus | CC Features |
|---|--------|-------|-------------|
| 1 | [Setup & First Contact](modules/01-setup.md) | Project setup, first conversation | CLAUDE.md, /init, /memory, interactive mode, keyboard shortcuts |
| 2 | [Blueprint & Build](modules/02-blueprint.md) | Architecture design, core implementation | Plan mode, git integration, basic prompting |
| 3 | [Rules, Memory & Context](modules/03-rules-memory-context.md) | Persistent instructions, context management | .claude/rules/, CLAUDE.local.md, @imports, /context, /compact, /stats, /cost |
| 4 | [Skills & Commands](modules/04-skills-commands.md) | Custom slash commands, reusable workflows | SKILL.md, frontmatter, hot-reload, argument substitution, disable-model-invocation |
| 5 | [Hooks](modules/05-hooks.md) | Automated scripts at key moments | SessionStart, PostToolUse, Stop hooks, matchers, settings.json |
| 6 | [MCP Servers](modules/06-mcp-servers.md) | External tool integration, database access | MCP servers, .mcp.json, scopes, skills+MCP, claude mcp add |
| 7 | [Guard Rails](modules/07-guard-rails.md) | Preventive hooks, input modification | PreToolUse, permissionDecision, additionalContext, updatedInput |
| 8 | [Subagents](modules/08-subagents.md) | Specialized AI agents, delegation | .claude/agents/, subagent frontmatter, chaining, parallel, background |
| 9 | [Tasks & TDD](modules/09-tasks-tdd.md) | Multi-step work, test-driven development | Tasks, dependencies, cross-session, TDD loops, SubagentStop |
| 10 | [Parallel Dev, Plugins & Eval](modules/10-parallel-plugins-eval.md) | Scaling workflow, distribution, evaluation | Worktrees, plugins, eval, PermissionRequest hooks, continuous learning |

---

## Final Verification Checklist

Review this checklist to confirm you have experienced every major Claude Code feature:

**Foundations (Modules 1-2)**
- [ ] Created CLAUDE.md with /init
- [ ] Used /memory to edit project memory
- [ ] Used plan mode to design before building
- [ ] Used git integration (branch, commit, merge) through Claude
- [ ] Tried all keyboard shortcuts from the Module 1 table

**Context Management (Module 3)**
- [ ] Created path-scoped rules in .claude/rules/
- [ ] Used CLAUDE.local.md for personal preferences
- [ ] Used @imports in CLAUDE.md
- [ ] Ran /context, /compact, and /stats or /cost

**Skills & Commands (Module 4)**
- [ ] Created at least 3 custom skills with SKILL.md
- [ ] Used argument substitution ($ARGUMENTS, $0, $1)
- [ ] Used disable-model-invocation for manual-only skills
- [ ] Used context: fork to run a skill in a subagent
- [ ] Verified hot-reload by editing a skill and re-running it

**Hooks (Modules 5, 7)**
- [ ] Configured SessionStart hook
- [ ] Configured PostToolUse hook with matcher
- [ ] Configured Stop hook (prompt-based)
- [ ] Used PreToolUse with permissionDecision (deny)
- [ ] Used PreToolUse with additionalContext
- [ ] Used PreToolUse with updatedInput
- [ ] Configured SubagentStop hook
- [ ] Configured PermissionRequest hook

**MCP (Module 6)**
- [ ] Added at least one MCP server with claude mcp add
- [ ] Used /mcp to check server status
- [ ] Created .mcp.json for project-scoped MCP config
- [ ] Created a skill that calls MCP tools

**Subagents (Module 8)**
- [ ] Created at least 3 custom subagents in .claude/agents/
- [ ] Chained subagents (output of one feeds into another)
- [ ] Ran subagents in parallel or background
- [ ] Resumed a completed subagent

**Tasks & TDD (Module 9)**
- [ ] Created tasks with dependencies
- [ ] Practiced strict TDD (red-green-refactor)
- [ ] Used cross-session task sharing with CLAUDE_CODE_TASK_LIST_ID
- [ ] Toggled task list with Ctrl+T

**Advanced (Module 10)**
- [ ] Used git worktrees with multiple Claude Code instances
- [ ] Built a plugin with .claude-plugin/plugin.json
- [ ] Created an evaluation framework with scoring
- [ ] Set up a continuous learning feedback loop

---

## Tips

- **Context is your most valuable resource.** Use `/compact` aggressively, use subagents for verbose operations, and keep CLAUDE.md focused.
- **Start with plan mode.** Press Shift+Tab before implementing non-trivial features. Think before you build.
- **Test early, test often.** The build-test-fix-commit cycle gives Claude concrete feedback. Always run tests before committing.
- **Use subagents for exploration.** Delegate searches and analysis to subagents to keep your main conversation clean.
- **Name your sessions.** Use `/rename sentinel-coverage-work` for easy `/resume` later.
- **Hooks time out at 60 seconds** by default. Set a custom `timeout` in hook config if you need more.
- **MCP tool names** follow the pattern `mcp__<server>__<tool>`. Use this in hook matchers.
- **Worktrees share git history.** Changes committed in one worktree are visible in all others.

**Reference docs** in `cc-self-train/context/` for deep dives:

| Topic | File |
|-------|------|
| CLAUDE.md / memory | `context/claudemd.txt` |
| Skills | `context/skillsmd.txt` |
| Hooks | `context/hooks.txt` |
| Hook configuration | `context/configure-hooks.txt` |
| Subagents | `context/subagents.txt` |
| Tasks | `context/tasks.txt` |
| MCP servers | `context/mcp.txt` |
| Skills + MCP | `context/skills-plus-mcp.txt` |
| Plugins | `context/plugins.txt` |
| Interactive mode | `context/interactive-mode.txt` |
| Workflow patterns | `context/boris-workflow.txt` |

---

## What's Next?

Take a second to appreciate what you just did. You built a real code analysis engine from scratch — one that scans files, enforces rules, generates tests, tracks coverage, and produces reports — and along the way, you mastered every major Claude Code feature: CLAUDE.md, plan mode, rules, skills, hooks, MCP servers, guard rails, subagents, tasks, worktrees, plugins, and evaluation. That's not a walkthrough you followed. That's a real tool you built.

You're not a beginner anymore. You know how to make Claude Code work for you.

Here are paths forward:

**Extend Sentinel.** Add support for more languages, more rules, a web dashboard, CI integration, or GitHub PR comments via MCP.

**Try another project.** [Forge](../forge/) if you want to build a personal dev toolkit, or [Nexus](../nexus/) if you want to build a local API gateway. Both cover the same features through different domains — and you'll move through them faster this time.

**Build your own tools.** Take the patterns you learned — skills, subagents, hooks, MCP, tasks — and apply them to your real projects. Start with a CLAUDE.md and a few rules, then add skills and hooks as your workflow matures.

**Share your plugin.** If your quality-tools plugin is useful, publish it for others.

**Contribute back.** If you found bugs, had ideas for improvements, or wrote useful patterns during this project, contribute them to the cc-self-train repository. Open an issue or PR.
