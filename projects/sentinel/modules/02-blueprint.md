# Module 2 -- Blueprint & Build

<!-- progress:start -->
**Progress:** Module 2 of 10 `[██░░░░░░░░]` 20%

**Estimated time:** ~60-90 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** Plan mode, model selection, git integration, basic prompting

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

</details>

In this module you design Sentinel's architecture in plan mode, then switch to execution mode to build the core.

### 2.1 Enter Plan Mode

**Why this actually matters -- a story:**

Dev A asks Claude to "refactor the auth flow to use JWT." Claude touches 14 files, introduces a bug in the refresh logic, and Dev A spends 3 hours reverting half the changes and debugging the other half.

Dev B enters plan mode first and asks the same question. Claude produces a 6-step plan, flags that the refresh logic is subtle, and asks whether the existing session-based code needs to coexist. Dev B clarifies the scope, agrees to the plan, exits plan mode -- and the refactor lands clean in 20 minutes.

Same model, same task, same prompt. **The difference is plan mode.** You spend 2 minutes planning to save 3 hours untangling. Use it every time the answer might touch more than one file.

So far, you've been talking to Claude in normal mode — you say something, Claude does it. Press `Shift+Tab` until you see the mode indicator switch to **Plan Mode**. **Instead of writing code, Claude thinks *with* you — it analyzes, suggests architecture, and asks clarifying questions, but doesn't touch any files.** This is read-only exploration.

Alternatively, type:

```
/plan
```

### 2.2 Design the Architecture

Now describe your code analyzer to Claude. You are in plan mode, so Claude will think through the design without creating any files. Tell it about the core pieces -- scanning files, applying rules, reporting issues -- and what CLI commands you want. Do not worry about getting the prompt perfect. Just describe your vision and let Claude ask clarifying questions.

Something like:

Try something like:

```
I want to build a code analyzer CLI called Sentinel. It should recursively scan source files, apply configurable rules (things like complexity thresholds, naming conventions, missing docs, unused imports), and report issues with severity levels. I also need a CLI with commands like `sentinel scan`, `sentinel rules`, and `sentinel report`. Help me design the architecture -- ask me questions about anything that's unclear.
```

Claude will probably ask about which languages to support, how rules should be structured, what output formats you want, and how the components should connect. Answer naturally -- these are your design decisions. Once Claude produces a plan, read through it carefully.

**STOP -- What you just did:** You used plan mode to design your analyzer before writing a single line of code. This is one of Claude Code's most powerful patterns: you can think through complex decisions *with* Claude before committing to an approach. Plan mode prevents the "just start coding" trap that leads to rewrites. You will use this pattern whenever you face a non-trivial feature -- sketch the design first, then build.

Ready to iterate on the plan?

### 2.3 Iterate on the Plan

Push back on the plan while you are still in plan mode. Ask Claude about the parts that feel unclear or where you have opinions. For example, you might want to know how users will add custom rules without touching the core engine, or whether the reporter should stream results or batch them for large codebases.

This is a conversation -- challenge the design, ask "why not X instead?", and let Claude refine the plan based on your feedback. The goal is a plan you actually agree with, not just whatever Claude suggests first.

### 2.3b Models Work Automatically for Now

**Why this step:** Claude Code picks a model for you based on your subscription -- for this training, the default just works. You will learn fine-grained model control later, once the basics are solid.

- **Pro / API users** default to Sonnet 4.6 -- the balanced model that handles most coding tasks well.
- **Max / Team Premium users** default to Opus 4.6 -- the most capable model for complex reasoning.

Either default is great for what we are doing. Module 8 (subagents) shows when and how to switch models with `/model`, tune reasoning depth with `/effort`, or speed up Opus with `/fast`.

**STOP -- What you just did:** You learned that Claude Code picks a model automatically. Trust the default for this training; you will learn when and how to switch it in Module 8. Full reference: `context/models.txt`.

### 2.4 Exit Plan Mode and Execute

**Why this step:** Switching from plan mode to normal mode is the moment you go from "thinking" to "doing." Claude will now create real files based on the architecture you just agreed on. Starting with stubs (empty functions with docstrings) lets you verify the structure is right before filling in logic.

Press `Shift+Tab` to switch back to normal mode. Now ask Claude to create the project skeleton based on the plan you just agreed on. Tell it you want the directory layout, the entry point, and stub modules with docstrings or comments explaining what each one does -- but not the full logic yet, just the structure.

Something like:

Try something like:

```
Let's build the skeleton we just designed. Set up the directory layout, create the entry point, and stub out each module with comments explaining its purpose. Don't implement the full logic yet -- just the structure.
```

Claude will create files. Review each one before accepting.

**Screenshot trick:** If you hit an error you can't figure out, take a screenshot and drag it directly into the Claude Code chat. Claude can see images -- so instead of copy-pasting a messy stack trace, just screenshot your terminal and drop it in. You can also paste images from clipboard with `Ctrl+V` (macOS/Linux) or `Alt+V` (Windows).

**STOP -- What you just did:** You went through the full plan-then-build cycle. Claude designed the architecture in plan mode, you asked questions to refine it, then you switched to normal mode and Claude created the project skeleton. Notice how you reviewed each file before accepting -- that review step is critical. Claude is a collaborator, not an autopilot.

Want to set up a feature branch and start building?

### 2.5 Create a Feature Branch

**New to branches?** A Git branch is a parallel copy of your code where you can experiment safely. If the experiment works, you merge it back to main. If it fails, you delete the branch and main is untouched. The command below creates a new branch called `feature/core` and switches you to it -- you can see which branch you are on anytime with `! git branch`.

```
! git status                # inspect what's about to be staged
! git add <files or dirs you want to commit>   # name them explicitly
! git commit -m "Initial project skeleton"
! git checkout -b feature/core
```

**Heads up:** `git add -A` is tempting, but it will stage `.env` files, IDE configs, and build artifacts you may not have meant to commit. Run `git status` first, then `git add` the specific paths you actually want. The first time someone commits a `.env` is a very bad day.

Or ask Claude to do it:

```
Create a feature branch called feature/core and commit the project skeleton.
```

**Why this step:** Feature branches keep your experiments separate from working code. If something goes wrong while building the scanner or rule engine, you can throw away the branch without affecting main. Claude can handle all the git operations for you -- branching, committing, merging -- so you stay in the flow.

### 2.6 Implement the File Scanner and Basic Rule Engine

Ask Claude to implement the file scanner module. Describe what you need -- it should walk a directory tree, filter by file extension, skip things like `.git` and `node_modules`, and return file paths with metadata. Then ask for a couple of starter rules, like detecting functions that are too long or public functions missing documentation.

Try something like:

```
Implement the file scanner -- it should recursively walk directories, filter by extension, skip hidden dirs and things like node_modules, and return file paths with metadata. Then add two basic analysis rules: one that flags functions over N lines, and one that flags public functions without docstrings.
```

Claude may ask you about thresholds, which extensions to support by default, or how to define "public function" in your chosen language. These details are up to you.

**Quick check before continuing:**
- [ ] Your project has a clear directory structure with separate modules
- [ ] The file scanner and at least two rules are implemented
- [ ] You are on the feature/core branch (not main)

### 2.7 Write and Run Tests

Ask Claude to write tests for what you just built. Tell it you want tests for the file scanner and both rules, using your language's standard test framework. Mention the kinds of cases you care about -- fixture directories with known files, making sure hidden directories get skipped, verifying extension filtering works, and checking that each rule catches real violations while passing clean code.

Try something like:

```
Write tests for the file scanner and both rules. Include tests with fixture files, make sure hidden dirs are skipped, test the extension filtering, and verify each rule catches violations and passes clean code. Then run them.
```

Watch Claude write tests, execute them with `!`, fix failures, and re-run. This is the build-test-fix-commit cycle.

**STOP -- What you just did:** You just experienced the build-test-fix loop that will be your primary workflow for the rest of this project. Claude wrote tests, ran them, saw failures, fixed the code, and re-ran until everything passed. This tight feedback loop is why Claude Code is so effective -- Claude gets concrete error messages and fixes them immediately, rather than guessing.

Shall we wire up the CLI next?

### 2.8 Implement the CLI

Ask Claude to wire up a CLI so you can run Sentinel from the command line. Describe the commands you want -- at minimum `sentinel scan <path>` to run analysis and `sentinel rules list` to show available rules. Let Claude pick the standard CLI framework for your language.

Try something like:

```
Add a CLI with `sentinel scan <path>` to run analysis and print results, and `sentinel rules list` to show available rules. Wire it up to the scanner and rule engine we already have.
```

### 2.9 Manual Test

```
! sentinel scan .
```

Or the equivalent command for your language. Scan the sentinel project itself and see what the analyzer finds.

**STOP -- What you just did:** You wired together the scanner, rule engine, and CLI into a working tool, then tested it on its own source code. Sentinel can now analyze real code. Running your analyzer on itself ("dog-fooding") is a great way to find gaps -- if Sentinel misses obvious issues in its own code, it needs better rules.

Ready to commit and merge everything to main?

### 2.10 Commit and Merge

**If something goes wrong:** The most common issue on a first merge is a *conflict* -- when Git cannot figure out how to combine changes. For this module, `main` has not moved since you branched, so conflicts are not expected. If you do see a conflict message, do not panic -- ask Claude: "I got a merge conflict. Can you help me resolve it?" and Claude will walk you through it.

Ask Claude to commit everything on `feature/core` and merge it back to main.

Try something like:

```
Commit all changes on feature/core with a good commit message, then merge back to main.
```

### 2.11 Branching & Quick Plans

Two workflow tricks to try now:

**`/branch`** -- makes a copy of your current conversation so you can explore a tangent without losing your main thread. Useful when you want to try something risky without burning your main session.

**`/plan <description>`** -- enters plan mode and immediately starts planning on the topic you describe. Example: `/plan add a contact form to the homepage`. Faster than pressing `Shift+Tab` then typing a prompt.

<details>
<summary><strong>Advanced settings you can ignore for now</strong></summary>

- **Session naming from plans.** When you accept a plan, your session is automatically named from the plan content, making `/resume` more useful.
- **Git instruction control.** The `includeGitInstructions` setting (or `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` env var) lets you remove Claude's built-in commit workflow from the system prompt if your CLAUDE.md already has custom git rules.
- **Edit without Read.** The Edit tool now works on files you have viewed via Bash (`sed -n` or `cat`), without requiring a separate `Read` call first -- fewer permission prompts when you are already looking at file content.

</details>

> **STOP** -- Try `/plan add a contact form to the homepage` to test the quick-plan workflow.

### Heads Up -- What's Coming in Module 3

Module 3 introduces **rule files** -- small Markdown files in `.claude/rules/` that tell Claude how to write code for different parts of your project. You will see files that start with `---` marks at the top, followed by lines like `name: react` or `paths: ["*.py"]`.

That opening block is called **frontmatter** -- metadata about the file, written in a format called **YAML**. Think of it like a form at the top of the document telling Claude Code how to use the file. One-sentence version: frontmatter lines are the file's settings, the body is its content. You will see much more of this starting in Module 3 and throughout skills, hooks, and agents.

If either term is still fuzzy, the [glossary](../../../GLOSSARY.md) has plain-English definitions.

### Checkpoint

You just went from an empty directory to a working code scanner. Plan mode helped you design the architecture first, and now `sentinel scan` actually runs.

- [ ] Tried `/branch` and `/plan <description>` quick workflow
- [ ] You used plan mode to design the architecture before writing code
- [ ] The project has a clear directory structure with separate modules
- [ ] File scanner works and filters by extension
- [ ] At least two analysis rules are implemented and tested
- [ ] CLI runs `sentinel scan <path>` and prints results
- [ ] All tests pass
- [ ] Changes are committed and merged to main
