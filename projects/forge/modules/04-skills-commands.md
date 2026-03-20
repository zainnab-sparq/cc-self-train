# Module 4 -- Skills and Commands

**CC features:** SKILL.md, frontmatter, custom slash commands, hot-reload,
argument substitution, `disable-model-invocation`

**Persona -- Collaborator:** Ask before telling, give pointers not answers. "What do you think…", "Try this and tell me…"

### 4.1 Create the "add-item" Skill

**Where do skills go?** Create all skills in the cc-self-train root `.claude/skills/` directory — NOT inside `workspace/forge-toolkit/.claude/skills/`. Since Claude runs from the cc-self-train root, it only sees skills at that level.

Skills are reusable slash commands you define for your project. Instead of typing a long prompt every time, you write it once as a `/skill-name` and invoke it with arguments. Let's build the first one.

Describe to Claude what your add-item skill should do. You want a slash command that takes an item type and details, validates the input, runs the forge add command, and shows the result. Tell Claude about your validation rules -- what makes a valid note vs. a valid snippet vs. a valid bookmark.

"Create an add-item skill in .claude/skills/add-item/SKILL.md. It should accept the item type as the first argument and details as additional arguments. It needs to validate inputs -- non-empty titles, valid URLs for bookmarks, lowercase tags, uppercase template variables -- before running forge add. Also create a validation-rules.md companion file that spells out what's valid for each data type. Restrict it to Read, Write, Bash, and Edit tools."

Claude may ask about edge cases in your validation rules. Answer based on what makes sense for your workflow -- these are your conventions.

### 4.2 Create the "search" Skill

Now create a search skill. Describe how you want search to work -- query parsing with special prefixes like `tag:` and `type:`, full-text search as the default, results displayed as a clean table, and helpful suggestions when nothing matches.

"Create a search skill in .claude/skills/search/SKILL.md. It should take the search query from $ARGUMENTS, support prefixes like tag:, type:, and since: for filtering, fall back to full-text search, display results as a table with ID, type, title, tags, and date, and suggest alternatives if nothing matches. Restrict tools to Read, Bash, Grep, and Glob."

**STOP -- What you just did:** You created two skills with different specialties: one for data entry with validation, one for intelligent search with query parsing. Each skill has its own SKILL.md with frontmatter that controls its name, description, and which tools it can use. The `allowed-tools` field is important -- it restricts what Claude can do when running the skill, which prevents unexpected side effects. You will use this pattern whenever you want a repeatable, constrained workflow.

**Engineering value:**
- *Entry-level:* Skills turn multi-step prompts into one-word commands. Instead of explaining 'create a new page with the nav and footer and...' every time, you type `/new-page faq`.
- *Mid-level:* Skills are how you enforce team consistency. A `/new-component` skill ensures every component follows the same structure, naming, and testing pattern — no matter who creates it.
- *Senior+:* Skills are essentially codified workflows — the same concept as project templates, Yeoman generators, or `rails generate`, but defined in natural language and version-controlled with your project.

Shall we create a manual-only skill next?

### 4.3 Create the "daily-summary" Skill

Create a daily summary skill that shows what you added to forge today. This one should be manual-only -- you do not want Claude invoking it automatically during other tasks.

"Create a daily-summary skill that lists everything I added or modified today, grouped by type, with title, tags, and a brief summary for each item. Set disable-model-invocation to true so it only runs when I type /daily-summary. Restrict tools to Read and Bash."

Notice `disable-model-invocation: true` -- this skill can only be triggered
by you typing `/daily-summary`. Claude will not invoke it automatically.

**STOP -- What you just did:** You created a skill with `disable-model-invocation: true`. This is a critical distinction: most skills can be triggered both by you (typing `/daily-summary`) and by Claude (when it decides the skill is relevant). Setting `disable-model-invocation: true` means *only you* can trigger it. Use this for skills that should never run automatically -- summaries, reports, destructive operations, anything where you want explicit human intent.

**Engineering value:**
- *Entry-level:* `disable-model-invocation` is your safety switch — it means this skill only runs when YOU ask for it, never automatically.
- *Mid-level:* In production repos, you'll want destructive or expensive operations (database resets, deployment scripts, full test suites) as manual-only skills. This prevents accidental execution during normal conversation.

**Quick check before continuing:**
- [ ] Three skill directories exist under `.claude/skills/`
- [ ] Each has a `SKILL.md` with frontmatter (name, description, allowed-tools)
- [ ] The daily-summary skill has `disable-model-invocation: true`

### 4.4 Exit and Resume

New skills don't appear in `/` autocomplete until you restart the session. This is a perfect time to learn how to exit and pick up where you left off.

Exit Claude Code:

```
/exit
```

Now resume your session:

```
claude --resume
```

Claude picks up right where you left off -- your conversation history, CLAUDE.md, and rules are all still loaded. Type `/` and you should see your new skills (`add-item`, `search`, `daily-summary`) in the autocomplete list.

**STOP -- What you just did:** You learned how to exit and resume a Claude Code session. The `--resume` flag restores your full conversation context, so you never lose progress. This is essential whenever you need to restart -- whether for new skills to appear, to free up memory, or just to take a break.

### 4.5 Test Your Skills

Test each skill:

```
/add-item note
/search testing
/daily-summary
```

Try with arguments:

```
/add-item snippet python
/search tag:reference
```

### 4.6 Argument Substitution

Skills support these substitution variables:

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed after the skill name |
| `$ARGUMENTS[0]` or `$0` | First argument |
| `$ARGUMENTS[1]` or `$1` | Second argument |
| `$ARGUMENTS[N]` or `$N` | Nth argument (zero-indexed) |
| `${CLAUDE_SESSION_ID}` | Current session ID |

### 4.7 Hot-Reload

**Why this step:** Skills hot-reload means you can iterate on a skill's behavior without restarting Claude Code. Edit the SKILL.md file, save it, and the next invocation uses the updated version. This makes skill development fast and interactive.

With Claude Code still running, open `.claude/skills/search/SKILL.md` in a
separate editor and add a line to the steps:

```
7. After displaying results, show the total search time
```

Save the file. Now invoke `/search` again in Claude Code. The updated skill
content takes effect immediately -- no restart needed.

### 4.8 Create a Manual-Only Skill

Create one more manual-only skill -- a bug report template generator. Tell Claude what fields you want in the template (type, steps to reproduce, expected vs. actual behavior, version) and that the issue title should come from the first argument.

"Create an issue-template skill with disable-model-invocation: true. It should take an issue title as $0 and output a bug report template with fields for Type, Steps to reproduce, Expected behavior, Actual behavior, and Forge version."

Test it: `/issue-template "Search returns wrong results"`

**STOP -- What you just did:** You now have a library of custom slash commands tailored to your forge toolkit. Skills are one of the most practical Claude Code features -- they turn multi-step workflows into one-line commands. The combination of argument substitution (`$0`, `$ARGUMENTS`), tool restrictions (`allowed-tools`), and invocation control (`disable-model-invocation`) gives you fine-grained control over what each skill does and when it runs.

### 4.9 Skill Frontmatter & Built-in Skills

A few skill authoring features have landed recently. What do you think each one is useful for?

**`effort` frontmatter.** Add `effort: low` (or `medium`/`high`) to a skill's frontmatter to override the model effort level when that skill is invoked. Try adding it to one of your skills -- when would you want a skill to force low effort? (v2.1.80)

**`${CLAUDE_SKILL_DIR}`.** This variable resolves to the skill's own directory. Use it in SKILL.md to reference sibling files -- for example, `Read ${CLAUDE_SKILL_DIR}/template.txt`. Check the skills docs if you want the full variable reference (v2.1.69).

**`/claude-api` bundled skill.** Claude Code ships with a built-in skill for building apps with the Claude API. It triggers automatically when your code imports `anthropic` or `@anthropic-ai/sdk`. Try typing `/claude-api` to see what it offers (v2.1.69).

Try adding `effort: low` to one of your existing skills and invoking it -- does the response feel different?

> **STOP** -- Experiment with `effort` frontmatter and `${CLAUDE_SKILL_DIR}` in one of your skills.

### Checkpoint

You just built your own commands. These skills encode your workflow -- use them every time you add or search items.

- [ ] `.claude/skills/add-item/SKILL.md` exists with frontmatter and supporting files
- [ ] `.claude/skills/search/SKILL.md` exists with argument parsing
- [ ] `.claude/skills/daily-summary/SKILL.md` exists with `disable-model-invocation: true`
- [ ] All three skills invoke correctly with `/skill-name`
- [ ] Argument substitution works (`$0`, `$ARGUMENTS`)
- [ ] Hot-reload works: edit SKILL.md while Claude runs, changes take effect
- [ ] Issue template skill outputs raw text without Claude processing
- [ ] Tested `effort` frontmatter and `${CLAUDE_SKILL_DIR}` in a skill
