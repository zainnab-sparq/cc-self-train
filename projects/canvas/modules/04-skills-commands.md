# Module 4 -- Skills and Commands

**CC features:** SKILL.md, frontmatter, custom slash commands, hot-reload,
argument substitution, `disable-model-invocation`

**Persona -- Collaborator:** Ask before telling, give pointers not answers. "What do you think…", "Try this and tell me…"

### 4.1 Create the "new-page" Skill

**Where do skills go?** Create all skills in the cc-self-train root `.claude/skills/` directory — NOT inside `workspace/canvas-site/.claude/skills/`. Since Claude runs from the cc-self-train root, it only sees skills at that level.

Skills are reusable slash commands you define for your project. Instead of typing a long prompt every time, you write it once as a `/skill-name` and invoke it with arguments. Let's build the first one.

Describe the skill you want to Claude. You want a skill that scaffolds a new HTML page with your site's shared layout -- so every time you invoke `/new-page faq`, it reads your existing nav and footer, creates a new page with the right boilerplate, and reminds you to update links.

```
Create a 'new-page' skill in .claude/skills/new-page/SKILL.md. It should take a page name as an argument (using $0), read index.html to get the shared nav and footer, then create a new HTML file with the full boilerplate and shared layout. Also create a page-template.md reference file showing the expected structure. Set allowed-tools to Read, Write, Edit, and Bash.
```

Claude will ask you clarifying questions about the template structure or what the skill should do after creating the file. Answer based on how you want your pages to work.

**STOP -- What you just did:** You created a skill with a supporting file. The `SKILL.md` is the instruction template -- it tells Claude what to do when you invoke `/new-page`. The `page-template.md` is a reference document the skill can read for the HTML boilerplate. This pattern (instruction + reference files) is how you build skills that produce consistent, high-quality output every time.

**Engineering value:**
- *Entry-level:* Skills turn multi-step prompts into one-word commands. Instead of explaining 'create a new page with the nav and footer and...' every time, you type `/new-page faq`.
- *Mid-level:* Skills are how you enforce team consistency. A `/new-component` skill ensures every component follows the same structure, naming, and testing pattern — no matter who creates it.
- *Senior+:* Skills are essentially codified workflows — the same concept as project templates, Yeoman generators, or `rails generate`, but defined in natural language and version-controlled with your project.

Ready to build the component skill?

### 4.2 Create the "component" Skill

Now create a skill for generating reusable CSS components. This one should take a component type as an argument (like "card", "button", "hero") and create the CSS following your design system.

```
Create a 'component' skill that takes a component type as $0, reads the existing CSS to understand our design tokens, then creates a new BEM-style CSS class with responsive styles and hover/focus states. Also create a component-templates.md reference with example HTML and CSS for common component types.
```

Discuss with Claude what component types you want supported and how the CSS should be organized -- appended to the main file or in separate component files.

**Quick check before continuing:**
- [ ] `.claude/skills/new-page/SKILL.md` exists with frontmatter and a supporting template file
- [ ] `.claude/skills/component/SKILL.md` exists with a component templates reference
- [ ] Both skills use `$0` for argument substitution

### 4.3 Create the "check-site" Skill

This skill is different -- it validates your site without modifying anything. Describe the quality checks you want to Claude:

```
Create a 'check-site' skill that scans all HTML pages and checks for common issues -- missing doctype, missing lang attribute, missing meta tags, heading hierarchy problems, images without alt text, broken internal links, missing title elements. Output a pass/fail report. Set disable-model-invocation to true so it only runs when I explicitly invoke it, and limit allowed-tools to Read, Bash, Grep, and Glob.
```

Notice `disable-model-invocation: true` -- this skill can only be triggered
by you typing `/check-site`. Claude will not invoke it automatically.

**STOP -- What you just did:** You created three skills with different purposes: `new-page` generates files, `component` creates CSS, and `check-site` validates without modifying anything. The `disable-model-invocation: true` flag on `check-site` is important -- it means Claude will never run this validation on its own, only when you explicitly ask. You will use this flag whenever a skill should be user-triggered only (like destructive operations or expensive checks).

**Engineering value:**
- *Entry-level:* `disable-model-invocation` is your safety switch — it means this skill only runs when YOU ask for it, never automatically.
- *Mid-level:* In production repos, you'll want destructive or expensive operations (database resets, deployment scripts, full test suites) as manual-only skills. This prevents accidental execution during normal conversation.

Want to test all three skills in action?

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

Claude picks up right where you left off -- your conversation history, CLAUDE.md, and rules are all still loaded. Type `/` and you should see your new skills (`new-page`, `component`, `check-site`) in the autocomplete list.

**STOP -- What you just did:** You learned how to exit and resume a Claude Code session. The `--resume` flag restores your full conversation context, so you never lose progress. This is essential whenever you need to restart -- whether for new skills to appear, to free up memory, or just to take a break.

### 4.5 Test Your Skills

Test each skill:

```
/new-page faq
/component card
/check-site
```

Try with different arguments:

```
/new-page resume
/component hero
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

**Why this step:** Hot-reload means you can iterate on your skills without restarting Claude Code. This makes skill development fast -- edit, save, test, repeat. No restart cycle.

With Claude Code still running, open `.claude/skills/check-site/SKILL.md` in a
separate editor and add a line to the checks:

```
8. All <a> tags with external URLs have target="_blank" and rel="noopener"
```

Save the file. Now invoke `/check-site` again in Claude Code. The updated skill
content takes effect immediately -- no restart needed.

### 4.8 Create a Manual-Only Skill

Create one more skill -- a page brief template that outputs a planning document for a new page without Claude processing it.

```
Create a 'page-brief' skill with disable-model-invocation set to true. It should take a page name as $0 and output a planning template with fields like purpose, target audience, key sections, SEO keywords, and design notes.
```

Test it: `/page-brief "Services"`

**STOP -- What you just did:** You now have four custom skills that extend Claude Code's capabilities specifically for your portfolio project. The `new-page` and `component` skills are productivity multipliers -- what used to be a multi-paragraph prompt is now a single slash command. The `check-site` skill is a quality gate. The `page-brief` skill outputs raw text without Claude processing it (because of `disable-model-invocation`). Together, these skills form a custom toolkit tailored to your project.

### 4.9 Skill Frontmatter & Built-in Skills

A few skill authoring features have landed recently. What do you think each one is useful for?

**`effort` frontmatter.** Add `effort: low` (or `medium`/`high`) to a skill's frontmatter to override the model effort level when that skill is invoked. Try adding it to one of your skills -- when would you want a skill to force low effort? (v2.1.80)

**`${CLAUDE_SKILL_DIR}`.** This variable resolves to the skill's own directory. Use it in SKILL.md to reference sibling files -- for example, `Read ${CLAUDE_SKILL_DIR}/template.txt`. Check the skills docs if you want the full variable reference (v2.1.69).

**`/claude-api` bundled skill.** Claude Code ships with a built-in skill for building apps with the Claude API. It triggers automatically when your code imports `anthropic` or `@anthropic-ai/sdk`. Try typing `/claude-api` to see what it offers (v2.1.69).

Try adding `effort: low` to one of your existing skills and invoking it -- does the response feel different?

> **STOP** -- Experiment with `effort` frontmatter and `${CLAUDE_SKILL_DIR}` in one of your skills.

### Checkpoint

You just built your own commands. These skills will save you real time on every page you add from here on.

- [ ] `.claude/skills/new-page/SKILL.md` exists with frontmatter and supporting files
- [ ] `.claude/skills/component/SKILL.md` exists with component templates
- [ ] `.claude/skills/check-site/SKILL.md` exists with `disable-model-invocation: true`
- [ ] All three skills invoke correctly with `/skill-name`
- [ ] Argument substitution works (`$0`, `$ARGUMENTS`)
- [ ] Hot-reload works: edit SKILL.md while Claude runs, changes take effect
- [ ] Page brief skill outputs raw text without Claude processing
- [ ] Tested `effort` frontmatter and `${CLAUDE_SKILL_DIR}` in a skill
