# Module 2 -- Blueprint & Build

**CC features:** Plan mode, model selection, git integration, basic prompting

> **Persona — Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

In this module you design Sentinel's architecture in plan mode, then switch to execution mode to build the core.

### Step 1: Enter plan mode

> **Why this step:** Plan mode is Claude Code's "think before you build" feature. Instead of jumping straight into generating files, you get to explore architecture decisions with Claude while it is prevented from changing anything. This is where you catch design mistakes cheaply -- before they are baked into code.

So far, you've been talking to Claude in normal mode — you say something, Claude does it. Press `Shift+Tab` until you see the mode indicator switch to **Plan Mode**. **Instead of writing code, Claude thinks *with* you — it analyzes, suggests architecture, and asks clarifying questions, but doesn't touch any files.** This is read-only exploration.

Alternatively, type:

```
/plan
```

### Step 2: Design the architecture

Now describe your code analyzer to Claude. You are in plan mode, so Claude will think through the design without creating any files. Tell it about the core pieces -- scanning files, applying rules, reporting issues -- and what CLI commands you want. Do not worry about getting the prompt perfect. Just describe your vision and let Claude ask clarifying questions.

Something like:

> "I want to build a code analyzer CLI called Sentinel. It should recursively scan source files, apply configurable rules (things like complexity thresholds, naming conventions, missing docs, unused imports), and report issues with severity levels. I also need a CLI with commands like `sentinel scan`, `sentinel rules`, and `sentinel report`. Help me design the architecture -- ask me questions about anything that's unclear."

Claude will probably ask about which languages to support, how rules should be structured, what output formats you want, and how the components should connect. Answer naturally -- these are your design decisions. Once Claude produces a plan, read through it carefully.

> **STOP -- What you just did:** You used plan mode to design your analyzer before writing a single line of code. This is one of Claude Code's most powerful patterns: you can think through complex decisions *with* Claude before committing to an approach. Plan mode prevents the "just start coding" trap that leads to rewrites. You will use this pattern whenever you face a non-trivial feature -- sketch the design first, then build.

Ready to iterate on the plan?

### Step 3: Iterate on the plan

Push back on the plan while you are still in plan mode. Ask Claude about the parts that feel unclear or where you have opinions. For example, you might want to know how users will add custom rules without touching the core engine, or whether the reporter should stream results or batch them for large codebases.

This is a conversation -- challenge the design, ask "why not X instead?", and let Claude refine the plan based on your feedback. The goal is a plan you actually agree with, not just whatever Claude suggests first.

### Step 3b: Choose your model

> **Why this step:** Claude Code is not one model -- it is three. Picking the right one for the task at hand saves time and money, and gets you better results.

Type `/model` to open the model picker. You will see three tiers:

- **Haiku** -- fastest and cheapest. Great for quick lookups, simple edits, and repetitive tasks.
- **Sonnet** -- the balanced default. Handles ~90% of everyday coding: building features, fixing bugs, writing tests.
- **Opus** -- deepest reasoning. Use it for architecture decisions, complex refactors, and security reviews.

You just spent time in plan mode designing your analyzer's architecture. That kind of open-ended design thinking is where Opus shines -- deeper reasoning means better tradeoff analysis (like how rules should be structured and how the scanner should handle large codebases). Now that you are about to switch to execution mode and build the skeleton, Sonnet is the right choice -- the instructions are clear and scoped.

**Other useful commands:**

- `Alt+P` (or `Option+P` on Mac) -- switch models without clearing your prompt
- `/fast` -- toggle fast mode for quicker responses (same model, optimized output)
- Effort levels (Opus only) -- control reasoning depth via `/model` menu: low for quick tasks, high for deep analysis

> **STOP -- What you just did:** You learned that Claude Code is not one-size-fits-all. Planning benefits from Opus's deeper reasoning. Mechanical code generation can use Sonnet. Quick lookups can use Haiku. Matching the model to the task is a habit that saves time and money. Use Opus for analysis algorithm design, Sonnet for report generation. See `context/models.txt` for the full reference.

### Step 4: Exit plan mode and execute

> **Why this step:** Switching from plan mode to normal mode is the moment you go from "thinking" to "doing." Claude will now create real files based on the architecture you just agreed on. Starting with stubs (empty functions with docstrings) lets you verify the structure is right before filling in logic.

Press `Shift+Tab` to switch back to normal mode. Now ask Claude to create the project skeleton based on the plan you just agreed on. Tell it you want the directory layout, the entry point, and stub modules with docstrings or comments explaining what each one does -- but not the full logic yet, just the structure.

Something like:

> "Let's build the skeleton we just designed. Set up the directory layout, create the entry point, and stub out each module with comments explaining its purpose. Don't implement the full logic yet -- just the structure."

Claude will create files. Review each one before accepting.

**Screenshot trick:** If you hit an error you can't figure out, take a screenshot and drag it directly into the Claude Code chat. Claude can see images -- so instead of copy-pasting a messy stack trace, just screenshot your terminal and drop it in. You can also paste images from clipboard with `Ctrl+V` (macOS/Linux) or `Alt+V` (Windows).

> **STOP -- What you just did:** You went through the full plan-then-build cycle. Claude designed the architecture in plan mode, you asked questions to refine it, then you switched to normal mode and Claude created the project skeleton. Notice how you reviewed each file before accepting -- that review step is critical. Claude is a collaborator, not an autopilot.

Want to set up a feature branch and start building?

### Step 5: Create a feature branch

```
! git add -A
! git commit -m "Initial project skeleton"
! git checkout -b feature/core
```

Or ask Claude to do it:

```
Create a feature branch called feature/core and commit the project skeleton.
```

> **Why this step:** Feature branches keep your experiments separate from working code. If something goes wrong while building the scanner or rule engine, you can throw away the branch without affecting main. Claude can handle all the git operations for you -- branching, committing, merging -- so you stay in the flow.

### Step 6: Implement the file scanner and basic rule engine

Ask Claude to implement the file scanner module. Describe what you need -- it should walk a directory tree, filter by file extension, skip things like `.git` and `node_modules`, and return file paths with metadata. Then ask for a couple of starter rules, like detecting functions that are too long or public functions missing documentation.

> "Implement the file scanner -- it should recursively walk directories, filter by extension, skip hidden dirs and things like node_modules, and return file paths with metadata. Then add two basic analysis rules: one that flags functions over N lines, and one that flags public functions without docstrings."

Claude may ask you about thresholds, which extensions to support by default, or how to define "public function" in your chosen language. These details are up to you.

> **Quick check before continuing:**
> - [ ] Your project has a clear directory structure with separate modules
> - [ ] The file scanner and at least two rules are implemented
> - [ ] You are on the feature/core branch (not main)

### Step 7: Write and run tests

Ask Claude to write tests for what you just built. Tell it you want tests for the file scanner and both rules, using your language's standard test framework. Mention the kinds of cases you care about -- fixture directories with known files, making sure hidden directories get skipped, verifying extension filtering works, and checking that each rule catches real violations while passing clean code.

> "Write tests for the file scanner and both rules. Include tests with fixture files, make sure hidden dirs are skipped, test the extension filtering, and verify each rule catches violations and passes clean code. Then run them."

Watch Claude write tests, execute them with `!`, fix failures, and re-run. This is the build-test-fix-commit cycle.

> **STOP -- What you just did:** You just experienced the build-test-fix loop that will be your primary workflow for the rest of this project. Claude wrote tests, ran them, saw failures, fixed the code, and re-ran until everything passed. This tight feedback loop is why Claude Code is so effective -- Claude gets concrete error messages and fixes them immediately, rather than guessing.

Shall we wire up the CLI next?

### Step 8: Implement the CLI

Ask Claude to wire up a CLI so you can run Sentinel from the command line. Describe the commands you want -- at minimum `sentinel scan <path>` to run analysis and `sentinel rules list` to show available rules. Let Claude pick the standard CLI framework for your language.

> "Add a CLI with `sentinel scan <path>` to run analysis and print results, and `sentinel rules list` to show available rules. Wire it up to the scanner and rule engine we already have."

### Step 9: Manual test

```
! sentinel scan .
```

Or the equivalent command for your language. Scan the sentinel project itself and see what the analyzer finds.

> **STOP -- What you just did:** You wired together the scanner, rule engine, and CLI into a working tool, then tested it on its own source code. Sentinel can now analyze real code. Running your analyzer on itself ("dog-fooding") is a great way to find gaps -- if Sentinel misses obvious issues in its own code, it needs better rules.

Ready to commit and merge everything to main?

### Step 10: Commit and merge

Ask Claude to commit everything on `feature/core` and merge it back to main.

> "Commit all changes on feature/core with a good commit message, then merge back to main."

### Checkpoint

You just went from an empty directory to a working code scanner. Plan mode helped you design the architecture first, and now `sentinel scan` actually runs.

- [ ] You used plan mode to design the architecture before writing code
- [ ] The project has a clear directory structure with separate modules
- [ ] File scanner works and filters by extension
- [ ] At least two analysis rules are implemented and tested
- [ ] CLI runs `sentinel scan <path>` and prints results
- [ ] All tests pass
- [ ] Changes are committed and merged to main
