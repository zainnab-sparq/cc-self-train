# Module 1 -- Setup and First Contact

**CC features:** CLAUDE.md, `/init`, `/memory`, interactive mode, keyboard
shortcuts

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try...", "Here's what that does..."

**Used `/start`?** Module 1 was completed during onboarding. Jump to [Module 2 -- Blueprint and Build](02-blueprint.md).

### 1.1 Verify Your Project

Before launching Claude Code, make sure your existing project is ready. Open a terminal in your project directory and run:

```
git status
```

Confirm that:

- Your project is a git repository (if not, run `git init`)
- You know roughly how many files and what languages are in the project
- You have a clean working tree (no uncommitted changes you are not aware of)

Take a quick inventory. Ask yourself: what languages does this project use? What is the directory structure? Are there existing docs, configs, or READMEs? You will feed this context to Claude in a moment.

**STOP -- What you just did:** You confirmed your project is git-initialized and took stock of its structure. This matters because Claude Code works best when it can see your project's git history and file layout. A clean starting point means fewer surprises.

### 1.2 Launch Claude Code

Navigate to your project directory and start Claude Code:

```
cd /path/to/your/project
claude
```

Claude Code starts in interactive mode. You are now inside a session.

### 1.2b Terminal or IDE? Choose Your Setup

Claude Code works in two modes. You can use either -- or both at the same time.

**VS Code / Cursor extension (recommended for beginners).** Install the Claude Code extension from the marketplace (`Ctrl+Shift+X` -> search "Claude Code" -> Install). You get a graphical chat panel, inline diffs, and you can see files appear in your editor's file tree as Claude creates them. The extension includes a built-in terminal, so you still have CLI access.

**Terminal (full power).** Some features are CLI-only: all slash commands (`/init`, `/memory`, `/resume`), the `!` bash shortcut, tab completion, and MCP server configuration. If you installed the extension, these work in the VS Code integrated terminal too.

**Best of both worlds.** Run the VS Code extension for the graphical experience and open the integrated terminal (`` Ctrl+` ``) when you need CLI-only features. This curriculum works in either mode -- we will note when a feature requires the terminal.

You do not have to choose one forever. The extension and CLI share the same conversation history and project configuration.

**STOP -- What you just did:** You chose your development environment -- terminal, IDE, or both. This is a personal preference, not a locked-in decision. You can switch anytime because the CLI and extension share the same project configuration and conversation history.

### 1.3 Run /init OR Enhance Existing CLAUDE.md

Type this into Claude Code:

```
/init
```

Claude scans your project and generates a `CLAUDE.md` file. If your project already has a `CLAUDE.md`, Claude will read it and suggest enhancements based on what it finds in your codebase.

Read through the generated or updated `CLAUDE.md`. It should contain:

- A project description
- Build and test commands
- Code style conventions
- Key dependencies or frameworks

Since this is your own project, you know it better than Claude does. Review what Claude generated and correct anything that is wrong or incomplete. Add details Claude could not infer -- your deployment process, team conventions, or architectural decisions.

**Engineering value:**
- *Entry-level:* A CLAUDE.md is like onboarding docs for your AI pair programmer -- it remembers your project so you don't re-explain it every session.
- *Mid-level:* On teams, CLAUDE.md ensures every developer's Claude session follows the same conventions -- consistent code style, correct build commands, shared architecture decisions.
- *Senior+:* CLAUDE.md is declarative project configuration for AI tooling -- the same pattern as .editorconfig, .eslintrc, or Makefile, but for your AI assistant. It scales across repos.

**STOP -- What you just did:** You ran `/init` to create or enhance CLAUDE.md for your existing project. Since you already know this codebase, you are the expert -- Claude drafted, you edited. This is a pattern you will use constantly: Claude proposes, you decide.

### 1.4 Tour of CLAUDE.md

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

**STOP -- What you just did:** You now understand the memory hierarchy -- project, local, user, and managed. This matters because it controls what Claude knows and when. Project memory is shared with your team. Local memory is just for you. User memory follows you everywhere.

### 1.5 Keyboard Shortcuts

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
| `Ctrl+O` | Toggle verbose output (then `/` to search transcript) |
| `Ctrl+R` | Reverse search command history |
| `Ctrl+X Ctrl+E` | Open external editor for composing long prompts |
| `/` | Start a command or skill |

Try these now:

1. Type `@` and browse files in your project
2. Type `! git status` to run a shell command
3. Press `Shift+Tab` twice to cycle through modes -- notice the mode indicator
4. Type a long prompt using `Shift+Enter` for multiple lines
5. Press `Ctrl+L` to clear the screen

**Engineering value:**
- *Entry-level:* These shortcuts aren't just convenience -- they're how you stay in flow. Switching between Claude and your terminal without reaching for the mouse keeps you productive.
- *Mid-level:* Plan mode (Shift+Tab) is critical for code review workflows -- you can have Claude analyze and propose changes without executing them, which is how you safely use AI on production code.

**STOP -- What you just did:** You practiced the keyboard shortcuts that keep you in flow. The most important ones to internalize: `Shift+Tab` for plan mode, `@` for file mentions, and `!` for shell commands. These three will be your most-used shortcuts across every remaining module.

### 1.5b Slash Commands

That `/` shortcut you just saw in the table opens up Claude Code's built-in commands. You already know `/init` -- here are a few more worth trying now:

| Command | What It Does |
|---------|-------------|
| `/memory` | Opens your memory files (CLAUDE.md) in your editor so you can view and manage what Claude remembers across sessions |
| `/copy` | Opens an interactive picker that lets you select and copy specific code blocks from the conversation -- handy when Claude generated something you want to paste elsewhere |
| `/simplify` | Asks Claude to simplify complex code or explanations -- useful when a response feels overwhelming |
| `/batch` | Runs commands in batch mode for non-interactive automation |
| `/powerup` | Interactive lessons teaching Claude Code features with animated demos -- a great way to learn new features |
| `/btw` | Ask a quick side question without interrupting Claude's current work -- like raising your hand in class |

Try typing `/` and then pressing `Tab` -- you will see the full list of available commands autocomplete. This is a good habit: whenever you are wondering "can Claude Code do X?", type `/` and Tab to browse what is available.

**STOP -- What you just did:** You explored slash commands and discovered Tab completion for the `/` menu. From here on, whenever you wonder "can Claude Code do X?", your first instinct should be to type `/` and Tab to check.

### 1.6 Explore /memory

Type:

```
/memory
```

This opens your memory files in your system editor. You can directly edit
`CLAUDE.md` here. Since this is your own project, add details that Claude could not have inferred from scanning the codebase -- things like:

- Why the project exists and who it serves
- Architectural decisions and the reasoning behind them
- Common pitfalls or gotchas that trip up new contributors
- Your preferred workflow (how you test, deploy, review code)

Save and close the editor.

**STOP -- What you just did:** You edited CLAUDE.md through `/memory` and gave Claude persistent context about your project. This is how you teach Claude what it needs to know -- not by repeating yourself every session, but by writing it down once in CLAUDE.md.

### 1.7 Exercise

Ask Claude:

```
Read the CLAUDE.md file in this project and explain what it contains.
Then suggest three improvements I could make to it based on what you can
see in the codebase.
```

Review Claude's suggestions. Apply at least one of them by editing `CLAUDE.md`. Since this is your own project, Claude might spot patterns, conventions, or dependencies that you forgot to document. It might also get things wrong -- correct it when it does.

**STOP -- What you just did:** You asked Claude to read and improve its own memory file. This is a powerful pattern -- Claude can analyze and suggest improvements to CLAUDE.md, and you decide what to keep. You are the editor, Claude is the drafter.

### 1.8 Skip -- Your Project Already Exists

Unlike the other learning paths, you do not need to create any starter files. Your project already has its codebase. Instead, take a moment to verify that Claude can see and understand your project:

```
Describe the structure of this project. What languages and frameworks does it
use? What are the main entry points?
```

If Claude's description is wrong or incomplete, correct it and update CLAUDE.md with the accurate information. This ensures Claude has the right mental model of your project going forward.

**STOP -- What you just did:** You verified that Claude understands your existing project structure. Any corrections you made go into CLAUDE.md so Claude gets it right in future sessions. This replaces the file-creation step in other learning paths -- your project is already built, so the goal is to make Claude understand it.

### 1.9 First Commit

Commit the CLAUDE.md and any other configuration files Claude created:

```
! git add CLAUDE.md .claude/
! git commit -m "feat: add Claude Code configuration with CLAUDE.md"
```

**STOP -- What you just did:** You made your first commit with Claude Code configuration. From Module 2 onward, you will commit after every significant step. Building a clean commit history is a professional habit -- it lets you rewind, review, and understand your project's evolution.

### Leaving and Coming Back

You can exit Claude Code at any time with `Ctrl+D` or `/exit`. To pick up where you left off:

- **`claude -c`** -- continues your most recent session in this directory. This is the fastest way to resume.
- **`/resume`** -- opens a session picker so you can choose which session to continue. Use this if you have multiple sessions.
- **`/rename my-session-name`** -- names your current session before you leave, so you can find it easily with `/resume` later.
- **`claude --resume`** -- opens an interactive picker (like `/resume`) from the command line. Useful when you have multiple named sessions and want to choose which one to continue.

Your CLAUDE.md, rules, and project files persist between sessions. Conversation history is restored when you resume, but you may need to re-approve permission prompts.

**Tip:** Before exiting a long session, run `/memory` to save any important context. Claude reads CLAUDE.md at the start of every session, so anything saved there carries forward automatically.

**Pro tip: Multiple Claude sessions in your IDE.** In VS Code, you can open multiple Claude conversations: use the Command Palette (`Ctrl+Shift+P`) -> "Claude Code: Open in New Tab" to run side-by-side conversations. In the terminal, split your terminal pane (`Ctrl+Shift+5` in VS Code) and run `claude` in each. This becomes especially useful in Module 10 when you work with git worktrees and parallel development.

**Engineering value:**
- *Entry-level:* Session persistence means you can work on a problem across days without losing context -- like saving your game.
- *Mid-level:* Named sessions (`/rename`) let you maintain separate contexts for different workstreams -- bug investigation in one, feature work in another.

### 1.10 Session Personalization & Effort

Claude Code has added several ways to customize your session experience since the initial release.

**Color your prompt bar.** Type `/color` and pick a color — this sets your prompt bar's accent color for the session. Try `/color blue` or just `/color` to see options. Use `/color default` to reset.

**Name your sessions.** Start Claude Code with `-n` to name it: `claude -n "My Project"`. You can also rename mid-session with `/rename`. Named sessions are easier to find in `/resume`.

**Set effort level.** Type `/effort` to see the current reasoning depth (low, medium, or high). Try `/effort low` for quick lookups or `/effort high` for deeper reasoning. The effort level shows on the logo spinner.

**Model updates.** Opus 4.6 now defaults to 1M context window (Max/Team/Enterprise) and 64k output tokens. Use `modelOverrides` in settings to map model picker entries to custom provider model IDs.

> **STOP** — Try `/color` and `/effort` before continuing. Notice how the prompt bar and spinner change.

### Checkpoint

You just configured Claude Code for your existing project, taught it about your codebase, and made your first commit. That is a real foundation -- everything from here builds on it.

- [ ] Your project directory has `git init` completed (or was already a git repo)
- [ ] `CLAUDE.md` exists and accurately describes your project
- [ ] Claude can describe your project structure, languages, and entry points correctly
- [ ] You ran `/init` and `/memory` successfully
- [ ] You tried all keyboard shortcuts from the table above
- [ ] You know how to exit (`Ctrl+D`) and resume (`claude -c`) a session
- [ ] You made your first commit with Claude Code configuration
- [ ] Tried `/color` and `/effort` to customize your session
