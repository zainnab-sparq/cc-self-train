# Module 3 -- Rules, Memory & Context

**CC features:** .claude/rules/, CLAUDE.local.md, @imports, /context, /compact, memory hierarchy, /cost

> **Persona — Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

> **Why this step:** Rules files let you give Claude permanent, file-specific instructions. Instead of repeating "always validate HTTP methods" in every prompt, you write it once in a rules file and Claude follows it automatically whenever it touches matching files.

> **Engineering value:**
> - *Entry-level:* Rules are like linting configs but for Claude's behavior — they enforce your team's conventions automatically.
> - *Mid-level:* Path-scoped rules mean your test files get different AI guidance than your production code. A rule in `tests/` can enforce test patterns without affecting `src/`.
> - *Senior+:* This is the same configuration-as-code pattern used by .gitattributes (path-scoped git behavior) and CODEOWNERS (path-scoped review). Modular, composable, version-controlled.

### Step 1: Create Path-Scoped Rules

Ask Claude to create a `.claude/rules/` directory with three rule files. Describe what each rule should enforce and which files it should apply to. Let Claude figure out the exact frontmatter syntax.

> "Create a .claude/rules/ directory with three rule files. First, a routing rule that applies to route and handler files -- it should enforce HTTP method validation, proper status codes (200, 400, 404, 502, 503), and request logging. Second, a config rule that applies to YAML, JSON, and TOML files -- it should enforce validation on load with clear error messages. Third, a testing rule for test and spec files -- it should require both success and error path coverage with descriptive test names."

Claude will create the files with the correct `paths:` frontmatter to scope each rule. After creating them, edit a route handler file and notice Claude follows the routing rules automatically.

> **STOP -- What you just did:** You created path-scoped rules that automatically activate when Claude works on matching files. The `paths:` frontmatter is the key -- it means Claude only sees routing rules when editing route files, not when editing tests or configs. This keeps Claude's context focused and its behavior consistent without you having to remind it every time.

Want to set up CLAUDE.local.md for your personal preferences?

### Step 2: Create CLAUDE.local.md

Ask Claude to create a CLAUDE.local.md with your personal development preferences. Think about what matters to you locally -- maybe you like verbose logging, your test upstream runs on a specific port, or you want a shorthand for running quick tests.

> "Create a CLAUDE.local.md with my personal preferences: I like verbose logging during development, my test upstream runs on port 4001, and when I say 'quick test' I mean skip integration tests. Also note any monitoring or dev tools I use (like Sentry or GitHub) -- we'll connect them in Module 6. Make sure it's gitignored."

CLAUDE.local.md is for personal, per-project preferences that should not be committed to version control.

### Step 3: Understand the Memory Hierarchy

Ask Claude: `Show me the complete memory hierarchy for this project, what files are loaded, in what order, and which takes precedence.`

The hierarchy (highest to lowest): Managed policy > Project CLAUDE.md > .claude/rules/*.md > User ~/.claude/CLAUDE.md > CLAUDE.local.md.

> **STOP -- What you just did:** You now understand the full memory hierarchy -- from managed policy (highest) down to CLAUDE.local.md (lowest). This hierarchy means you can have project-wide rules that everyone shares (CLAUDE.md, .claude/rules/) and personal preferences that only affect you (CLAUDE.local.md). Knowing this hierarchy matters because when rules conflict, the higher-priority source wins.

> **Quick check before continuing:**
> - [ ] `.claude/rules/` has at least 3 rule files with `paths:` frontmatter
> - [ ] CLAUDE.local.md exists and is in .gitignore
> - [ ] You can list the memory hierarchy from highest to lowest priority

### Step 4: Modularize CLAUDE.md with @imports

> **Why this step:** As your project grows, CLAUDE.md gets bloated with documentation. The `@import` syntax lets you keep CLAUDE.md concise (a table of contents) while giving Claude access to detailed docs on demand. This is how you scale Claude's knowledge without wasting context window on every session.

Ask Claude to create documentation files for the route matching algorithm and the configuration format, then reference them from CLAUDE.md using `@imports`.

> "Create a docs/routing.md that documents how route matching works and a docs/config-format.md that documents the config file schema with examples. Then update CLAUDE.md to import both using the @path syntax."

The `@path` syntax in CLAUDE.md imports the referenced file into Claude's context. This keeps CLAUDE.md concise while giving Claude access to detailed documentation.

> **Engineering value:**
> - *Entry-level:* Large projects have too much code for Claude to read at once. @imports let you point Claude at exactly the files it needs — like giving a new teammate the right docs before they start.
> - *Mid-level:* /compact reclaims context space during long sessions. Without it, Claude loses track of earlier conversation — with it, you can run marathon refactoring sessions.

### Step 5: Explore Context Tools

Try each command:
- `/context` -- visualizes context usage as a colored grid
- `/compact Focus on the rate limiting feature we are about to build` -- compacts conversation, keeping focus on what you specify
- `/cost` -- shows token usage statistics for the current session

> **Note:** On Claude subscriptions (Pro/Max/Team), `/cost` may show limited or empty output due to known issues. If you see blank results, don't worry -- your token usage is still being tracked. API key users will see detailed cost breakdowns.

> **STOP -- What you just did:** You learned the three context management tools: `/context` shows what Claude is "thinking about" (and how full its context window is), `/compact` frees up space while preserving key information, and `/cost` tracks your token usage. These tools become essential in longer sessions -- you will use `/compact` regularly to keep Claude focused and responsive.

Ready to build the rate limiting feature?

### Step 6: Build Rate Limiting

Now build the rate limiting feature while actively using the context tools. Describe the behavior you want to Claude -- per-route limits from config, what to return when a client is rate-limited, and how to track state. Let Claude suggest the algorithm (token bucket, sliding window, etc.) and discuss the tradeoffs.

> "I want to add rate limiting to the gateway. Each route should have a configurable rate limit in the config file. When a client exceeds the limit, return 429 with a Retry-After header. Store the state in memory for now. What algorithm do you recommend?"

Claude will implement the rate limiter and may ask about edge cases like what happens on server restart (state resets). After building, ask Claude to write tests, run them, and commit. Then run `/compact` to free context and `/cost` to see how many tokens you used.

### Checkpoint

You just taught Claude how your gateway works. Rules, memory, and context management mean Claude understands your conventions and enforces them automatically.

- [ ] `.claude/rules/` has at least 3 rule files with path-scoped frontmatter
- [ ] CLAUDE.local.md exists and is in .gitignore
- [ ] CLAUDE.md uses `@imports` to reference docs/routing.md and docs/config-format.md
- [ ] You ran `/context` and can read the context grid
- [ ] You ran `/compact` at least once
- [ ] You ran `/cost` to check token usage
- [ ] Rate limiting is implemented with tests passing
- [ ] Changes committed to git
