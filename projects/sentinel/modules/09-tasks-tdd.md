# Module 9 -- Tasks & TDD

<!-- progress:start -->
**Progress:** Module 9 of 10 `[█████████░]` 90%

**Estimated time:** ~45-60 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** Tasks system, TaskCreate, dependencies/blockedBy, cross-session persistence, TDD loops, SubagentStop

**Persona -- Peer:** Terse guidance, point to docs, let them debug first. "Your call", "What would you do here?"

</details>

In this module you use the Tasks system for multi-step work and practice strict TDD.

### 9.1 Tasks System Overview

**Why this step:** The Tasks system solves a problem you have probably already hit: multi-step features that are too big for a single conversation. Tasks let you break work into pieces with explicit dependencies (Task B cannot start until Task A is done), persist across sessions, and share between multiple Claude instances. This is project management built into Claude Code.

Ask Claude to explain the Tasks system and how it differs from a simple to-do list.

Try something like:

```
Explain the Claude Code Tasks system. How do tasks differ from TodoWrite? How do dependencies work, and how do tasks persist across sessions?
```

Key points: Tasks support dependency graphs (task B depends on task A). They are stored in `~/.claude/tasks/` on the filesystem. Multiple sessions or subagents can share a task list using `CLAUDE_CODE_TASK_LIST_ID`.

### 9.2 Cross-Session Task Persistence

Ask Claude to create a task list for adding coverage tracking to Sentinel. Describe the feature at a high level and ask Claude to break it into dependent tasks. You might suggest roughly how many tasks and what the dependencies should be, or let Claude propose a breakdown and then discuss it.

Try something like:

```
I want to add coverage tracking to Sentinel. Break this into about 5 tasks with dependencies -- start with designing the data model, then building the parser, integrating with the engine, adding to reports, and historical trends with SQLite. Show me the dependency graph.
```

Claude will use the Tasks system to create these. Press `Ctrl+T` to toggle the task list view in your terminal.

**STOP -- What you just did:** You created a dependency graph, not a flat to-do list. Task 2 (implement parser) cannot start until Task 1 (design data model) is done, because the parser needs to know what structures to produce. Task 5 depends on both Tasks 3 and 4. Claude enforces these dependencies -- it will not start a blocked task. This prevents the common mistake of building on top of unfinished foundations.

Ready to start building the first task?

### 9.3 Start the First Task

Tell Claude to start working on the first task.

Try something like:

```
Start on Task 1 -- design the coverage data model.
```

Claude will update the task status and begin working. When it finishes, the task will be marked complete and Task 2 will become unblocked.

### 9.4 Practice Strict TDD -- Build the Coverage Parser

**Why this step:** Test-driven development (TDD) is the most disciplined way to build reliable code with Claude. By writing the test first, you give Claude a concrete, unambiguous specification. Claude does not have to guess what "correct" means -- the test defines it. The red-green-refactor cycle (fail, pass, clean up) produces code that is tested by definition.

For Task 2, tell Claude to use strict test-driven development. Describe the TDD cycle you want it to follow -- write one failing test, write minimum code to pass it, refactor, repeat. Give it a simple starting behavior to test first.

Try something like:

```
Implement the coverage parser using strict TDD. Write ONE failing test for the simplest behavior first -- like 'the parser can read a coverage report file and return the total line count.' Run it, confirm it fails, then write the minimum code to pass. Refactor if needed, then move to the next test. Don't skip ahead.
```

Watch Claude go through multiple red-green-refactor cycles. This is where the build-test-fix loop becomes second nature.

**STOP -- What you just did:** You watched Claude do strict TDD: write a failing test, write the minimum code to pass it, then move on. Notice how each cycle was small and focused. Claude did not try to implement the entire parser at once -- it built one behavior at a time, with tests proving each step works. This incremental approach catches bugs immediately instead of at the end when they are hard to trace.

**Quick check before continuing:**
- [ ] The coverage parser has at least one passing test
- [ ] You saw Claude go through the red-green-refactor cycle (test fails, then passes)
- [ ] Task 1 is marked complete and Task 2 is in progress

Continue through progressively harder tests. Guide Claude to the next behavior you want to test:

```
Next test: the parser should extract per-file coverage data.
```

Then after that passes:

```
Next: handle missing or malformed coverage files gracefully.
```

Then edge cases:

```
Now test coverage percentage calculation -- include edge cases like zero lines, 100% coverage, and empty files.
```

### 9.4a Walkthrough: one worked TDD cycle

Before Claude runs the full pipeline, walk through a single test end to end by hand. Three moves: RED, GREEN, REFACTOR.

**RED — write a failing test first.**

```
Add exactly one test: assert that checkFunctionLength(["function foo() {", "  return 1;", "}"]) returns {passed: true}. Do NOT implement checkFunctionLength yet.
```

Run your test runner. You should see red — "checkFunctionLength is not defined" or the test-framework equivalent. If it passes, something is wrong.

**GREEN — minimum code to pass.**

```
Write the smallest checkFunctionLength that makes the failing test pass. Handle only the short-function case -- nothing about thresholds, nothing about multiple functions.
```

Claude writes a few lines. Run tests: green. Don't add behavior the tests don't ask for; later tests will surface threshold logic and multi-function handling.

**REFACTOR — improve without changing behavior.**

```
Refactor checkFunctionLength for clarity -- name the magic number if there is one. All existing tests must still pass.
```

Run tests: still green. That's a complete red-green-refactor cycle on one named behavior.

**Why this matters.** Without TDD, Claude will happily write a 50-line checker covering every case it imagines -- nested functions, arrow syntax, class methods -- most of them subtly wrong, then claim it's done. TDD forces one test at a time. Each test names one behavior. Each implementation covers exactly what the tests require. The final function is exactly as large as your tests demand -- not larger.

**STOP -- What you just did:** You saw the full red/green/refactor loop on one test case. The remaining tests (threshold violations, multi-function files, edge cases) run through the same loop -- each cycle short, each forcing you to decide "what's the next behavior?" before Claude writes code. That cadence is the discipline.

### 9.5 Complete the Remaining Tasks

**Why this step:** Now you let the task system guide your workflow. Instead of deciding what to build next, you ask Claude for the next unblocked task. The dependency graph ensures you build things in the right order. As each task completes, downstream tasks become available automatically.

Work through Tasks 3-5, letting Claude update task status as each completes. Just tell it to move on:

```
What's the next unblocked task? Let's work on it.
```

Check the task list periodically with `Ctrl+T` or ask Claude for a status update:

```
Show me the current status of all tasks.
```

**STOP -- What you just did:** You completed a multi-task feature using the dependency graph to guide your work order. Notice how you never had to think about "what should I build next?" -- the task system told you. In a real project, you would create task lists at the start of each feature and let the dependency graph keep you on track across sessions.

Shall we add quality gates for subagent work?

### 9.6 SubagentStop Hooks for Verification

**Why this step:** SubagentStop hooks are quality gates for subagent work. Just like Stop hooks check your main conversation, SubagentStop hooks check what subagents produce before they finish. This is especially important because subagents run with less oversight -- you might not see their intermediate steps.

Ask Claude to add a SubagentStop hook that acts as a quality gate for subagent work.

Try something like:

```
Add a prompt-based SubagentStop hook to settings.json that checks whether a subagent that wrote code also ran the test suite. If tests weren't run, respond with ok: false and tell the subagent to run tests before finishing.
```

### 9.7 Cross-Session Collaboration

**Why this step:** Cross-session task sharing is how you scale to multiple Claude instances working on the same feature. This is the foundation for the parallel development workflow you will use in Module 10.

Start a second Claude Code session that shares the same task list:

```
CLAUDE_CODE_TASK_LIST_ID=sentinel-coverage claude
```

In the second session, you can see the same tasks and their current statuses. If one session completes a task, the other session sees the update.

**STOP -- What you just did:** You shared a task list between two separate Claude Code sessions using `CLAUDE_CODE_TASK_LIST_ID`. Both sessions see the same tasks and their statuses update in real time. This is how you coordinate parallel work -- one session works on Task A while another works on the independent Task B, and neither duplicates effort. You will use this pattern heavily in Module 10 with git worktrees.

### 9.8 Recurring Tasks with /loop & Cron

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

Task graphs, TDD, cross-session persistence, and subagent verification. This is how real multi-session projects get coordinated.

- [ ] Tasks were created with dependencies (task graph, not flat list)
- [ ] You built the coverage parser using strict TDD (red-green-refactor)
- [ ] All 5 tasks are complete with coverage tracking integrated
- [ ] SubagentStop hook verifies subagents run tests
- [ ] You understand cross-session task sharing via CLAUDE_CODE_TASK_LIST_ID
- [ ] `Ctrl+T` shows the task list in the terminal
- [ ] Tried `/loop` for a recurring task
