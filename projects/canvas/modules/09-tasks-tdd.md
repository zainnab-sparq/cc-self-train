# Module 9 -- Tasks and TDD

<!-- progress:start -->
**Progress:** Module 9 of 10 `[█████████░]` 90%

**Estimated time:** ~45-60 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** Tasks system, `TaskCreate`, dependencies/blockedBy,
cross-session persistence, TDD loops, SubagentStop

**Persona -- Peer:** Terse guidance, point to docs, let them debug first. "Your call", "What would you do here?"

</details>

### 9.1 Tasks System Overview

**Why this step:** Tasks give Claude Code a built-in project management system. Instead of keeping a mental checklist of what needs to happen, you define tasks with explicit dependencies -- task B cannot start until task A finishes. This prevents Claude from jumping ahead or working on things out of order, which is especially important for multi-step features like building a contact form.

Tasks replace the old TODO system. They provide:
- Dependency graphs (task A blocks task B)
- Cross-session persistence (stored on disk at `~/.claude/tasks/`)
- Multi-agent collaboration (shared task lists)
- Progress tracking visible in the terminal

Press `Ctrl+T` to toggle the task list view at any time.

### 9.2 Cross-Session Persistence

To share a task list across sessions, set the environment variable:

```
CLAUDE_CODE_TASK_LIST_ID=canvas-contact claude
```

Any session started with this ID shares the same task list. This enables
multiple Claude instances to coordinate work.

**Why this step:** Cross-session persistence means you can close Claude Code, come back tomorrow, and your task list is still there. It also means multiple Claude instances can share the same task list -- you will use this in Module 10 for parallel development with git worktrees.

### 9.3 Build a Multi-Step Pipeline

Create a task chain for building the contact form end-to-end. Describe the steps and their dependencies to Claude:

```
I want to build a contact form as a multi-step task pipeline. The steps are: design the form layout first, then create the HTML, then style it with CSS, then write JS validation, then add success/error states, then test everything. Each step depends on the previous one. Create these as tasks with blockedBy dependencies.
```

Press `Ctrl+T` to see tasks in the status area. Then tell Claude to execute:

```
Work through the contact form pipeline. Execute each task in dependency order.
```

**STOP -- What you just did:** You created a dependency graph where each task explicitly blocks the next. Task 3 ("Style form with CSS") cannot start until task 2 ("Create HTML form") is complete. Claude respects these dependencies automatically -- it will not jump to styling before the HTML exists. Press `Ctrl+T` to see the task list update in real time as each task completes. This is how you manage complex, multi-step features without losing track of progress.

**Quick check before continuing:**
- [ ] All 6 contact form tasks were created with `blockedBy` dependencies
- [ ] `Ctrl+T` shows the task list in the terminal status area
- [ ] Tasks executed in order (no blocked task ran before its dependency completed)
- [ ] The contact form page exists with HTML, CSS, and basic structure

### 9.4 TDD Workflow: Build with Tests First

Use strict test-driven development to build the form validation. Since this
is plain JavaScript, you will use a simple browser-based test runner.

Tell Claude you want to do strict TDD and describe the test cases:

```
Let's build form validation with strict TDD. First, create a test.html file that acts as a simple test runner -- loads the validation script, runs assertions, and shows pass/fail in the browser. I want test cases for email validation, required field checks, XSS prevention on the name field, message length limits, and correct error messages. Write the test runner and the first failing test now -- do NOT write any validation code yet.
```

The key discipline: Claude writes a test first, you verify it fails in the browser (red), then Claude writes the minimum code to pass, you verify it passes (green), then refactor. Push back if Claude tries to write all the validation code at once.

Let Claude work through the TDD cycle. For each test:
1. Claude writes the test
2. You open test.html in the browser (it should show red/fail)
3. Claude writes just enough code to pass
4. Refresh the browser (should show green/pass)
5. Refactor

This enforces disciplined development and gives you a solid test suite.

**STOP -- What you just did:** You used TDD (test-driven development) with Claude Code. The discipline is critical: write the test *first*, see it fail, *then* write the minimum code to pass. This prevents Claude from writing a monolithic validation function and then backfilling tests. The browser-based test runner (`test.html`) is your verification -- you can see red/green status with every refresh. TDD with Claude Code is one of the most effective development patterns because it forces both you and Claude to think about behavior before implementation.

Ready to add a SubagentStop hook for verifying agent output?

**Why this step (for the next section):** SubagentStop hooks verify that subagents actually completed their work properly. Without this check, a subagent could fail silently or return incomplete results, and you might not notice.

### 9.5 Stop and SubagentStop Hooks for Verification

Add a SubagentStop hook that verifies subagent output. Describe the check to Claude:

```
Add a SubagentStop hook to settings.json with type 'prompt' that evaluates whether a subagent actually completed its task -- did it produce output? Were there errors? Is the work complete? It should respond with ok true or ok false with a reason.
```

This ensures subagents finish their work properly before returning results.

**STOP -- What you just did:** You added a SubagentStop hook that acts as a quality gate for subagent output. This is a prompt-based hook (using an LLM to evaluate) rather than a script-based hook -- because determining whether a subagent "completed its task" requires judgment, not just string matching. This closes the loop on subagent reliability: you delegate work to a subagent, and the hook verifies the work was actually done.

### 9.6 Recurring Tasks with /loop & Cron

Two new tools for recurring automation within a session:

**`/loop`** (v2.1.71) — run a prompt or slash command on a recurring interval. Examples:
- `/loop 5m check the deploy` — runs every 5 minutes
- `/loop 10m /doctor` — runs `/doctor` every 10 minutes
- Default interval is 10 minutes if omitted

**Cron scheduling** (v2.1.71) — create recurring prompts using cron-style scheduling within a session. More flexible than `/loop` for complex schedules.

**`CLAUDE_CODE_DISABLE_CRON`** (v2.1.72) — set this env var to immediately stop all scheduled cron jobs mid-session.

Try `/loop` with a monitoring task that makes sense for your project.

- `/proactive` is now an alias for `/loop` (v2.1.105) -- use whichever name feels more natural.
- `--resume`/`--continue` now resurrects unexpired scheduled tasks (v2.1.110) -- scheduled work survives session restarts.

### Checkpoint

Task pipelines, TDD, and quality gates on subagent output. You are managing complex work the way professional teams do.

- [ ] You created a multi-step task pipeline with dependencies
- [ ] Tasks appeared in the terminal status area (`Ctrl+T`)
- [ ] Tasks executed in dependency order (blocked tasks waited)
- [ ] You built form validation using strict TDD (test first, then implement)
- [ ] All form validation tests pass in the browser
- [ ] You understand cross-session persistence with `CLAUDE_CODE_TASK_LIST_ID`
- [ ] SubagentStop hook verifies subagent completion
- [ ] Tried `/loop` for a recurring task
