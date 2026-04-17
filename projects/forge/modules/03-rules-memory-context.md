# Module 3 -- Rules, Memory, and Context

<!-- progress:start -->
**Progress:** Module 3 of 10 `[███░░░░░░░]` 30%

**Estimated time:** ~45-60 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** `.claude/rules/`, `CLAUDE.local.md`, `@imports`, `/context`,
`/compact`, `/stats`, `/cost`, `/statusline`, memory hierarchy

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

</details>

> **New terms this module uses:**
> - **Rule file** -- a Markdown file in `.claude/rules/` that tells Claude how to write code for a specific part of your project (example: "use functional components, not classes").
> - **Frontmatter** -- a block of settings at the top of a Markdown file, fenced by `---` lines. Written in YAML. It tells a tool how to use the file.
> - **YAML** -- a human-readable config format with indentation and colons (`name: react`, `paths: ["*.py"]`).
> - **Path scoping** -- telling a rule file to only apply to certain directories or file types via its frontmatter. Example: a rule with `paths: ["*.py"]` only activates on Python files.
>
> If these are still fuzzy after the first few steps, the [glossary](../../../GLOSSARY.md) has them written out in more detail.

### 3.1 Create Project Rules

**Why this step:** Rules are how you teach Claude your project's conventions. Instead of repeating "use fixtures in tests" or "add docstrings" in every prompt, you write it once in a rule file and Claude follows it automatically in every session.

**Engineering value:**
- *Entry-level:* Rules are like linting configs but for Claude's behavior — they enforce your team's conventions automatically.
- *Mid-level:* Path-scoped rules mean your test files get different AI guidance than your production code. A rule in `tests/` can enforce test patterns without affecting `src/`.
- *Senior+:* This is the same configuration-as-code pattern used by .gitattributes (path-scoped git behavior) and CODEOWNERS (path-scoped review). Modular, composable, version-controlled.

Create the rules directory in your project:

```
! mkdir -p .claude/rules
```

Rules are modular, topic-specific instructions that Claude loads automatically.
They use markdown files with optional YAML frontmatter for path scoping.

### 3.2 Create Path-Scoped Rules

**Why this step:** Path-scoped rules only activate when Claude works on matching files. Your testing rules apply in test files, your source code rules apply in source files. This keeps context lean -- Claude does not load storage rules when editing a test, and vice versa.

Ask Claude to create three rule files for you: one for testing conventions, one for source code style, and one for storage operations. Describe the conventions you care about for each area, and tell Claude to scope them to the right file paths using YAML frontmatter.

"Create three rule files in .claude/rules/. First, a testing.md scoped to test files -- I want rules about using fixtures, descriptive assertions, and testing both success and failure cases. Second, a source-code.md scoped to src/lib/pkg -- rules about single responsibility, docstrings, error handling, and function length. Third, a storage.md scoped to storage and data files -- rules about validation, graceful handling of missing files, and atomic writes. Use YAML frontmatter with path globs to scope each one."

Claude will ask you if it is unsure about your file structure or which glob patterns to use. Answer based on how your project is organized. Review the generated rules and adjust any conventions that do not match your preferences.

**STOP -- What you just did:** You created three rule files with YAML frontmatter that scopes each one to specific file paths. From now on, whenever Claude touches a test file, it automatically follows your testing conventions. Whenever it edits source code, it follows your source code rules. You never have to remind it -- the rules are always active. This is how teams enforce consistency without relying on code review alone.

Ready to create your CLAUDE.local.md?

### 3.3 Create CLAUDE.local.md

**Why this step:** CLAUDE.local.md is your *personal* preferences file. It gets added to `.gitignore`, which means git will never track or commit it -- your preferences stay on your machine and do not get pushed to the shared repository where they would affect other contributors. This is the split between team standards (CLAUDE.md, rules) and personal workflow (CLAUDE.local.md).

Create a personal, non-committed preferences file. Tell Claude about your individual workflow preferences -- things like how you like test output formatted, your commit message style, and your language of choice. These are *your* preferences, not team rules.

"Create a CLAUDE.local.md with my personal preferences. I like [your test output style], [your commit style], and I'm working in [your language]. Also note any productivity tools I use regularly (like Notion or Linear) -- we'll connect them in Module 6. Make sure it's in .gitignore."

Claude should add it to `.gitignore` automatically. Verify:

```
! cat .gitignore
```

If `CLAUDE.local.md` is not listed, ask Claude to add it.

**STOP -- What you just did:** You created a personal preferences file that is *not* committed to version control. This is the distinction between `CLAUDE.md` (shared team knowledge) and `CLAUDE.local.md` (your personal preferences). Your teammates see the project rules; your local preferences are yours alone. You will use this separation whenever you have personal workflow preferences that should not be imposed on the team.

Want to see how the full memory hierarchy works?

### 3.4 Understand the Memory Hierarchy

Ask Claude to explain the full memory hierarchy -- where each file lives, what takes precedence, and which ones are shared with your team vs. private to you.

"Explain the Claude Code memory hierarchy. What are all the layers, what's the precedence order, and which ones are shared vs. personal?"

The hierarchy from highest to lowest precedence:

1. Managed policy (organization-wide, system directory)
2. Project memory (`./CLAUDE.md` or `./.claude/CLAUDE.md`)
3. Project rules (`.claude/rules/*.md`)
4. User memory (`~/.claude/CLAUDE.md`)
5. Project local (`./CLAUDE.local.md`)

**Quick check before continuing:**
- [ ] `.claude/rules/` contains three rule files with YAML frontmatter
- [ ] `CLAUDE.local.md` exists and is listed in `.gitignore`
- [ ] You can explain the difference between project memory, project rules, user memory, and project local

### 3.5 Modularize CLAUDE.md with @imports

As your project grows, CLAUDE.md can become a wall of text. Ask Claude to extract the architecture and API documentation into separate files and link them with `@imports`.

"Create a docs/architecture.md that describes our project structure, data models, and storage layer. Then create docs/api.md with the storage layer's public API. Finally, add @imports to CLAUDE.md so Claude loads these when it needs that context."

The `@path` syntax tells Claude Code to load those files as additional context
when needed. Both relative and absolute paths work.

**Why this step:** As your project grows, `CLAUDE.md` can become a wall of text. `@imports` let you keep CLAUDE.md concise while linking to detailed docs that Claude loads on demand. Think of it like a table of contents that points to full chapters.

**Engineering value:**
- *Entry-level:* Large projects have too much code for Claude to read at once. @imports let you point Claude at exactly the files it needs — like giving a new teammate the right docs before they start.
- *Mid-level:* /compact reclaims context space during long sessions. Without it, Claude loses track of earlier conversation — with it, you can run marathon refactoring sessions.

**STOP -- What you just did:** You modularized your project documentation. Instead of cramming everything into one file, you created focused reference docs and linked them with `@imports`. Claude loads these when it needs architectural context or API details, keeping your main CLAUDE.md clean and scannable.

Want to explore the /context and /compact commands?

### 3.6 /context Deep Dive

**Why this step:** Claude has a finite context window -- think of it as Claude's working memory. Everything Claude needs to respond (your conversation history, CLAUDE.md, rules files, file contents it has read, tool outputs) has to fit in this window. When it fills up, Claude starts forgetting earlier parts of your conversation. The `/context` command shows you exactly what is using that space so you can manage it.

Run:

```
/context
```

You will see a colored grid and a breakdown of what is consuming context. Look at the output and identify:

- **System prompt & instructions** -- CLAUDE.md, rules files, and skills. These load automatically every session and take up space even before you say anything.
- **Conversation history** -- every message you have sent and every response Claude has given. This grows as you work.
- **Tool results** -- file contents Claude has read, command outputs, search results. These can be large.
- **Remaining capacity** -- how much room is left before Claude needs to compact.

**What consumes the most context?** Conversation history and tool outputs. Every file Claude reads and every command it runs adds to context. A single large file read can consume more context than dozens of chat messages.

**Tip:** Be specific about what you need. "Read lines 1-50 of storage.py" costs less context than "read storage.py" for a 500-line file. Similarly, targeted searches use less context than reading entire files.

The percentage tells you how full the window is. Early in a session it will be low. After several rounds of building and testing, it climbs. When it gets high, Claude will auto-compact -- or you can do it manually with `/compact` (next step).

### 3.7 /compact with Focus Argument

**Why this step:** Every Claude Code session has a finite context window. As your conversation grows, you will eventually run out of room. `/compact` reclaims space by summarizing older parts of the conversation while preserving what matters most. The focus argument is your steering wheel -- it tells Claude what to keep in detail.

When context gets large, use `/compact` to summarize the conversation:

```
/compact Preserve all details about the storage layer API and data models.
```

The argument tells Claude what to prioritize when compacting. Without it,
Claude uses its own judgment.

**What happens automatically:** You do not have to run `/compact` manually every time. When your context reaches approximately 95% capacity, Claude auto-compacts the conversation. Here is what survives:

- **Always preserved:** Your CLAUDE.md, rules files, and CLAUDE.local.md. These are re-read from disk after every compaction -- they always survive. This is the key insight: anything you put in these files is permanent. Anything you only said in chat is temporary.
- **Mostly preserved:** Recent messages and code you were just working on.
- **May be lost:** Detailed instructions from early in the conversation, older file reads, and verbose command outputs (tool outputs are cleared first to make room).

**Key takeaway:** If a decision or convention is important enough to always remember, put it in CLAUDE.md or a rules file -- not in a chat message.

**STOP -- What you just did:** You used `/context` to see how your session's context is distributed, then `/compact` to reclaim space. Context management is a real skill -- long sessions accumulate history, and eventually Claude "forgets" earlier details. Using `/compact` with a focus argument lets you control what survives the compression. Auto-compact handles this for you at ~95% capacity, but manual compacting with a focus argument gives you more control over what is preserved.

### 3.8 Check Your Usage

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

### 3.9 When Claude Forgets

Sometimes Claude gives vague answers, forgets an earlier decision, or asks about something you already discussed. This is not a bug -- it means context is getting full.

**Diagnosis:** Run `/context`. If usage is 80%+, older details are being compressed or lost.

**Fix 1 -- Compact with focus:** Run `/compact` with a specific focus argument to preserve what matters:

```
/compact Preserve details about the storage layer API and data models
```

**Fix 2 -- Start fresh:** If compacting is not enough, start a new session by running `claude` again in your project directory. Your CLAUDE.md, rules, and CLAUDE.local.md reload automatically -- only conversation history is lost. This is often the fastest fix for a cluttered session.

**Prevention:** If you find yourself repeatedly telling Claude the same thing, that is a sign it belongs in CLAUDE.md or a rules file, not in conversation. Chat is temporary; memory files are permanent.

### 3.10 Build a Feature Using These Tools

Now put everything together by building the template rendering feature. Create a feature branch and describe to Claude what you want: a command that takes a template name and variable assignments, renders the template with those values, and validates that all required variables are provided.

"Create a feature branch 'feature/templates' and build template rendering. I want a forge render command that substitutes variables into templates, validates that all required variables are provided, and errors on unknown variables. Write tests too -- follow our testing rules."

Notice how Claude follows the testing rules you created in `.claude/rules/testing.md` without you having to remind it. After building, run `/context` again to see how context changed. Then commit.

### 3.11 HTML Comments & Memory Directory

Two useful updates for managing Claude's context:

**HTML comments are now hidden.** If you add `<!-- internal notes -->` to your CLAUDE.md, Claude won't see them when the file is auto-loaded. They're only visible when Claude explicitly reads the file with the Read tool. Use this for maintainer notes, TODOs, or internal documentation that shouldn't influence Claude's behavior (v2.1.72).

**Custom memory directory.** The `autoMemoryDirectory` setting lets you store auto-memory in a custom location instead of `~/.claude/`. Useful for shared drives or custom project structures (v2.1.74).

**Smarter `/context`.** The `/context` command now gives actionable suggestions -- it identifies context-heavy tools, memory bloat, and capacity warnings with specific optimization tips (v2.1.74).

Try adding an HTML comment to your CLAUDE.md now -- something like `<!-- TODO: add testing conventions after Module 9 -->` -- and verify Claude doesn't reference it unless you ask it to read the file directly.

> **STOP** -- Add an HTML comment to your project's CLAUDE.md and verify it's hidden from Claude.

### 3.12 Path-Scoped Rules with `paths:` Frontmatter

Rules can now accept `paths:` as a YAML list of globs in their frontmatter, restricting which files they apply to. This means you can have different rules for different parts of your project -- testing conventions for test files, source code conventions for library code, storage conventions for data handling.

Try creating two rules with different scopes. Ask Claude something like:

```
Create two rule files in .claude/rules/:
1. test-style.md with paths: [tests/**] that enforces descriptive test names and fixture usage
2. lib-style.md with paths: [src/lib/**] that enforces single-responsibility functions and docstrings
```

After creating them, test the scoping: ask Claude to edit a test file and see if it follows the test rule, then ask it to edit a library file and verify it follows the lib rule instead.

**STOP -- What you just did:** You created rules that only load when Claude works on matching files. This is powerful for larger projects where different directories have different conventions. The `paths:` field accepts standard glob patterns -- `**` matches any depth, `*` matches any file.

> **STOP** -- Try editing files in both directories to verify each rule applies only to its scoped path.

### Checkpoint

You just taught Claude how your toolkit works. Rules enforce your conventions automatically, and @imports keep documentation modular.

- [ ] Tested `paths:` frontmatter on at least one rule
- [ ] Added an HTML comment to CLAUDE.md and verified it's hidden
- [ ] `.claude/rules/` directory contains `testing.md`, `source-code.md`, `storage.md`
- [ ] Each rule file has correct path-scoped frontmatter
- [ ] `CLAUDE.local.md` exists with personal preferences
- [ ] `docs/architecture.md` and `docs/api.md` exist
- [ ] `CLAUDE.md` contains `@imports` referencing the docs
- [ ] You ran `/context` and understand the context grid
- [ ] You ran `/compact` with a focus argument
- [ ] You ran `/stats` or `/cost` to check your usage
- [ ] Template rendering feature works with tests passing
- [ ] Changes committed on a feature branch and merged
