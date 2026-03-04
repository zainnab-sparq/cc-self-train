# Module 5 -- Hooks

**CC features:** SessionStart, PostToolUse, Stop hooks, matchers, hook
scripting, settings.json

> **Persona — Collaborator:** Ask before telling, give pointers not answers. "What do you think…", "Try this and tell me…"

## 5.1 Hook Lifecycle Overview

> **Why this step:** Hooks let you automate actions at key moments in Claude Code's lifecycle -- when a session starts, after a file is written, before Claude stops responding. They are the foundation of quality automation: auto-formatting, auto-testing, injecting context, and blocking dangerous operations. Understanding the hook lifecycle is essential before you start writing hooks.

Hooks fire at specific points during a Claude Code session:

| Hook Event | When It Fires |
|-----------|--------------|
| `SessionStart` | Session begins or resumes |
| `UserPromptSubmit` | User submits a prompt |
| `PreToolUse` | Before a tool executes |
| `PermissionRequest` | When a permission dialog appears |
| `PostToolUse` | After a tool succeeds |
| `Stop` | Claude finishes responding |
| `SubagentStop` | When a subagent finishes |
| `PreCompact` | Before context compaction |
| `SessionEnd` | Session terminates |

Hooks are configured in settings files:
- `.claude/settings.json` -- project hooks (shared with team)
- `.claude/settings.local.json` -- local hooks (personal, not committed)
- `~/.claude/settings.json` -- user hooks (all projects)

## 5.2 Create a SessionStart Hook

This hook will inject project stats into context when Claude starts. Describe to Claude what you want: a script that counts your stored items and prints a summary, wired up as a SessionStart hook.

> "Create a SessionStart hook that counts the number of notes, snippets, bookmarks, and templates in storage and prints a one-line summary. Create the script in .claude/hooks/ and add the hook entry to .claude/settings.json. Use whichever scripting language makes sense for my setup."

Claude may ask about your OS or scripting preference (bash vs. Python). For SessionStart hooks, stdout is added to Claude's context automatically.

Restart Claude Code (exit and re-launch `claude`) to test it. You should see
the stats injected on startup.

> **STOP -- What you just did:** You created your first hook -- a script that runs automatically when Claude starts a session. The key insight is that SessionStart hooks inject their stdout into Claude's context. This means Claude *starts every session knowing* how many notes, snippets, and bookmarks you have. You did not have to tell it -- the hook did it for you. This pattern is powerful for any project state you want Claude to be aware of from the start.

> **Engineering value:**
> - *Entry-level:* Hooks automate the checks you'd forget to do manually — like a spell-checker that runs every time you save.
> - *Mid-level:* SessionStart hooks inject environment context so Claude always knows the current state of your project. No more 'Claude, remember we're using Postgres now' at the start of every session.
> - *Senior+:* Hooks are event-driven middleware for your AI workflow — the same pattern as git hooks, CI/CD pipelines, and Lambda triggers. You're building an automated quality pipeline that runs on every interaction.

Ready to build a PostToolUse hook for auto-formatting?

## 5.3 Create a PostToolUse Hook

This hook auto-formats files after Claude writes or edits them. Tell Claude which formatter you use and ask it to wire it up as a PostToolUse hook that triggers on Write and Edit operations.

> "Add a PostToolUse hook to settings.json that runs my formatter whenever Claude writes or edits a file. I use [your formatter -- e.g., black, prettier, gofmt, rustfmt]. Use a Write|Edit matcher and make it fail gracefully if the formatter isn't installed."

> **Quick check before continuing:**
> - [ ] `.claude/settings.json` has a SessionStart hook entry
> - [ ] `.claude/settings.json` has a PostToolUse hook entry with a `Write|Edit` matcher
> - [ ] The SessionStart hook prints stats when you restart Claude

## 5.4 Create a Stop Hook

> **Why this step:** A Stop hook runs after Claude finishes responding but before it hands control back to you. By running the test suite at this point, you catch breakage *immediately* -- Claude broke something and you know before you even type your next prompt. If the tests fail, the hook can block and feed the failures back to Claude for automatic fixing.

> **Engineering value:**
> - *Entry-level:* A blocking Stop hook means Claude can't finish until the check passes — like a teacher who won't let you submit until you've spell-checked.
> - *Mid-level:* In team repos, Stop hooks enforce quality gates that individual developers can't skip. Broken links, failing tests, lint errors — they get caught before the code leaves Claude's hands.
> - *Senior+:* This is shift-left testing in its most extreme form. Instead of catching issues in CI (minutes later) or code review (hours later), hooks catch them in the same second the code is written.

This hook runs the test suite after Claude finishes to verify nothing is broken. Describe what you want to Claude -- it needs to handle the infinite loop case (the hook itself triggers Claude, which triggers the hook again).

> "Create a Stop hook that runs my test suite after Claude finishes responding. If tests fail, it should block and feed the failures back so Claude can fix them. Make sure it handles the infinite loop problem -- if it's already running inside a Stop hook, it should exit cleanly. Add it to settings.json."

Claude will ask about your test command if it is not obvious. It will also need to figure out the right way to detect re-entrancy for your setup.

## 5.4b What the Stop Hook Receives

One thing to notice: the Stop hook input includes a `last_assistant_message` field containing the last message Claude sent before the hook fired. Think about what you could do with that -- you could scan it for unfinished TODOs, verify that Claude actually did what it said it did, or log it for review. SubagentStop hooks get the same field.

While you are here -- hooks are not limited to local scripts. You can also use `"type": "http"` with a `"url"` field to POST hook events to a remote endpoint instead of running a command. Useful if you want to send hook data to a logging service or a CI system. See `context/hooks.txt` for the format.

## 5.5 Matchers, Timeouts, and Scripting

Matchers filter which tools trigger a hook. Key patterns:

| Pattern | Matches |
|---------|---------|
| `"Write"` | Exactly the Write tool |
| `"Write\|Edit"` | Write or Edit tools |
| `"Bash(npm test*)"` | Bash commands starting with `npm test` |
| `"*"` | All tools |
| `"mcp__.*"` | All MCP tools |

Add `"timeout": 30` to any hook command to override the default 60-second
timeout. Every hook script receives JSON on stdin, uses exit codes to
communicate (0 = success, 2 = blocking error), and can access
`$CLAUDE_PROJECT_DIR` for the project root.

> **STOP -- What you just did:** You learned about matchers and timeouts -- the configuration layer that controls *when* and *how long* hooks run. Matchers prevent hooks from firing on every tool call (which would slow everything down). Timeouts prevent runaway scripts from freezing your session. These two settings are what make hooks practical for real workflows rather than just demos.

Want to verify all three hooks are working?

## 5.7 Exercise: Trigger Each Hook

1. **SessionStart:** Exit and restart `claude`. Check that stats appear.
2. **PostToolUse:** Ask Claude to create a new file. Verify the formatter ran.
3. **Stop:** Ask Claude a question and let it finish. Verify tests ran.

Use `Ctrl+O` (verbose mode) to see hook execution details.

## Checkpoint

Your toolkit now automates its own quality checks. Hooks catch mistakes the moment they happen -- no manual checking required.

- [ ] `.claude/settings.json` exists with hook configuration
- [ ] SessionStart hook injects project stats on session start
- [ ] PostToolUse hook auto-formats files after writes/edits
- [ ] Stop hook runs tests before Claude stops
- [ ] Matchers filter correctly (Write|Edit, not all tools)
- [ ] You verified each hook fires by triggering it and checking output
