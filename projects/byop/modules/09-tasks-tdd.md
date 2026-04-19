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

<!-- guide-only -->
**Why this step:** Tasks give Claude Code a built-in project management system. Instead of keeping a mental checklist of what needs to happen, you define tasks with explicit dependencies -- task B cannot start until task A finishes. This prevents Claude from jumping ahead or working on things out of order, which is especially important for multi-step features.
<!-- /guide-only -->

Tasks replace the old TODO system. They provide:
- Dependency graphs (task A blocks task B)
- Cross-session persistence (stored on disk at `~/.claude/tasks/`)
- Multi-agent collaboration (shared task lists)
- Progress tracking visible in the terminal

Press `Ctrl+T` to toggle the task list view at any time.

### 9.2 Cross-Session Persistence

To share a task list across sessions, set the environment variable:

```
CLAUDE_CODE_TASK_LIST_ID=my-project-tasks claude
```

Any session started with this ID shares the same task list. This enables
multiple Claude instances to coordinate work.

<!-- guide-only -->
**Why this step:** Cross-session persistence means you can close Claude Code, come back tomorrow, and your task list is still there. It also means multiple Claude instances can share the same task list -- you will use this in Module 10 for parallel development with git worktrees.
<!-- /guide-only -->

### 9.3 Build a Multi-Step Pipeline

Pick a real feature for your project -- something that requires multiple sequential steps. Break it into a task pipeline with dependencies. Describe the steps to Claude:

```
I want to build [your feature -- e.g., "user authentication", "a REST API endpoint", "a data processing pipeline", "a CLI subcommand"] as a multi-step task pipeline. The steps are: [list your steps in order -- e.g., "design the data model first, then create the database migration, then implement the service layer, then add the route handler, then write validation, then add tests"]. Each step depends on the previous one. Create these as tasks with blockedBy dependencies.
```

Press `Ctrl+T` to see tasks in the status area. Then tell Claude to execute:

```
Work through the pipeline. Execute each task in dependency order.
```

**STOP -- What you just did:** You created a dependency graph where each task explicitly blocks the next. Claude respects these dependencies automatically -- it will not jump to a later step before the prerequisite is complete. Press `Ctrl+T` to see the task list update in real time as each task completes. This is how you manage complex, multi-step features without losing track of progress.

**Quick check before continuing:**
- [ ] All tasks were created with `blockedBy` dependencies
- [ ] `Ctrl+T` shows the task list in the terminal status area
- [ ] Tasks executed in order (no blocked task ran before its dependency completed)
- [ ] The feature is partially or fully built with real code

### 9.4 TDD Workflow: Build with Tests First

Use strict test-driven development to build a component of your feature. Use whatever test framework your project already uses -- pytest, jest, go test, cargo test, JUnit, or anything else.

Tell Claude you want to do strict TDD and describe the test cases:

```
Let's build [a specific component -- e.g., "input validation", "the data transformer", "the API response serializer"] with strict TDD. First, write test cases for [your scenarios -- e.g., "valid input, missing required fields, invalid email format, XSS prevention, edge cases"]. Use our existing test framework ([your framework]). Write the tests now -- do NOT write any implementation code yet.
```

The key discipline: Claude writes a test first, you verify it fails (red), then Claude writes the minimum code to pass, you verify it passes (green), then refactor. Push back if Claude tries to write all the implementation code at once.

Let Claude work through the TDD cycle. For each test:
1. Claude writes the test
2. You run the tests (they should fail)
3. Claude writes just enough code to pass
4. You run the tests again (they should pass)
5. Refactor

This enforces disciplined development and gives you a solid test suite.

**STOP -- What you just did:** You used TDD (test-driven development) with Claude Code. The discipline is critical: write the test *first*, see it fail, *then* write the minimum code to pass. This prevents Claude from writing a monolithic function and then backfilling tests. TDD with Claude Code is one of the most effective development patterns because it forces both you and Claude to think about behavior before implementation.

Ready to add a SubagentStop hook for verifying agent output?

**Why this step (for the next section):** SubagentStop hooks verify that subagents actually completed their work properly. Without this check, a subagent could fail silently or return incomplete results, and you might not notice.

### 9.4a Walkthrough: one worked TDD cycle

Before Claude runs the full pipeline, walk through a single test end to end by hand. Pick one small function from your project that doesn't exist yet — something you could implement in 5 lines. Then three moves: RED, GREEN, REFACTOR.

**RED — write a failing test first.** Ask Claude for a single failing test:

```
Add exactly one test: assert that <yourFunction>(<input>) returns <expected>. Do NOT implement <yourFunction> yet.
```

Run your test runner. You should see red — "not defined" or the test-framework equivalent. If it passes, something is wrong.

**GREEN — minimum code to pass.**

```
Write the smallest <yourFunction> that makes the failing test pass. Handle only the case the test covers -- nothing else.
```

Claude writes a few lines. Run tests: green. Don't add behavior the tests don't ask for; later tests will surface other cases.

**REFACTOR — improve without changing behavior.**

```
Refactor <yourFunction> for clarity -- extract a named helper, pull out a constant, rename a variable. All existing tests must still pass.
```

Run tests: still green. That's a complete red-green-refactor cycle on one named behavior.

**Why this matters.** Without TDD, Claude will happily write a 50-line function covering every case it imagines, most of them wrong, and then claim it's done. TDD forces one test at a time. Each test names one behavior. Each implementation covers exactly what the tests require. The final function is exactly as large as your tests demand -- not larger.

**STOP -- What you just did:** You saw the full red/green/refactor loop on one test case. Subsequent tests run through the same loop — each cycle short, each forcing you to decide "what's the next behavior?" before Claude writes code. That cadence is the discipline.

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

### 9.7 /loop cancellation and wakeup banner (v2.1.113)

Two small `/loop` refinements worth noting:

- **Esc cancels pending wakeups.** Press Esc mid-session to cancel any pending `/loop` wakeup. Before this, you had to wait for the wakeup to fire before you could stop the loop.
- **Wakeup banner.** When a scheduled `/loop` fires, Claude displays "Claude resuming /loop wakeup" so you can tell the current turn is from the schedule rather than fresh input.

If you wire a long-running `/loop` for TDD verification or deployment polling, these make the loop safe to interrupt without hunting for the right signal.

### Checkpoint

Task pipelines, TDD, and quality gates on subagent output. You are managing complex work the way professional teams do.

- [ ] You created a multi-step task pipeline with dependencies for a real feature
- [ ] Tasks appeared in the terminal status area (`Ctrl+T`)
- [ ] Tasks executed in dependency order (blocked tasks waited)
- [ ] You built a component using strict TDD (test first, then implement)
- [ ] All tests pass using your project's test framework
- [ ] You understand cross-session persistence with `CLAUDE_CODE_TASK_LIST_ID`
- [ ] SubagentStop hook verifies subagent completion
- [ ] Tried `/loop` for a recurring task
