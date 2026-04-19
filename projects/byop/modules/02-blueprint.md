# Module 2 -- Blueprint and Build

<!-- progress:start -->
**Progress:** Module 2 of 10 `[██░░░░░░░░]` 20%

**Estimated time:** ~60-90 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** Plan mode, model selection, git integration, basic prompting

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try...", "Here's what that does..."

</details>

### 2.1 Enter Plan Mode

**Why this actually matters -- a story:**

Dev A asks Claude to "refactor the auth flow to use JWT." Claude touches 14 files, introduces a bug in the refresh logic, and Dev A spends 3 hours reverting half the changes and debugging the other half.

Dev B enters plan mode first and asks the same question. Claude produces a 6-step plan, flags that the refresh logic is subtle, and asks whether the existing session-based code needs to coexist. Dev B clarifies the scope, agrees to the plan, exits plan mode -- and the refactor lands clean in 20 minutes.

Same model, same task, same prompt. **The difference is plan mode.** You spend 2 minutes planning to save 3 hours untangling. Use it every time the answer might touch more than one file.

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

### 2.3b Models Work Automatically for Now

**Why this step:** Claude Code picks a model for you based on your subscription -- for this training, the default just works. You will learn fine-grained model control later, once the basics are solid.

- **Pro / API users** default to Sonnet 4.6 -- the balanced model that handles most coding tasks well.
- **Max / Team Premium users** default to Opus 4.6 -- the most capable model for complex reasoning.

Either default is great for what we are doing. Module 8 (subagents) shows when and how to switch models with `/model`, tune reasoning depth with `/effort`, or speed up Opus with `/fast`.

**STOP -- What you just did:** You learned that Claude Code picks a model automatically. Trust the default for this training; you will learn when and how to switch it in Module 8. Full reference: `context/models.txt`.

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

**New to branches?** A Git branch is a parallel copy of your code where you can experiment safely. If the experiment works, you merge it back to main. If it fails, you delete the branch and main is untouched. The command below creates a new branch called `feature/your-feature-name` and switches you to it -- you can see which branch you are on anytime with `! git branch`.

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

**If something goes wrong:** The most common issue on a first merge is a *conflict* -- when Git cannot figure out how to combine changes. For this module, `main` has not moved since you branched, so conflicts are not expected. If you do see a conflict message, do not panic -- ask Claude: "I got a merge conflict. Can you help me resolve it?" and Claude will walk you through it.

```
! git status                # inspect what's about to be staged
! git add <files or dirs you want to commit>   # name them explicitly
! git commit -m "feat: add [your feature description]"
! git checkout main
! git merge feature/your-feature-name
```

**Heads up:** `git add -A` is tempting, but it will stage `.env` files, IDE configs, and build artifacts you may not have meant to commit. Run `git status` first, then `git add` the specific paths you actually want. The first time someone commits a `.env` is a very bad day.

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

You just planned and built a real feature for your project. Plan mode helped you think before building, and you shipped something real.

- [ ] Tried `/branch` and `/plan <description>` quick workflow
- [ ] You used plan mode to design the feature before writing code
- [ ] You chose an appropriate model for planning (Opus) and building (Sonnet)
- [ ] The feature was built incrementally -- scoped pieces, not all at once
- [ ] Each piece was verified before moving to the next
- [ ] Automated tests exist and pass for the new feature
- [ ] Manual testing confirmed the feature works as expected
- [ ] Changes are committed and merged to main
