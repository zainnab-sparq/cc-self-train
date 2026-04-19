# Module 7 -- Guard Rails

<!-- progress:start -->
**Progress:** Module 7 of 10 `[███████░░░]` 70%

**Estimated time:** ~30-45 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** PreToolUse, hook decision control, prompt-based hooks, permissionDecision, additionalContext, updatedInput

**Persona -- Peer:** Terse guidance, point to docs, let them debug first. "Your call", "What would you do here?"

</details>

<!-- guide-only -->
**Why this step:** In Module 5 you built hooks that react *after* things happen (PostToolUse, Stop). PreToolUse hooks are different -- they fire *before* a tool runs, giving you the power to block, modify, or annotate tool calls before they execute. This is how you build guardrails that prevent mistakes rather than just catching them.
<!-- /guide-only -->

### 7.1 PreToolUse with Decision Control

PreToolUse hooks fire before a tool executes. They can return JSON to control the outcome:

| Decision | Effect |
|----------|--------|
| `"permissionDecision": "allow"` | Auto-approve the tool call |
| `"permissionDecision": "deny"` | Block the tool call, show reason to Claude |
| `"permissionDecision": "ask"` | Show the permission dialog to the user |
| `additionalContext` | Inject context for Claude before the tool runs |
| `updatedInput` | Modify the tool's input parameters |

### 7.2 Guard -- Prevent Unvalidated Config Edits

Ask Claude to create a PreToolUse hook that blocks writes to route config files when they are missing required fields. Describe the guardrail behavior you want.

```
Create a PreToolUse hook that guards config file edits. If Claude tries to write a route config file that's missing a 'path' field, deny the write with a clear reason. Put the script in .claude/hooks/guard-config-edit.sh and add it to settings.json with a Write|Edit matcher.
```

Claude will create the hook script that reads the tool input from stdin, checks config file writes, and returns a `permissionDecision: deny` JSON response when validation fails. Test it: ask Claude to write a config file missing the `path` field. The hook should block it.

**STOP -- What you just did:** You created your first guardrail that actively *prevents* a mistake. When Claude tries to write an invalid config, the hook blocks it with a clear reason. Claude sees the denial reason and corrects its approach automatically. This is fundamentally different from the PostToolUse validation in Module 5 -- that caught errors after the write; this prevents the write from happening at all.

Want to try softer guardrails with context injection?

### 7.3 Guard -- Add Context to Route Handler Reads

<!-- guide-only -->
**Why this step:** Not all guardrails block actions. `additionalContext` is a softer approach: it injects helpful information into Claude's context before a tool runs, nudging Claude toward better behavior without forcing it. Think of it as whispering a reminder rather than slamming a door.
<!-- /guide-only -->

Ask Claude to create a PreToolUse hook that injects helpful context whenever Claude reads a route handler file. The context should remind Claude about method validation, proper status codes, and rate limit checks.

```
Create a PreToolUse hook that detects when you're reading a route handler file and injects a reminder about validating HTTP methods, returning proper status codes, and checking rate limits. Use additionalContext, not deny -- I want to nudge your behavior, not block the read.
```

The `additionalContext` field injects text into Claude's context before the tool runs, without changing the tool's behavior.

### 7.4 Guard -- Auto-Add Logging to New Route Handlers

Ask Claude to create another PreToolUse hook that checks whether a route handler being written includes logging. If not, it should inject a reminder via `additionalContext`.

```
Create a PreToolUse hook that checks when you're writing a route handler file. If the content doesn't include any logging, inject an additionalContext reminder to add request logging with method, path, status code, and response time. Don't block the write -- just remind.
```

Using `additionalContext` to remind Claude is more reliable than forcibly rewriting content with `updatedInput`.

**STOP -- What you just did:** You now have three guard rail strategies: `deny` (block the action), `additionalContext` (inject a reminder), and `ask` (show the user a permission dialog). You also saw the logging injection hook, which demonstrates a pattern you will use often: instead of trying to rewrite Claude's output with `updatedInput`, use `additionalContext` to add instructions that Claude follows naturally.

**Quick check before continuing:**
- [ ] The config validation hook blocks writes to config files that are missing required fields
- [ ] The route context hook injects reminders when Claude reads route handler files
- [ ] The logging injection hook reminds Claude to add logging to new route handlers
- [ ] You can explain the difference between `deny`, `additionalContext`, and `updatedInput`

### 7.5 Prompt-Based Hook -- Security Gate

<!-- guide-only -->
**Why this step:** Shell script hooks are great for pattern matching (does this file contain "path"?), but some decisions require judgment. Prompt-based hooks send the context to a fast LLM (Haiku) that can evaluate nuanced questions like "is this route config a security risk?" This is how you build guardrails for things that cannot be checked with a regex.
<!-- /guide-only -->

Prompt-based hooks use an LLM (Haiku) to evaluate decisions. Create a Stop hook that checks whether route configs are secure:

Add to `.claude/settings.json`:

```json
"Stop": [
  {
    "hooks": [
      {
        "type": "prompt",
        "prompt": "Review the conversation and check if any route configuration changes were made. If they were, evaluate: 1) Are any routes exposing internal-only paths like /admin or /internal to public access? 2) Are there routes without rate limiting that should have it? 3) Are there routes forwarding to external hosts that could be a security risk? If any security issues exist, respond with {\"ok\": false, \"reason\": \"Security issue found: <description>. Fix before stopping.\"}. If everything looks safe, respond with {\"ok\": true}.",
        "timeout": 30
      }
    ]
  }
]
```

Prompt-based hooks send the context to a fast LLM which returns a JSON decision. This is more flexible than shell scripts for nuanced evaluations.

**STOP -- What you just did:** You built a complete guard rail system for your gateway: shell-script hooks for deterministic checks (config validation, logging reminders) and a prompt-based hook for judgment calls (security review). The prompt-based hook is especially powerful -- it evaluates route configs for security issues using an LLM, catching things that no regex could. You now have hooks at every stage of the lifecycle: SessionStart (context), PreToolUse (guard), PostToolUse (validate), and Stop (quality gate + security check).

### 7.6 Sandbox Read Control & Network Settings

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
echo '{"tool_input":{"file_path":"config/routes.yaml"}}' | .claude/scripts/guard.sh
echo "exit: $?"

# Case 2: should deny -- non-zero exit or explicit deny on stderr
echo '{"tool_input":{"file_path":"../../etc/passwd"}}' | .claude/scripts/guard.sh
echo "exit: $?"
```

**Both outputs must differ.** If the two cases produce identical exit codes and identical stdout, your guard is silently allowing everything — it's not enforcing anything. Common cause: a `read` heredoc or input-consumption bug that makes the guard's logic branch unreachable.

**Stuck?** `/stuck` walks you through isolating the bug — compare what Claude's seeing vs. what your script is actually evaluating.

### Checkpoint

Full guard rail system in place. Config validation, context injection, and AI-powered security review -- all running on every tool call.

- [ ] PreToolUse hook blocks config writes that fail validation
- [ ] PreToolUse hook injects context when reading route handlers
- [ ] PreToolUse hook reminds Claude to add logging to route handlers
- [ ] Prompt-based Stop hook checks for security issues in route configs
- [ ] You understand the three decision types: allow, deny, ask
- [ ] You understand additionalContext vs updatedInput vs permissionDecision
- [ ] All hooks configured in `.claude/settings.json`
- [ ] Reviewed new sandbox settings: `allowRead` and `enableWeakerNetworkIsolation`
- [ ] Changes committed to git
- [ ] Created a PermissionDenied hook
- [ ] Tested PreToolUse hook with `updatedInput` for AskUserQuestion
