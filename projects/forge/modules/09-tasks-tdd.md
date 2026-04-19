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
**Why this step:** Up to now, you have been giving Claude one instruction at a time. Tasks let you define a *plan of work* with dependencies -- "do A, then B (which needs A), then C (which needs B)." Claude tracks progress, respects the dependency order, and persists the task list across sessions. This is how you manage multi-step work that spans hours or days.
<!-- /guide-only -->

Tasks replace the old TODO system. They provide:
- Dependency graphs (task A blocks task B)
- Cross-session persistence (stored on disk at `~/.claude/tasks/`)
- Multi-agent collaboration (shared task lists)
- Progress tracking visible in the terminal

Press `Ctrl+T` to toggle the task list view at any time.

### 9.2 Cross-Session Persistence

<!-- guide-only -->
**Why this step:** By default, tasks live only in the current session. But real projects span multiple sessions -- you might define tasks today and work through them tomorrow. Cross-session persistence solves this. It also enables a powerful pattern: multiple Claude instances sharing the same task list, coordinating work across parallel sessions.
<!-- /guide-only -->

To share a task list across sessions, set the environment variable:

```
CLAUDE_CODE_TASK_LIST_ID=forge-import claude
```

Any session started with this ID shares the same task list. This enables
multiple Claude instances to coordinate work.

### 9.3 Build a Multi-Step Pipeline

Describe a multi-step import pipeline to Claude. Walk through the steps you envision -- scanning a directory for markdown files, parsing them, validating the data, importing into storage, rebuilding the index, and generating a report. Tell Claude about the dependencies between steps.

"Create a task list for importing markdown files as notes. I need these steps in order: scan the imports/ directory for .md files, parse title/body/tags from each one, validate the data, import into the forge database, rebuild the search index, and generate a summary report. Each step depends on the one before it. Use TaskCreate with blockedBy dependencies."

Press `Ctrl+T` to see tasks in the status area. Before executing, you need test data:

"Create an imports/ directory with 5 sample markdown files that have YAML frontmatter (title, tags) and varied body content for testing."

Then tell Claude to execute the pipeline:

"Execute the import pipeline. Work through each task in order."

**STOP -- What you just did:** You created a dependency graph of tasks and watched Claude execute them in order. Task 2 waited for Task 1 to complete, Task 3 waited for Task 2, and so on. The `blockedBy` field is what makes this work -- it tells the tasks system which tasks must finish before others can start. Press `Ctrl+T` to see the visual progress tracker. This is how you break down complex features into manageable, ordered steps.

**Quick check before continuing:**
- [ ] All six import pipeline tasks completed in dependency order
- [ ] `Ctrl+T` shows the task list with completion status
- [ ] The sample markdown files were successfully imported into forge

### 9.4 TDD Workflow: Build with Tests First

<!-- guide-only -->
**Why this step:** Test-driven development (TDD) flips the usual order: you write the test *first*, watch it fail, then write just enough code to make it pass. With Claude Code, TDD is especially effective because Claude can see the failing test, understand what is expected, and write precisely the code needed. This prevents over-engineering and gives you a comprehensive test suite as a side effect.
<!-- /guide-only -->

Use strict test-driven development to build a new feature -- fuzzy search. Explain the TDD workflow to Claude and describe the search behavior you want. Be clear about the discipline: test first, then code, never the other way around.

"Let's build smart search with fuzzy matching using strict TDD. The rules: write a failing test first, run it to confirm it fails, write the minimum code to make it pass, run it to confirm it passes, refactor if needed, then repeat. I want fuzzy search to handle typos like 'ntes' matching 'notes', abbreviations like 'py snippet' matching Python snippets, and be case-insensitive. Start with the first failing test -- do NOT write any implementation yet."

Let Claude work through the TDD cycle. For each test case:
1. Claude writes the test
2. You or Claude runs it (it should fail)
3. Claude writes just enough code to pass
4. Run tests again (should pass)
5. Refactor

This enforces disciplined development and gives you a solid test suite.

**STOP -- What you just did:** You experienced the TDD cycle with Claude Code: write a failing test, run it (red), write minimal code to pass (green), refactor if needed. Each cycle produces both working code and a test that proves it works. After several cycles, you have a fuzzy search feature with comprehensive test coverage. This discipline is worth practicing -- it is one of the most reliable ways to build correct software, and Claude Code makes the cycle fast because Claude can see the test failure and write targeted fixes.

Want to add verification hooks for subagent output?

### 9.4a Walkthrough: one worked TDD cycle

Before Claude runs the full pipeline, walk through a single test end to end by hand. Three moves: RED, GREEN, REFACTOR.

**RED — write a failing test first.**

```
Add exactly one test: assert that validateItemTitle("") returns {valid: false, error: "Title is required"}. Do NOT write validateItemTitle yet.
```

Run your test runner. You should see red — "validateItemTitle is not defined" or the test-framework equivalent. If it passes, something is wrong.

**GREEN — minimum code to pass.**

```
Write the smallest validateItemTitle that makes the failing test pass. Handle only the empty-string case -- nothing else.
```

Claude writes about three lines. Run tests: green. Don't add behavior the tests don't ask for; later tests will surface other cases.

**REFACTOR — improve without changing behavior.**

```
Refactor validateItemTitle for clarity -- pull the validation rule into a named constant if it helps. All existing tests must still pass.
```

Run tests: still green. That's a complete red-green-refactor cycle on one named behavior.

**Why this matters.** Without TDD, Claude will happily write a 50-line validator covering every case it imagines, most of them wrong, and then claim it's done. TDD forces one test at a time. Each test names one behavior. Each implementation covers exactly what the tests require. The final function is exactly as large as your tests demand -- not larger.

**STOP -- What you just did:** You saw the full red/green/refactor loop on one test case. The remaining tests (URL validation for bookmarks, tag format, length limits) run through the same loop -- each cycle short, each forcing you to decide "what's the next behavior?" before Claude writes code. That cadence is the discipline.

### 9.5 Stop and SubagentStop Hooks for Verification

Add a quality gate for subagent output. Ask Claude to create a SubagentStop hook that verifies subagents actually completed their tasks before returning results.

"Add a SubagentStop hook to settings.json with type: prompt that evaluates whether the subagent completed its task. It should check: Did it produce output? Were there errors? Is the work complete? It should respond ok: true or ok: false with a reason."

This ensures subagents finish their work properly before returning results.

**STOP -- What you just did:** You added a quality gate that runs every time a subagent finishes. The SubagentStop hook uses a prompt (not a script) to evaluate whether the subagent actually completed its task. This catches a common problem: subagents that return partial results or silently fail. In production workflows with multiple agents, this verification step ensures you can trust the output before passing it downstream.

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

Task pipelines, TDD, and subagent quality gates. Your toolkit now builds itself with the same rigor as production software.

- [ ] You created a multi-step task pipeline with dependencies
- [ ] Tasks appeared in the terminal status area (`Ctrl+T`)
- [ ] Tasks executed in dependency order (blocked tasks waited)
- [ ] You built fuzzy search using strict TDD (test first, then implement)
- [ ] All fuzzy search tests pass
- [ ] You understand cross-session persistence with `CLAUDE_CODE_TASK_LIST_ID`
- [ ] SubagentStop hook verifies subagent completion
- [ ] Tried `/loop` for a recurring task
