# Canvas -- Personal Portfolio Site

You're going to build a real portfolio site — and learn every Claude Code feature along the way. By the end, you'll have a polished, multi-page site with responsive design, a blog, and a contact form. More importantly, you'll know Claude Code inside and out.

**Who this is for:** Anyone who wants the simplest possible setup to focus
purely on learning Claude Code. No build tools, no package managers, no
compilers -- just open a file in your browser and start building.

**What you will learn:** All 10 modules cover the full Claude Code feature set,
from CLAUDE.md and plan mode through skills, hooks, MCP servers, subagents,
tasks, plugins, and parallel development.

**Time estimate:** 3-5 focused sessions (roughly 10-15 hours total).

**Prerequisites:** Familiarity with the terminal, git basics, and basic
HTML/CSS/JS. No frameworks or build tools required.

---

## What You'll Build

By the end of all 10 modules, you'll have a polished multi-page portfolio site AND deep expertise in every Claude Code feature. Here's what your project looks like at key milestones:

### After Module 3 — A Real Site Takes Shape

A responsive multi-page portfolio with navigation, an about page, and a projects showcase. Your Claude Code environment has custom rules, persistent memory, and context management.

```
canvas-site/
├── index.html              # Home with hero section
├── about.html              # About page
├── projects.html           # Projects showcase
├── styles/
│   ├── main.css            # Design system with custom properties
│   └── responsive.css      # Mobile-first responsive styles
├── scripts/main.js         # Navigation and interactions
├── .claude/rules/          # Your coding conventions
├── CLAUDE.md               # Project memory
└── CLAUDE.local.md         # Personal progress tracker
```

### After Module 6 — Interactive and Connected

A live-reload dev server via MCP, a contact form, a blog with multiple posts, and accessibility improvements. You've built custom skills and hooks that automate your workflow.

```
canvas-site/
├── index.html
├── about.html
├── projects.html
├── blog/
│   ├── index.html          # Blog listing page
│   └── posts/              # Individual blog posts
├── contact.html            # Contact form
├── styles/...
├── scripts/...
├── .claude/
│   ├── skills/             # Custom commands you built
│   ├── settings.json       # Hook configuration
│   └── rules/
└── .mcp.json               # MCP server config
```

### After Module 10 — Portfolio Complete

A production-ready portfolio with animations, performance optimization, an image gallery, SEO meta tags, and a dark mode toggle. Your Claude Code setup includes subagents, a task system, and a custom plugin — you've mastered every CC feature.

---

## Set Up Your Dev Environment

Canvas uses plain HTML, CSS, and JavaScript. No build tools, no npm, no
compilers. You just need a browser and a text editor.

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

### Verify Your Browser

Open any `.html` file in your browser of choice (Chrome, Firefox, Safari, Edge).
That is your entire runtime. No server needed until Module 6 when you optionally
add a local dev server via MCP.

### Initialize Your Project

```
mkdir -p workspace/canvas-site && cd workspace/canvas-site && git init
```

Create the basic project structure:

| File | Purpose |
|------|---------|
| `index.html` | Home page -- hero section, intro, navigation |
| `styles/main.css` | CSS reset, custom properties, base styles |
| `scripts/main.js` | Shared JavaScript (navigation, utilities) |
| `.gitignore` | Standard web project ignores |

### Verify Everything

Run these checks before continuing:

- [ ] `claude --version` prints a version number
- [ ] `git --version` prints a version number
- [ ] You can open an `.html` file in your browser
- [ ] You can create and enter the `workspace/canvas-site` directory

---

## Modules

| # | Module | Focus | CC Features |
|---|--------|-------|-------------|
| 1 | [Setup & First Contact](modules/01-setup.md) | Project setup, first files, first commit | CLAUDE.md, /init, /memory, keyboard shortcuts |
| 2 | [Blueprint & Build](modules/02-blueprint.md) | Architecture planning, building core pages | Plan mode, git branches, scoped prompting |
| 3 | [Rules, Memory & Context](modules/03-rules-memory-context.md) | Coding standards, context management, blog page | .claude/rules/, CLAUDE.local.md, @imports, /context, /compact, /stats, /cost |
| 4 | [Skills & Commands](modules/04-skills-commands.md) | Custom slash commands for page scaffolding and validation | SKILL.md, frontmatter, $ARGUMENTS, hot-reload, disable-model-invocation |
| 5 | [Hooks](modules/05-hooks.md) | Automated quality gates and site validation | SessionStart, PostToolUse, Stop hooks, matchers, settings.json |
| 6 | [MCP Servers](modules/06-mcp-servers.md) | External data, filesystem tools, publish workflow | MCP servers, .mcp.json, scopes, skills+MCP, claude mcp add |
| 7 | [Guard Rails](modules/07-guard-rails.md) | Accessibility enforcement, auto-fix hooks, prompt-based checks | PreToolUse, permissionDecision, additionalContext, updatedInput, prompt hooks |
| 8 | [Subagents](modules/08-subagents.md) | Specialized review agents for accessibility, design, content | .claude/agents/, frontmatter, chaining, parallel (Ctrl+B), resuming |
| 9 | [Tasks & TDD](modules/09-tasks-tdd.md) | Contact form pipeline, test-driven validation | Tasks, dependencies/blockedBy, cross-session persistence, TDD, SubagentStop |
| 10 | [Parallel Dev, Plugins & Eval](modules/10-parallel-plugins-eval.md) | Dark mode, blog engine, plugin packaging, evaluation | Git worktrees, plugins, evaluation, PermissionRequest hooks, continuous learning |
