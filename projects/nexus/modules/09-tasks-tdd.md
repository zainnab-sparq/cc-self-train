# Module 9 -- Tasks & TDD

**CC features:** Tasks system, TaskCreate, dependencies/blockedBy, cross-session persistence, TDD loops, SubagentStop

**Persona -- Peer:** Terse guidance, point to docs, let them debug first. "Your call", "What would you do here?"

### 9.1 Tasks System Overview

Tasks replace the old "Todos" system. Key differences: dependency graphs (DAG structure where tasks can block other tasks), filesystem persistence (`~/.claude/tasks`), cross-session sharing (multiple Claude instances on one task list), and broadcast updates.

**Why this step:** Up to now, each conversation with Claude has been self-contained. Tasks persist across sessions and even across multiple Claude instances. This means you can start building a feature, close your laptop, come back tomorrow, and Claude picks up exactly where you left off -- with the same task list, the same dependency graph, the same progress.

### 9.2 Cross-Session Persistence

To share a task list across sessions: `CLAUDE_CODE_TASK_LIST_ID=nexus-middleware claude`. Any tasks created are stored under that ID. Another terminal with the same command sees the same tasks.

### 9.3 Multi-Step Pipeline -- Add Middleware System

Describe the middleware system you want to build and ask Claude to break it into a task list with dependencies. Explain the high-level pieces -- a middleware interface, a couple of concrete middleware implementations, wiring them into the pipeline, and integration tests.

```
I want to add a middleware system to the gateway. Break this into a task list with dependencies. I need: defining the middleware interface (how functions are called, ordering), implementing a logging middleware, implementing an auth middleware that checks for API keys, wiring the middleware chain into the request pipeline, and integration tests for the whole thing. Figure out the dependency order -- what blocks what.
```

Claude will create the dependency graph automatically. It will recognize that the logging and auth middleware both depend on the interface definition, and that wiring and tests come after the implementations.

**STOP -- What you just did:** You created a dependency graph (DAG) where tasks explicitly declare what they depend on. Task 4 (wire middleware into the pipeline) cannot start until both Tasks 2 and 3 (logging and auth middleware) are complete. Task 5 (integration tests) waits for Task 4. Claude enforces this ordering automatically -- it will not skip ahead or start a blocked task. This is how you decompose complex features into safe, ordered steps.

Claude creates tasks with explicit dependencies. Task 4 cannot start until both Tasks 2 and 3 are complete. Task 5 cannot start until Task 4 is done.

Press `Ctrl+T` to toggle the task list view in your terminal. You will see tasks with their status indicators.

Now work through the tasks. Ask Claude to start with the first one and show you the plan before implementing.

```
Start on the first task -- define the middleware interface. Show me the plan before you implement.
```

After completing each task, Claude automatically marks it done and moves to the next unblocked task.

**Quick check before continuing:**
- [ ] `Ctrl+T` shows the task list with status indicators
- [ ] You have completed at least Tasks 1-3 of the middleware system
- [ ] You can see that Task 4 became unblocked after Tasks 2 and 3 completed
- [ ] Each completed task has a corresponding commit

### 9.4 TDD -- Build Request Validation Middleware

**Why this step:** TDD (Test-Driven Development) flips the normal workflow: you write the test first, watch it fail, then write the minimum code to make it pass. This might feel backwards, but it guarantees every feature has a test and prevents over-engineering. Claude is particularly good at this cycle because it can write a precise failing test, then implement exactly what is needed.

Use strict Test-Driven Development to build one more middleware. Tell Claude you want to follow the red-green-refactor cycle and describe the middleware you are building.

```
Let's build a request validation middleware using strict TDD. I want to follow the red-green-refactor cycle: write a failing test first, then the minimum code to pass it, then refactor. The middleware should validate Content-Type for POST/PUT requests, check Content-Length is reasonable, and reject directory traversal in paths. Start with the first failing test.
```

Claude will write a failing test, then ask you to confirm before implementing. Each red-green-refactor cycle should be a separate commit. Work through at least 4 cycles. Notice how each cycle adds exactly one behavior -- this incremental approach keeps the code clean and every feature tested.

**STOP -- What you just did:** You experienced the red-green-refactor TDD cycle with Claude. Each cycle produced a focused commit: failing test, passing implementation, cleanup. Look at your git log -- you should see a clean, incremental history where each commit adds one specific behavior. This is the gold standard for maintainable code, and Claude's tight build-test-commit loop makes it practical rather than tedious.

Ready to add quality gate hooks to the task system?

### 9.5 Stop and SubagentStop Hooks for Quality

**Why this step:** Tasks and TDD work best when there is a quality gate preventing premature completion. The Stop hook checks whether Claude's current task is truly done (tests pass, requirements met). The SubagentStop hook does the same for subagent output. Together, they prevent Claude from marking work as "done" when it is merely "started."

Add hooks that enforce quality during task execution.

**Stop hook** (prompt-based) -- ensure tasks are truly complete:

Add to `.claude/settings.json`:

```json
"Stop": [
  {
    "hooks": [
      {
        "type": "prompt",
        "prompt": "Check if Claude is working on a task list. If yes, evaluate: 1) Is the current task actually complete? 2) Do the tests pass? 3) Is there a next task to start? If the current task is not complete or tests are failing, respond with {\"ok\": false, \"reason\": \"Task not complete: <explanation>\"}. Otherwise respond with {\"ok\": true}.",
        "timeout": 30
      }
    ]
  }
]
```

**SubagentStop hook** -- validate subagent output quality:

```json
"SubagentStop": [
  {
    "hooks": [
      {
        "type": "prompt",
        "prompt": "Evaluate whether this subagent completed its assigned task successfully. Check: 1) Did it produce the expected output? 2) Are there any errors or incomplete work? 3) Does the output meet quality standards? Respond with {\"ok\": true} if satisfactory, or {\"ok\": false, \"reason\": \"explanation\"} if the subagent should continue.",
        "timeout": 30
      }
    ]
  }
]
```

**STOP -- What you just did:** You added quality gates at two levels: the Stop hook ensures Claude itself does not prematurely finish a task, and the SubagentStop hook ensures subagents produce complete, quality output before returning control. These hooks close the loop on the task system -- tasks define *what* to do, dependencies define *when* to do it, and quality hooks ensure it is *actually done*. This is the complete automated development pipeline: plan, decompose, implement, verify.

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

Tasks, TDD, and quality hooks -- the full automated development pipeline. Plan, decompose, implement, verify.

- [ ] You created a task list with dependencies (Tasks 1-5)
- [ ] Tasks display correctly with `Ctrl+T`
- [ ] You completed the middleware system by working through tasks in order
- [ ] You used strict TDD (red-green-refactor) for the validation middleware
- [ ] At least 4 TDD cycles committed separately
- [ ] Stop hook checks task completion
- [ ] SubagentStop hook validates subagent output
- [ ] Middleware system works end-to-end with tests passing
- [ ] Changes committed to git
- [ ] Tried `/loop` for a recurring task
