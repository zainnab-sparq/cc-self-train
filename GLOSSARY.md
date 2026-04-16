# Glossary

Plain-English definitions for terms you'll encounter in this curriculum. If a word in a module confuses you, check here first.

---

**Agent / Subagent** — A separate, focused instance of Claude that you can spawn to handle a specific task (code review, research, refactoring). Each agent gets its own context window so it doesn't pollute your main conversation. You define them in `.claude/agents/`.

**Agentic** — Describes AI that takes multi-step actions on its own. Instead of one-shot responses ("answer my question"), agentic tools can plan, use tools, check results, and iterate toward a goal — like a coworker rather than a search engine.

**API key** — A secret string that identifies you to an API (like Anthropic's). You get one from [console.anthropic.com](https://console.anthropic.com/). Treat it like a password — never commit it to Git.

**Branch (Git)** — A parallel copy of your code where you can experiment safely. If the experiment works, you *merge* it back to the main code. If it fails, you delete the branch and main is untouched. Create one with `git checkout -b my-feature`.

**CLAUDE.md** — A Markdown file that Claude Code automatically reads at the start of every session. Think of it as a briefing note telling Claude about your project: what it's for, what rules to follow, what commands to run. Created with `/init`.

**CLI (Command-Line Interface)** — A tool you operate by typing commands into a terminal, not by clicking buttons in a window. Claude Code is a CLI. Git is a CLI. `npm` is a CLI.

**Configuration (config) file** — A file that tells a tool how to behave. Often written in JSON, YAML, or TOML. Examples: `.claude/settings.json`, `package.json`, `tsconfig.json`.

**Context / Context window** — Everything Claude "sees" in the current conversation: your messages, its replies, file contents you've shared, rules from CLAUDE.md. Context has a size limit (measured in tokens). When it fills up, older content gets compacted or falls out.

**Effort (`/effort`)** — A Claude Code setting (low / medium / high / max) that controls how much reasoning Claude applies before responding. Higher effort = slower, more thorough; lower = faster, simpler. Leave it on the default until you have a reason to change it.

**Environment variable** — A value stored at the operating-system level that programs can read. Example: `ANTHROPIC_API_KEY=sk-abc123` means any program can read that key without you hardcoding it. Set them in your shell profile or a `.env` file.

**Fast mode (`/fast`)** — An Opus-only setting in Claude Code that makes responses 2.5× faster at higher per-token cost. Not a different model — same quality, different speed/cost tradeoff.

**Frontmatter** — A block of settings at the top of a Markdown file, fenced by `---` lines. It's written in YAML and tells a tool how to use the file. Example:
```yaml
---
name: my-skill
description: Does useful stuff
---
```

**Hook (Claude Code)** — A script that runs automatically at a specific moment — like when a session starts, when Claude edits a file, or when Claude finishes responding. These are **not** React hooks. Think: "when X happens, automatically do Y." Configured in `.claude/settings.json`.

**Merge (Git)** — Combining the changes from one branch into another. If both branches edited the same lines, you get a *merge conflict* that you have to resolve manually.

**MCP (Model Context Protocol)** — An open standard for connecting Claude Code to external tools (databases, APIs, filesystems). An "MCP server" is a program that exposes tools Claude can call. Installed via `claude mcp add`.

**Model** — The specific Claude variant doing the work: Opus (most capable, slower), Sonnet (balanced, default for most plans), Haiku (fastest, simplest). Switch with `/model`.

**npm / npx** — npm is Node.js's package manager (`npm install` downloads packages). npx runs a package without permanently installing it.

**Path scoping** — Telling a rule file to only apply to certain directories or file types. Example: a `paths: ["*.py"]` rule only applies to Python files. Written in the frontmatter.

**Permission mode** — How Claude Code handles tool approvals. Ranges from asking for each action (safest) to auto-approving everything (fastest, riskier). Set with `/permissions` or in `settings.json`.

**Plan mode** — A Claude Code mode where Claude thinks *with* you about architecture and approach but cannot edit files. Toggle with `Shift+Tab`. Great for "let's figure out the design before we write code."

**Plugin** — A bundled set of Claude Code extensions (skills, hooks, agents, MCP servers) that other people can install in their projects. Installed with `/plugin`.

**Prompt** — The text you type to Claude. Good prompts are specific: what to do, with which files, to achieve what outcome.

**Rule file** — A Markdown file in `.claude/rules/` that tells Claude how to write code for a specific part of your project. Example: `react.md` might say "use functional components, not classes." Rules can be path-scoped so they only apply where relevant.

**Scaffold** — The starting files and folders a project needs before you can write real code. `claude` can scaffold an entire project based on a description.

**Session** — One conversation with Claude Code, from when you run `claude` to when you exit. Sessions can be named, resumed, and have their own context.

**Skill (Claude Code)** — A reusable prompt you save as a Markdown file in `.claude/skills/`. You invoke it with a slash command like `/my-skill`. Different from a React/software skill — this specifically means the Claude Code feature.

**Slash command** — A command you type starting with `/` inside Claude Code (like `/init`, `/compact`, `/memory`). Some are built in; others are custom skills you create.

**Task (Claude Code)** — A unit of work tracked by Claude Code's task system. Tasks have status (pending/in_progress/completed), can depend on each other, and persist across sessions.

**Terminal** — The text-based window where you type commands. On Windows: Command Prompt, PowerShell, or Git Bash. On Mac/Linux: Terminal or iTerm. Claude Code runs in a terminal.

**Tool (Claude Code)** — A capability Claude can invoke: Read, Write, Edit, Bash, Grep, WebFetch, etc. Each tool call can be auto-approved, approved once, or denied. You control which tools are available with permission settings.

**Worktree** — A Git feature that lets you check out multiple branches in separate directories at the same time. Useful for running parallel experiments without stashing and switching.

**YAML** — A human-readable data format with indentation and colons. Used for configuration files and frontmatter. Example:
```yaml
name: my-project
version: 1.0
features:
  - hooks
  - skills
```
