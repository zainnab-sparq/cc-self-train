# Module 3 -- Rules, Memory, and Context

**CC features:** `.claude/rules/`, `CLAUDE.local.md`, `@imports`, `/context`,
`/compact`, memory hierarchy, `/cost`

> **Persona — Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

### 3.1 Create Project Rules

> **Why this step:** Rules are how you teach Claude your project's standards permanently. Instead of repeating "use semantic HTML" every session, you write it once in a rule file and Claude follows it automatically. Path-scoped rules only activate when Claude works on matching files, keeping context lean.

> **Engineering value:**
> - *Entry-level:* Rules are like linting configs but for Claude's behavior — they enforce your team's conventions automatically.
> - *Mid-level:* Path-scoped rules mean your test files get different AI guidance than your production code. A rule in `tests/` can enforce test patterns without affecting `src/`.
> - *Senior+:* This is the same configuration-as-code pattern used by .gitattributes (path-scoped git behavior) and CODEOWNERS (path-scoped review). Modular, composable, version-controlled.

Create the rules directory in your project:

```
! mkdir -p .claude/rules
```

Rules are modular, topic-specific instructions that Claude loads automatically.
They use markdown files with optional YAML frontmatter for path scoping.

### 3.2 Create Path-Scoped Rules

Now you need three rule files -- one each for HTML, CSS, and JavaScript. Each file uses YAML frontmatter to scope it to specific file types, so Claude only loads the relevant rules when working on matching files.

Tell Claude what coding standards matter to you for each language. Think about the conventions you want enforced. Something like:

> "Create three rule files in .claude/rules/. For HTML rules (scoped to *.html files), I want semantic elements, accessibility standards like alt attributes on images, proper heading hierarchy, and correct meta tags. For CSS rules (scoped to *.css and styles/**), I want mobile-first design, CSS custom properties for all design tokens, BEM naming, and visible focus styles. For JavaScript rules (scoped to *.js and scripts/**), I want vanilla JS only, addEventListener instead of inline handlers, const by default, and explicit error handling. Use path-scoped YAML frontmatter in each file."

Claude will create the rule files. Review them and adjust any rules that do not match your preferences -- these are *your* coding standards, not Claude's.

> **STOP -- What you just did:** You created three rule files, each scoped to specific file types using YAML frontmatter. When Claude edits an `.html` file, it loads `html-rules.md` automatically. When it edits `.css`, it loads `css-rules.md`. This is how you enforce coding standards without repeating yourself -- and unlike CLAUDE.md instructions, path-scoped rules only consume context when relevant files are being worked on.

Ready to create your CLAUDE.local.md for personal preferences?

### 3.3 Create CLAUDE.local.md

Create a personal preferences file that will not be committed to git. Ask Claude to create `CLAUDE.local.md` and tell it about your personal workflow preferences -- your design taste, how you like commit messages, which browser you test in, anything that is about *you* rather than the project.

> "Create a CLAUDE.local.md with my personal preferences. I like [describe your design style], I test in [your browser], and I prefer [your commit message style]. Also note any design tools I use regularly (like Figma or Canva) -- we'll connect them to Claude in Module 6."

Verify it was added to `.gitignore`:

```
! cat .gitignore
```

If `CLAUDE.local.md` is not listed, add it.

> **STOP -- What you just did:** You created a personal preferences file that is not committed to git. This is the split between team standards (rules, CLAUDE.md) and personal preferences (CLAUDE.local.md). On a real team, everyone shares the same rules but can have different personal preferences -- like which browser they test in or what commit message style they prefer.

Want to see how the memory hierarchy works?

### 3.4 Understand the Memory Hierarchy

Ask Claude to explain the memory hierarchy -- where each file lives, what order they are loaded in, and which ones are shared with a team versus kept private.

> "Explain the full Claude Code memory hierarchy. Which files take precedence over which? Which ones get shared with teammates?"

The hierarchy from highest to lowest precedence:

1. Managed policy (organization-wide, system directory)
2. Project memory (`./CLAUDE.md` or `./.claude/CLAUDE.md`)
3. Project rules (`.claude/rules/*.md`)
4. User memory (`~/.claude/CLAUDE.md`)
5. Project local (`./CLAUDE.local.md`)

> **Quick check before continuing:**
> - [ ] `.claude/rules/` contains three rule files with path-scoped frontmatter
> - [ ] `CLAUDE.local.md` exists and is listed in `.gitignore`
> - [ ] You can explain the five levels of the memory hierarchy

### 3.5 Modularize CLAUDE.md with @imports

As your CLAUDE.md grows, it eats into your available context window. The solution is to break detailed documentation into separate files and reference them with `@imports`.

Ask Claude to create supporting docs for your project and wire them up:

> "Create a docs/style-guide.md that documents our visual design system -- the color palette, typography, spacing, and component patterns. Also create docs/sitemap.md listing all pages and their components. Then add @imports to CLAUDE.md so Claude Code loads these when needed."

The `@path` syntax tells Claude Code to load those files as additional context
when needed. Both relative and absolute paths work.

> **Why this step:** As your CLAUDE.md grows, it eats into your available context window. The `@import` pattern keeps CLAUDE.md concise while making detailed documentation available on demand. Think of it like splitting a large function into smaller helpers -- same information, better organized.

> **Engineering value:**
> - *Entry-level:* Large projects have too much code for Claude to read at once. @imports let you point Claude at exactly the files it needs — like giving a new teammate the right docs before they start.
> - *Mid-level:* /compact reclaims context space during long sessions. Without it, Claude loses track of earlier conversation — with it, you can run marathon refactoring sessions.

### 3.6 /context Deep Dive

Run:

```
/context
```

This shows a visual grid of your current context usage. Observe:

- How much context is used by CLAUDE.md and rules
- How much is used by conversation history
- How much remains available

Understanding context is critical. As your session grows, context fills up.

### 3.7 /compact with Focus Argument

When context gets large, use `/compact` to summarize the conversation:

```
/compact Preserve all details about the CSS design system and page structure.
```

The argument tells Claude what to prioritize when compacting. Without it,
Claude uses its own judgment.

> **STOP -- What you just did:** You used `/context` to see how your session's context is distributed, then `/compact` to reclaim space. Context management is a real skill -- long sessions accumulate history, and eventually Claude "forgets" earlier details. Using `/compact` with a focus argument lets you control what survives the compression. You will use this pattern whenever a session gets long or sluggish.

Shall we check your token usage with /cost?

### 3.8 /cost Tracking

Run:

```
/cost
```

This shows your token usage for the current session. Check it periodically to
understand how much context different operations consume.

> **Note:** On Claude subscriptions (Pro/Max/Team), `/cost` may show limited or empty output due to known issues. If you see blank results, don't worry -- your token usage is still being tracked. API key users will see detailed cost breakdowns.

### 3.9 Build a Feature Using These Tools

Now build the blog listing page to see your rules and context tools in action. Create a feature branch first:

```
! git checkout -b feature/blog
```

Then describe the blog page you want to Claude. Tell it about the layout, how blog post cards should look, and ask it to follow all the rules you just created:

> "Build a blog listing page with post cards showing title, date, excerpt, and tags. Add a few sample posts so I can see how it looks. Make sure to follow our HTML, CSS, and JS rules."

After building, run `/context` again to see how context changed. Then commit.

### Checkpoint

You just taught Claude how your project works. Rules, memory, and imports mean Claude gets smarter about your codebase with every session.

- [ ] `.claude/rules/` directory contains `html-rules.md`, `css-rules.md`, `js-rules.md`
- [ ] Each rule file has correct path-scoped frontmatter
- [ ] `CLAUDE.local.md` exists with personal preferences
- [ ] `docs/style-guide.md` and `docs/sitemap.md` exist
- [ ] `CLAUDE.md` contains `@imports` referencing the docs
- [ ] You ran `/context` and understand the context grid
- [ ] You ran `/compact` with a focus argument
- [ ] You ran `/cost` and checked token usage
- [ ] Blog listing page works with styled post cards
- [ ] Changes committed on a feature branch and merged
