# Nexus -- Local API Gateway

You're going to build the thing that sits between services and makes them work together — a real API gateway with routing, rate limiting, SQLite caching, and health checks. Along the way, you'll learn every major Claude Code feature by using it to build something most developers never look under the hood of.

**Who this is for:** Backend developers and service builders who want hands-on practice with every major Claude Code feature.

**What you will build:** A local API gateway that accepts HTTP requests, matches them against a route registry, forwards them to upstream services, applies rate limiting, caches responses in SQLite, and exposes health check endpoints. By the end, you will have a CLI tool (`nexus start`, `nexus routes list`, `nexus health`) and a deeply customized Claude Code environment with hooks, skills, subagents, tasks, and plugins.

**What you will learn:** All 10 modules cover the complete Claude Code feature set:

| Module | CC Features | Project Feature |
|--------|------------|-----------------|
| 1 | CLAUDE.md, /init, /memory, keyboard shortcuts | Project setup |
| 2 | Plan mode, git integration, prompting | Core gateway + CLI |
| 3 | .claude/rules/, @imports, /context, /compact, /stats, /cost | Rate limiting |
| 4 | Skills, SKILL.md, frontmatter, custom commands | Route management skills |
| 5 | Hooks, SessionStart, PostToolUse, Stop | Gateway automation |
| 6 | MCP servers, .mcp.json, scopes | SQLite caching layer |
| 7 | PreToolUse, decision control, prompt-based hooks | Guard rails |
| 8 | Subagents, .claude/agents/, chaining | Specialized agents |
| 9 | Tasks, dependencies, TDD, SubagentStop | Middleware system |
| 10 | Worktrees, plugins, evaluation | Parallel dev + packaging |

**Prerequisites:** None — all 3 projects are independent. Pick based on what sounds fun to build.

## What You'll Build

By the end of all 10 modules, you'll have a fully functional local API gateway AND deep expertise in every Claude Code feature. Here's what your project looks like at key milestones:

### After Module 3 — Routing and Rate Limiting

An HTTP server that accepts requests, matches routes from a registry, and applies rate limiting. `nexus start` and `nexus routes list` work from your terminal.

```
nexus-gateway/
├── src/
│   ├── main.*              # Server entry point
│   ├── router.*            # Route matching and dispatch
│   ├── rate_limiter.*      # Token bucket rate limiting
│   └── config.*            # Route registry loader
├── routes.yml              # Route definitions
├── .claude/rules/          # Your conventions
├── CLAUDE.md
└── CLAUDE.local.md
```

### After Module 6 — Caching and Health Checks

SQLite-backed response caching, health check endpoints, and request logging. An MCP server lets Claude query gateway metrics directly.

```
nexus-gateway/
├── src/
│   ├── cache.*             # SQLite response cache
│   ├── health.*            # Health check system
│   ├── logger.*            # Request/response logging
│   └── ...
├── data/
│   └── cache.db            # SQLite cache database
├── .claude/
│   ├── skills/             # Custom commands
│   ├── settings.json       # Automation hooks
│   └── rules/
└── .mcp.json               # MCP server config
```

### After Module 10 — Full Service Mesh

A complete local gateway with middleware pipeline, circuit breakers, load balancing, request transformation, and comprehensive test coverage. Subagents, tasks, and a publishable plugin round out your CC mastery.

---

## Set Up Your Dev Environment

Before starting, set up your language toolchain and SQLite. Pick any language you are comfortable with. The exercises describe **what** to build, not how -- you choose the implementation.

### Python

```
python --version          # 3.10+
mkdir -p workspace/nexus-gateway && cd workspace/nexus-gateway
python -m venv .venv
# Windows: .venv\Scripts\activate | macOS/Linux: source .venv/bin/activate
pip install pytest
```

### TypeScript / Node.js

```
node --version            # 18+
mkdir -p workspace/nexus-gateway && cd workspace/nexus-gateway
npm init -y
npm install --save-dev typescript @types/node ts-node jest @types/jest ts-jest
npx tsc --init
```

### Go

```
go version                # 1.21+
mkdir -p workspace/nexus-gateway && cd workspace/nexus-gateway
go mod init nexus-gateway
```

### Rust

```
rustc --version && cargo --version
cargo new workspace/nexus-gateway && cd workspace/nexus-gateway
```

### Environment Isolation

**Environment isolation:** If you chose an environment during `/start` (venv, conda, or Docker), it's already set up in your project directory. If you skipped it and want to add one later, ask Claude: "Help me set up [venv/conda/Docker] for this project."

### SQLite Setup

This project uses SQLite for caching from Module 6 onward. Install it now.

```
sqlite3 --version
# Windows: download from https://sqlite.org/download.html
# macOS: ships with the OS
# Linux (Debian/Ubuntu): sudo apt-get install sqlite3 libsqlite3-dev
# Verify: sqlite3 :memory: "SELECT 'SQLite is working';"
```

Your language will also need an SQLite library:

| Language | Library |
|----------|---------|
| Python | `sqlite3` (built-in) |
| TypeScript | `better-sqlite3` or `sql.js` |
| Go | `github.com/mattn/go-sqlite3` or `modernc.org/sqlite` |
| Rust | `rusqlite` |

### Verify Your Environment

Run `<language> --version`, `git --version`, `sqlite3 --version`, and `claude --version`. If any command fails, fix it before continuing. Claude Code can help -- launch `claude` and ask it to troubleshoot.

---

## Modules

| # | Module | Focus | CC Features |
|---|--------|-------|-------------|
| 1 | [Setup & First Contact](modules/01-setup.md) | Project setup | CLAUDE.md, /init, /memory, keyboard shortcuts |
| 2 | [Blueprint & Build](modules/02-blueprint.md) | Core gateway + CLI | Plan mode, git integration, prompting |
| 3 | [Rules, Memory & Context](modules/03-rules-memory-context.md) | Rate limiting | .claude/rules/, @imports, /context, /compact, /stats, /cost |
| 4 | [Skills & Commands](modules/04-skills-commands.md) | Route management skills | SKILL.md, frontmatter, custom commands, argument substitution |
| 5 | [Hooks](modules/05-hooks.md) | Gateway automation | SessionStart, PostToolUse, Stop hooks, matchers |
| 6 | [MCP Servers](modules/06-mcp-servers.md) | SQLite caching layer | MCP servers, .mcp.json, scopes, skills+MCP |
| 7 | [Guard Rails](modules/07-guard-rails.md) | Guard rails | PreToolUse, decision control, prompt-based hooks |
| 8 | [Subagents](modules/08-subagents.md) | Specialized agents | .claude/agents/, subagent frontmatter, chaining, parallel |
| 9 | [Tasks & TDD](modules/09-tasks-tdd.md) | Middleware system | Tasks, dependencies, TDD loops, SubagentStop |
| 10 | [Parallel Dev, Plugins & Evaluation](modules/10-parallel-plugins-eval.md) | Parallel dev + packaging | Worktrees, plugins, eval, PermissionRequest hooks |
