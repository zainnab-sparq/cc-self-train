# Module 7 -- Guard Rails

**CC features:** PreToolUse, hook decision control, prompt-based hooks, permissionDecision, additionalContext, updatedInput

**Persona -- Peer:** Terse guidance, point to docs, let them debug first. "Your call", "What would you do here?"

In this module you build hooks that act as guardrails -- preventing bad actions, injecting context, and modifying inputs before tools execute.

### 7.1 Understand PreToolUse Decision Control

**Why this step:** PreToolUse is the most powerful hook event because it fires *before* a tool runs, giving you three options: allow it silently, block it with a reason, or ask the user to confirm. On top of that, you can inject extra context or even modify the tool's input. This is Claude Code's programmable permission system -- you are about to build custom guardrails for Sentinel.

Ask Claude to explain how PreToolUse decision control works.

Try something like:

```
Explain PreToolUse hooks -- what are the permissionDecision options (allow, deny, ask), and how do additionalContext and updatedInput work?
```

PreToolUse hooks can return JSON with:
- `permissionDecision: "allow"` -- auto-approve the tool call
- `permissionDecision: "deny"` -- block the tool call, with a reason shown to Claude
- `permissionDecision: "ask"` -- prompt the user to confirm
- `additionalContext` -- inject extra information into Claude's context
- `updatedInput` -- modify the tool's input parameters before execution

### 7.2 Guard Against Invalid Rule Schemas

Ask Claude to create a hook that prevents saving analysis rules with missing required fields. Describe the behavior you want -- it should check files being written to the rules or analyzers directory, validate they have the right structure, and deny the write with a helpful reason if something is missing.

Try something like:

```
Create a PreToolUse hook that validates rule schemas. If I'm writing a file to rules/ or analyzers/, the hook should check that it has the required fields. If invalid, deny the write with a reason. If valid, let it through. Put the script in .claude/scripts/ and add it to settings.json on the 'Write' tool.
```

Claude may ask what "required fields" means for your rules. Point it to your rule format documentation.

A denial returns JSON like: `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "Rule file missing required 'severity' field."}}`

**STOP -- What you just did:** You built a schema validation guardrail. When Claude tries to write a rule file with missing required fields, the hook blocks the write and tells Claude exactly what is wrong. Claude then sees the denial reason and can fix the file before trying again. This is "fail fast" automation -- bad data never reaches disk. You will use this pattern whenever you have strict format requirements for generated files.

Ready to try context injection with additionalContext?

### 7.3 Inject Context About Related Analyzers

Now create a hook that enriches Claude's context when it reads rule files. Ask Claude to build a script that detects when a rule file is being read and injects information about related analyzer files using `additionalContext`.

Try something like:

```
Create a PreToolUse hook on 'Read' that checks if the file being read is in rules/. If so, find all related analyzer files and inject them as additionalContext so you know the full picture when working on rules. Put the script in .claude/scripts/ and add it to settings.json.
```

The output uses `additionalContext` to inject text like: "Related analyzers: complexity_rule, naming_rule, docstring_rule. See docs/rule-format.md for the rule interface."

**STOP -- What you just did:** You built a context injection hook. Unlike the deny hook which blocks actions, this one enriches Claude's understanding by adding information when it reads certain files. When Claude opens a rule file, the hook automatically tells it about related analyzers. This is like giving Claude a "see also" sidebar -- it makes connections between files that Claude might not discover on its own.

**Quick check before continuing:**
- [ ] Your deny hook blocks writes of invalid rule schemas
- [ ] Your context injection hook adds related analyzer info when reading rule files
- [ ] Both hooks are configured in `.claude/settings.json` as PreToolUse entries

### 7.4 Auto-Add Metadata to Generated Test Files

Now create a hook that silently adds metadata to generated test files. Ask Claude to build a script that detects when a test file is being written and uses `updatedInput` to prepend a metadata comment with the generation timestamp and the source file being tested.

Try something like:

```
Create a PreToolUse hook on 'Write' that checks if the file being written is a test file. If so, use updatedInput to prepend a metadata comment with the timestamp and the source file being tested. Put the script in .claude/scripts/ and add it to settings.json.
```

The output uses `updatedInput` to modify the file content before it is written, prepending a metadata header with the timestamp and source file path.

**Why this step:** `updatedInput` is the third and most subtle PreToolUse capability. While `deny` blocks an action and `additionalContext` injects information, `updatedInput` silently transforms what Claude writes. The test file reaches disk with metadata already included -- Claude does not even need to remember to add it. Use this for any boilerplate that should always be present in generated files.

### 7.5 Prompt-Based Quality Gate for Generated Tests

Add a second prompt-based Stop hook that specifically reviews test quality. Ask Claude to create one that checks whether generated tests have good edge case coverage, meaningful assertions (not just "assert true"), and proper test independence.

Try something like:

```
Add a prompt-based Stop hook (type: prompt, timeout: 30) that evaluates test quality when tests were generated. It should check for edge case coverage, meaningful assertions, and test independence. Return ok: false with a reason if it finds quality issues.
```

This demonstrates stacking multiple Stop hooks -- the Module 5 hook checks that tests exist, this one checks that they are good.

**STOP -- What you just did:** You now have four PreToolUse/Stop hooks working together: schema validation (deny), context injection (additionalContext), metadata insertion (updatedInput), and quality review (prompt-based Stop). These hooks form a layered defense -- each catches a different category of problem. Notice how they stack: you can have multiple hooks on the same event, and they all run. This composability is what makes hooks powerful for real projects.

### 7.6 Test the Guard Rails

**Quick check before continuing:**
- [ ] All four hooks are configured in `.claude/settings.json`
- [ ] You understand the difference between deny, additionalContext, and updatedInput
- [ ] The prompt-based Stop hook is set up to review test quality

1. Try to create a rule file with missing fields -- the deny hook should block it
2. Read a rule file -- check that additional context is injected
3. Generate a test file -- check that metadata is added
4. Complete a task involving tests -- the Stop hook should review quality

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

> **STOP** -- Create a PermissionDenied hook and test the defer pattern.

### 7.9 Auto-Answering with PreToolUse Hooks

PreToolUse hooks can now satisfy `AskUserQuestion` by returning `updatedInput` alongside `permissionDecision: "allow"`. This means hooks can answer Claude's questions programmatically -- enabling fully headless workflows where no human input is needed.

Think about when this is useful: CI/CD pipelines, automated testing, or any scenario where Claude needs to ask a question but you want a predetermined answer. Wire up a PreToolUse hook for `AskUserQuestion` that auto-responds to a specific question type.

### Checkpoint

Guard rails locked in. Schema validation, context injection, metadata stamps, and AI-reviewed test quality -- all automatic.

- [ ] PreToolUse hook denies writes of invalid rule schemas
- [ ] PreToolUse hook injects additionalContext when reading rule files
- [ ] PreToolUse hook uses updatedInput to add metadata to test files
- [ ] Prompt-based Stop hook reviews test quality
- [ ] All hooks are configured in `.claude/settings.json`
- [ ] You tested each guard rail and saw it work
- [ ] Reviewed new sandbox settings: `allowRead` and `enableWeakerNetworkIsolation`
- [ ] Created a PermissionDenied hook
- [ ] Tested PreToolUse hook with `updatedInput` for AskUserQuestion
