# Module 3 -- Rules, Memory & Context

<!-- progress:start -->
**Progress:** Module 3 of 10 `[███░░░░░░░]` 30%

**Estimated time:** ~45-60 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** .claude/rules/, CLAUDE.local.md, @imports, /context, /compact, /stats, /cost, /statusline, memory hierarchy

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try...", "Here's what that does..."

</details>

**Why this step:** Rules files let you give Claude permanent, file-specific instructions. Instead of repeating "always validate HTTP methods" in every prompt, you write it once in a rules file and Claude follows it automatically whenever it touches matching files.

**Engineering value:**
- *Entry-level:* Rules are like linting configs but for Claude's behavior -- they enforce your team's conventions automatically.
- *Mid-level:* Path-scoped rules mean your test files get different AI guidance than your production code. A rule in `tests/` can enforce test patterns without affecting `src/`.
- *Senior+:* This is the same configuration-as-code pattern used by .gitattributes (path-scoped git behavior) and CODEOWNERS (path-scoped review). Modular, composable, version-controlled.

> **New terms this module uses:**
> - **Rule file** -- a Markdown file in `.claude/rules/` that tells Claude how to write code for a specific part of your project (example: "use functional components, not classes").
> - **Frontmatter** -- a block of settings at the top of a Markdown file, fenced by `---` lines. Written in YAML. It tells a tool how to use the file.
> - **YAML** -- a human-readable config format with indentation and colons (`name: react`, `paths: ["*.py"]`).
> - **Path scoping** -- telling a rule file to only apply to certain directories or file types via its frontmatter. Example: a rule with `paths: ["*.py"]` only activates on Python files.
>
> If these are still fuzzy after the first few steps, the [glossary](../../../GLOSSARY.md) has them written out in more detail.

### 3.1 Create Path-Scoped Rules

Ask Claude to create a `.claude/rules/` directory with three rule files. Describe what each rule should enforce and which files it should apply to. Let Claude figure out the exact frontmatter syntax.

```
Create a .claude/rules/ directory with three rule files. First, a routing rule that applies to route and handler files -- it should enforce HTTP method validation, proper status codes (200, 400, 404, 502, 503), and request logging. Second, a config rule that applies to YAML, JSON, and TOML files -- it should enforce validation on load with clear error messages. Third, a testing rule for test and spec files -- it should require both success and error path coverage with descriptive test names.
```

Claude will create the files with the correct `paths:` frontmatter to scope each rule. After creating them, edit a route handler file and notice Claude follows the routing rules automatically.

**STOP -- What you just did:** You created path-scoped rules that automatically activate when Claude works on matching files. The `paths:` frontmatter is the key -- it means Claude only sees routing rules when editing route files, not when editing tests or configs. This keeps Claude's context focused and its behavior consistent without you having to remind it every time.

Want to set up CLAUDE.local.md for your personal preferences?

### 3.2 Create CLAUDE.local.md

**Why this step:** CLAUDE.local.md is your *personal* memory file -- it stores preferences that should not be shared with the team (like your preferred output format, local ports, or testing shortcuts). It gets added to `.gitignore`, which means git will never track or commit it. That way your personal preferences stay on your machine and do not get pushed to the shared repository where they would affect other contributors.

Ask Claude to create a CLAUDE.local.md with your personal development preferences. Think about what matters to you locally -- maybe you like verbose logging, your test upstream runs on a specific port, or you want a shorthand for running quick tests.

```
Create a CLAUDE.local.md with my personal preferences: I like verbose logging during development, my test upstream runs on port 4001, and when I say 'quick test' I mean skip integration tests. Also note any monitoring or dev tools I use (like Sentry or GitHub) -- we'll connect them in Module 6.
```

Claude should add it to `.gitignore` automatically. Verify:

```
! cat .gitignore
```

If `CLAUDE.local.md` is not listed, ask Claude to add it.

### 3.3 Understand the Memory Hierarchy

Ask Claude: `Show me the complete memory hierarchy for this project, what files are loaded, in what order, and which takes precedence.`

The hierarchy (highest to lowest): Managed policy > Project CLAUDE.md > .claude/rules/*.md > User ~/.claude/CLAUDE.md > CLAUDE.local.md.

**STOP -- What you just did:** You now understand the full memory hierarchy -- from managed policy (highest) down to CLAUDE.local.md (lowest). This hierarchy means you can have project-wide rules that everyone shares (CLAUDE.md, .claude/rules/) and personal preferences that only affect you (CLAUDE.local.md). Knowing this hierarchy matters because when rules conflict, the higher-priority source wins.

**Quick check before continuing:**
- [ ] `.claude/rules/` has at least 3 rule files with `paths:` frontmatter
- [ ] CLAUDE.local.md exists and is in .gitignore
- [ ] You can list the memory hierarchy from highest to lowest priority

### 3.4 Modularize CLAUDE.md with @imports

**Why this step:** As your project grows, CLAUDE.md gets bloated with documentation. The `@import` syntax lets you keep CLAUDE.md concise (a table of contents) while giving Claude access to detailed docs on demand. This is how you scale Claude's knowledge without wasting context window on every session.

Ask Claude to create documentation files for the route matching algorithm and the configuration format, then reference them from CLAUDE.md using `@imports`.

```
Create a docs/routing.md that documents how route matching works and a docs/config-format.md that documents the config file schema with examples. Then update CLAUDE.md to import both using the @path syntax.
```

The `@path` syntax in CLAUDE.md imports the referenced file into Claude's context. This keeps CLAUDE.md concise while giving Claude access to detailed documentation.

**Engineering value:**
- *Entry-level:* Large projects have too much code for Claude to read at once. @imports let you point Claude at exactly the files it needs -- like giving a new teammate the right docs before they start.
- *Mid-level:* /compact reclaims context space during long sessions. Without it, Claude loses track of earlier conversation -- with it, you can run marathon refactoring sessions.

### 3.5 Check Context Usage with /context

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

**Tip:** Be specific about what you need. "Read lines 1-50 of router.py" costs less context than "read router.py" for a 500-line file. Similarly, targeted searches use less context than reading entire files.

The percentage tells you how full the window is. Early in a session it will be low. After several rounds of building and testing, it climbs.

### 3.5b Manage Context with /compact

When context gets large, use `/compact` to summarize the conversation:

```
/compact Focus on the rate limiting feature we are about to build
```

The argument tells Claude what to prioritize when compacting. Without it, Claude uses its own judgment.

**What happens automatically:** You do not have to run `/compact` manually every time. When your context reaches approximately 95% capacity, Claude auto-compacts the conversation. Here is what survives:

- **Always preserved:** Your CLAUDE.md, rules files, and CLAUDE.local.md. These are re-read from disk after every compaction -- they always survive. This is the key insight: anything you put in these files is permanent. Anything you only said in chat is temporary.
- **Mostly preserved:** Recent messages and code you were just working on.
- **May be lost:** Detailed instructions from early in the conversation, older file reads, and verbose command outputs (tool outputs are cleared first to make room).

**Key takeaway:** If a decision or convention is important enough to always remember, put it in CLAUDE.md or a rules file -- not in a chat message.

**STOP -- What you just did:** You learned three context management tools: `/context` shows what Claude is "thinking about" (and how full its context window is), `/compact` frees up space while preserving key information, and `/stats` or `/cost` (next step) tracks your overall usage. These tools become essential in longer sessions -- you will use `/compact` regularly to keep Claude focused and responsive.

### 3.5c Check Your Usage

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

### 3.5d When Claude Forgets

Sometimes Claude gives vague answers, forgets an earlier decision, or asks about something you already discussed. This is not a bug -- it means context is getting full.

**Diagnosis:** Run `/context`. If usage is 80%+, older details are being compressed or lost.

**Fix 1 -- Compact with focus:** Run `/compact` with a specific focus argument to preserve what matters:

```
/compact Preserve details about the route matching algorithm and config format
```

**Fix 2 -- Start fresh:** If compacting is not enough, start a new session by running `claude` again in your project directory. Your CLAUDE.md, rules, and CLAUDE.local.md reload automatically -- only conversation history is lost. This is often the fastest fix for a cluttered session.

**Prevention:** If you find yourself repeatedly telling Claude the same thing, that is a sign it belongs in CLAUDE.md or a rules file, not in conversation. Chat is temporary; memory files are permanent.

Ready to build the rate limiting feature?

### 3.6 Build Rate Limiting

Now build the rate limiting feature while actively using the context tools. Describe the behavior you want to Claude -- per-route limits from config, what to return when a client is rate-limited, and how to track state. Let Claude suggest the algorithm (token bucket, sliding window, etc.) and discuss the tradeoffs.

Try something like:

```
I want to add rate limiting to the gateway. Each route should have a configurable rate limit in the config file. When a client exceeds the limit, return 429 with a Retry-After header. Store the state in memory for now. What algorithm do you recommend?
```

Claude will implement the rate limiter and may ask about edge cases like what happens on server restart (state resets). After building, ask Claude to write tests, run them, and commit. Then run `/compact` to free context.

### 3.7 HTML Comments & Memory Directory

Two useful updates for managing Claude's context:

**HTML comments are now hidden.** If you add `<!-- internal notes -->` to your CLAUDE.md, Claude won't see them when the file is auto-loaded. They're only visible when Claude explicitly reads the file with the Read tool. Use this for maintainer notes, TODOs, or internal documentation that shouldn't influence Claude's behavior (v2.1.72).

**Custom memory directory.** The `autoMemoryDirectory` setting lets you store auto-memory in a custom location instead of `~/.claude/`. Useful for shared drives or custom project structures (v2.1.74).

**Smarter `/context`.** The `/context` command now gives actionable suggestions -- it identifies context-heavy tools, memory bloat, and capacity warnings with specific optimization tips (v2.1.74).

Try adding an HTML comment to your CLAUDE.md now -- something like `<!-- TODO: add testing conventions after Module 9 -->` -- and verify Claude doesn't reference it unless you ask it to read the file directly.

> **STOP** -- Add an HTML comment to your project's CLAUDE.md and verify it's hidden from Claude.

### 3.8 Path-Scoped Rules with `paths:` Frontmatter

Rules can now accept `paths:` as a YAML list of globs in their frontmatter, restricting which files they apply to. This means you can have different rules for different parts of your project -- routing conventions for handler files, config conventions for YAML/JSON files, test conventions for spec files.

Try creating two rules with different scopes. Ask Claude something like:

```
Create two rule files in .claude/rules/:
1. handler-style.md with paths: [src/handlers/**] that enforces input validation and proper status codes
2. config-style.md with paths: [config/**] that enforces schema validation and clear error messages
```

After creating them, test the scoping: ask Claude to edit a handler file and see if it follows the handler rule, then ask it to edit a config file and verify it follows the config rule instead.

**STOP -- What you just did:** You created rules that only load when Claude works on matching files. This is powerful for larger projects where different directories have different conventions. The `paths:` field accepts standard glob patterns -- `**` matches any depth, `*` matches any file.

> **STOP** -- Try editing files in both directories to verify each rule applies only to its scoped path.

### Checkpoint

You just taught Claude how your gateway works. Rules, memory, and context management mean Claude understands your conventions and enforces them automatically.

- [ ] Tested `paths:` frontmatter on at least one rule
- [ ] Added an HTML comment to CLAUDE.md and verified it's hidden
- [ ] `.claude/rules/` has at least 3 rule files with path-scoped frontmatter
- [ ] CLAUDE.local.md exists and is in .gitignore
- [ ] CLAUDE.md uses `@imports` to reference docs/routing.md and docs/config-format.md
- [ ] You ran `/context` and can read the context grid
- [ ] You ran `/compact` at least once
- [ ] You ran `/stats` or `/cost` to check your usage
- [ ] Rate limiting is implemented with tests passing
- [ ] Changes committed to git
