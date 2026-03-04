# Module 1 -- Setup & First Contact

**CC features:** CLAUDE.md, /init, /memory, interactive mode, keyboard shortcuts

> **Persona — Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

> **Used `/start`?** Module 1 was completed during onboarding. Jump to [Module 2 -- Blueprint & Build](02-blueprint.md).

### Step 1: Create Your Project

Open a terminal in the cc-self-train directory and create the project under `workspace/`:

```
mkdir -p workspace/nexus-gateway
cd workspace/nexus-gateway
git init
```

### Step 2: Launch Claude Code

```
claude
```

You are now in an interactive Claude Code session. This is your primary interface for the entire project.

### Step 2b: Terminal or IDE? Choose Your Setup

Claude Code works in two modes. You can use either — or both at the same time.

**VS Code / Cursor extension (recommended for beginners).** Install the Claude Code extension from the marketplace (`Ctrl+Shift+X` → search "Claude Code" → Install). You get a graphical chat panel, inline diffs, and you can see files appear in your editor's file tree as Claude creates them. The extension includes a built-in terminal, so you still have CLI access.

**Terminal (full power).** Some features are CLI-only: all slash commands (`/init`, `/memory`, `/resume`), the `!` bash shortcut, tab completion, and MCP server configuration. If you installed the extension, these work in the VS Code integrated terminal too.

**Best of both worlds.** Run the VS Code extension for the graphical experience and open the integrated terminal (`` Ctrl+` ``) when you need CLI-only features. This curriculum works in either mode — we will note when a feature requires the terminal.

You do not have to choose one forever. The extension and CLI share the same conversation history and project configuration.

### Step 3: Run /init

Type the following into Claude Code:

```
/init
```

Claude will scan your directory and generate a `CLAUDE.md` file. Since the directory is mostly empty, the file will be minimal. That is fine -- you will build it up throughout the project.

> **Engineering value:**
> - *Entry-level:* A CLAUDE.md is like onboarding docs for your AI pair programmer — it remembers your project so you don't re-explain it every session.
> - *Mid-level:* On teams, CLAUDE.md ensures every developer's Claude session follows the same conventions — consistent code style, correct build commands, shared architecture decisions.
> - *Senior+:* CLAUDE.md is declarative project configuration for AI tooling — the same pattern as .editorconfig, .eslintrc, or Makefile, but for your AI assistant. It scales across repos.

### Step 4: Tour of CLAUDE.md

Ask Claude: `Read CLAUDE.md and explain what each section does and why it matters`

CLAUDE.md is Claude's persistent memory for your project. It loads automatically every session and can contain build commands, architecture notes, coding conventions, and workflow preferences.

### Step 5: Keyboard Shortcuts

Practice each shortcut in the table below. Do not skip this -- muscle memory with these shortcuts saves significant time across the remaining 9 modules.

| Shortcut | What It Does | Try It Now |
|----------|-------------|------------|
| `Tab` | Accept a suggestion or autocomplete | Type a partial file path and press Tab |
| `Shift+Tab` | Toggle between Plan mode and Act mode | Press it twice to cycle back |
| `Ctrl+C` | Cancel current generation or clear input | Start a long prompt, then cancel |
| `Ctrl+L` | Clear terminal screen (keeps history) | Clear the screen, then scroll up |
| `@` | File path autocomplete | Type `@CLAUDE` and see the suggestion |
| `!` | Bash mode -- run a shell command directly | Type `! git status` |
| `Shift+Enter` or `\` + `Enter` | Multiline input | Type a two-line message |
| `Esc Esc` | Rewind conversation/code to a previous state | Press Escape twice |
| `Ctrl+O` | Toggle verbose output | See detailed tool usage |
| `Ctrl+R` | Reverse search command history | Search through previous inputs |

> **Engineering value:**
> - *Entry-level:* These shortcuts aren't just convenience — they're how you stay in flow. Switching between Claude and your terminal without reaching for the mouse keeps you productive.
> - *Mid-level:* Plan mode (Shift+Tab) is critical for code review workflows — you can have Claude analyze and propose changes without executing them, which is how you safely use AI on production code.

### Step 5b: Slash Commands

The `/` shortcut from the table above opens Claude Code's built-in commands. You used `/init` already -- here are a few more to know about:

| Command | What It Does |
|---------|-------------|
| `/memory` | Opens your memory files (CLAUDE.md) in your editor -- view and manage what Claude remembers across sessions |
| `/copy` | Interactive picker to select and copy specific code blocks from the conversation into your clipboard |
| `/simplify` | Asks Claude to simplify complex code or explanations -- useful when a response is more detailed than you need |
| `/batch` | Runs commands in batch mode for non-interactive automation |

Try typing `/` and pressing `Tab` to see the full list. Tab completion works here just like it does for file paths -- it is the fastest way to discover commands you did not know existed.

### Step 6: Explore /memory

Type `/memory` to open CLAUDE.md in your system editor. Add a project overview, placeholder commands (start server, run tests, check health), and an architecture section to be filled in Module 2. Save and close -- Claude now has this context in every future session.

### Step 7: Exercise

Ask Claude: `Explain what CLAUDE.md is, where it lives in the hierarchy, and how it differs from .claude/rules/ files. Show the memory hierarchy from most to least specific.`

Verify Claude explains: CLAUDE.md (project) > CLAUDE.local.md (local/personal) > ~/.claude/CLAUDE.md (user-global), plus .claude/rules/ for modular, path-scoped rules.

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

You just set up a gateway project, configured Claude Code's memory, learned the keyboard shortcuts, and explored the memory hierarchy. That's a real foundation -- everything from here builds on it.

- [ ] `workspace/nexus-gateway/` directory exists with `git init` completed
- [ ] CLAUDE.md exists with project overview content
- [ ] You ran `/init` successfully
- [ ] You can use `Shift+Tab` to toggle plan mode
- [ ] You tried all 10 keyboard shortcuts from the table
- [ ] You opened `/memory` and edited CLAUDE.md
- [ ] You know how to exit (`Ctrl+D`) and resume (`claude -c`) a session
- [ ] You can explain the memory hierarchy
