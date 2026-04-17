# Module 5 -- Hooks

<!-- progress:start -->
**Progress:** Module 5 of 10 `[█████░░░░░]` 50%

**Estimated time:** ~60-75 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** SessionStart, PostToolUse, Stop hooks, matchers, hook
scripting, settings.json

**Persona -- Collaborator:** Ask before telling, give pointers not answers. "What do you think...", "Try this and tell me..."

</details>

> **First, a plain-English definition:** A **hook** is a small script that runs automatically at a specific moment -- like when a session starts, when Claude edits a file, or when Claude finishes responding. These are **not** React hooks. Think of them as "when X happens, automatically do Y" rules. You configure them in `.claude/settings.json`. This module walks you through building several. See the [glossary](../../../GLOSSARY.md) for other terms you may hit.

### 5.1 Hook Lifecycle Overview

**Why this step:** Hooks are Claude Code's automation layer. While skills require you to type a command, hooks fire automatically at specific moments -- when a session starts, after a file is written, when Claude finishes responding. This is how you build guardrails and quality gates that work without you remembering to invoke them.

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

This hook will inject a project status summary into context when Claude starts. Think about what information would help Claude understand your project's current state every session -- file counts by type, git status, recent changes, test summary, dependency health.

Describe what you want the hook to do:

```
Create a SessionStart hook that runs a script (.claude/hooks/project-status.py) to summarize my project's current state -- count source files by type, show git branch and recent commits, check if tests pass, and note any uncommitted changes. Print a concise summary. Add it to .claude/settings.json as a SessionStart hook.
```

Claude will create both the script and the settings.json configuration. For SessionStart hooks, stdout is added to Claude's context automatically.

Restart Claude Code (exit and re-launch `claude`) to test it. You should see the project status summary injected on startup.

**STOP -- What you just did:** You created your first hook -- a SessionStart hook that runs a script every time Claude Code launches. The script summarizes your project's state and injects it into Claude's context. This means Claude always knows the current state of your project without you having to explain it. SessionStart hooks are perfect for injecting project status, environment info, or reminders.

**Engineering value:**
- *Entry-level:* Hooks automate the checks you'd forget to do manually -- like a spell-checker that runs every time you save.
- *Mid-level:* SessionStart hooks inject environment context so Claude always knows the current state of your project. No more 'Claude, remember we switched to the v2 API' at the start of every session.
- *Senior+:* Hooks are event-driven middleware for your AI workflow -- the same pattern as git hooks, CI/CD pipelines, and Lambda triggers. You're building an automated quality pipeline that runs on every interaction.

Ready to build a PostToolUse hook for your language's toolchain?

### 5.3 Create a PostToolUse Hook

This hook runs your language's linter or formatter after Claude writes or edits a source file. Pick the tool that fits your stack:

- **Python:** ruff, black, flake8, mypy
- **JavaScript/TypeScript:** eslint, prettier, tsc
- **Go:** go fmt, go vet, golangci-lint
- **Rust:** cargo fmt, cargo clippy
- **Ruby:** rubocop
- **Java/Kotlin:** ktlint, checkstyle

Tell Claude what you want:

```
Create a PostToolUse hook that runs [your linter/formatter] on source files after they are written or edited. The script (.claude/hooks/lint-on-write.py) should only check files with [your extensions -- e.g., .py, .js, .ts]. Use a matcher of 'Write|Edit' so it only fires on those tools. Remember, PostToolUse hooks are feedback only -- they cannot block.
```

Claude will ask about the specifics or handle them based on the description. Review the script to make sure it targets the right file types and runs the right tool.

**STOP -- What you just did:** You created a PostToolUse hook with a matcher. The matcher `"Write|Edit"` ensures this hook only fires when Claude writes or edits a file -- not on every tool call. PostToolUse hooks cannot block actions (the file is already written), but they give Claude immediate feedback. If the linter finds issues, Claude sees them in its next response and can fix them automatically.

**Quick check before continuing:**
- [ ] `.claude/settings.json` has both SessionStart and PostToolUse hooks configured
- [ ] `.claude/hooks/` contains your project status script and your linter script
- [ ] You restarted Claude Code and saw the project status summary on startup

### 5.4 Create a Stop Hook

This hook runs a validation check relevant to your project before Claude finishes. Think about what should always be true after Claude makes changes:

- **Tests pass** -- run your test suite
- **Lint is clean** -- no new lint errors introduced
- **No TODO markers left** -- Claude should resolve all TODOs it creates
- **Type checking passes** -- no new type errors
- **Build succeeds** -- the project still compiles/bundles

Describe the behavior you want:

```
Create a Stop hook that runs [your validation -- e.g., test suite, lint check, type check] after Claude finishes responding. If the check fails, it should block (exit 2) and report what failed. Add it to .claude/settings.json.
```

The key difference from PostToolUse: a Stop hook with exit code 2 is *blocking* -- it forces Claude to address the issue before moving on.

**Common gotcha — feedback loops:** If a Stop hook writes to stdout with exit code 0, Claude may treat that output as new input and continue responding — which triggers the Stop hook again, creating an infinite loop. To avoid this: use **stderr** (not stdout) when blocking with exit 2, and output **nothing** to stdout on success (exit 0). Pattern: silent exit 0 = Claude stops cleanly. Exit 2 with stderr = Claude sees the error and must fix it.

**Why this step:** Stop hooks are different from PostToolUse hooks -- they run once when Claude finishes its entire response, not after each individual tool call. A Stop hook with exit code 2 is *blocking*: it forces Claude to address the issue before moving on. This makes Stop hooks ideal for final validation checks that ensure your project stays healthy.

**Engineering value:**
- *Entry-level:* A blocking Stop hook means Claude can't finish until the check passes -- like a teacher who won't let you submit until you've spell-checked.
- *Mid-level:* In team repos, Stop hooks enforce quality gates that individual developers can't skip. Failing tests, lint errors, type errors -- they get caught before the code leaves Claude's hands.
- *Senior+:* This is shift-left testing in its most extreme form. Instead of catching issues in CI (minutes later) or code review (hours later), hooks catch them in the same second the code is written.

Want to learn about matchers and hook scripting?

### 5.4b What the Stop Hook Receives

The Stop hook input includes a `last_assistant_message` field -- this is the last message Claude sent before the hook fired. What could you do with that? You could inspect it to check whether Claude mentioned creating a file it did not actually create, or whether the response included a TODO it forgot to address. The same field is available in SubagentStop hooks.

Also worth knowing: hooks are not limited to running local scripts. You can use `"type": "http"` with a `"url"` field to POST hook events to a remote URL instead. This is useful if you want an external service to process hook events -- a CI server, a logging endpoint, or a webhook receiver. Check `context/hooks.txt` for the full format.

### 5.5 Matchers & Timeouts

Matchers filter which tools trigger a hook. Key patterns:

| Pattern | Matches |
|---------|---------|
| `"Write"` | Exactly the Write tool |
| `"Write\|Edit"` | Write or Edit tools |
| `"Bash(npm test*)"` | Bash commands starting with `npm test` |
| `"*"` | All tools |
| `"mcp__.*"` | All MCP tools |

Add `"timeout": 30` to any hook command to override the default 60-second
timeout. Matchers prevent hooks from firing on every tool call (which would slow everything down). Timeouts prevent runaway scripts from freezing your session.

### 5.6 Shell Scripting with Hook Input

Hooks receive JSON via stdin with fields like `session_id`, `hook_event_name`, `tool_name`, `tool_input`, and `tool_response`. Every hook script uses exit codes to communicate (0 = success, 2 = blocking error) and can access `$CLAUDE_PROJECT_DIR` for the project root. Extract values with jq:

```
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')
```

Ask Claude to show you the full input schema for each hook type you configured.

### 5.7 Exercise: Trigger Each Hook

1. **SessionStart:** Exit and restart `claude`. Check that the project status summary appears.
2. **PostToolUse:** Ask Claude to create or edit a source file in your project. Verify the linter ran.
3. **Stop:** Ask Claude a question and let it finish. Verify the validation check ran.

Use `Ctrl+O` (verbose mode) to see hook execution details.

**STOP -- What you just did:** You built a three-layer hook system: SessionStart injects project context at launch, PostToolUse lints individual file writes, and Stop performs a final quality check when Claude finishes. These layers work together without you doing anything -- they are the automated quality gates that catch mistakes before they accumulate. This is how professional teams use Claude Code: automate the boring checks so you can focus on the creative work.

### 5.8 New Hook Events

Five new hook events have been added. Which ones would be most useful for your project?

**`StopFailure`** (v2.1.78) -- fires when a turn ends due to an API error (rate limit, auth failure, etc.). Use for alerting or recovery. The input includes `error` type and `error_details`.

**`PostCompact`** (v2.1.76) -- fires after compaction completes. Matcher values: `manual` (from `/compact`) or `auto` (context window full). Input includes `compact_summary`.

**`InstructionsLoaded`** (v2.1.69) -- fires when CLAUDE.md or `.claude/rules/*.md` files are loaded. Matcher values: `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`. Great for audit logging.

**`Elicitation` / `ElicitationResult`** (v2.1.76) -- intercept MCP server input requests. `Elicitation` fires when a server asks for input; `ElicitationResult` fires before the response is sent back. Use to auto-respond or validate.

Hook events now also include `agent_id` and `agent_type` fields when firing inside subagents (v2.1.69).

**`TaskCreated`** (v2.1.84) -- fires when a task is created via `TaskCreate`. Use for auditing task creation or triggering workflows when new tasks appear.

Try wiring up a `PostCompact` hook that logs when auto-compaction happens -- what would you put in the command?

- **PreCompact blocking** (v2.1.105): PreCompact hooks can now block compaction by exiting with code 2 or returning `{"decision":"block"}`. Use matcher `auto` to block only automatic compaction while allowing manual `/compact`.
- **Settings resilience** (v2.1.101): Unrecognized hook event names in `settings.json` no longer cause the entire file to be ignored -- only the unrecognized event is skipped.

> **STOP** -- Add a hook for one of the new events and test it.

### 5.9 Conditional Hooks & Reactive Events

Two features that transform what hooks can do:

**The `if` field.** Hooks can now include an `if` field using permission rule syntax to filter when they fire. Instead of a hook running on every Bash command, you can scope it: `"if": "Bash(git *)"` makes it fire only on git commands. This reduces overhead and makes hooks surgical.

**Reactive events: `CwdChanged` and `FileChanged`.** These fire when the working directory changes or when files change on disk. Combined with `if`, you can build reactive automation -- a hook that runs your linter only when source files change, or one that loads different environment variables when you move between directories.

Ask Claude to create a reactive hook. Something like:

```
Create a FileChanged hook that runs a validation script only when source files change in your project's main source directory. Use the if field to scope it. Add it to .claude/settings.json.
```

> **STOP** -- Create a conditional hook using the `if` field and test a reactive event hook.

### Choose Your Battles (Hooks Edition)

You've seen the full hook lifecycle. Resist the urge to instrument every event. Each hook runs on every matching tool call -- cumulative latency and complexity adds up fast.

**Rule of thumb:** Start with **2 hooks**: one SessionStart (for context injection) and one PostToolUse or Stop (for quality gating). Add a third only if a specific pain point emerges.

### Checkpoint

Your project now has automated quality gates. Hooks catch mistakes the moment they happen -- you will never go back to checking manually.

- [ ] Created a conditional hook using `if` field and a reactive event hook
- [ ] `.claude/settings.json` exists with hook configuration
- [ ] SessionStart hook injects project status summary on session start
- [ ] PostToolUse hook runs your linter/formatter after writes/edits
- [ ] Stop hook runs your validation check before Claude stops
- [ ] Matchers filter correctly (Write|Edit, not all tools)
- [ ] You verified each hook fires by triggering it and checking output
- [ ] Wired up a hook using one of the new hook events
