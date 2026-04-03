# Module 4 -- Skills and Commands

**CC features:** SKILL.md, frontmatter, custom slash commands, hot-reload,
argument substitution, `disable-model-invocation`

**Persona -- Collaborator:** Ask before telling, give pointers not answers. "What do you think...", "Try this and tell me..."

### 4.1 Create a Workflow Skill

**Where do skills go?** Create skills in your external project's `.claude/skills/` directory — that's where Claude looks when running from your project root. If you're running Claude from the cc-self-train directory instead, use cc-self-train's `.claude/skills/` directory.

Skills are reusable slash commands you define for your project. Instead of typing a long prompt every time, you write it once as a `/skill-name` and invoke it with arguments. Let's build one that automates a repetitive task in your project.

Think about what you create repeatedly. New components? New endpoints? New test files? New modules or packages? Pick the most common one and describe it to Claude:

```
Create a skill in .claude/skills/<name>/SKILL.md that automates scaffolding a new [component/module/endpoint/test file] in my project. It should take a name as $0, read existing examples to understand the patterns we follow, then generate the new files with the right boilerplate and structure. Also create a reference template file showing the expected structure. Set allowed-tools to Read, Write, Edit, and Bash.
```

Replace `[component/module/endpoint/test file]` with whatever fits your project. Claude will ask clarifying questions about your project's conventions. Answer based on how you actually structure things.

**STOP -- What you just did:** You created a skill with a supporting reference file. The `SKILL.md` is the instruction template -- it tells Claude what to do when you invoke the skill. The reference file gives it a concrete example to follow. This pattern (instruction + reference files) is how you build skills that produce consistent, high-quality output every time.

**Engineering value:**
- *Entry-level:* Skills turn multi-step prompts into one-word commands. Instead of explaining 'create a new module with the right imports and structure and...' every time, you type `/scaffold api-handler`.
- *Mid-level:* Skills are how you enforce team consistency. A `/new-component` skill ensures every component follows the same structure, naming, and testing pattern -- no matter who creates it.
- *Senior+:* Skills are essentially codified workflows -- the same concept as project templates, Yeoman generators, or `rails generate`, but defined in natural language and version-controlled with your project.

Ready to build a second skill?

### 4.2 Create a Second Skill

Now create a skill for a different purpose -- generating boilerplate that matches your project's patterns. Think about what kind of boilerplate you write most often. Some examples by project type:

- **Web app:** form components, API route handlers, middleware
- **CLI tool:** new subcommand, argument parser, output formatter
- **Library:** new public module, docstring template, example usage
- **Data project:** new notebook setup, ETL pipeline stage, model experiment

Describe the skill to Claude:

```
Create a skill that takes a name as $0 and generates [your boilerplate type] following the patterns in my existing code. It should read [relevant existing files] to understand our conventions, then create the new files with the right structure.
```

Discuss with Claude what conventions matter -- naming, file placement, imports, test stubs. The skill should capture your project's way of doing things.

**Quick check before continuing:**
- [ ] `.claude/skills/` contains two skill directories, each with a `SKILL.md` and supporting files
- [ ] Both skills use `$0` for argument substitution
- [ ] Each skill serves a different purpose (scaffolding vs. boilerplate generation)

### 4.3 Create a Validation Skill

This skill is different -- it checks your project's quality without modifying anything. Think about the quality checks that matter for your codebase:

- **Linting:** ruff, eslint, golangci-lint, clippy
- **Type checking:** mypy, tsc, flow
- **Tests:** pytest, jest, go test, cargo test
- **Custom checks:** import cycles, naming conventions, TODO markers, missing docs

Describe the checks you want to Claude:

```
Create a 'check-project' skill that runs quality checks on my codebase -- [list your checks: linting, type checking, tests, etc.]. Output a pass/fail report for each check. Set disable-model-invocation to true so it only runs when I explicitly invoke it, and limit allowed-tools to Read, Bash, Grep, and Glob.
```

Notice `disable-model-invocation: true` -- this skill can only be triggered by you typing `/check-project`. Claude will not invoke it automatically.

**STOP -- What you just did:** You created three skills with different purposes: the first scaffolds new files, the second generates boilerplate, and `check-project` validates without modifying anything. The `disable-model-invocation: true` flag on `check-project` is important -- it means Claude will never run this validation on its own, only when you explicitly ask. You will use this flag whenever a skill should be user-triggered only (like destructive operations or expensive checks).

**Engineering value:**
- *Entry-level:* `disable-model-invocation` is your safety switch -- it means this skill only runs when YOU ask for it, never automatically.
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

Claude picks up right where you left off -- your conversation history, CLAUDE.md, and rules are all still loaded. Type `/` and you should see your new skills in the autocomplete list.

**STOP -- What you just did:** You learned how to exit and resume a Claude Code session. The `--resume` flag restores your full conversation context, so you never lose progress. This is essential whenever you need to restart -- whether for new skills to appear, to free up memory, or just to take a break.

### 4.5 Test Your Skills

Test each skill with real arguments from your project:

```
/scaffold-name some-feature
/boilerplate-name some-module
/check-project
```

Replace the skill names with whatever you named yours. Try with different arguments:

```
/scaffold-name another-feature
/boilerplate-name another-module
```

If a skill doesn't produce what you expected, iterate on its `SKILL.md` -- you'll learn hot-reload in the next step.

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

With Claude Code still running, open your validation skill's `SKILL.md` in a separate editor and add a new check to the list. For example, if you're checking for lint and tests, add a check for TODO/FIXME markers or missing documentation.

Save the file. Now invoke your validation skill again in Claude Code. The updated skill content takes effect immediately -- no restart needed.

### 4.8 Create a Manual-Only Skill

Create one more skill -- a planning template that outputs a structured document without Claude processing it further.

```
Create a skill with disable-model-invocation set to true that takes a feature name as $0 and outputs a planning template with fields like purpose, acceptance criteria, files to modify, dependencies, testing approach, and rollback plan.
```

Test it: `/plan-feature "user-auth"`

**STOP -- What you just did:** You now have four custom skills that extend Claude Code's capabilities specifically for your project. The scaffolding and boilerplate skills are productivity multipliers -- what used to be a multi-paragraph prompt is now a single slash command. The validation skill is a quality gate. The planning skill outputs raw text without Claude processing it (because of `disable-model-invocation`). Together, these skills form a custom toolkit tailored to your project.

### 4.9 Skill Frontmatter & Built-in Skills

A few skill authoring features have landed recently. What do you think each one is useful for?

**`effort` frontmatter.** Add `effort: low` (or `medium`/`high`) to a skill's frontmatter to override the model effort level when that skill is invoked. Try adding it to one of your skills -- when would you want a skill to force low effort? (v2.1.80)

**`${CLAUDE_SKILL_DIR}`.** This variable resolves to the skill's own directory. Use it in SKILL.md to reference sibling files -- for example, `Read ${CLAUDE_SKILL_DIR}/template.txt`. Check the skills docs if you want the full variable reference (v2.1.69).

**`/claude-api` bundled skill.** Claude Code ships with a built-in skill for building apps with the Claude API. It triggers automatically when your code imports `anthropic` or `@anthropic-ai/sdk`. Try typing `/claude-api` to see what it offers (v2.1.69).

Try adding `effort: low` to one of your existing skills and invoking it -- does the response feel different?

> **STOP** -- Experiment with `effort` frontmatter and `${CLAUDE_SKILL_DIR}` in one of your skills.

### 4.10 Skill Scoping & Shell Execution Control

Two new skill features have landed that give you more control over when and how skills run.

**`paths:` frontmatter for skills.** Just like rules (Module 3), skills can now accept `paths:` as a YAML list of globs. Try adding it to one of your existing skills -- for example, scope a skill so it only activates when you're working in a specific directory of your project.

**`disableSkillShellExecution` setting.** Set `"disableSkillShellExecution": true` in settings.json to prevent skills from executing shell commands. This is a safety feature for shared environments where you want skills to generate and edit files but not run arbitrary commands.

Try both: add `paths:` to an existing skill, then toggle `disableSkillShellExecution` and invoke a skill that uses Bash to see what happens.

> **STOP** -- Test `paths:` scoping on a skill and observe what `disableSkillShellExecution` does.

### Checkpoint

You just built your own commands. These skills will save you real time on every feature you add from here on.

- [ ] Tested `paths:` on a skill and `disableSkillShellExecution`
- [ ] `.claude/skills/` contains at least two generative skills with frontmatter and supporting files
- [ ] `.claude/skills/check-project/SKILL.md` (or similar) exists with `disable-model-invocation: true`
- [ ] All skills invoke correctly with `/skill-name`
- [ ] Argument substitution works (`$0`, `$ARGUMENTS`)
- [ ] Hot-reload works: edit SKILL.md while Claude runs, changes take effect
- [ ] Planning skill outputs raw text without Claude processing
- [ ] Tested `effort` frontmatter and `${CLAUDE_SKILL_DIR}` in a skill
