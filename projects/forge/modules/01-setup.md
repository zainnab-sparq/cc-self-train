# Module 1 -- Setup and First Contact

**CC features:** CLAUDE.md, `/init`, `/memory`, interactive mode, keyboard
shortcuts

> **Persona — Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

> **Used `/start`?** Module 1 was completed during onboarding. Jump to [Module 2 -- Blueprint and Build](02-blueprint.md).

## 1.1 Create Your Project

Open a terminal in the cc-self-train directory and create the project:

```
mkdir -p workspace/forge-toolkit
cd workspace/forge-toolkit
git init
```

## 1.2 Launch Claude Code

```
claude
```

Claude Code starts in interactive mode. You are now inside a session.

## 1.2b Terminal or IDE? Choose Your Setup

Claude Code works in two modes. You can use either — or both at the same time.

**VS Code / Cursor extension (recommended for beginners).** Install the Claude Code extension from the marketplace (`Ctrl+Shift+X` → search "Claude Code" → Install). You get a graphical chat panel, inline diffs, and you can see files appear in your editor's file tree as Claude creates them. The extension includes a built-in terminal, so you still have CLI access.

**Terminal (full power).** Some features are CLI-only: all slash commands (`/init`, `/memory`, `/resume`), the `!` bash shortcut, tab completion, and MCP server configuration. If you installed the extension, these work in the VS Code integrated terminal too.

**Best of both worlds.** Run the VS Code extension for the graphical experience and open the integrated terminal (`` Ctrl+` ``) when you need CLI-only features. This curriculum works in either mode — we will note when a feature requires the terminal.

You do not have to choose one forever. The extension and CLI share the same conversation history and project configuration.

## 1.3 Run /init

Type this into Claude Code:

```
/init
```

Claude scans your project and generates a `CLAUDE.md` file. This is the single
most important file for working with Claude Code -- it is loaded into context
at the start of every session and tells Claude about your project.

Read through the generated `CLAUDE.md`. It should contain:

- A project description
- Build and test commands
- Code style conventions

If it is sparse, that is fine. You will build it up throughout this project.

> **Engineering value:**
> - *Entry-level:* A CLAUDE.md is like onboarding docs for your AI pair programmer — it remembers your project so you don't re-explain it every session.
> - *Mid-level:* On teams, CLAUDE.md ensures every developer's Claude session follows the same conventions — consistent code style, correct build commands, shared architecture decisions.
> - *Senior+:* CLAUDE.md is declarative project configuration for AI tooling — the same pattern as .editorconfig, .eslintrc, or Makefile, but for your AI assistant. It scales across repos.

## 1.4 Tour of CLAUDE.md

Ask Claude:

```
Explain what CLAUDE.md is, how Claude Code uses it, and why it matters.
Mention the memory hierarchy: user, project, project-local, and managed.
```

Key points to understand:

- **Project memory** (`./CLAUDE.md` or `./.claude/CLAUDE.md`): shared with
  your team via version control
- **Project local** (`./CLAUDE.local.md`): your personal preferences for this
  project, auto-added to `.gitignore`
- **User memory** (`~/.claude/CLAUDE.md`): your personal preferences across
  all projects
- **Managed policy**: organization-wide, deployed by IT

## 1.5 Keyboard Shortcuts

Try each shortcut below and note what happens:

| Shortcut | What It Does |
|----------|-------------|
| `Tab` | Accept suggestion or autocomplete |
| `Shift+Tab` | Toggle between normal mode, plan mode, and auto-accept mode |
| `Ctrl+C` | Cancel current input or generation |
| `Ctrl+L` | Clear terminal screen (keeps conversation history) |
| `@` | File path mention -- trigger file autocomplete |
| `!` | Bash mode -- run a shell command directly |
| `Shift+Enter` | Multiline input (or `\` + `Enter` in any terminal) |
| `Esc Esc` | Rewind conversation/code to a previous point |
| `Ctrl+O` | Toggle verbose output |
| `Ctrl+R` | Reverse search command history |
| `/` | Start a command or skill |

Try these now:

1. Type `@` and browse files in your project
2. Type `! git status` to run a shell command
3. Press `Shift+Tab` twice to cycle through modes -- notice the mode indicator
4. Type a long prompt using `Shift+Enter` for multiple lines
5. Press `Ctrl+L` to clear the screen

> **Engineering value:**
> - *Entry-level:* These shortcuts aren't just convenience — they're how you stay in flow. Switching between Claude and your terminal without reaching for the mouse keeps you productive.
> - *Mid-level:* Plan mode (Shift+Tab) is critical for code review workflows — you can have Claude analyze and propose changes without executing them, which is how you safely use AI on production code.

## 1.5b Slash Commands

That `/` shortcut opens Claude Code's built-in commands. You already know `/init` -- here are a few more that are useful right away:

| Command | What It Does |
|---------|-------------|
| `/memory` | Opens your memory files (CLAUDE.md) in your editor so you can view and manage what Claude remembers across sessions |
| `/copy` | Opens an interactive picker to select and copy specific code blocks from the conversation -- great for grabbing a snippet Claude generated |
| `/simplify` | Asks Claude to simplify complex code or explanations -- helpful when a response has more detail than you need |
| `/batch` | Runs commands in batch mode for non-interactive automation |

Try typing `/` and then pressing `Tab` to see the full list of available commands. This is worth doing -- there are more commands than the ones listed here, and Tab completion is the fastest way to discover them.

## 1.6 Explore /memory

Type:

```
/memory
```

This opens your memory files in your system editor. You can directly edit
`CLAUDE.md` here. Add a line:

```
This project is a personal dev toolkit CLI called "forge" for managing notes,
snippets, bookmarks, and templates.
```

Save and close the editor.

## 1.7 Exercise

Ask Claude:

```
Read the CLAUDE.md file in this project and explain what it contains.
Then suggest three improvements I could make to it for a CLI tool project.
```

Review Claude's suggestions. Apply at least one of them by editing `CLAUDE.md`.

## 1.8 First Commit

```
! git add -A
! git commit -m "Initial project setup with CLAUDE.md"
```

## Leaving and Coming Back

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

## Checkpoint

You just set up your toolkit project, configured Claude Code's memory, learned the keyboard shortcuts, and made your first commit. That's a real foundation -- everything from here builds on it.

- [ ] `workspace/forge-toolkit/` directory exists with `git init` completed
- [ ] `CLAUDE.md` exists and describes the project
- [ ] You ran `/init` and `/memory` successfully
- [ ] You tried all keyboard shortcuts from the table above
- [ ] You know how to exit (`Ctrl+D`) and resume (`claude -c`) a session
- [ ] You made your first commit
