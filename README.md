# Agentic Education:<br>Using Claude Code to Teach Claude Code

[![Paper](https://img.shields.io/badge/Paper-PDF-red)](Agentic%20Education%20-%20Using%20Claude%20Code%20to%20Teach%20Claude%20Code.pdf) [![v2.25.0](https://img.shields.io/badge/version-2.25.0-blue)](CHANGELOG.md)

## TL;DR

Learn [Claude Code](https://docs.anthropic.com/en/docs/claude-code) by building a real project. Pick from 5 project types, work through 10 hands-on modules, and go from "what is this?" to "I can build anything with this." No prior experience with AI coding tools needed — the curriculum adapts to your level and walks you through one step at a time.

> **First time hearing of Claude Code?** It's a tool that runs in your terminal (the text window where you type commands). You describe in plain English what you want to build, and Claude writes the code, creates files, and runs commands — but only after you approve each one. Think of it as a very skilled coding partner that lives in your terminal. See the [glossary](GLOSSARY.md) for any unfamiliar terms below.

<details>
<summary>Under the hood: the research behind this curriculum</summary>

**cc-self-train** implements five research contributions: (1) a **persona progression model** that adapts the AI instructor's tone across four stages (Guide → Collaborator → Peer → Launcher); (2) an **adaptive learning system** that observes engagement quality through hook-based heuristics and adjusts scaffolding at two timescales; (3) a **cross-domain unified curriculum** in which five project domains share identical feature sequencing; (4) a **step-pacing mechanism** with explicit pause primitives to manage information overload; and (5) an **auto-updating curriculum design** in which the onboarding agent detects upstream tool changes and updates teaching materials before instruction. A pilot evaluation with 27 participants showed statistically significant self-efficacy gains across all 10 skill areas (*p* < 0.001). Full details in the [paper](Agentic%20Education%20-%20Using%20Claude%20Code%20to%20Teach%20Claude%20Code.pdf).

</details>

## Prerequisites

You should be comfortable with:

- **Opening a terminal** and typing commands (`cd`, `ls`, `mkdir`)
- **Basic Git** — at minimum, `git add` / `git commit` / `git push`. You don't need to understand branches yet; Module 2 will teach that.
- **Installing software** on your computer (npm, brew, winget, or apt)
- **Reading error messages** without panicking (a little anxiety is fine — the curriculum helps with that)

If any of these feel unfamiliar, spend an hour with a basic terminal tutorial before starting. You'll have a much better experience.

**Jargon reference:** If a term in the modules confuses you (hooks, frontmatter, YAML, MCP, etc.), check [GLOSSARY.md](GLOSSARY.md) for plain-English definitions.

**Safety & trust:** Before running Claude against code you care about, skim [docs/SAFETY-AND-TRUST.md](docs/SAFETY-AND-TRUST.md) — covers prompt injection, hallucinated packages, what Anthropic sees in your requests, destructive-operation posture, code-review-the-agent mindset, and cognitive debt. Read it now; come back after each new feature module.

## Quick Start

**Time to first working feature:** ~90 minutes (Module 2). **Full curriculum:** ~10-15 hours across 10 modules. Progress tracking lives in `CLAUDE.local.md` once you start — no guessing how far you've come.

```bash
# 1. Install Claude Code (if you haven't already)
npm install -g @anthropic-ai/claude-code

# 2. Clone this repo
git clone https://github.com/suspicious-cow/cc-self-train.git
cd cc-self-train

# 3. Launch Claude Code
claude

# 4. When prompted to trust project hooks, approve them
#    (they show a welcome banner and check GitHub for
#     CC updates, nothing else — /hooks to review if curious)

# 5. Type this when Claude starts:
/start
```

That's it. Claude will walk you through picking a project, checking your dev environment, and scaffolding everything. You'll need an [Anthropic API key](https://console.anthropic.com/) or a Claude subscription (Pro, Max, or Team).

**Stuck on a step?** Once you're in the curriculum, type `/stuck` anytime — it reads where you are and re-explains differently. No judgment, no "try harder."

> **What are those hooks?** This repo includes two small SessionStart hooks. The first shows the welcome banner above. The second pings GitHub to check if a newer version of Claude Code is available — if so, it tells you to run `claude update`. Both are read-only, open source, and visible in `.claude/scripts/`.

## Who This Is For

You've installed Claude Code and maybe run `/init`. Now what? This is your answer. Pick one of 4 tutorial projects (or bring your own) and work through 10 progressive modules that take you from "first session" to "multi-agent orchestration." By the end, you won't just know what these features do — you'll have used every one of them to build something you're proud of.

**No specific language required.** Forge, Nexus, and Sentinel describe *what* to build, not *how*. You choose Python, TypeScript, Go, Rust, or whatever you're comfortable with. Canvas uses plain HTML/CSS/JS — no build tools needed.

## Manual Setup (if you prefer)

<details>
<summary>Click to expand manual setup instructions</summary>

### Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

### Set Up Your Dev Environment

Make sure your language toolchain is ready:

| Language | What you need | Quick check |
|----------|--------------|-------------|
| **Python** | Python 3.10+, a package manager (conda, venv, uv, or pip) | `python --version` |
| **TypeScript/Node** | Node.js 18+, npm/pnpm/yarn | `node --version` |
| **Go** | Go 1.21+ | `go version` |
| **Rust** | Rust via rustup, cargo | `rustc --version` |
| **Other** | Whatever your language needs — Claude can help you set it up | |

**Docker users:** Any project can be done inside a container. Bring your own Dockerfile or ask Claude to generate one for your language.

### Install Git

```bash
git --version
```

If you don't have it: [git-scm.com/downloads](https://git-scm.com/downloads)

### Pick a Project and Go

Each project covers all 10 modules. Pick based on what sounds fun to build.

</details>

## The 5 Options

### [Canvas — Personal Portfolio Site](projects/canvas/README.md) ⭐ Recommended for first-timers

Build a multi-page portfolio site with responsive design, a blog, and a contact form using plain HTML, CSS, and JavaScript.

**Why this project?** Every developer needs a portfolio site but never gets around to building one. Canvas uses zero build tools — no npm, no frameworks, no compilers. Just open `index.html` in your browser. That means you spend 100% of your time learning Claude Code instead of fighting your toolchain. You'll walk away with a real, deployable site *and* mastery of every CC feature.

**Best for:** First-timers, anyone who wants the fastest path to learning CC

---

### [Forge — Personal Dev Toolkit](projects/forge/README.md)

Build a command-line tool (a program you run from your terminal) for notes, snippets, bookmarks, and templates that grows into a searchable, pluggable knowledge base with API.

**Why this project?** Most tutorials build throwaway apps you'll never open again. Forge builds something you'll actually use every day — a personal tool that organizes your dev life. Notes from meetings, code snippets you keep re-Googling, project templates you set up the same way every time. By the end, you'll have a tool that saves you time *and* deep expertise in Claude Code.

**Best for:** Tool builders, "I want something I'll actually use after this course"

---

### [Nexus — Local API Gateway](projects/nexus/README.md)

Build a local server that sits between apps and manages their traffic — routing requests, limiting how fast clients can call, caching responses, and checking if services are healthy.

**Why this project?** Every production system has a gateway that manages traffic between services, but most developers treat it as a black box. By building one from scratch — routing, rate limiting, caching, health checks — you'll understand how services actually talk to each other at a level most developers never reach. If you've ever wondered what sits between a user's request and the server that handles it, this is your chance to find out by building it yourself.

**Best for:** Backend devs, anyone curious about infrastructure and how services connect

---

### [Sentinel — Code Analyzer & Test Generator](projects/sentinel/README.md)

Build a tool that scans code for problems, generates tests automatically, and tracks how well-tested your code is — growing into a full quality dashboard.

**Why this project?** Sentinel is a tool that makes your *other* code better. It finds bugs before they ship, writes tests so you don't have to start from scratch, and tracks quality over time. If you care about code quality, this project teaches you how to enforce it automatically. It's the "meta-tool" — a program that improves every other program you write.

**Best for:** Quality-focused devs, "I want to build a tool that levels up everything else I write"

---

### [Bring Your Own Project](projects/byop/README.md) -- For Experienced Developers

Already have a project you're working on? Learn every CC feature by applying it to YOUR existing codebase. Same 10 modules, but every exercise targets your real code instead of a tutorial project.

**Best for:** Developers with an existing project who want practical CC skills, not another tutorial

---

All five options teach the same CC features through the same 10 modules. Canvas, Forge, Nexus, and Sentinel are **local-only** and **genuinely useful**. Canvas uses HTML/CSS/JS (no setup needed); Forge, Nexus, and Sentinel are **language-agnostic** — you choose. BYOP works with any existing project. Pick based on interest, not difficulty.

## The 10 Modules

Every project follows this same progression:

| # | Module | CC Features Taught |
|---|--------|--------------------|
| 1 | **Setup & First Contact** | CLAUDE.md, /init, /memory, interactive mode, keyboard shortcuts, /color, /effort, session naming |
| 2 | **Blueprint & Build** | Plan mode, git integration, basic prompting, /branch, /plan with descriptions, includeGitInstructions |
| 3 | **Rules, Memory & Context** | .claude/rules/, CLAUDE.local.md, @imports, /context, /compact, memory hierarchy, HTML comment hiding, autoMemoryDirectory |
| 4 | **Skills & Commands** | SKILL.md, frontmatter, custom commands, hot-reload, argument substitution, effort frontmatter, ${CLAUDE_SKILL_DIR}, /claude-api |
| 5 | **Hooks** | SessionStart, PostToolUse, Stop hooks, matchers, hook scripting, StopFailure, PostCompact, InstructionsLoaded, Elicitation hooks |
| 6 | **MCP Servers** | MCP servers, .mcp.json, scopes, skills+MCP integration, elicitation, channels |
| 7 | **Guard Rails** | PreToolUse, hook decision control, prompt-based hooks, allowRead, sandbox network isolation |
| 8 | **Subagents** | .claude/agents/, subagent frontmatter, chaining, parallel, background, SendMessage, agent frontmatter fields |
| 9 | **Tasks & TDD** | Tasks system, dependencies, cross-session persistence, TDD loops, /loop, cron scheduling |
| 10 | **Parallel Dev, Plugins & Evaluation** | Worktrees, agent teams (experimental), plugins, eval, PermissionRequest hooks, continuous learning, plugin ecosystem, /remote-control, ExitWorktree |

## Feature Coverage Matrix

Every major CC feature is taught in all 5 options:

| Feature | Canvas | Forge | Nexus | Sentinel | BYOP | Module |
|---------|:------:|:-----:|:-----:|:--------:|:----:|:------:|
| CLAUDE.md, /init, /memory | x | x | x | x | x | 1 |
| Interactive mode (shortcuts, @, /, !) | x | x | x | x | x | 1 |
| /color, /effort, session naming (-n) | x | x | x | x | x | 1 |
| Plan mode | x | x | x | x | x | 2 |
| Git integration, /branch | x | x | x | x | x | 2 |
| .claude/rules/ (path-scoped) | x | x | x | x | x | 3 |
| CLAUDE.local.md, memory hierarchy | x | x | x | x | x | 3 |
| @imports, /context, /compact, HTML comments | x | x | x | x | x | 3 |
| paths: frontmatter for rules | x | x | x | x | x | 3 |
| Skills (SKILL.md, frontmatter, hot-reload) | x | x | x | x | x | 4 |
| Custom slash commands, effort frontmatter | x | x | x | x | x | 4 |
| paths: for skills, disableSkillShellExecution | x | x | x | x | x | 4 |
| Hooks (SessionStart, PostToolUse, Stop) | x | x | x | x | x | 5 |
| Hook scripting, new events (StopFailure, PostCompact, etc.) | x | x | x | x | x | 5 |
| Hook `if` conditions, CwdChanged, FileChanged | x | x | x | x | x | 5 |
| MCP servers (.mcp.json, scopes) | x | x | x | x | x | 6 |
| Skills + MCP, elicitation, channels | x | x | x | x | x | 6 |
| PreToolUse, hook decision control | x | x | x | x | x | 7 |
| Prompt-based hooks, allowRead, sandbox settings | x | x | x | x | x | 7 |
| PermissionDenied, defer, PreToolUse updatedInput | x | x | x | x | x | 7 |
| Subagents (.claude/agents/) | x | x | x | x | x | 8 |
| Subagent chaining, parallel, SendMessage | x | x | x | x | x | 8 |
| Agent initialPrompt frontmatter | x | x | x | x | x | 8 |
| Tasks system (dependencies, cross-session) | x | x | x | x | x | 9 |
| TDD, /loop, cron scheduling | x | x | x | x | x | 9 |
| Git worktrees, parallel dev, ExitWorktree | x | x | x | x | x | 10 |
| Agent teams (experimental) | x | x | x | x | x | 10 |
| Plugins, /remote-control, plugin ecosystem | x | x | x | x | x | 10 |
| Plugin userConfig, sensitive storage | x | x | x | x | x | 10 |
| Evaluation framework | x | x | x | x | x | 10 |
| Continuous learning patterns | x | x | x | x | x | 10 |

## Reference Docs

The `context/` folder contains detailed reference documentation for every CC feature:

| File | Covers |
|------|--------|
| `context/claudemd.txt` | CLAUDE.md hierarchy, @imports, rules |
| `context/skillsmd.txt` | Skills SKILL.md format, frontmatter, arguments |
| `context/hooks.txt` | Hook lifecycle, events, scripting, decision control |
| `context/configure-hooks.txt` | Practical hook configuration examples |
| `context/subagents.txt` | Subagent creation, frontmatter, patterns |
| `context/agent-teams.txt` | Agent teams (experimental), coordination |
| `context/plugins.txt` | Plugin structure, manifest, bundling |
| `context/tasks.txt` | Tasks system, dependencies, cross-session |
| `context/mcp.txt` | MCP servers, transports, scopes |
| `context/skills-plus-mcp.txt` | Combining skills with MCP tools |
| `context/interactive-mode.txt` | Keyboard shortcuts, vim mode |
| `context/common-workflows.txt` | Common workflows and patterns |
| `context/when-to-use-features.txt` | Feature comparison and selection guide |
| `context/boris-workflow.txt` | Real-world patterns, parallel Claude workflows |
| `context/anthropic-basics.txt` | How Claude Code works (agentic loop, models, tools) |
| `context/sl-guide.txt` | Real-world CC patterns from daily use and hackathon experience |
| `context/changelog-cc.txt` | Claude Code changelog (v2.0.0 — v2.1.80) |
| `context/auto-memory.txt` | Auto-memory system reference |
| `context/models.txt` | Model tiers (Haiku/Sonnet/Opus), selection guidance, effort levels |
| `context/ide-integration.txt` | VS Code/Cursor extension, IDE setup, CLI vs extension features |

## Design Principles

- **Learn by building.** You won't read a single tutorial. Every feature is taught through a real task in your project — you use it, see the result, and move on.
- **Language-agnostic.** Every project works in any language. You choose.
- **Local-only.** No cloud services required (MCP connections are optional/local).
- **Same curriculum, different domains.** All 5 options teach the same features in the same order. Pick based on interest.
- **Real tools, not toys.** Every project produces something genuinely useful that you can keep using after you finish.

## Always Current

You don't need to worry about the curriculum going stale. When you run `/start`, two things happen automatically:

1. **Repo freshness check** — If the maintainers have pushed updates since you last pulled, Claude offers to `git pull` so you get the latest modules and docs.
2. **CC version sync** — If your installed Claude Code is newer than what the curriculum covers, Claude fetches the changelog and updates the relevant lesson files and reference docs on the spot.

Returning users get a banner reminder at session start if updates are available. Everything works offline too — if either check fails, onboarding continues with the current materials.

## Companion Resources

- [everything-claude-code](https://github.com/affaan-m/everything-claude-code) — Reference docs, agents, skills, and commands for Claude Code
- [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) — Official documentation
- [Claude Code changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) — Latest changes

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## License

This project is created by Zain Naboulsi and licensed under the [MIT License](LICENSE). Co-authored with [Claude](https://claude.ai) by Anthropic — see [DISCLAIMER.md](DISCLAIMER.md) for details on AI-generated content, warranty, and support.
