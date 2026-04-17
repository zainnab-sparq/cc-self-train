# Module 2 -- Blueprint and Build

**CC features:** Plan mode, model selection, git integration, basic prompting

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

### 2.1 Enter Plan Mode

**Why this actually matters -- a story:**

Dev A asks Claude to "refactor the auth flow to use JWT." Claude touches 14 files, introduces a bug in the refresh logic, and Dev A spends 3 hours reverting half the changes and debugging the other half.

Dev B enters plan mode first and asks the same question. Claude produces a 6-step plan, flags that the refresh logic is subtle, and asks whether the existing session-based code needs to coexist. Dev B clarifies the scope, agrees to the plan, exits plan mode -- and the refactor lands clean in 20 minutes.

Same model, same task, same prompt. **The difference is plan mode.** You spend 2 minutes planning to save 3 hours untangling. Use it every time the answer might touch more than one file.

So far, you've been talking to Claude in normal mode — you say something, Claude does it. Press `Shift+Tab` to switch to plan mode. You will see the mode indicator
change. **Instead of writing code, Claude thinks *with* you — it analyzes, suggests architecture, and asks clarifying questions, but doesn't touch any files.** This is where you design before you build.

Alternatively, type:

```
/plan
```

### 2.2 Design the Architecture

Now describe your dev toolkit to Claude. Tell it about the data types you want to manage -- notes, code snippets, bookmarks, templates -- and how you would want to interact with them from the CLI. Don't worry about getting the prompt perfect. Just describe your vision and let Claude ask clarifying questions.

Something like:

"I want to build a CLI tool called forge that stores notes, code snippets, bookmarks, and templates. Help me design the architecture -- ask me questions about storage format, CLI commands, and data models. Don't write any code yet, just the plan."

Claude will probably ask about your storage preferences (JSON files vs SQLite), how you want IDs to work, and how search should behave. Answer naturally -- these are your design decisions. The back-and-forth is how you get a plan that actually fits your needs.

Once Claude produces a plan, read it carefully. Push back on anything you would do differently.

### 2.3 Review and Iterate

Still in plan mode, challenge the plan. Ask Claude about the trade-offs it made -- storage format, ID generation strategy, how search will work across types. If something feels over-engineered or too simple, say so. This is a design conversation, not a rubber stamp.

For example:

"Why did you choose that storage format? What are the trade-offs vs the alternatives? And how will search work efficiently across all four types?"

Refine the plan until you are satisfied with the design.

**STOP -- What you just did:** You used plan mode to design your entire storage layer, data models, and CLI interface before writing a single line of code. This is one of Claude Code's most valuable patterns: *think with Claude before you build with Claude.* Plan mode prevents the "just start coding" trap that leads to rewrites. You will use this design-first approach whenever you start a new feature.

Ready to exit plan mode and start building? First, let's make sure you are using the right model.

### 2.3b Models Work Automatically for Now

**Why this step:** Claude Code picks a model for you based on your subscription -- for this training, the default just works. You will learn fine-grained model control later, once the basics are solid.

- **Pro / API users** default to Sonnet 4.6 -- the balanced model that handles most coding tasks well.
- **Max / Team Premium users** default to Opus 4.6 -- the most capable model for complex reasoning.

Either default is great for what we are doing. Module 8 (subagents) shows when and how to switch models with `/model`, tune reasoning depth with `/effort`, or speed up Opus with `/fast`.

**STOP -- What you just did:** You learned that Claude Code picks a model automatically. Trust the default for this training; you will learn when and how to switch it in Module 8. Full reference: `context/models.txt`.

### 2.4 Exit Plan Mode and Execute

Press `Shift+Tab` to return to normal mode. Now ask Claude to start building -- but keep the scope narrow. Tell it to create the data models and storage layer first, without the CLI interface. You want to build in layers, not all at once.

Something like:

"Let's start building from the plan. Create the data models and the storage layer first -- no CLI yet. I want to review the core library before we add the interface on top."

Let Claude create the files. Review what it produces -- check that the models match what you agreed on in the plan.

**Screenshot trick:** If you hit an error you can't figure out, take a screenshot and drag it directly into the Claude Code chat. Claude can see images -- so instead of copy-pasting a messy stack trace, just screenshot your terminal and drop it in. You can also paste images from clipboard with `Ctrl+V` (macOS/Linux) or `Alt+V` (Windows).

**Why this step:** Feature branches keep your experiments separate from working code. If something goes wrong, you can throw away the branch without affecting main.

### 2.5 Create a Feature Branch

**New to branches?** A Git branch is a parallel copy of your code where you can experiment safely. If the experiment works, you merge it back to main. If it fails, you delete the branch and main is untouched. The command below creates a new branch called `feature/core` and switches you to it -- you can see which branch you are on anytime with `! git branch`.

```
! git checkout -b feature/core
```

### 2.6 Build the Storage Layer

If the storage layer is not fully implemented yet, describe what you still need. Tell Claude about the operations you want -- creating, reading, updating, deleting items -- plus tag filtering, search, timestamps, and validation. Let Claude figure out the implementation details.

"The storage layer still needs full CRUD operations, tag-based filtering, search across all text fields, automatic timestamps, and validation before writes. Can you fill in what's missing?"

If Claude asks you questions about how search should work or what validation means for your data types, answer based on what makes sense for your toolkit.

**STOP -- What you just did:** You went from an architecture plan to working code -- data models and a storage layer -- by giving Claude specific, scoped instructions. Notice you did not ask Claude to build everything at once. You built the core library *without* the CLI, keeping the first step focused. This incremental approach (plan, then build layer by layer) gives you chances to review and course-correct at each stage.

**Quick check before continuing:**
- [ ] Your data models exist for Note, Snippet, Bookmark, and Template
- [ ] The storage layer handles create, read, update, and delete
- [ ] You are on the `feature/core` branch (not main)

### 2.7 Write and Run Tests

Ask Claude to write tests for the storage layer. Describe what you want covered -- the happy paths (create, read, list, search, delete) and the edge cases (what happens with duplicate IDs, empty fields, missing files). Claude will likely ask about your test framework preferences if it is not obvious from your language choice.

"Write tests for the storage layer. I want coverage for all CRUD operations, tag filtering, search, and edge cases like duplicate IDs and missing files."

Run the tests:

```
! <your-test-command>
```

For example: `python -m pytest`, `npm test`, `go test ./...`, `cargo test`

If tests fail, ask Claude to fix them. This is the build-test-fix cycle you
will use throughout the project.

**Why this step:** The build-test-fix cycle is the heartbeat of working with Claude Code. You ask Claude to build something, run tests to verify it, and fix what is broken -- all without leaving the conversation. This tight loop is much faster than writing code in an editor and debugging manually.

### 2.8 Build the CLI Interface

Now ask Claude to build the CLI on top of your storage layer. Describe the commands you want -- adding items, listing them, searching, showing details, deleting, and browsing tags. Claude already knows your data models and storage API, so it can wire everything together.

"Build the CLI interface for forge. I want commands for add, list, search, show, delete, and tags. Wire them up to the storage layer we already built."

If Claude suggests a CLI framework (like argparse, click, cobra, clap), discuss whether it fits your project's needs.

### 2.9 Manual Testing

Test your CLI by actually using it:

```
! forge add note --title "First Note" --body "Testing the forge CLI" --tags "test,meta"
! forge list notes
! forge search "First"
! forge show <ID-from-list>
! forge tags
! forge delete <ID>
```

Verify each command works. Fix anything broken.

**STOP -- What you just did:** You just tested your CLI by running real commands -- not unit tests, but the actual tool a user would run. Manual testing catches problems that unit tests miss: bad argument parsing, unclear output formatting, confusing error messages. Always do both: automated tests for correctness, manual tests for usability.

Want to commit and merge everything to main?

### 2.10 Commit and Merge

**If something goes wrong:** The most common issue on a first merge is a *conflict* -- when Git cannot figure out how to combine changes. For this module, `main` has not moved since you branched, so conflicts are not expected. If you do see a conflict message, do not panic -- ask Claude: "I got a merge conflict. Can you help me resolve it?" and Claude will walk you through it.

```
! git add -A
! git commit -m "feat: core data models, storage layer, and CLI interface"
! git checkout main
! git merge feature/core
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

You just went from an idea to a working CLI tool. Plan mode helped you think through the architecture first, and now `forge` actually runs.

- [ ] Tried `/branch` and `/plan <description>` quick workflow
- [ ] You used plan mode to design the architecture before writing code
- [ ] Data models exist for Note, Snippet, Bookmark, Template
- [ ] Storage layer handles CRUD, search, and tag filtering
- [ ] CLI commands work: `forge add`, `forge list`, `forge search`, `forge show`, `forge delete`, `forge tags`
- [ ] Tests pass
- [ ] Changes are committed and merged to main
