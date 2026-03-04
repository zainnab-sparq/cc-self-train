# Module 1 -- Setup & First Contact

**CC features:** CLAUDE.md, /init, /memory, interactive mode, keyboard shortcuts

> **Persona — Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

> **Used `/start`?** Module 1 was completed during onboarding. Jump to [Module 2 -- Blueprint & Build](02-blueprint.md).

In this module you create the sentinel project, initialize it with Claude Code, and learn the fundamentals of interactive mode.

### Step 1: Create your project directory

Create the project directory inside cc-self-train under `workspace/`:

```
mkdir -p workspace/sentinel
cd workspace/sentinel
git init
```

### Step 2: Launch Claude Code

```
claude
```

Claude starts in interactive mode. You are now inside the Claude Code REPL.

### Step 2b: Terminal or IDE? Choose Your Setup

Claude Code works in two modes. You can use either — or both at the same time.

**VS Code / Cursor extension (recommended for beginners).** Install the Claude Code extension from the marketplace (`Ctrl+Shift+X` → search "Claude Code" → Install). You get a graphical chat panel, inline diffs, and you can see files appear in your editor's file tree as Claude creates them. The extension includes a built-in terminal, so you still have CLI access.

**Terminal (full power).** Some features are CLI-only: all slash commands (`/init`, `/memory`, `/resume`), the `!` bash shortcut, tab completion, and MCP server configuration. If you installed the extension, these work in the VS Code integrated terminal too.

**Best of both worlds.** Run the VS Code extension for the graphical experience and open the integrated terminal (`` Ctrl+` ``) when you need CLI-only features. This curriculum works in either mode — we will note when a feature requires the terminal.

You do not have to choose one forever. The extension and CLI share the same conversation history and project configuration.

### Step 3: Run /init

Type this inside Claude Code:

```
/init
```

Claude will scan your (empty) project and generate a `CLAUDE.md` file. Since the project is new, the file will be minimal. That is fine -- you will build it up.

> **Engineering value:**
> - *Entry-level:* A CLAUDE.md is like onboarding docs for your AI pair programmer — it remembers your project so you don't re-explain it every session.
> - *Mid-level:* On teams, CLAUDE.md ensures every developer's Claude session follows the same conventions — consistent code style, correct build commands, shared architecture decisions.
> - *Senior+:* CLAUDE.md is declarative project configuration for AI tooling — the same pattern as .editorconfig, .eslintrc, or Makefile, but for your AI assistant. It scales across repos.

### Step 4: Tour of CLAUDE.md

Open the generated CLAUDE.md and read it. This file is Claude's persistent memory for your project. Everything you put here, Claude reads at the start of every session.

Ask Claude to explain what CLAUDE.md does:

```
What is CLAUDE.md and how does Claude Code use it? Explain the memory hierarchy.
```

Claude should explain the four memory levels: managed policy, project memory (CLAUDE.md), project rules (.claude/rules/), user memory (~/.claude/CLAUDE.md), and local project memory (CLAUDE.local.md).

### Step 5: Keyboard shortcuts

Try each of these shortcuts now. Do not skip this -- muscle memory matters.

| Shortcut | What it does | Try it now |
|----------|-------------|------------|
| `Tab` | Accept Claude's suggestion or autocomplete | Type a partial word and press Tab |
| `Shift+Tab` | Toggle between normal mode, plan mode, and auto-accept mode | Press it twice to cycle through modes |
| `Ctrl+C` | Cancel current generation or input | Press while Claude is responding |
| `Ctrl+L` | Clear terminal screen (keeps conversation) | Press it -- notice history is preserved |
| `@` | File path mention / autocomplete | Type `@` and start typing a filename |
| `!` | Bash mode -- run a shell command directly | Type `! git status` |
| `Shift+Enter` or `\` + `Enter` | Multiline input | Start a multi-line prompt |
| `Esc Esc` | Rewind conversation/code to a previous point | Double-tap Escape |
| `Ctrl+O` | Toggle verbose output | Shows detailed tool usage |
| `Ctrl+R` | Reverse search through command history | Search your previous prompts |

> **Engineering value:**
> - *Entry-level:* These shortcuts aren't just convenience — they're how you stay in flow. Switching between Claude and your terminal without reaching for the mouse keeps you productive.
> - *Mid-level:* Plan mode (Shift+Tab) is critical for code review workflows — you can have Claude analyze and propose changes without executing them, which is how you safely use AI on production code.

### Step 5b: Slash Commands

The `/` shortcut from the table above opens Claude Code's built-in commands. You have already used `/init` -- here are a few more to try now:

| Command | What It Does |
|---------|-------------|
| `/memory` | Opens your memory files (CLAUDE.md) in your editor so you can view and manage what Claude remembers across sessions |
| `/copy` | Interactive picker that lets you select and copy specific code blocks from the conversation -- useful when Claude generates something you want to use elsewhere |
| `/simplify` | Asks Claude to simplify complex code or explanations -- handy when a response feels like too much at once |
| `/batch` | Runs commands in batch mode for non-interactive automation |

Try typing `/` and pressing `Tab` to see the full list of available commands. Tab completion works here the same way it works for file paths -- it is the quickest way to discover what Claude Code can do.

### Step 6: Explore /memory

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

### Step 7: First conversation

Ask Claude something about your project plan:

```
I am building a code analyzer called Sentinel. It will scan source files for
quality issues, generate tests, and track coverage. What would be a good
high-level architecture for this kind of tool?
```

Read the response. You do not need to act on it yet -- Module 2 is where you plan and build.

### Leaving and Coming Back

You can exit Claude Code at any time with `Ctrl+D` or `/exit`. To pick up where you left off:

- **`claude -c`** — continues your most recent session in this directory. This is the fastest way to resume.
- **`/resume`** — opens a session picker so you can choose which session to continue. Use this if you have multiple sessions.
- **`/rename my-session-name`** — names your current session before you leave, so you can find it easily with `/resume` later.
- **`claude --resume`** — opens an interactive picker (like `/resume`) from the command line. Useful when you have multiple named sessions and want to choose which one to continue.

Your CLAUDE.md, rules, and project files persist between sessions. Conversation history is restored when you resume, but you may need to re-approve permission prompts.

> **Tip:** Before exiting a long session, run `/memory` to save any important context. Claude reads CLAUDE.md at the start of every session, so anything saved there carries forward automatically.

> **Pro tip: Multiple Claude sessions in your IDE.** In VS Code, you can open multiple Claude conversations: use the Command Palette (`Ctrl+Shift+P`) → "Claude Code: Open in New Tab" to run side-by-side conversations. In the terminal, split your terminal pane (`Ctrl+Shift+5` in VS Code) and run `claude` in each. This becomes especially useful in Module 10 when you work with git worktrees and parallel development.

> **Engineering value:**
> - *Entry-level:* Session persistence means you can work on a problem across days without losing context — like saving your game.
> - *Mid-level:* Named sessions (`/rename`) let you maintain separate contexts for different workstreams — bug investigation in one, feature work in another.

### Checkpoint

You just set up a code analysis project, configured Claude Code's memory, learned the keyboard shortcuts, and had your first real conversation with Claude. That's a real foundation -- everything from here builds on it.

- [ ] `workspace/sentinel/` directory exists with `git init` completed
- [ ] CLAUDE.md exists (generated by /init, then edited via /memory)
- [ ] You tried all keyboard shortcuts from the table above
- [ ] You successfully ran `/memory` and edited CLAUDE.md
- [ ] You know how to exit (`Ctrl+D`) and resume (`claude -c`) a session
- [ ] You had at least one conversation with Claude about the project
