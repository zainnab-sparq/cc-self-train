# Module 1 -- Setup & First Contact

<!-- progress:start -->
**Progress:** Module 1 of 10 `[█░░░░░░░░░]` 10%

**Estimated time:** ~30-45 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** CLAUDE.md, /init, /memory, interactive mode, keyboard shortcuts

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

</details>

**Used `/start`?** Module 1 was completed during onboarding. Jump to [Module 2 -- Blueprint & Build](02-blueprint.md).

In this module you create the sentinel project, initialize it with Claude Code, and learn the fundamentals of interactive mode.

**Stuck on a step anywhere in the curriculum?** Type `/stuck` — it reads where you are and re-explains differently. No judgment, no "try harder."

**Safety & trust primer:** Skim [docs/SAFETY-AND-TRUST.md](../../../docs/SAFETY-AND-TRUST.md) before Module 7. Covers prompt injection, hallucinated packages, secrets-in-context, destructive-op posture, and cognitive debt. One read now will save you from a bad day later.

### 1.1 Create Your Project Directory

Create the project directory inside cc-self-train under `workspace/`:

```
mkdir -p workspace/sentinel
cd workspace/sentinel
git init
```

### 1.2 Launch Claude Code

```
claude
```

Claude starts in interactive mode. You are now inside the Claude Code REPL.

> **If you see "command not found: claude"** -- Claude Code is not installed or not on your PATH. Run `npm install -g @anthropic-ai/claude-code` (needs Node.js 18+). If that succeeds but the error persists, close and reopen your terminal so it picks up the new PATH. Still stuck? See the [Manual Setup section of the README](../../../README.md#manual-setup-if-you-prefer).

### 1.2b Terminal or IDE? Choose Your Setup

Claude Code works in two modes. You can use either — or both at the same time.

> **What is an "extension"?** In VS Code and Cursor, an extension is a plugin that adds features to the editor -- like a browser extension adds features to Chrome. You install them from a marketplace inside the editor.

**VS Code / Cursor extension (recommended for beginners).** Install the Claude Code extension from the marketplace (`Ctrl+Shift+X` → search "Claude Code" → Install). You get a graphical chat panel, inline diffs, and you can see files appear in your editor's file tree as Claude creates them. The extension includes a built-in terminal, so you still have CLI access.

**Terminal (full power).** Some features are CLI-only: all slash commands (`/init`, `/memory`, `/resume`), the `!` bash shortcut, tab completion, and MCP server configuration. If you installed the extension, these work in the VS Code integrated terminal too.

**Best of both worlds.** Run the VS Code extension for the graphical experience and open the integrated terminal (`` Ctrl+` ``) when you need CLI-only features. This curriculum works in either mode — we will note when a feature requires the terminal.

You do not have to choose one forever. The extension and CLI share the same conversation history and project configuration.

**STOP -- What you just did:** You chose your development environment -- terminal, IDE, or both. This is a personal preference, not a locked-in decision. You can switch anytime because the CLI and extension share the same project configuration and conversation history.

### 1.3 Run /init

Type this inside Claude Code:

```
/init
```

Claude will scan your (empty) project and generate a `CLAUDE.md` file. Since the project is new, the file will be minimal. That is fine -- you will build it up.

**Engineering value:**
- *Entry-level:* A CLAUDE.md is like onboarding docs for your AI pair programmer — it remembers your project so you don't re-explain it every session.
- *Mid-level:* On teams, CLAUDE.md ensures every developer's Claude session follows the same conventions — consistent code style, correct build commands, shared architecture decisions.
- *Senior+:* CLAUDE.md is declarative project configuration for AI tooling — the same pattern as .editorconfig, .eslintrc, or Makefile, but for your AI assistant. It scales across repos.

**STOP -- What you just did:** You ran your first Claude Code command. `/init` created CLAUDE.md -- the file Claude reads at the start of every session. This is how Claude "remembers" your project. Every time you start a new session, Claude already knows what you told it here.

### 1.4 Tour of CLAUDE.md

Open the generated CLAUDE.md and read it. This file is Claude's persistent memory for your project. Everything you put here, Claude reads at the start of every session.

> **If `/init` fails or seems to hang** -- most often this is a permission prompt waiting for your response in the terminal (scroll up to check). Approve it and `/init` will continue. If you see a real error, paste it to Claude and ask "what does this mean?" -- Claude can debug its own errors.

Ask Claude to explain what CLAUDE.md does:

```
What is CLAUDE.md and how does Claude Code use it? Explain the memory hierarchy.
```

Claude should explain the four memory levels: managed policy, project memory (CLAUDE.md), project rules (.claude/rules/), user memory (~/.claude/CLAUDE.md), and local project memory (CLAUDE.local.md).

**STOP -- What you just did:** You now understand the memory hierarchy -- project, local, user, and managed. This matters because it controls what Claude knows and when. Project memory is shared with your team. Local memory is just for you. User memory follows you everywhere.

### 1.5 Keyboard Shortcuts

Start with just these three. You will learn the rest naturally as you go:

| Shortcut | What It Does |
|----------|-------------|
| `Tab` | Accept suggestion or autocomplete |
| `@` | File path mention -- trigger file autocomplete |
| `!` | Bash mode -- run a shell command directly (e.g., `! git status`) |

Try these now:

1. Type `@` and browse files in your project
2. Type `! git status` to run a shell command
3. Type a few characters and press `Tab` to see autocomplete

<details>
<summary><strong>More shortcuts</strong> -- open this when you are comfortable with the three above</summary>

| Shortcut | What It Does |
|----------|-------------|
| `Shift+Tab` | Toggle between normal mode, plan mode, and auto-accept mode (Module 2 uses this) |
| `Ctrl+C` | Cancel current input or generation |
| `Ctrl+L` | Clear terminal screen (keeps conversation history) |
| `Shift+Enter` | Multiline input (or `\` + `Enter` in any terminal) |
| `Esc Esc` | Rewind conversation/code to a previous point -- your "undo button" |
| `Ctrl+O` | Toggle between normal and verbose transcript view |
| `Ctrl+A` (in `/resume` picker) | Show sessions from all projects |
| `Ctrl+R` | Reverse search command history |
| `Ctrl+X Ctrl+E` | Open external editor for composing long prompts |
| `/` | Start a command or skill |

Full reference: `context/interactive-mode.txt`.

</details>

### 1.5b Slash Commands

Slash commands are Claude Code's built-in commands -- you type `/` followed by a command name. You already know `/init`. The two most useful right now:

| Command | What It Does |
|---------|-------------|
| `/memory` | Opens your memory files (CLAUDE.md) in your editor so you can view and edit what Claude remembers |
| `/recap` | Get a context summary when returning to a session (auto-triggers after 75+ minutes away) |

**The discovery trick:** Type `/` and press `Tab`. You will see every available command autocomplete. Whenever you wonder "can Claude Code do X?", this is the fastest way to check.

<details>
<summary><strong>More slash commands</strong> -- open when you want to explore</summary>

| Command | What It Does |
|---------|-------------|
| `/copy` | Pick and copy specific code blocks from the conversation |
| `/simplify` | Ask Claude to simplify a complex response |
| `/powerup` | Interactive lessons with animated demos of CC features |
| `/btw` | Ask a side question without interrupting Claude's current work |
| `/focus` | Minimal display -- only last prompt and final response |
| `/undo` | Step back to a previous point in the conversation (alias for `/rewind`) |
| `/team-onboarding` | Generate a teammate ramp-up guide from your usage |
| `/batch` | Run commands non-interactively for automation |
| `/tui fullscreen` | Flicker-free alternate-screen rendering |

</details>

**STOP -- What you just did:** You explored slash commands and discovered Tab completion for the `/` menu. From here on, whenever you wonder "can Claude Code do X?", your first instinct should be to type `/` and Tab to check.

### 1.6 Explore /memory

Type this in Claude Code:

```
/memory
```

This opens your CLAUDE.md in your system editor. Add these lines:

```
# Sentinel Project

## About
Code analyzer and test generator CLI tool.

## Commands
- Build: (fill in when you have a build command)
- Test: (fill in when you have a test command)
- Lint: (fill in when you have a lint command)
```

Save and close the editor. Claude now has this context for every future session.

**STOP -- What you just did:** You edited CLAUDE.md through `/memory` and gave Claude persistent context about your project. This is how you teach Claude what it needs to know -- not by repeating yourself every session, but by writing it down once in CLAUDE.md.

### 1.7 First Conversation

Ask Claude something about your project plan:

```
I am building a code analyzer called Sentinel. It will scan source files for
quality issues, generate tests, and track coverage. What would be a good
high-level architecture for this kind of tool?
```

Read the response. You do not need to act on it yet -- Module 2 is where you plan and build.

**STOP -- What you just did:** You had your first real conversation with Claude about your project. Notice how Claude gave a structured, thoughtful response -- this is because it has context from CLAUDE.md. Without that file, Claude would have given a generic answer. Context is everything.

### Leaving and Coming Back

You can exit Claude Code at any time with `Ctrl+D` or `/exit`. To pick up where you left off:

- **`claude -c`** — continues your most recent session in this directory. This is the fastest way to resume.
- **`/resume`** — opens a session picker so you can choose which session to continue. Use this if you have multiple sessions.
- **`/rename my-session-name`** — names your current session before you leave, so you can find it easily with `/resume` later.
- **`claude --resume`** — opens an interactive picker (like `/resume`) from the command line. Useful when you have multiple named sessions and want to choose which one to continue.

Your CLAUDE.md, rules, and project files persist between sessions. Conversation history is restored when you resume, but you may need to re-approve permission prompts.

**Tip:** Before exiting a long session, run `/memory` to save any important context. Claude reads CLAUDE.md at the start of every session, so anything saved there carries forward automatically.

**Pro tip: Multiple Claude sessions in your IDE.** In VS Code, you can open multiple Claude conversations: use the Command Palette (`Ctrl+Shift+P`) → "Claude Code: Open in New Tab" to run side-by-side conversations. In the terminal, split your terminal pane (`Ctrl+Shift+5` in VS Code) and run `claude` in each. This becomes especially useful in Module 10 when you work with git worktrees and parallel development.

**Engineering value:**
- *Entry-level:* Session persistence means you can work on a problem across days without losing context — like saving your game.
- *Mid-level:* Named sessions (`/rename`) let you maintain separate contexts for different workstreams — bug investigation in one, feature work in another.

### 1.8 Make the Session Your Own

Two small personalizations to try now:

**Color your prompt bar.** Type `/color` and pick a color -- this sets the accent color on your prompt bar for the session. Try `/color blue` or just `/color` to see options.

**Name your sessions.** Launch Claude with `-n`: `claude -n "Sentinel Build"`. Named sessions are easier to find when you come back via `/resume`.

<details>
<summary><strong>More customization you can explore later</strong></summary>

- **Effort level.** `/effort` shows your current reasoning depth (low / medium / high). Higher = deeper thinking, slower responses. Leave it on the default until you have a reason to change it -- Module 8 covers this in depth.
- **Model overrides.** `modelOverrides` in settings lets you point the model picker at custom provider model IDs. Ignore until Module 8.
- **Recent release notes.** `/release-notes` opens an interactive version picker. `/tag` and `/vim` were removed -- use `/config` -> Editor mode for vim keybindings and `/rename` for session naming.

</details>

> **STOP** -- Try `/color` and name your session with `-n` on your next launch. These small touches make sessions easier to find and more personal.

### Shell tools you'll need later

Module 5 (Hooks) uses **`jq`** to parse JSON from hook stdin. If you don't already have it, install now so you're not blocked later:

- **macOS:** `brew install jq`
- **Ubuntu/Debian:** `sudo apt install jq`
- **Windows (Git Bash):** `choco install jq` (requires [Chocolatey](https://chocolatey.org/install)) or download from https://jqlang.github.io/jq/download/. Module 5 also shows a Python fallback if you'd rather skip the install.

Verify with `jq --version`.

### Windows setup — one-time fixes for Git Bash / MSYS

Skip this section if you're on macOS or Linux. Windows users: these four tweaks prevent friction you'll otherwise hit in Modules 2, 5, and 6.

**1. Default branch.** Later modules use `main` as the branch name. Git's default on Windows is `master`:

```bash
git config --global init.defaultBranch main
```

Run this once; every new `git init` now uses `main`. If you already created a repo as `master`, rename with `git branch -m master main`.

**2. Line endings.** Git will show `warning: LF will be replaced by CRLF` on every commit — this is informational, not an error. To acknowledge and stop worrying:

```bash
git config --global core.autocrlf true
```

This converts line endings on checkout (CRLF for Windows tools) and commit (LF for the repo). If your team uses LF everywhere, set `core.autocrlf input` instead.

**3. `cmd /c` wrapper for npx.** Several `claude mcp add` commands in Module 6 prefix `npx` with `cmd /c`:

```
claude mcp add --transport stdio fs -- cmd /c npx -y @modelcontextprotocol/server-filesystem --root .
```

The `cmd /c` tells Git Bash to invoke `npx` through the native Windows `cmd` shell, which is how `npx` is typically installed on Windows. Without it, you may hit "command not found." macOS/Linux users drop `cmd /c`.

**Stuck?** `/stuck` re-explains any of the above for your specific platform.

**4. Windows path translation for hook scripts.** Git Bash sets `$CLAUDE_PROJECT_DIR` to a POSIX-style path like `/c/Users/you/project`. Native Windows tools (Python, PowerShell) expect `C:\Users\you\project`. When a hook script pipes `$CLAUDE_PROJECT_DIR` into native tools, convert with `cygpath`:

```bash
# In a hook script:
PROJECT_DIR_WIN=$(cygpath -w "$CLAUDE_PROJECT_DIR")
python "$PROJECT_DIR_WIN\\scripts\\check.py"
```

Module 5 revisits this at the first hook script that pipes into Python.

### Checkpoint

You just set up a code analysis project, configured Claude Code's memory, learned the keyboard shortcuts, and had your first real conversation with Claude. That's a real foundation -- everything from here builds on it.

- [ ] `workspace/sentinel/` directory exists with `git init` completed
- [ ] CLAUDE.md exists (generated by /init, then edited via /memory)
- [ ] You tried all keyboard shortcuts from the table above
- [ ] You successfully ran `/memory` and edited CLAUDE.md
- [ ] You know how to exit (`Ctrl+D`) and resume (`claude -c`) a session
- [ ] You had at least one conversation with Claude about the project
- [ ] Tried `/color` and `/effort` to customize your session
