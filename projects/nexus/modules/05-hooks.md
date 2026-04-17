# Module 5 -- Hooks

<!-- progress:start -->
**Progress:** Module 5 of 10 `[█████░░░░░]` 50%

**Estimated time:** ~60-75 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** SessionStart, PostToolUse, Stop hooks, matchers, hook scripting, settings.json

**Persona -- Collaborator:** Ask before telling, give pointers not answers. "What do you think...", "Try this and tell me..."

</details>

> **First, a plain-English definition:** A **hook** is a small script that runs automatically at a specific moment -- like when a session starts, when Claude edits a file, or when Claude finishes responding. These are **not** React hooks. Think of them as "when X happens, automatically do Y" rules. You configure them in `.claude/settings.json`. This module walks you through building several. See the [glossary](../../../GLOSSARY.md) for other terms you may hit.

### 5.1 Hook Lifecycle Overview

Hooks are custom shell commands that fire at specific points during a Claude Code session. They are configured in `.claude/settings.json` (project) or `~/.claude/settings.json` (user).

Key hook events you will use in this module:

| Event | When It Fires | Use Case |
|-------|--------------|----------|
| SessionStart | Session begins or resumes | Inject gateway status into context |
| PostToolUse | After a tool succeeds | Auto-lint config after writes |
| Stop | Claude finishes responding | Run tests before stopping |

**Why this step:** A SessionStart hook runs every time you launch Claude Code, automatically injecting information into context. Instead of manually telling Claude "the gateway is running on port 3000 with 5 routes," the hook does it for you. This is how you eliminate repetitive setup at the start of every session.

### 5.2 SessionStart Hook -- Inject Gateway Status

Ask Claude to create a SessionStart hook script that checks whether the gateway is running and reports its state. Describe what you want the script to do -- check the health endpoint, count configured routes, and print a summary.

```
Create a SessionStart hook that checks if the gateway is running by hitting the /health endpoint, counts how many routes are configured, and prints a status summary. Put the script in .claude/hooks/gateway-status.sh and wire it up in .claude/settings.json.
```

Claude will create the script and configure the hook. The key: stdout from a SessionStart hook gets injected into Claude's context automatically. Adjust the script if your config format is different from what Claude assumes -- tell it your actual format.

Test it: exit Claude Code and relaunch. The gateway status appears in context automatically.

**STOP -- What you just did:** You created your first hook and wired it into `.claude/settings.json`. The key insight: anything a SessionStart hook prints to stdout becomes part of Claude's context automatically. Claude now knows the gateway's status without you saying a word. You will use this pattern whenever there is information Claude should have at the start of every session.

**Engineering value:**
- *Entry-level:* Hooks automate the checks you'd forget to do manually -- like a spell-checker that runs every time you save.
- *Mid-level:* SessionStart hooks inject environment context so Claude always knows the current state of your project. No more 'Claude, remember we're using Postgres now' at the start of every session.
- *Senior+:* Hooks are event-driven middleware for your AI workflow -- the same pattern as git hooks, CI/CD pipelines, and Lambda triggers. You're building an automated quality pipeline that runs on every interaction.

Want to build a PostToolUse hook for config validation?

### 5.3 PostToolUse Hook -- Auto-Lint Config Files

**Why this step:** PostToolUse hooks fire after Claude successfully uses a tool. By validating config files right after Claude writes them, you catch errors immediately -- before they cause a confusing runtime failure minutes later. This is "shift left" validation: catch problems at write time, not at run time.

Ask Claude to create a PostToolUse hook that validates config files after they are written or edited. Describe the behavior -- it should check if the file is a config file (YAML, JSON, TOML), validate it, and report errors.

```
Create a PostToolUse hook that validates config files after Claude writes or edits them. If the file is JSON, YAML, or TOML, parse it and fail with exit code 2 if it's invalid. Put the script in .claude/hooks/validate-config.sh and add it to settings.json with a matcher for Write and Edit tools.
```

Claude will create the validation script and add a PostToolUse entry to `.claude/settings.json` with a **matcher** of `"Write|Edit"`, which means it fires only when Claude uses those specific tools. Matchers are case-sensitive and support regex.

**Quick check before continuing:**
- [ ] SessionStart hook injects gateway status when you launch Claude Code
- [ ] PostToolUse hook validates config files after Claude writes them
- [ ] Both hooks are registered in `.claude/settings.json`
- [ ] You understand that matchers (`"Write|Edit"`) control which tool calls trigger the hook

### 5.4 Stop Hook -- Run Tests Before Stopping

**Why this step:** A Stop hook acts as a quality gate -- it runs when Claude finishes a response and can *block* Claude from stopping if something is wrong (exit code 2). This prevents Claude from declaring "done" while tests are failing.

**Engineering value:**
- *Entry-level:* A blocking Stop hook means Claude can't finish until the check passes -- like a teacher who won't let you submit until you've spell-checked.
- *Mid-level:* In team repos, Stop hooks enforce quality gates that individual developers can't skip. Broken links, failing tests, lint errors -- they get caught before the code leaves Claude's hands.
- *Senior+:* This is shift-left testing in its most extreme form. Instead of catching issues in CI (minutes later) or code review (hours later), hooks catch them in the same second the code is written.

A Stop hook fires when Claude finishes a response. Exit code 2 blocks Claude from stopping. Ask Claude to create one that runs your tests before allowing completion.

```
Create a Stop hook that runs my test suite when you finish responding. If tests fail, block with exit code 2 and show the failure output. Make sure to avoid infinite loops -- if the hook itself triggers a stop, it should exit cleanly. Add it to settings.json with a 30-second timeout.
```

Claude will ask what your test command is (pytest, npm test, cargo test, etc.) and create the script accordingly. It will also add the Stop hook entry to `.claude/settings.json`.

**Common gotcha — feedback loops:** If a Stop hook writes to stdout with exit code 0, Claude may treat that output as new input and continue responding — which triggers the Stop hook again, creating an infinite loop. To avoid this: use **stderr** (not stdout) when blocking with exit 2, and output **nothing** to stdout on success (exit 0). Pattern: silent exit 0 = Claude stops cleanly. Exit 2 with stderr = Claude sees the error and must fix it.

**STOP -- What you just did:** You now have three hooks covering three different lifecycle events: SessionStart (inject context on launch), PostToolUse (validate after writes), and Stop (block completion until tests pass). Together, these form an automated safety net around your development workflow. The exit code convention (0 = success, 2 = blocking error) is the mechanism that gives hooks real power -- they are not just notifications, they can enforce rules.

Want to dig into hook configuration details?

### 5.4b What the Stop Hook Receives

The Stop hook input includes a `last_assistant_message` field -- the last thing Claude said before the hook fired. What could you do with that? You might scan it to verify Claude actually addressed the issue it claimed to fix, or check whether the response mentioned creating a route that does not exist yet. SubagentStop hooks get the same field.

One more thing: hooks can also POST to URLs instead of running local commands. Use `"type": "http"` with a `"url"` field in place of `"type": "command"`. This is handy if you want hook events sent to an external service -- a logging endpoint, a CI trigger, or a monitoring dashboard. See `context/hooks.txt` for the full format.

### 5.5 Understand Hook Configuration Details

Key points about hooks:
- **$CLAUDE_PROJECT_DIR**: environment variable pointing to the project root
- **timeout**: maximum seconds a hook can run (default 60)
- **exit codes**: 0 = success, 2 = blocking error, other = non-blocking error
- **stdin**: hooks receive JSON with session info and event-specific data
- **stdout**: for SessionStart and UserPromptSubmit, stdout is added to context
- **stderr**: for exit code 2, stderr is shown to Claude as the error message
- **matchers**: only apply to PreToolUse, PostToolUse, and PermissionRequest

Verify your hooks are registered:

```
/hooks
```

### 5.6 Shell Scripting with Hook Input

Hooks receive JSON via stdin with fields like `session_id`, `hook_event_name`, `tool_name`, `tool_input`, and `tool_response`. Extract values with jq:

```
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')
```

Ask Claude to show you the full input schema for each hook type you configured.

### 5.7 New Hook Events

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

### 5.8 Conditional Hooks & Reactive Events

Two features that transform what hooks can do:

**The `if` field.** Hooks can now include an `if` field using permission rule syntax to filter when they fire. Instead of a hook running on every Bash command, you can scope it: `"if": "Bash(git *)"` makes it fire only on git commands. This reduces overhead and makes hooks surgical.

**Reactive events: `CwdChanged` and `FileChanged`.** These fire when the working directory changes or when files change on disk. Combined with `if`, you can build reactive automation -- a hook that validates config only when YAML or JSON files change, or one that restarts the gateway when route config changes.

Ask Claude to create a reactive hook. Something like:

```
Create a FileChanged hook that validates the gateway config only when config files change. Use the if field to scope it. Add it to .claude/settings.json.
```

> **STOP** -- Create a conditional hook using the `if` field and test a reactive event hook.

### Choose Your Battles (Hooks Edition)

You've seen the full hook lifecycle. Resist the urge to instrument every event. Each hook runs on every matching tool call -- cumulative latency and complexity adds up fast.

**Rule of thumb:** Start with **2 hooks**: one SessionStart (for context injection) and one PostToolUse or Stop (for quality gating). Add a third only if a specific pain point emerges.

### Checkpoint

Your gateway now has automated quality gates. Config validation, test runs, and status checks happen without you lifting a finger.

- [ ] Created a conditional hook using `if` field and a reactive event hook
- [ ] `.claude/settings.json` exists with hook configuration
- [ ] SessionStart hook injects gateway status on session launch
- [ ] PostToolUse hook validates config files after writes
- [ ] Stop hook runs tests before allowing Claude to stop
- [ ] You can explain matchers and when they apply
- [ ] You understand exit code behavior (0, 2, other)
- [ ] `/hooks` shows your registered hooks
- [ ] All hook scripts committed to git
- [ ] Wired up a hook using one of the new hook events
