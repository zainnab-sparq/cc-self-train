# Module 3 -- Rules, Memory, and Context

**CC features:** `.claude/rules/`, `CLAUDE.local.md`, `@imports`, `/context`,
`/compact`, memory hierarchy, `/cost`

> **Persona — Guide:** Explain everything, define terms, celebrate small wins. "Let's try…", "Here's what that does…"

## 3.1 Create Project Rules

> **Why this step:** Rules are how you teach Claude your project's conventions. Instead of repeating "use fixtures in tests" or "add docstrings" in every prompt, you write it once in a rule file and Claude follows it automatically in every session.

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

## 3.2 Create Path-Scoped Rules

> **Why this step:** Path-scoped rules only activate when Claude works on matching files. Your testing rules apply in test files, your source code rules apply in source files. This keeps context lean -- Claude does not load storage rules when editing a test, and vice versa.

Ask Claude to create three rule files for you: one for testing conventions, one for source code style, and one for storage operations. Describe the conventions you care about for each area, and tell Claude to scope them to the right file paths using YAML frontmatter.

> "Create three rule files in .claude/rules/. First, a testing.md scoped to test files -- I want rules about using fixtures, descriptive assertions, and testing both success and failure cases. Second, a source-code.md scoped to src/lib/pkg -- rules about single responsibility, docstrings, error handling, and function length. Third, a storage.md scoped to storage and data files -- rules about validation, graceful handling of missing files, and atomic writes. Use YAML frontmatter with path globs to scope each one."

Claude will ask you if it is unsure about your file structure or which glob patterns to use. Answer based on how your project is organized. Review the generated rules and adjust any conventions that do not match your preferences.

> **STOP -- What you just did:** You created three rule files with YAML frontmatter that scopes each one to specific file paths. From now on, whenever Claude touches a test file, it automatically follows your testing conventions. Whenever it edits source code, it follows your source code rules. You never have to remind it -- the rules are always active. This is how teams enforce consistency without relying on code review alone.

Ready to create your CLAUDE.local.md?

## 3.3 Create CLAUDE.local.md

Create a personal, non-committed preferences file. Tell Claude about your individual workflow preferences -- things like how you like test output formatted, your commit message style, and your language of choice. These are *your* preferences, not team rules.

> "Create a CLAUDE.local.md with my personal preferences. I like [your test output style], [your commit style], and I'm working in [your language]. Also note any productivity tools I use regularly (like Notion or Linear) -- we'll connect them in Module 6. Make sure it's in .gitignore."

Claude should add it to `.gitignore` automatically. Verify:

```
! cat .gitignore
```

If `CLAUDE.local.md` is not listed, ask Claude to add it.

> **STOP -- What you just did:** You created a personal preferences file that is *not* committed to version control. This is the distinction between `CLAUDE.md` (shared team knowledge) and `CLAUDE.local.md` (your personal preferences). Your teammates see the project rules; your local preferences are yours alone. You will use this separation whenever you have personal workflow preferences that should not be imposed on the team.

Want to see how the full memory hierarchy works?

## 3.4 Understand the Memory Hierarchy

Ask Claude to explain the full memory hierarchy -- where each file lives, what takes precedence, and which ones are shared with your team vs. private to you.

> "Explain the Claude Code memory hierarchy. What are all the layers, what's the precedence order, and which ones are shared vs. personal?"

The hierarchy from highest to lowest precedence:

1. Managed policy (organization-wide, system directory)
2. Project memory (`./CLAUDE.md` or `./.claude/CLAUDE.md`)
3. Project rules (`.claude/rules/*.md`)
4. User memory (`~/.claude/CLAUDE.md`)
5. Project local (`./CLAUDE.local.md`)

> **Quick check before continuing:**
> - [ ] `.claude/rules/` contains three rule files with YAML frontmatter
> - [ ] `CLAUDE.local.md` exists and is listed in `.gitignore`
> - [ ] You can explain the difference between project memory, project rules, user memory, and project local

## 3.5 Modularize CLAUDE.md with @imports

As your project grows, CLAUDE.md can become a wall of text. Ask Claude to extract the architecture and API documentation into separate files and link them with `@imports`.

> "Create a docs/architecture.md that describes our project structure, data models, and storage layer. Then create docs/api.md with the storage layer's public API. Finally, add @imports to CLAUDE.md so Claude loads these when it needs that context."

The `@path` syntax tells Claude Code to load those files as additional context
when needed. Both relative and absolute paths work.

> **Why this step:** As your project grows, `CLAUDE.md` can become a wall of text. `@imports` let you keep CLAUDE.md concise while linking to detailed docs that Claude loads on demand. Think of it like a table of contents that points to full chapters.

> **Engineering value:**
> - *Entry-level:* Large projects have too much code for Claude to read at once. @imports let you point Claude at exactly the files it needs — like giving a new teammate the right docs before they start.
> - *Mid-level:* /compact reclaims context space during long sessions. Without it, Claude loses track of earlier conversation — with it, you can run marathon refactoring sessions.

> **STOP -- What you just did:** You modularized your project documentation. Instead of cramming everything into one file, you created focused reference docs and linked them with `@imports`. Claude loads these when it needs architectural context or API details, keeping your main CLAUDE.md clean and scannable.

Want to explore the /context and /compact commands?

## 3.6 /context Deep Dive

Run:

```
/context
```

This shows a visual grid of your current context usage. Observe:

- How much context is used by CLAUDE.md and rules
- How much is used by conversation history
- How much remains available

Understanding context is critical. As your session grows, context fills up.

## 3.7 /compact with Focus Argument

> **Why this step:** Every Claude Code session has a finite context window. As your conversation grows, you will eventually run out of room. `/compact` reclaims space by summarizing older parts of the conversation while preserving what matters most. The focus argument is your steering wheel -- it tells Claude what to keep in detail.

When context gets large, use `/compact` to summarize the conversation:

```
/compact Preserve all details about the storage layer API and data models.
```

The argument tells Claude what to prioritize when compacting. Without it,
Claude uses its own judgment.

## 3.8 /cost Tracking

Run:

```
/cost
```

This shows your token usage for the current session. Check it periodically to
understand how much context different operations consume.

> **Note:** On Claude subscriptions (Pro/Max/Team), `/cost` may show limited or empty output due to known issues. If you see blank results, don't worry -- your token usage is still being tracked. API key users will see detailed cost breakdowns.

## 3.9 Build a Feature Using These Tools

Now put everything together by building the template rendering feature. Create a feature branch and describe to Claude what you want: a command that takes a template name and variable assignments, renders the template with those values, and validates that all required variables are provided.

> "Create a feature branch 'feature/templates' and build template rendering. I want a forge render command that substitutes variables into templates, validates that all required variables are provided, and errors on unknown variables. Write tests too -- follow our testing rules."

Notice how Claude follows the testing rules you created in `.claude/rules/testing.md` without you having to remind it. After building, run `/context` again to see how context changed. Then commit.

## Checkpoint

You just taught Claude how your toolkit works. Rules enforce your conventions automatically, and @imports keep documentation modular.

- [ ] `.claude/rules/` directory contains `testing.md`, `source-code.md`, `storage.md`
- [ ] Each rule file has correct path-scoped frontmatter
- [ ] `CLAUDE.local.md` exists with personal preferences
- [ ] `docs/architecture.md` and `docs/api.md` exist
- [ ] `CLAUDE.md` contains `@imports` referencing the docs
- [ ] You ran `/context` and understand the context grid
- [ ] You ran `/compact` with a focus argument
- [ ] You ran `/cost` and checked token usage
- [ ] Template rendering feature works with tests passing
- [ ] Changes committed on a feature branch and merged
