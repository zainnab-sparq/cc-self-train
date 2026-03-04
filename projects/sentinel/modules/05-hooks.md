# Module 5 -- Hooks

**CC features:** SessionStart, PostToolUse, Stop hooks, matchers, hook scripting, settings.json

> **Persona — Collaborator:** Ask before telling, give pointers not answers. "What do you think…", "Try this and tell me…"

In this module you add automation that fires at key moments during your Claude Code session.

### Step 1: Understand the hook lifecycle

> **Why this step:** Hooks are the automation layer of Claude Code. They let you run scripts at specific moments -- when a session starts, after a file is written, when Claude finishes a task. Understanding the lifecycle is essential because each hook event fires at a different moment and has different capabilities (some can block actions, others can only observe).

Ask Claude to walk you through the hook lifecycle. You want to understand what hooks are available, when each one fires, and how they communicate back to Claude Code.

> "Explain the Claude Code hook lifecycle -- what hooks exist, when does each one fire, and how do they communicate back?"

The key hooks are: SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, Stop, SubagentStop, and SessionEnd. Each receives JSON via stdin and communicates via exit codes and stdout/stderr.

### Step 2: Create a SessionStart hook

This hook injects a project quality summary every time you start a session.

First, create the hook script. Ask Claude to write a script that runs Sentinel's scan on `src/`, counts issues by severity, and prints a short summary. Tell it to pick whatever scripting language makes sense for your project.

> "Create a script at .claude/scripts/session-summary.sh (or .py) that runs sentinel scan on src/, counts issues by severity, and prints a one-line summary like 'Sentinel Status: 3 errors, 12 warnings, 5 info across 24 files'. If tests have been run recently, include the pass/fail count too."

Then ask Claude to wire it up as a SessionStart hook:

> "Add a SessionStart hook to .claude/settings.json that runs the session-summary script. The stdout gets automatically added to your context, right?"

Claude will confirm and create the configuration.

The configuration should look like:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/scripts/session-summary.sh"
          }
        ]
      }
    ]
  }
}
```

Restart Claude Code and verify you see the summary injected at session start.

> **STOP -- What you just did:** You created your first hook -- a SessionStart script that gives you a project health snapshot every time you open Claude Code. The key insight is that SessionStart hook stdout is automatically injected into Claude's context. This means Claude *starts every session knowing* the current state of your codebase. You will use this pattern whenever you want Claude to have up-to-date project awareness from the first prompt.

> **Engineering value:**
> - *Entry-level:* Hooks automate the checks you'd forget to do manually — like a spell-checker that runs every time you save.
> - *Mid-level:* SessionStart hooks inject environment context so Claude always knows the current state of your project. No more 'Claude, remember we're using Postgres now' at the start of every session.
> - *Senior+:* Hooks are event-driven middleware for your AI workflow — the same pattern as git hooks, CI/CD pipelines, and Lambda triggers. You're building an automated quality pipeline that runs on every interaction.

Shall we build a PostToolUse hook for auto-validation?

### Step 3: Create a PostToolUse hook

This hook auto-validates rule configuration files after Claude writes them. Ask Claude to create a validation script and wire it up as a PostToolUse hook.

> "Create a script at .claude/scripts/validate-rules.sh that checks if a written file is in the rules/ directory, and if so, validates it has the required structure. It should exit 0 if valid and exit 2 with an error if invalid. Then add a PostToolUse hook in .claude/settings.json that triggers on 'Write|Edit' and runs this script."

Claude may ask about what "required structure" means for your rule files. Point it to your `docs/rule-format.md` or describe the fields you expect.

The settings.json entry:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/scripts/validate-rules.sh"
          }
        ]
      }
    ]
  }
}
```

> **STOP -- What you just did:** You created a PostToolUse hook with a matcher. The matcher `"Write|Edit"` means this hook only fires when Claude uses the Write or Edit tool -- it ignores Bash, Read, and other tools. The hook validates rule files automatically, so if Claude writes a malformed rule definition, the validation catches it immediately and Claude sees the error. This is quality automation -- you never have to manually check rule file structure again.

> **Quick check before continuing:**
> - [ ] SessionStart hook script exists and is executable
> - [ ] `.claude/settings.json` has both SessionStart and PostToolUse hooks configured
> - [ ] You restarted Claude Code and saw the session summary appear

### Step 4: Create a Stop hook

> **Why this step:** Stop hooks fire when Claude finishes responding. They act as a final quality gate -- you can check whether Claude did what it should have (like updating tests when it changed code) before the task is considered "done." If the hook returns failure, Claude gets the feedback and can continue working.

> **Engineering value:**
> - *Entry-level:* A blocking Stop hook means Claude can't finish until the check passes — like a teacher who won't let you submit until you've spell-checked.
> - *Mid-level:* In team repos, Stop hooks enforce quality gates that individual developers can't skip. Broken links, failing tests, lint errors — they get caught before the code leaves Claude's hands.
> - *Senior+:* This is shift-left testing in its most extreme form. Instead of catching issues in CI (minutes later) or code review (hours later), hooks catch them in the same second the code is written.

This hook checks whether tests were updated when code changes were made. Ask Claude to add a prompt-based Stop hook that reviews whether tests were updated alongside any code changes.

> "Add a prompt-based Stop hook to .claude/settings.json. It should check if the task involved writing or modifying code, and if so, verify that tests were updated. If tests weren't updated, it should respond with ok: false and a reason."

The hook uses `"type": "prompt"` instead of `"type": "command"`. Claude Code sends the prompt to a fast LLM (Haiku) which returns a JSON decision.

### Step 4b: What the Stop Hook Receives

The Stop hook input includes a `last_assistant_message` field -- the last message Claude sent before the hook fired. Think about how you could use that in Sentinel: you could check whether Claude's response actually references the test file it claimed to update, or scan for unfinished TODOs. SubagentStop hooks get the same field.

Also worth noting: hooks are not limited to local scripts. You can use `"type": "http"` with a `"url"` field to POST hook events to a remote URL. This is an alternative to command hooks -- useful if you want an external service (a CI server, a logging endpoint) to react to hook events. See `context/hooks.txt` for the format details.

### Step 5: Test your hooks

Restart Claude Code (to load the hooks). Then:

1. Verify SessionStart hook prints the quality summary
2. Ask Claude to create a new analysis rule -- verify the PostToolUse hook validates it
3. Ask Claude to modify some code -- verify the Stop hook checks for tests

> **STOP -- What you just did:** You tested the three hook types that cover the most common automation needs: SessionStart (inject context at startup), PostToolUse (validate after actions), and Stop (quality gate at the end). Together, these hooks form an invisible safety net -- they work in the background, catching issues and injecting context without you having to think about them.

Want to inspect all your hooks with the /hooks command?

### Step 6: Inspect hooks with /hooks

Type in Claude Code:

```
/hooks
```

This shows all registered hooks and lets you review or approve changes.

### Checkpoint

Your analyzer now watches itself. Hooks validate rules on write, run tests on stop, and inject context on start -- all automatically.

- [ ] `.claude/settings.json` exists with hook configuration
- [ ] SessionStart hook injects a quality summary at session start
- [ ] PostToolUse hook validates rule files after writes
- [ ] Stop hook verifies tests are updated when code changes
- [ ] You restarted Claude Code and saw hooks in action
- [ ] You ran `/hooks` to inspect the registered hooks
