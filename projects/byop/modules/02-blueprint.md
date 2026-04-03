# Module 2 -- Blueprint and Build

**CC features:** Plan mode, model selection, git integration, basic prompting

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try...", "Here's what that does..."

### 2.1 Enter Plan Mode

**Why this step:** Plan mode is one of Claude Code's most important features. It lets you think through architecture *with* Claude before any code gets written. This prevents the "just start coding" trap that leads to messy rewrites later.

So far, you've been talking to Claude in normal mode -- you say something, Claude does it. Press `Shift+Tab` to switch to plan mode. You will see the mode indicator change. In plan mode, Claude analyzes and plans without making changes. **Instead of writing code, Claude thinks *with* you -- it analyzes, suggests architecture, and asks clarifying questions, but doesn't touch any files.** This is where you design before you build.

Alternatively, type:

```
/plan
```

### 2.2 Design a Feature

Think about a feature you have been wanting to add to your project. Maybe it is a new API endpoint, a UI component, a refactored module, a CLI subcommand, or a performance improvement. Pick something real -- something you would actually want to ship.

Now describe it to Claude in plan mode. Don't worry about getting the prompt perfect. Just explain what you want and let Claude ask clarifying questions:

```
I want to add [describe your feature]. Help me plan the implementation --
what files need to change, what new files should I create, what are the
edge cases, and what is the best approach given our existing architecture?
Don't write any code yet, just the plan.
```

Claude will probably ask about your existing patterns, how this feature fits with the rest of the codebase, and what trade-offs you are willing to make. Answer naturally -- these choices are yours. The back-and-forth is the point: you are designing *with* Claude, not dictating to it.

Once Claude produces a plan, read it carefully.

### 2.3 Review and Iterate

Still in plan mode, push back on the plan. Ask about the trade-offs Claude made. Challenge the decisions you are unsure about. For example:

```
Why did you choose that approach? What are the trade-offs? Are there
simpler alternatives? How does this interact with [existing part of
your codebase]?
```

Claude does not get defensive about its plans -- ask hard questions and it will revise. If something does not feel right, say so. Refine the plan until you are satisfied with the approach.

**STOP -- What you just did:** You used plan mode to design a real feature for your project before writing a single line of code. This is a pattern you will use constantly: plan first, then build. The back-and-forth questioning in step 2.3 is how you pressure-test a design. Claude does not get defensive about its plans -- ask hard questions and it will revise.

### 2.3b Choose Your Model

**Why this step:** Claude Code is not one model -- it is three. Picking the right one for the task at hand saves time and money, and gets you better results.

Type `/model` to open the model picker. You will see three tiers:

- **Haiku** -- fastest and cheapest. Great for quick lookups, simple edits, and repetitive tasks.
- **Sonnet** -- the balanced default. Handles ~90% of everyday coding: building features, fixing bugs, writing tests.
- **Opus** -- deepest reasoning. Use it for architecture decisions, complex refactors, and security reviews.

You will also see an **effort level** bar at the bottom of the picker (low / medium / high) when Opus or Sonnet is selected. Use the `<-` `->` arrow keys to adjust it. Higher effort means deeper reasoning but slower responses. Medium is the default and works for most tasks. Try low for simple edits, high for complex design decisions.

You just spent time in plan mode designing a feature. That kind of open-ended design thinking is where Opus shines -- deeper reasoning means better tradeoff analysis. Now that you are about to switch to execution mode and build, Sonnet is the right choice -- the instructions are clear and scoped.

**Other useful commands:**

- `Alt+P` (or `Option+P` on Mac) -- switch models without clearing your prompt
- `/fast` -- toggle fast mode for quicker responses (same model, optimized output)

**STOP -- What you just did:** You learned that Claude Code is not one-size-fits-all. Planning benefits from Opus's deeper reasoning. Mechanical code generation can use Sonnet. Quick lookups can use Haiku. Matching the model to the task is a habit that saves time and money. Use Opus for design and architecture, Sonnet for building. See `context/models.txt` for the full reference.

### 2.4 Exit Plan Mode and Execute

Press `Shift+Tab` to return to normal mode. Now tell Claude to start building -- but scope it down. You do not want the entire feature at once. Pick the smallest piece that is independently useful:

```
Let's start building from the plan. Implement just [the first piece --
e.g., the data model, the core function, the base component]. Don't build
[the rest] yet -- just this foundation.
```

Constraining scope is a key prompting skill -- it keeps Claude focused and prevents runaway changes across your codebase. Let Claude make the changes, then verify them.

**Try it now -- show Claude the result.** If your project has a UI, open it in the browser, take a screenshot, and paste it into the Claude Code chat. On Windows use `Alt+V` to paste from clipboard, on macOS/Linux use `Ctrl+V`. You can also drag and drop a screenshot file directly into the chat. Tell Claude something like: "Here is what the result looks like -- what do you think?" If your project is backend or CLI-based, run the relevant commands and share the output with Claude.

**STOP -- What you just did:** You went from plan mode to normal mode and gave Claude a focused, scoped instruction. Notice that you told Claude what to build *and* what NOT to build yet. Constraining scope is a key prompting skill -- it keeps Claude focused and prevents runaway changes. You also learned that you can share screenshots or command output with Claude for feedback.

**Quick check before continuing:**
- [ ] You have a plan that covers the full feature
- [ ] Claude built the first scoped piece of the feature
- [ ] You verified the changes work (browser, tests, or manual check)
- [ ] You are back in normal mode (check the mode indicator)

### 2.5 Create a Feature Branch

**Why this step:** Feature branches keep your experiments separate from working code. If something goes wrong, you can throw away the branch without affecting main. This is also how real teams work -- every feature gets its own branch.

```
! git checkout -b feature/your-feature-name
```

### 2.6 Build the Next Piece

Ask Claude to build the next component from your plan. Be specific about what this piece should do and how it connects to what you already built:

```
Now build [the next piece from the plan]. It should [describe how it
connects to the first piece]. Follow the patterns we already use in
this project.
```

If the result does not match what you imagined, tell Claude what to change. This is a conversation, not a one-shot.

### 2.7 Build the Remaining Pieces

Continue building the remaining parts of your feature, one piece at a time. Each prompt should reference the plan and connect to what already exists:

```
Next, build [another piece]. It needs to [describe the behavior and
how it integrates with what we have so far].
```

After each piece, verify it works. Test the integration between the pieces you have built so far.

**STOP -- What you just did:** You gave Claude multiple focused prompts to build your feature incrementally. Notice the pattern: each prompt specified what to build, how it connects to existing code, and what standards to follow. The more specific your prompt, the closer the result matches what you want. You also tested after each piece -- always verify Claude's output before moving on.

### 2.8 Write and Run Tests

**Why this step:** Every project benefits from automated tests. Claude can write tests using whatever framework your project already uses -- pytest, Jest, Go's testing package, JUnit, or even a simple validation script. If your project does not have a test framework yet, this is a good time to add one.

Ask Claude to write tests for the feature you just built. Reference your project's existing test patterns:

```
Write tests for the feature we just built. Use [your test framework]
and follow the patterns in [your existing test directory]. Cover the
happy path, edge cases, and error handling. Then run them.
```

If your project has no tests yet, try:

```
Set up a test framework for this project and write tests for the feature
we just built. Pick a framework that fits our language and project
structure. Then run the tests.
```

Watch Claude write the tests, run them, and fix any failures. The build-test-fix cycle is the core workflow -- Claude gets concrete error messages and fixes them immediately.

**STOP -- What you just did:** You just experienced the build-test-fix loop that will be your primary workflow for the rest of this project. Claude wrote tests, ran them, saw failures, fixed the code, and re-ran until everything passed. This tight feedback loop is why Claude Code is so effective -- Claude gets concrete error messages and fixes them immediately, rather than guessing.

### 2.9 Manual Testing

Test your feature manually. Run your application, exercise the new functionality, and look for anything that seems off. If you find issues -- bugs, unexpected behavior, integration problems -- tell Claude what you see and ask it to fix them.

```
I found an issue: [describe what you observed]. The expected behavior
is [what should happen instead]. Fix it.
```

### 2.10 Commit and Merge

**Why this step:** Committing through Claude Code (using `!` prefix for shell commands) keeps everything in one place. You do not need to switch terminals. The merge back to main means your feature branch work is now part of your stable codebase.

```
! git add -A
! git commit -m "feat: add [your feature description]"
! git checkout main
! git merge feature/your-feature-name
```

### 2.11 Branching & Quick Plans

Two workflow commands have been updated recently:

**`/branch` (was `/fork`).** The command to branch your conversation into a new session has been renamed from `/fork` to `/branch` (v2.1.77). The old name still works as an alias, but `/branch` is now the canonical command.

**`/plan` with a description.** You can now pass a description directly: `/plan fix the auth bug`. This enters plan mode and immediately starts planning -- no extra prompt needed (v2.1.72).

**Session naming from plans.** When you accept a plan, your session is automatically named based on the plan content (v2.1.77). This makes `/resume` more useful since sessions have meaningful names.

**Git instruction control.** The `includeGitInstructions` setting (or `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` env var) lets you remove Claude's built-in commit and PR workflow instructions from the system prompt. Useful if your CLAUDE.md already has custom git rules (v2.1.69).

**Edit without Read.** The Edit tool now works on files you've viewed via Bash (using `sed -n` or `cat`), without requiring a separate `Read` call first. This means fewer permission prompts when you're already looking at file content (v2.1.89).

> **STOP** -- Try `/plan add a contact form to the homepage` to test the quick-plan workflow.

### Checkpoint

You just planned and built a real feature for your project. Plan mode helped you think before building, and you shipped something real.

- [ ] Tried `/branch` and `/plan <description>` quick workflow
- [ ] You used plan mode to design the feature before writing code
- [ ] You chose an appropriate model for planning (Opus) and building (Sonnet)
- [ ] The feature was built incrementally -- scoped pieces, not all at once
- [ ] Each piece was verified before moving to the next
- [ ] Automated tests exist and pass for the new feature
- [ ] Manual testing confirmed the feature works as expected
- [ ] Changes are committed and merged to main
