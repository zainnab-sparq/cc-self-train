# Module 3 -- Rules, Memory, and Context

**CC features:** `.claude/rules/`, `CLAUDE.local.md`, `@imports`, `/context`,
`/compact`, `/stats`, `/cost`, `/statusline`, memory hierarchy

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

### 3.1 Create Project Rules

**Why this step:** Rules are how you teach Claude your project's standards permanently. Instead of repeating "use semantic HTML" every session, you write it once in a rule file and Claude follows it automatically. Path-scoped rules only activate when Claude works on matching files, keeping context lean.

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

Now you need three rule files -- one each for HTML, CSS, and JavaScript. Each file uses YAML frontmatter to scope it to specific file types, so Claude only loads the relevant rules when working on matching files.

Tell Claude what coding standards matter to you for each language. Think about the conventions you want enforced. Something like:

```
Create three rule files in .claude/rules/. For HTML rules (scoped to *.html files), I want semantic elements, accessibility standards like alt attributes on images, proper heading hierarchy, and correct meta tags. For CSS rules (scoped to *.css and styles/**), I want mobile-first design, CSS custom properties for all design tokens, BEM naming, and visible focus styles. For JavaScript rules (scoped to *.js and scripts/**), I want vanilla JS only, addEventListener instead of inline handlers, const by default, and explicit error handling. Use path-scoped YAML frontmatter in each file.
```

Claude will create the rule files. Review them and adjust any rules that do not match your preferences -- these are *your* coding standards, not Claude's.

**STOP -- What you just did:** You created three rule files, each scoped to specific file types using YAML frontmatter. When Claude edits an `.html` file, it loads `html-rules.md` automatically. When it edits `.css`, it loads `css-rules.md`. This is how you enforce coding standards without repeating yourself -- and unlike CLAUDE.md instructions, path-scoped rules only consume context when relevant files are being worked on.

Ready to create your CLAUDE.local.md for personal preferences?

### 3.3 Create CLAUDE.local.md

**Why this step:** CLAUDE.local.md is your *personal* preferences file. It gets added to `.gitignore`, which means git will never track or commit it -- your preferences stay on your machine and do not get pushed to the shared repository where they would affect other contributors. This is the split between team standards (CLAUDE.md, rules) and personal workflow (CLAUDE.local.md).

Create a personal preferences file that will not be committed to git. Ask Claude to create `CLAUDE.local.md` and tell it about your personal workflow preferences -- your design taste, how you like commit messages, which browser you test in, anything that is about *you* rather than the project.

```
Create a CLAUDE.local.md with my personal preferences. I like [describe your design style], I test in [your browser], and I prefer [your commit message style]. Also note any design tools I use regularly (like Figma or Canva) -- we'll connect them to Claude in Module 6.
```

Verify it was added to `.gitignore`:

```
! cat .gitignore
```

If `CLAUDE.local.md` is not listed, add it.

**STOP -- What you just did:** You created a personal preferences file that is not committed to git. This is the split between team standards (rules, CLAUDE.md) and personal preferences (CLAUDE.local.md). On a real team, everyone shares the same rules but can have different personal preferences -- like which browser they test in or what commit message style they prefer.

Want to see how the memory hierarchy works?

### 3.4 Understand the Memory Hierarchy

Ask Claude to explain the memory hierarchy -- where each file lives, what order they are loaded in, and which ones are shared with a team versus kept private.

```
Explain the full Claude Code memory hierarchy. Which files take precedence over which? Which ones get shared with teammates?
```

The hierarchy from highest to lowest precedence:

1. Managed policy (organization-wide, system directory)
2. Project memory (`./CLAUDE.md` or `./.claude/CLAUDE.md`)
3. Project rules (`.claude/rules/*.md`)
4. User memory (`~/.claude/CLAUDE.md`)
5. Project local (`./CLAUDE.local.md`)

**Quick check before continuing:**
- [ ] `.claude/rules/` contains three rule files with path-scoped frontmatter
- [ ] `CLAUDE.local.md` exists and is listed in `.gitignore`
- [ ] You can explain the five levels of the memory hierarchy

### 3.5 Modularize CLAUDE.md with @imports

As your CLAUDE.md grows, it eats into your available context window. The solution is to break detailed documentation into separate files and reference them with `@imports`.

Ask Claude to create supporting docs for your project and wire them up:

```
Create a docs/style-guide.md that documents our visual design system -- the color palette, typography, spacing, and component patterns. Also create docs/sitemap.md listing all pages and their components. Then add @imports to CLAUDE.md so Claude Code loads these when needed.
```

The `@path` syntax tells Claude Code to load those files as additional context
when needed. Both relative and absolute paths work.

**Why this step:** As your CLAUDE.md grows, it eats into your available context window. The `@import` pattern keeps CLAUDE.md concise while making detailed documentation available on demand. Think of it like splitting a large function into smaller helpers -- same information, better organized.

**Engineering value:**
- *Entry-level:* Large projects have too much code for Claude to read at once. @imports let you point Claude at exactly the files it needs — like giving a new teammate the right docs before they start.
- *Mid-level:* /compact reclaims context space during long sessions. Without it, Claude loses track of earlier conversation — with it, you can run marathon refactoring sessions.

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

**Tip:** Be specific about what you need. "Read lines 1-50 of main.js" costs less context than "read main.js" for a 500-line file. Similarly, targeted searches use less context than reading entire files.

The percentage tells you how full the window is. Early in a session it will be low. After several rounds of building and testing, it climbs. When it gets high, Claude will auto-compact -- or you can do it manually with `/compact` (next step).

### 3.7 /compact with Focus Argument

When context gets large, use `/compact` to summarize the conversation:

```
/compact Preserve all details about the CSS design system and page structure.
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
/compact Preserve details about the CSS design system and page layout decisions
```

**Fix 2 -- Start fresh:** If compacting is not enough, start a new session by running `claude` again in your project directory. Your CLAUDE.md, rules, and CLAUDE.local.md reload automatically -- only conversation history is lost. This is often the fastest fix for a cluttered session.

**Prevention:** If you find yourself repeatedly telling Claude the same thing, that is a sign it belongs in CLAUDE.md or a rules file, not in conversation. Chat is temporary; memory files are permanent.

### 3.10 Build a Feature Using These Tools

Now build the blog listing page to see your rules and context tools in action. Create a feature branch first:

```
! git checkout -b feature/blog
```

Then describe the blog page you want to Claude. Tell it about the layout, how blog post cards should look, and ask it to follow all the rules you just created:

```
Build a blog listing page with post cards showing title, date, excerpt, and tags. Add a few sample posts so I can see how it looks. Make sure to follow our HTML, CSS, and JS rules.
```

After building, run `/context` again to see how context changed. Then commit.

### 3.11 HTML Comments & Memory Directory

Two useful updates for managing Claude's context:

**HTML comments are now hidden.** If you add `<!-- internal notes -->` to your CLAUDE.md, Claude won't see them when the file is auto-loaded. They're only visible when Claude explicitly reads the file with the Read tool. Use this for maintainer notes, TODOs, or internal documentation that shouldn't influence Claude's behavior (v2.1.72).

**Custom memory directory.** The `autoMemoryDirectory` setting lets you store auto-memory in a custom location instead of `~/.claude/`. Useful for shared drives or custom project structures (v2.1.74).

**Smarter `/context`.** The `/context` command now gives actionable suggestions -- it identifies context-heavy tools, memory bloat, and capacity warnings with specific optimization tips (v2.1.74).

Try adding an HTML comment to your CLAUDE.md now -- something like `<!-- TODO: add testing conventions after Module 9 -->` -- and verify Claude doesn't reference it unless you ask it to read the file directly.

> **STOP** -- Add an HTML comment to your project's CLAUDE.md and verify it's hidden from Claude.

### 3.12 Path-Scoped Rules with `paths:` Frontmatter

Rules can now accept `paths:` as a YAML list of globs in their frontmatter, restricting which files they apply to. This means you can have different rules for different parts of your project -- CSS conventions for stylesheets, JS conventions for scripts, HTML conventions for pages.

Try creating two rules with different scopes. Ask Claude something like:

```
Create two rule files in .claude/rules/:
1. css-conventions.md with paths: [styles/**] that enforces CSS custom properties over hardcoded colors
2. js-conventions.md with paths: [scripts/**] that enforces const over let for variables that don't change
```

After creating them, test the scoping: ask Claude to edit a CSS file and see if it follows the CSS rule, then ask it to edit a JS file and verify it follows the JS rule instead.

**STOP -- What you just did:** You created rules that only load when Claude works on matching files. This is powerful for larger projects where different directories have different conventions. The `paths:` field accepts standard glob patterns -- `**` matches any depth, `*` matches any file.

> **STOP** -- Try editing files in both directories to verify each rule applies only to its scoped path.

### Checkpoint

You just taught Claude how your project works. Rules, memory, and imports mean Claude gets smarter about your codebase with every session.

- [ ] Tested `paths:` frontmatter on at least one rule
- [ ] Added an HTML comment to CLAUDE.md and verified it's hidden
- [ ] `.claude/rules/` directory contains `html-rules.md`, `css-rules.md`, `js-rules.md`
- [ ] Each rule file has correct path-scoped frontmatter
- [ ] `CLAUDE.local.md` exists with personal preferences
- [ ] `docs/style-guide.md` and `docs/sitemap.md` exist
- [ ] `CLAUDE.md` contains `@imports` referencing the docs
- [ ] You ran `/context` and understand the context grid
- [ ] You ran `/compact` with a focus argument
- [ ] You ran `/stats` or `/cost` to check your usage
- [ ] Blog listing page works with styled post cards
- [ ] Changes committed on a feature branch and merged
