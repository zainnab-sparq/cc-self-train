# Module 3 -- Rules, Memory & Context

**CC features:** .claude/rules/, CLAUDE.local.md, @imports, /context, /compact, memory hierarchy, /cost

> **Persona — Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

In this module you learn how to give Claude structured, persistent instructions that apply to specific parts of your codebase.

### Step 1: Create path-scoped rules

> **Why this step:** Path-scoped rules let you give Claude different instructions for different parts of your codebase. Instead of one giant instruction file, you can say "when working on analyzers, follow these conventions" and "when working on tests, follow these conventions." Claude automatically loads only the rules relevant to the files it is touching.

> **Engineering value:**
> - *Entry-level:* Rules are like linting configs but for Claude's behavior — they enforce your team's conventions automatically.
> - *Mid-level:* Path-scoped rules mean your test files get different AI guidance than your production code. A rule in `tests/` can enforce test patterns without affecting `src/`.
> - *Senior+:* This is the same configuration-as-code pattern used by .gitattributes (path-scoped git behavior) and CODEOWNERS (path-scoped review). Modular, composable, version-controlled.

Create the `.claude/rules/` directory in your sentinel project. Ask Claude to set up path-scoped rule files -- one for analyzer modules, one for reporters, and one for tests. Describe the conventions you want each rule file to enforce.

For example, you might want analyzer rules to say that every analyzer must be stateless and return structured Issue objects. Reporter rules might require streaming support for large codebases. Test rules might require fixture files with known issues rather than testing against live code.

> "Create a `.claude/rules/` directory with three path-scoped rule files: one for analyzers (scoped to analyzer/rule paths), one for reporters (scoped to reporter/formatter paths), and one for tests (scoped to test paths). Each should describe the conventions for that area of the codebase -- I'll tell you what they should say."

Claude will ask you about the conventions, or propose some based on your project. Discuss them until you are happy with what each rule file says. Make sure each file has `paths:` frontmatter so it only loads when Claude is working on relevant files.

> **STOP -- What you just did:** You created targeted instructions that Claude loads based on file paths. Now when Claude edits an analyzer file, it knows analyzers must be stateless and return structured Issue objects. When it writes tests, it knows to use fixture files. This is far more effective than dumping all conventions into a single file -- Claude gets precisely the context it needs, when it needs it.

Want to see how CLAUDE.local.md handles personal preferences?

### Step 2: Create CLAUDE.local.md

> **Why this step:** CLAUDE.local.md is your *personal* memory file -- it stores preferences that should not be shared with the team (like your preferred output format or local file paths). It is automatically gitignored, so it never gets committed.

Create a `CLAUDE.local.md` file in the project root. This file is for your personal preferences and is automatically added to .gitignore. Ask Claude to create it, and tell it about your personal preferences -- things like your preferred output format, where your test fixtures live, or how you like test output displayed.

> "Create a CLAUDE.local.md with my personal preferences -- I like verbose test output, my fixtures are in tests/fixtures/, and I prefer JSON format for local testing. Also note any code quality or issue-tracking tools I use (like GitHub or Jira) -- we'll connect them in Module 6."

Your preferences will be different from the example above. Put whatever is actually useful for your workflow.

### Step 3: Understand the memory hierarchy

Ask Claude to walk you through the full memory hierarchy for this project. You want to understand what files are loaded, in what order, and which ones take precedence.

> "Show me the full memory hierarchy for this project -- what files get loaded, in what order, and which ones override which?"

Claude should describe: managed policy (if any) -> user memory (~/.claude/CLAUDE.md) -> project memory (CLAUDE.md) -> project rules (.claude/rules/*.md) -> local project memory (CLAUDE.local.md).

> **STOP -- What you just did:** You explored the full memory hierarchy -- from global user settings down to local project preferences. Understanding this hierarchy matters because it determines what Claude knows and when. Managed policy overrides everything, then user memory, then project memory, then rules, then local memory. When Claude does something unexpected, checking which memory files are loaded is the first debugging step.

Want to try @imports to keep CLAUDE.md concise?

### Step 4: Use @imports

> **Why this step:** @imports let CLAUDE.md reference other files without copying their contents inline. This keeps CLAUDE.md concise while giving Claude access to detailed documentation. When the imported file changes, Claude automatically picks up the latest version.

Ask Claude to create documentation files that CLAUDE.md will import. You want a rule format guide (how to define new rules, required fields, an example) and a brief architecture overview. Then update CLAUDE.md to reference both using `@`-syntax imports.

> "Create docs/rule-format.md describing how to define custom rules, and docs/architecture.md with an architecture overview. Then update CLAUDE.md to import both using @-syntax, like `See @docs/rule-format.md for the rule definition format.`"

After Claude creates the files, open CLAUDE.md and verify the `@imports` are there. These references let Claude load the full docs on demand without cluttering CLAUDE.md itself.

> **Engineering value:**
> - *Entry-level:* Large projects have too much code for Claude to read at once. @imports let you point Claude at exactly the files it needs — like giving a new teammate the right docs before they start.
> - *Mid-level:* /compact reclaims context space during long sessions. Without it, Claude loses track of earlier conversation — with it, you can run marathon refactoring sessions.

> **Quick check before continuing:**
> - [ ] `.claude/rules/` has at least 3 path-scoped rule files with frontmatter
> - [ ] `CLAUDE.local.md` exists in the project root
> - [ ] `CLAUDE.md` uses @imports to reference your docs files

### Step 5: Check context usage with /context

Type in Claude Code:

```
/context
```

This shows a colored grid representing how much of Claude's context window is used. Notice how memory files, rules, and conversation history all consume context.

### Step 6: Manage context with /compact

```
/compact Focus on the rule engine and analyzer modules
```

This compacts the conversation, keeping the parts most relevant to your focus instruction. Useful when your context window fills up during long sessions.

### Step 7: Check costs with /cost

```
/cost
```

This shows your token usage statistics for the current session. Get in the habit of checking this periodically.

> **Note:** On Claude subscriptions (Pro/Max/Team), `/cost` may show limited or empty output due to known issues. If you see blank results, don't worry -- your token usage is still being tracked. API key users will see detailed cost breakdowns.

> **STOP -- What you just did:** You learned the three context management commands: `/context` shows how full your context window is, `/compact` compresses conversation history to free up space, and `/cost` shows your token usage. These are essential for long sessions -- if Claude starts forgetting things or giving vague answers, your context window is probably full. Use `/compact` with a focus instruction to keep the most relevant context and discard the rest.

How about we build a new rule using all these tools together?

### Step 8: Build a new rule using these tools

Now put it all together. Ask Claude to build a new analysis rule while it has all this context loaded. Describe a complexity rule -- something that estimates cyclomatic complexity by counting decision points (if/else, loops, logical operators) and flags functions that exceed a threshold.

> "Add a new analyzer rule that estimates cyclomatic complexity. It should count decision points and flag functions over a configurable threshold. Follow the conventions in our rules files and the format in @docs/rule-format.md, and include tests."

Notice how you can reference `@docs/rule-format.md` in your prompt -- Claude will load the imported file. Watch how Claude follows the path-scoped rules automatically when it creates the analyzer and test files.

### Checkpoint

You just taught Claude how your analyzer works. Rules enforce your conventions automatically, and context management keeps sessions focused.

- [ ] `.claude/rules/` directory exists with at least 3 path-scoped rule files
- [ ] `CLAUDE.local.md` exists and is in .gitignore
- [ ] `CLAUDE.md` uses `@imports` to reference docs/rule-format.md and docs/architecture.md
- [ ] You ran `/context` and understood the context grid
- [ ] You ran `/compact` with a focus instruction
- [ ] You ran `/cost` to check token usage
- [ ] A new analyzer rule was built following the path-scoped conventions
