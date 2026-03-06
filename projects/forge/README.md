# Forge -- Personal Dev Toolkit

You're going to build a tool you'll actually use every day — a personal CLI for notes, snippets, bookmarks, and templates that grows into a searchable, pluggable knowledge base with an API layer. Along the way, you'll pick up every major Claude Code feature by putting it to work.

**Who this is for:** Tool builders who want something they will actually use
after the course is over. If you enjoy building your own productivity tools,
this is your project.

**What you will learn:** All 10 modules cover the full Claude Code feature set,
from CLAUDE.md and plan mode through skills, hooks, MCP servers, subagents,
tasks, plugins, and parallel development.

**Time estimate:** 3-5 focused sessions (roughly 10-15 hours total).

**Prerequisites:** Familiarity with the terminal, git basics, and one
programming language of your choice.

---

## What You'll Build

By the end of all 10 modules, you'll have a CLI tool you actually use every day AND deep expertise in every Claude Code feature. Here's what your project looks like at key milestones:

### After Module 3 — A Working CLI

A command-line tool that stores and retrieves notes and snippets. `forge add`, `forge list`, `forge search` work from your terminal. Your Claude Code environment has custom rules and persistent memory.

```
forge-toolkit/
├── src/                    # CLI source code
│   ├── main.*              # Entry point and command router
│   ├── commands/           # add, list, search, delete
│   └── storage.*           # File/JSON-based data store
├── data/                   # Where notes and snippets live
├── .claude/rules/          # Your coding conventions
├── CLAUDE.md
└── CLAUDE.local.md
```

### After Module 6 — Searchable Knowledge Base

Bookmarks and templates join notes and snippets. Full-text search, tags, and categories. An MCP server exposes your data to Claude directly.

```
forge-toolkit/
├── src/
│   ├── commands/           # Expanded command set
│   ├── storage.*           # Upgraded storage layer
│   └── search.*            # Full-text search engine
├── data/
├── .claude/
│   ├── skills/             # Custom commands (e.g., /forge-test)
│   ├── settings.json       # Hooks for auto-lint, auto-test
│   └── rules/
└── .mcp.json               # MCP server for Claude integration
```

### After Module 10 — Pluggable Toolkit

A full-featured personal dev toolkit with an API layer, plugin system, import/export, and comprehensive test coverage. Your Claude Code setup includes subagents, tasks, and a publishable plugin.

---

## Set Up Your Dev Environment

Before you begin, make sure your development tools are ready. You can use
**any language** for this project. Below are setup instructions for common
choices.

### Install Claude Code

```
npm install -g @anthropic-ai/claude-code
claude --version
```

You need an [Anthropic API key](https://console.anthropic.com/) or a Max
subscription.

### Install Git

```
git --version
```

If you do not have it: [git-scm.com/downloads](https://git-scm.com/downloads)

### Language Toolchains

Pick your language and verify the toolchain:

| Language | Requirements | Verify |
|----------|-------------|--------|
| **Python** | Python 3.10+, a package manager (venv, uv, conda, pip) | `python --version` |
| **TypeScript/Node** | Node.js 18+, npm/pnpm/yarn | `node --version && npm --version` |
| **Go** | Go 1.21+ | `go version` |
| **Rust** | Rust via rustup, cargo | `rustc --version && cargo --version` |
| **Other** | Whatever your language needs -- Claude can help you set it up | -- |

### Initialize Your Language Project

Create the project directory and set up your language toolchain. Examples:

| Language | Init Commands |
|----------|--------------|
| **Python** | `mkdir -p workspace/forge-toolkit && cd workspace/forge-toolkit && python -m venv .venv` then activate the venv |
| **TypeScript** | `mkdir -p workspace/forge-toolkit && cd workspace/forge-toolkit && npm init -y && npm i typescript @types/node -D` |
| **Go** | `mkdir -p workspace/forge-toolkit && cd workspace/forge-toolkit && go mod init forge-toolkit` |
| **Rust** | `cargo new workspace/forge-toolkit && cd workspace/forge-toolkit` |
| **Docker** | Any project can be done in a container -- ask Claude to generate a Dockerfile |

### Environment Isolation

**Environment isolation:** If you chose an environment during `/start` (venv, conda, or Docker), it's already set up in your project directory. If you skipped it and want to add one later, ask Claude: "Help me set up [venv/conda/Docker] for this project."

### Verify Everything

Run these checks before continuing:

- [ ] `claude --version` prints a version number
- [ ] `git --version` prints a version number
- [ ] Your language toolchain runs (compiler/interpreter version check passes)
- [ ] You can create and enter the `workspace/forge-toolkit` directory

---

## Modules

| # | Module | Focus | CC Features |
|---|--------|-------|-------------|
| 1 | [Setup & First Contact](modules/01-setup.md) | Project setup, first commit | CLAUDE.md, /init, /memory, keyboard shortcuts |
| 2 | [Blueprint & Build](modules/02-blueprint.md) | Architecture design, core CLI | Plan mode, git integration, basic prompting |
| 3 | [Rules, Memory & Context](modules/03-rules-memory-context.md) | Conventions, context management | .claude/rules/, CLAUDE.local.md, @imports, /context, /compact, /stats, /cost |
| 4 | [Skills & Commands](modules/04-skills-commands.md) | Custom slash commands | SKILL.md, frontmatter, hot-reload, $ARGUMENTS, disable-model-invocation |
| 5 | [Hooks](modules/05-hooks.md) | Lifecycle automation | SessionStart, PostToolUse, Stop hooks, matchers, settings.json |
| 6 | [MCP Servers](modules/06-mcp-servers.md) | External data sources | MCP servers, .mcp.json, scopes, skills+MCP, claude mcp add |
| 7 | [Guard Rails](modules/07-guard-rails.md) | Safety and validation | PreToolUse, permissionDecision, additionalContext, updatedInput, prompt hooks |
| 8 | [Subagents](modules/08-subagents.md) | Specialized AI assistants | .claude/agents/, frontmatter, chaining, parallel, background |
| 9 | [Tasks & TDD](modules/09-tasks-tdd.md) | Task pipelines, test-driven dev | Tasks, dependencies, cross-session persistence, TDD loops, SubagentStop |
| 10 | [Parallel Dev, Plugins & Eval](modules/10-parallel-plugins-eval.md) | Advanced workflows | Git worktrees, plugins, evaluation, PermissionRequest hooks, continuous learning |
