# Module 7 -- Guard Rails

<!-- progress:start -->
**Progress:** Module 7 of 10 `[███████░░░]` 70%

**Estimated time:** ~30-45 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** PreToolUse, hook decision control, prompt-based hooks,
`permissionDecision`, `additionalContext`, `updatedInput`

**Persona -- Peer:** Terse guidance, point to docs, let them debug first. "Your call", "What would you do here?"

</details>

### 7.1 PreToolUse Hooks with Decision Control

<!-- guide-only -->
**Why this step:** In Module 5 you built hooks that *observe* (SessionStart, PostToolUse, Stop). Now you are building hooks that *control* -- they intercept tool calls and decide whether to allow, deny, or modify them. This is the guard rail pattern: automated safety checks that prevent mistakes before they happen, without slowing you down.
<!-- /guide-only -->

PreToolUse hooks intercept tool calls before they execute. They can:
- **Allow:** bypass the permission system entirely
- **Deny:** block the tool call and tell Claude why
- **Ask:** show the user a confirmation prompt
- **Modify:** change the tool's input parameters

### 7.2 Guard: Validate Before Storage Writes

Create a hook that prevents writes to storage files unless validation passes. Describe the guard to Claude -- it should intercept Write operations, check if the target is a storage file, validate the JSON structure, and deny the write with a clear message if validation fails.

"Create a PreToolUse hook that validates storage writes. It should read the tool input from stdin, check if the file is a storage JSON file, and if so, validate the structure. If validation fails, deny the write with a permissionDecision of deny and a reason explaining what's wrong. If it's not a storage file, allow it through. Add it to settings.json with a Write matcher."

Claude will create the hook script and wire it into your settings. Discuss the validation rules -- what counts as valid JSON structure for your data types.

**STOP -- What you just did:** You created a guard that prevents Claude from writing invalid data to your storage files. The key mechanism is `permissionDecision: "deny"` -- it blocks the tool call entirely and sends a reason back to Claude. Claude sees the denial message and can try again with valid data. This is a safety net: even if your code has a bug that produces bad JSON, the hook catches it before it corrupts your storage.

Want to build a guard that injects context instead of blocking?

### 7.3 Guard: Inject Context on File Reads

Create a hook that adds context when Claude reads source files. This one does not block anything -- it injects a reminder about your coding conventions.

"Create a PreToolUse hook with a Read matcher that checks if the file being read is a source file (in src/, lib/, or pkg/). If it is, inject additionalContext reminding Claude to follow single-responsibility principle and add docstrings to public functions. If it's not a source file, do nothing."

The key is `hookSpecificOutput.additionalContext` -- it injects a string into
Claude's context before the tool executes.

**STOP -- What you just did:** You created a hook that injects `additionalContext` when Claude reads source files. Unlike `deny` which blocks an action, `additionalContext` *adds information* to Claude's context right before the tool executes. Claude does not even know the hook ran -- it just "remembers" to follow single-responsibility principle because the context was injected. This is a subtle but powerful pattern for enforcing conventions without blocking anything.

**Quick check before continuing:**
- [ ] Your storage validation hook denies writes with invalid JSON
- [ ] Your read-context hook injects reminders when Claude reads source files
- [ ] You understand the difference between `deny` (blocks) and `additionalContext` (informs)

### 7.4 Guard: Auto-Add Timestamps

Create a hook that silently modifies tool input to inject timestamps. This is the third PreToolUse mechanism -- instead of blocking or informing, it *rewrites* what Claude is about to write.

"Create a PreToolUse hook with a Write matcher that auto-adds timestamps to storage files. When Claude writes to a storage file, the hook should parse the content, inject or update an 'updated_at' field with the current ISO timestamp, and pass the modified content through using updatedInput with permissionDecision allow."

The key is `hookSpecificOutput.updatedInput` -- it replaces the tool's input
parameters before execution.

**STOP -- What you just did:** You created a hook that uses `updatedInput` to *modify* the tool's input before it executes. This is the third and most powerful PreToolUse mechanism: the hook silently rewrites what Claude is about to write, injecting timestamps into storage files. Claude thinks it wrote the original content, but the hook quietly added `updated_at`. This pattern is ideal for cross-cutting concerns like timestamps, audit trails, or data enrichment that should happen on every write without Claude having to remember.

Ready to try a prompt-based quality gate?

### 7.5 Prompt-Based Quality Gate

Now try a different kind of hook -- one powered by an LLM instead of a script. Ask Claude to create a prompt-based Stop hook that reviews the conversation for commit-quality issues.

"Add a prompt-based Stop hook (type: prompt, not command) with a 30-second timeout. The prompt should check whether Claude was asked to commit code, and if so, verify that tests pass, there are no unresolved TODOs, and no leftover debug statements. It should respond with ok: true or ok: false with a reason."

Prompt-based hooks use a fast LLM (Haiku) to evaluate context and return a
structured decision. They are powerful for nuanced, context-aware checks that would be impractical to write as regex or shell scripts.

<!-- guide-only -->
**Why this step:** Some quality checks cannot be expressed as simple scripts. "Are there leftover debug statements?" requires understanding code context. Prompt-based hooks delegate this judgment to a fast LLM (Haiku), combining the automation of hooks with the reasoning ability of an AI. This is one of the most advanced hook patterns -- use it for nuanced checks that would be impractical to write as regex or shell scripts.
<!-- /guide-only -->

### 7.6 Test Each Guard

1. **Storage validation:** Ask Claude to write invalid data to a storage file.
   Verify the hook blocks it.
2. **Read context:** Ask Claude to read a source file. Use `Ctrl+O` to verify
   the additional context was injected.
3. **Timestamp injection:** Ask Claude to update a storage file. Verify
   `updated_at` was added.
4. **Quality gate:** Ask Claude to write code with a `console.log` and commit.
   Verify the stop hook catches it.

### 7.7 Sandbox Read Control & Network Settings

New sandbox settings to know:

**`allowRead`** (v2.1.77) — re-allows read access within `denyRead` regions. Useful for blocking reads to a sensitive directory but allowing a specific subdirectory.

**`sandbox.enableWeakerNetworkIsolation`** (v2.1.69, macOS) — allows Go programs like `gh`, `gcloud`, and `terraform` to verify TLS certificates when using a custom MITM proxy with `httpProxyPort`. Without this, Go binaries fail certificate validation inside the sandbox.

**PreToolUse `"allow"` no longer bypasses `deny` rules** (v2.1.77) — if you have both a hook returning `"allow"` and a `deny` permission rule, the `deny` takes precedence. This includes enterprise managed settings.

Check `context/hooks.txt` for the full sandbox settings reference.

### 7.8 PermissionDenied Hook & Deferred Decisions

Two new capabilities complete the permission lifecycle you started learning in 7.1.

**`PermissionDenied` hook.** Fires after auto mode's classifier denies a command. Your hook receives the denied tool name and can return `{retry: true}` to tell the model to try a different approach. Use cases: logging denied operations for security auditing, or auto-retrying with modified parameters.

**`"defer"` permission decision.** PreToolUse hooks can return `{permissionDecision: "defer"}` to pause a tool call. In headless sessions (`-p`), the session pauses and can be resumed with `-p --resume` to have the hook re-evaluate. This enables human-in-the-loop approval flows for sensitive operations.

Create a `PermissionDenied` hook that logs all denied operations to a file. Check `context/hooks.txt` for the input schema.

- **`permissions.deny` precedence** (v2.1.101): `permissions.deny` rules now correctly override a PreToolUse hook's `permissionDecision: "ask"` -- previously the hook could downgrade a deny into a prompt.
- **`PreToolUse` reliability** (v2.1.110): `additionalContext` from PreToolUse hooks is no longer dropped when the tool call fails -- context is preserved for Claude's error handling.

> **STOP** -- Create a PermissionDenied hook and test the defer pattern.

### 7.9 Auto-Answering with PreToolUse Hooks

PreToolUse hooks can now satisfy `AskUserQuestion` by returning `updatedInput` alongside `permissionDecision: "allow"`. This means hooks can answer Claude's questions programmatically -- enabling fully headless workflows where no human input is needed.

Think about when this is useful: CI/CD pipelines, automated testing, or any scenario where Claude needs to ask a question but you want a predetermined answer. Wire up a PreToolUse hook for `AskUserQuestion` that auto-responds to a specific question type.

### 7.10 Permission-model refinements (v2.1.111 / v2.1.113)

Four changes to the permission and sandbox model worth knowing:

- **`sandbox.network.deniedDomains`** (v2.1.113) — settings.json now supports an explicit deny list that wins over allow patterns. Use this to block egress to credential brokers or metadata endpoints (`169.254.169.254`) even when a broader allow rule would otherwise permit them.
- **Read-only bash pass-through** (v2.1.111) — a curated list of read-only commands (`ls`, `pwd`, `git status`, `cat`, etc.) skips permission prompts entirely. Reduces fatigue without weakening protection. See `/less-permission-prompts` — a bundled skill that scans recent transcripts and suggests safe additions to your `permissions.allow` list.
- **Bash security-rule tightening** (v2.1.113) — `find:*` with `-exec` is now denied by default (it was an arbitrary-command vector), macOS `/private/*` paths are treated as dangerous `rm` targets, and exec-wrapper deny-matching (`env`, `xargs`, `bash -c …`) closed a bypass where a dangerous command could sail through via a shell wrapper.
- **`dangerouslyDisableSandbox`** (v2.1.113) — if your permissions actively disable sandbox mode, plan mode no longer silently re-enables it. The setting now means what it says.

Cross-reference: `context/security.txt` for the threat → section lookup table.

> **STOP** — If you set `sandbox.network.deniedDomains` alongside an allow rule, write a one-line test that confirms the deny wins. Same pattern as the guard-denies-and-allows check below — precedence bugs hide in the "looks right in the happy case" gap.

### Verify your guard denies as well as allows

**Security footgun:** a PreToolUse guard that accidentally always returns `{"permissionDecision": "allow"}` looks identical to a working guard at the exit-code level. If you only test the allow case, a silently-broken guard reads as green. Module 7's guards must be tested on **both** paths before you trust them.

Run each guard script against one input it should allow and one it should deny:

```bash
# Case 1: should allow -- exit 0, empty stdout (or explicit allow)
echo '{"tool_input":{"file_path":"notes/daily.md"}}' | .claude/scripts/guard.sh
echo "exit: $?"

# Case 2: should deny -- non-zero exit or explicit deny on stderr
echo '{"tool_input":{"file_path":"../../etc/passwd"}}' | .claude/scripts/guard.sh
echo "exit: $?"
```

**Both outputs must differ.** If the two cases produce identical exit codes and identical stdout, your guard is silently allowing everything — it's not enforcing anything. Common cause: a `read` heredoc or input-consumption bug that makes the guard's logic branch unreachable.

**Stuck?** `/stuck` walks you through isolating the bug — compare what Claude's seeing vs. what your script is actually evaluating.

### Checkpoint

Four guard patterns, all wired up. Your toolkit now prevents bad data, enforces conventions, and reviews quality -- without you asking.

- [ ] PreToolUse hook denies invalid storage writes with a clear message
- [ ] PreToolUse hook injects `additionalContext` when reading source files
- [ ] PreToolUse hook uses `updatedInput` to inject timestamps on writes
- [ ] Prompt-based Stop hook reviews code quality before commit
- [ ] Each guard was tested and verified working
- [ ] You understand the difference between `permissionDecision`, `additionalContext`, and `updatedInput`
- [ ] Reviewed new sandbox settings: `allowRead` and `enableWeakerNetworkIsolation`
- [ ] Created a PermissionDenied hook
- [ ] Tested PreToolUse hook with `updatedInput` for AskUserQuestion

**STOP -- What you just did in this module:** You built a complete guard rail system with four distinct mechanisms: `deny` blocks bad actions, `additionalContext` injects reminders, `updatedInput` silently modifies tool inputs, and prompt-based hooks use AI judgment for nuanced checks. Together, these form a safety layer that runs automatically on every tool call. In real projects, guard rails like these prevent data corruption, enforce conventions, and catch quality issues -- all without you having to remember to check.
