# Module 3 -- Rules, Memory & Context

<!-- progress:start -->
**Progress:** Module 3 of 10 `[███░░░░░░░]` 30%

**Estimated time:** ~45-60 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** .claude/rules/, CLAUDE.local.md, @imports, /context, /compact, /stats, /cost, /statusline, memory hierarchy

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

</details>

In this module you learn how to give Claude structured, persistent instructions that apply to specific parts of your codebase.

> **New terms this module uses:**
> - **Rule file** -- a Markdown file in `.claude/rules/` that tells Claude how to write code for a specific part of your project (example: "use functional components, not classes").
> - **Frontmatter** -- a block of settings at the top of a Markdown file, fenced by `---` lines. Written in YAML. It tells a tool how to use the file.
> - **YAML** -- a human-readable config format with indentation and colons (`name: react`, `paths: ["*.py"]`).
> - **Path scoping** -- telling a rule file to only apply to certain directories or file types via its frontmatter. Example: a rule with `paths: ["*.py"]` only activates on Python files.
>
> If these are still fuzzy after the first few steps, the [glossary](../../../GLOSSARY.md) has them written out in more detail.

### 3.1 Create Path-Scoped Rules

**Why this step:** Path-scoped rules let you give Claude different instructions for different parts of your codebase. Instead of one giant instruction file, you can say "when working on analyzers, follow these conventions" and "when working on tests, follow these conventions." Claude automatically loads only the rules relevant to the files it is touching.

**Engineering value:**
- *Entry-level:* Rules are like linting configs but for Claude's behavior — they enforce your team's conventions automatically.
- *Mid-level:* Path-scoped rules mean your test files get different AI guidance than your production code. A rule in `tests/` can enforce test patterns without affecting `src/`.
- *Senior+:* This is the same configuration-as-code pattern used by .gitattributes (path-scoped git behavior) and CODEOWNERS (path-scoped review). Modular, composable, version-controlled.

Create the `.claude/rules/` directory in your sentinel project. Ask Claude to set up path-scoped rule files -- one for analyzer modules, one for reporters, and one for tests. Describe the conventions you want each rule file to enforce.

For example, you might want analyzer rules to say that every analyzer must be stateless and return structured Issue objects. Reporter rules might require streaming support for large codebases. Test rules might require fixture files with known issues rather than testing against live code.

Try something like:

```
Create a `.claude/rules/` directory with three path-scoped rule files: one for analyzers (scoped to analyzer/rule paths), one for reporters (scoped to reporter/formatter paths), and one for tests (scoped to test paths). Each should describe the conventions for that area of the codebase -- I'll tell you what they should say.
```

Claude will ask you about the conventions, or propose some based on your project. Discuss them until you are happy with what each rule file says. Make sure each file has `paths:` frontmatter so it only loads when Claude is working on relevant files.

**STOP -- What you just did:** You created targeted instructions that Claude loads based on file paths. Now when Claude edits an analyzer file, it knows analyzers must be stateless and return structured Issue objects. When it writes tests, it knows to use fixture files. This is far more effective than dumping all conventions into a single file -- Claude gets precisely the context it needs, when it needs it.

Want to see how CLAUDE.local.md handles personal preferences?

### 3.2 Create CLAUDE.local.md

**Why this step:** CLAUDE.local.md is your *personal* memory file -- it stores preferences that should not be shared with the team (like your preferred output format or local file paths). It is automatically gitignored, so it never gets committed.

Create a `CLAUDE.local.md` file in the project root. This file is for your personal preferences and is automatically added to .gitignore. Ask Claude to create it, and tell it about your personal preferences -- things like your preferred output format, where your test fixtures live, or how you like test output displayed.

Try something like:

```
Create a CLAUDE.local.md with my personal preferences -- I like verbose test output, my fixtures are in tests/fixtures/, and I prefer JSON format for local testing. Also note any code quality or issue-tracking tools I use (like GitHub or Jira) -- we'll connect them in Module 6.
```

Your preferences will be different from the example above. Put whatever is actually useful for your workflow.

### 3.3 Understand the Memory Hierarchy

Ask Claude to walk you through the full memory hierarchy for this project. You want to understand what files are loaded, in what order, and which ones take precedence.

Try something like:

```
Show me the full memory hierarchy for this project -- what files get loaded, in what order, and which ones override which?
```

The hierarchy from highest to lowest precedence:

1. Managed policy (organization-wide, system directory)
2. Project memory (`./CLAUDE.md` or `./.claude/CLAUDE.md`)
3. Project rules (`.claude/rules/*.md`)
4. User memory (`~/.claude/CLAUDE.md`)
5. Project local (`./CLAUDE.local.md`)

**STOP -- What you just did:** You explored the full memory hierarchy -- from managed policy down to local project preferences. Understanding this hierarchy matters because it determines what Claude knows and when. Managed policy overrides everything, then project memory, then project rules, then user memory, then local memory. When Claude does something unexpected, checking which memory files are loaded is the first debugging step.

Want to try @imports to keep CLAUDE.md concise?

### 3.4 Use @imports

**Why this step:** @imports let CLAUDE.md reference other files without copying their contents inline. This keeps CLAUDE.md concise while giving Claude access to detailed documentation. When the imported file changes, Claude automatically picks up the latest version.

Ask Claude to create documentation files that CLAUDE.md will import. You want a rule format guide (how to define new rules, required fields, an example) and a brief architecture overview. Then update CLAUDE.md to reference both using `@`-syntax imports.

Try something like:

```
Create docs/rule-format.md describing how to define custom rules, and docs/architecture.md with an architecture overview. Then update CLAUDE.md to import both using @-syntax, like `See @docs/rule-format.md for the rule definition format.`
```

After Claude creates the files, open CLAUDE.md and verify the `@imports` are there. These references let Claude load the full docs on demand without cluttering CLAUDE.md itself.

**Engineering value:**
- *Entry-level:* Large projects have too much code for Claude to read at once. @imports let you point Claude at exactly the files it needs — like giving a new teammate the right docs before they start.
- *Mid-level:* /compact reclaims context space during long sessions. Without it, Claude loses track of earlier conversation — with it, you can run marathon refactoring sessions.

**Quick check before continuing:**
- [ ] `.claude/rules/` has at least 3 path-scoped rule files with frontmatter
- [ ] `CLAUDE.local.md` exists in the project root
- [ ] `CLAUDE.md` uses @imports to reference your docs files

### 3.5 Check Context Usage With /context

**Why this step:** Claude has a finite context window -- think of it as Claude's working memory. Everything Claude needs to respond (your conversation history, CLAUDE.md, rules files, file contents it has read, tool outputs) has to fit in this window. When it fills up, Claude starts forgetting earlier parts of your conversation. The `/context` command shows you exactly what is using that space so you can manage it.

Type in Claude Code:

```
/context
```

You will see a colored grid and a breakdown of what is consuming context. Look at the output and identify:

- **System prompt & instructions** -- CLAUDE.md, rules files, and skills. These load automatically every session and take up space even before you say anything.
- **Conversation history** -- every message you have sent and every response Claude has given. This grows as you work.
- **Tool results** -- file contents Claude has read, command outputs, search results. These can be large.
- **Remaining capacity** -- how much room is left before Claude needs to compact.

**What consumes the most context?** Conversation history and tool outputs. Every file Claude reads and every command it runs adds to context. A single large file read can consume more context than dozens of chat messages.

**Tip:** Be specific about what you need. "Read lines 1-50 of analyzer.py" costs less context than "read analyzer.py" for a 500-line file. Similarly, targeted searches use less context than reading entire files.

The percentage tells you how full the window is. Early in a session it will be low. After several rounds of building and testing, it climbs.

### 3.6 Manage Context With /compact

```
/compact Focus on the rule engine and analyzer modules
```

This compacts the conversation, keeping the parts most relevant to your focus instruction. Useful when your context window fills up during long sessions.

**What happens automatically:** You do not have to run `/compact` manually every time. When your context reaches approximately 95% capacity, Claude auto-compacts the conversation. Here is what survives:

- **Always preserved:** Your CLAUDE.md, rules files, and CLAUDE.local.md. These are re-read from disk after every compaction -- they always survive. This is the key insight: anything you put in these files is permanent. Anything you only said in chat is temporary.
- **Mostly preserved:** Recent messages and code you were just working on.
- **May be lost:** Detailed instructions from early in the conversation, older file reads, and verbose command outputs (tool outputs are cleared first to make room).

**Key takeaway:** If a decision or convention is important enough to always remember, put it in CLAUDE.md or a rules file -- not in a chat message.

**STOP -- What you just did:** You learned three context management commands: `/context` shows how full your context window is, `/compact` compresses conversation history to free up space, and `/stats` or `/cost` (next step) tracks your overall usage. These are essential for long sessions -- if Claude starts forgetting things or giving vague answers, your context window is probably full. Use `/compact` with a focus instruction to keep the most relevant context and discard the rest.

### 3.7 Check Your Usage

Are you using a **Claude subscription** (Pro, Max, or Team) or an **API key**?

**If you are on a subscription (Pro/Max/Team):**

Run:

```
/stats
```

This shows your usage patterns -- daily activity, session history, streaks, and which models you use most. Subscribers do not pay per token, so cost tracking is not relevant. Use `/stats` to understand your usage habits and `/usage` to check your plan's rate limits.

**If you are using an API key:**

Run:

```
/cost
```

This shows your token usage and cost in USD for the current session. API users pay per token, so checking `/cost` periodically helps you understand which operations are expensive. A single large file read can cost more than dozens of chat messages.

**Make it persistent with /statusline:**

Instead of running `/context` or `/cost` repeatedly, you can add a persistent status bar at the bottom of your terminal:

```
/statusline show context percentage, model name, and session cost
```

Claude generates a script and configures it automatically. The status line updates after each interaction, so you always know how full your context window is without running a command. Run `/statusline` again with a different description to change what it shows -- git branch, session duration, lines changed, or anything else you want at a glance.

**Note:** Both groups should use `/context` (which you already learned) to manage the context window. `/stats` and `/cost` track your overall usage; `/context` tracks what Claude is currently "thinking about."

### 3.7b When Claude Forgets

Sometimes Claude gives vague answers, forgets an earlier decision, or asks about something you already discussed. This is not a bug -- it means context is getting full.

**Diagnosis:** Run `/context`. If usage is 80%+, older details are being compressed or lost.

**Fix 1 -- Compact with focus:** Run `/compact` with a specific focus argument to preserve what matters:

```
/compact Preserve details about the rule engine and analyzer conventions
```

**Fix 2 -- Start fresh:** If compacting is not enough, start a new session by running `claude` again in your project directory. Your CLAUDE.md, rules, and CLAUDE.local.md reload automatically -- only conversation history is lost. This is often the fastest fix for a cluttered session.

**Prevention:** If you find yourself repeatedly telling Claude the same thing, that is a sign it belongs in CLAUDE.md or a rules file, not in conversation. Chat is temporary; memory files are permanent.

How about we build a new rule using all these tools together?

### 3.8 Build a New Rule Using These Tools

Now put it all together. Ask Claude to build a new analysis rule while it has all this context loaded. Describe a complexity rule -- something that estimates cyclomatic complexity by counting decision points (if/else, loops, logical operators) and flags functions that exceed a threshold.

Try something like:

```
Add a new analyzer rule that estimates cyclomatic complexity. It should count decision points and flag functions over a configurable threshold. Follow the conventions in our rules files and the format in @docs/rule-format.md, and include tests.
```

Notice how you can reference `@docs/rule-format.md` in your prompt -- Claude will load the imported file. Watch how Claude follows the path-scoped rules automatically when it creates the analyzer and test files.

### 3.9 HTML Comments & Memory Directory

Two useful updates for managing Claude's context:

**HTML comments are now hidden.** If you add `<!-- internal notes -->` to your CLAUDE.md, Claude won't see them when the file is auto-loaded. They're only visible when Claude explicitly reads the file with the Read tool. Use this for maintainer notes, TODOs, or internal documentation that shouldn't influence Claude's behavior (v2.1.72).

**Custom memory directory.** The `autoMemoryDirectory` setting lets you store auto-memory in a custom location instead of `~/.claude/`. Useful for shared drives or custom project structures (v2.1.74).

**Smarter `/context`.** The `/context` command now gives actionable suggestions -- it identifies context-heavy tools, memory bloat, and capacity warnings with specific optimization tips (v2.1.74).

Try adding an HTML comment to your CLAUDE.md now -- something like `<!-- TODO: add testing conventions after Module 9 -->` -- and verify Claude doesn't reference it unless you ask it to read the file directly.

> **STOP** -- Add an HTML comment to your project's CLAUDE.md and verify it's hidden from Claude.

### 3.10 Path-Scoped Rules with `paths:` Frontmatter

Rules can now accept `paths:` as a YAML list of globs in their frontmatter, restricting which files they apply to. This means you can have different rules for different parts of your project -- analyzer conventions for rule modules, reporter conventions for output formatters, test conventions for spec files.

Try creating two rules with different scopes. Ask Claude something like:

```
Create two rule files in .claude/rules/:
1. analyzer-style.md with paths: [src/analyzers/**] that enforces stateless design and structured Issue objects
2. reporter-style.md with paths: [src/reporters/**] that enforces streaming support and configurable output formats
```

After creating them, test the scoping: ask Claude to edit an analyzer file and see if it follows the analyzer rule, then ask it to edit a reporter file and verify it follows the reporter rule instead.

**STOP -- What you just did:** You created rules that only load when Claude works on matching files. This is powerful for larger projects where different directories have different conventions. The `paths:` field accepts standard glob patterns -- `**` matches any depth, `*` matches any file.

> **STOP** -- Try editing files in both directories to verify each rule applies only to its scoped path.

### Checkpoint

You just taught Claude how your analyzer works. Rules enforce your conventions automatically, and context management keeps sessions focused.

- [ ] Tested `paths:` frontmatter on at least one rule
- [ ] Added an HTML comment to CLAUDE.md and verified it's hidden
- [ ] `.claude/rules/` directory exists with at least 3 path-scoped rule files
- [ ] `CLAUDE.local.md` exists and is in .gitignore
- [ ] `CLAUDE.md` uses `@imports` to reference docs/rule-format.md and docs/architecture.md
- [ ] You ran `/context` and understood the context grid
- [ ] You ran `/compact` with a focus instruction
- [ ] You ran `/stats` or `/cost` to check your usage
- [ ] A new analyzer rule was built following the path-scoped conventions
