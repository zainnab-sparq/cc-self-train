# Module 5 -- Hooks

**CC features:** SessionStart, PostToolUse, Stop hooks, matchers, hook
scripting, settings.json

> **Persona — Collaborator:** Ask before telling, give pointers not answers. "What do you think…", "Try this and tell me…"

### 5.1 Hook Lifecycle Overview

> **Why this step:** Hooks are Claude Code's automation layer. While skills require you to type a command, hooks fire automatically at specific moments -- when a session starts, after a file is written, when Claude finishes responding. This is how you build guardrails and quality gates that work without you remembering to invoke them.

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

### 5.2 Create a SessionStart Hook

This hook will inject a site summary into context when Claude starts. Describe what you want the hook to do:

> "Create a SessionStart hook that runs a Python script (.claude/hooks/site-summary.py) to count my HTML pages, total CSS size, and images, then prints a one-line summary. Add it to .claude/settings.json as a SessionStart hook."

Claude will create both the Python script and the settings.json configuration. For SessionStart hooks, stdout is added to Claude's context automatically.

Restart Claude Code (exit and re-launch `claude`) to test it. You should see
the stats injected on startup.

> **STOP -- What you just did:** You created your first hook -- a SessionStart hook that runs a Python script every time Claude Code launches. The script counts your site's pages and injects a summary into Claude's context. This means Claude always knows the current state of your site without you having to explain it. SessionStart hooks are perfect for injecting project status, environment info, or reminders.

> **Engineering value:**
> - *Entry-level:* Hooks automate the checks you'd forget to do manually — like a spell-checker that runs every time you save.
> - *Mid-level:* SessionStart hooks inject environment context so Claude always knows the current state of your project. No more 'Claude, remember we're using Postgres now' at the start of every session.
> - *Senior+:* Hooks are event-driven middleware for your AI workflow — the same pattern as git hooks, CI/CD pipelines, and Lambda triggers. You're building an automated quality pipeline that runs on every interaction.

Ready to build a PostToolUse hook for HTML validation?

### 5.3 Create a PostToolUse Hook

This hook validates HTML structure after Claude writes or edits an HTML file. Tell Claude what you want it to check:

> "Create a PostToolUse hook that validates HTML files after they are written or edited. The Python script (.claude/hooks/validate-html.py) should check for doctype, lang attribute, title element, and basic tag matching. Use a matcher of 'Write|Edit' so it only fires on those tools. Remember, PostToolUse hooks are feedback only -- they cannot block."

Claude will ask you about the specifics of the validation or handle them based on the description. Review the script it creates to make sure the checks match what you care about.

> **STOP -- What you just did:** You created a PostToolUse hook with a matcher. The matcher `"Write|Edit"` ensures this hook only fires when Claude writes or edits a file -- not on every tool call. PostToolUse hooks cannot block actions (the file is already written), but they give Claude immediate feedback. If the validator finds issues, Claude sees them in its next response and can fix them automatically.

> **Quick check before continuing:**
> - [ ] `.claude/settings.json` has both SessionStart and PostToolUse hooks configured
> - [ ] `.claude/hooks/` contains `site-summary.py` and `validate-html.py`
> - [ ] You restarted Claude Code and saw the site summary on startup

### 5.4 Create a Stop Hook

This hook checks all internal links before Claude stops to catch broken links. Describe the behavior you want:

> "Create a Stop hook that scans all HTML files for internal links and checks if the linked files actually exist. If any broken links are found, it should block (exit 2) and report which page links to which missing file. Add it to .claude/settings.json."

The key difference from PostToolUse: a Stop hook with exit code 2 is *blocking* -- it forces Claude to address the issue before moving on.

> **Why this step:** Stop hooks are different from PostToolUse hooks -- they run once when Claude finishes its entire response, not after each individual tool call. A Stop hook with exit code 2 is *blocking*: it forces Claude to address the issue before moving on. This makes Stop hooks ideal for final validation checks like broken link detection.

> **Engineering value:**
> - *Entry-level:* A blocking Stop hook means Claude can't finish until the check passes — like a teacher who won't let you submit until you've spell-checked.
> - *Mid-level:* In team repos, Stop hooks enforce quality gates that individual developers can't skip. Broken links, failing tests, lint errors — they get caught before the code leaves Claude's hands.
> - *Senior+:* This is shift-left testing in its most extreme form. Instead of catching issues in CI (minutes later) or code review (hours later), hooks catch them in the same second the code is written.

Want to learn about matchers and hook scripting?

### 5.4b What the Stop Hook Receives

The Stop hook input includes a `last_assistant_message` field -- this is the last message Claude sent before the hook fired. What could you do with that? You could inspect it to check whether Claude mentioned creating a file it did not actually create, or whether the response included a TODO it forgot to address. The same field is available in SubagentStop hooks.

Also worth knowing: hooks are not limited to running local scripts. You can use `"type": "http"` with a `"url"` field to POST hook events to a remote URL instead. This is useful if you want an external service to process hook events -- a CI server, a logging endpoint, or a webhook receiver. Check `context/hooks.txt` for the full format.

### 5.5 Matchers, Timeouts, and Scripting

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

### 5.7 Exercise: Trigger Each Hook

1. **SessionStart:** Exit and restart `claude`. Check that the site summary appears.
2. **PostToolUse:** Ask Claude to create a new HTML file. Verify the validator ran.
3. **Stop:** Ask Claude a question and let it finish. Verify the link checker ran.

Use `Ctrl+O` (verbose mode) to see hook execution details.

> **STOP -- What you just did:** You built a three-layer hook system: SessionStart injects context at launch, PostToolUse validates individual file writes, and Stop performs a final quality check when Claude finishes. These layers work together without you doing anything -- they are the automated quality gates that catch mistakes before they accumulate. This is how professional teams use Claude Code: automate the boring checks so you can focus on the creative work.

### Checkpoint

Your site now has automated quality gates. Hooks catch mistakes the moment they happen -- you will never go back to checking manually.

- [ ] `.claude/settings.json` exists with hook configuration
- [ ] SessionStart hook injects site summary on session start
- [ ] PostToolUse hook validates HTML structure after writes/edits
- [ ] Stop hook checks for broken internal links before Claude stops
- [ ] Matchers filter correctly (Write|Edit, not all tools)
- [ ] You verified each hook fires by triggering it and checking output
