# Module 4 -- Skills & Commands

**CC features:** SKILL.md, frontmatter, custom slash commands, hot-reload, argument substitution, disable-model-invocation

> **Persona — Collaborator:** Ask before telling, give pointers not answers. "What do you think…", "Try this and tell me…"

In this module you create reusable skills that extend what Claude can do in your project.

### Step 1: Create the "analyze" skill

> **Why this step:** Skills turn multi-step workflows into single slash commands. Instead of typing a long prompt every time you want to analyze code, you type `/analyze src/` and Claude follows the same steps every time. Skills are reusable, shareable, and version-controlled -- they become part of your project's toolbox.

Ask Claude to create an `/analyze` skill. Describe what you want it to do: run Sentinel's scan on a given path, summarize findings by severity, highlight errors first, and suggest fixes for the top issues. Tell Claude it should accept a path argument so you can run `/analyze src/` or `/analyze src/rules/`.

> "Create a skill at .claude/skills/analyze/SKILL.md. It should run Sentinel analysis on whatever path I give it, summarize findings by severity, show errors first, and suggest fixes. It should accept a path argument using $ARGUMENTS."

Claude will create the SKILL.md file with frontmatter (name, description, argument-hint) and the skill body. Review it and tweak the steps if you want a different workflow.

Test it:

```
/analyze src/
```

> **STOP -- What you just did:** You created your first custom skill and tested it with a path argument. The `$ARGUMENTS` placeholder captured everything after `/analyze`, so `/analyze src/` passed `src/` to the skill. This is the foundation -- you will build several more skills that become your daily shortcuts for working with Sentinel.

> **Engineering value:**
> - *Entry-level:* Skills turn multi-step prompts into one-word commands. Instead of explaining 'create a new page with the nav and footer and...' every time, you type `/new-page faq`.
> - *Mid-level:* Skills are how you enforce team consistency. A `/new-component` skill ensures every component follows the same structure, naming, and testing pattern — no matter who creates it.
> - *Senior+:* Skills are essentially codified workflows — the same concept as project templates, Yeoman generators, or `rails generate`, but defined in natural language and version-controlled with your project.

Ready to create the generate-tests skill?

### Step 2: Create the "generate-tests" skill

Ask Claude to create a `/generate-tests` skill. This one should analyze a source file, identify all public functions, and generate comprehensive tests covering happy paths, edge cases, and error cases. Tell Claude you want this skill to use `context: fork` so it runs in a separate subagent and keeps your main conversation clean.

> "Create a skill at .claude/skills/generate-tests/SKILL.md. It should take a source file path, find all public functions, generate tests for happy paths, edge cases, and error cases, then run them. Use `context: fork` in the frontmatter so it runs in a subagent."

> **Why this step:** Notice `context: fork` in the frontmatter -- this skill runs in a separate subagent so test generation output does not clutter your main conversation. Forked context is ideal for verbose operations where you want the result but not the noise.

Test it by pointing it at one of your rule modules:

```
/generate-tests src/rules/complexity.py
```

(Replace with the actual path to one of your rule modules.)

### Step 3: Create the "quality-report" skill

Ask Claude to create a `/quality-report` skill. This one should run a full scan, collect findings by category and severity, calculate summary stats, and save a report to the `reports/` directory. Tell Claude to include `disable-model-invocation: true` in the frontmatter so this skill only runs when you explicitly type the command.

> "Create a skill at .claude/skills/quality-report/SKILL.md. It should run a full scan, summarize findings by category and severity, save a timestamped report to reports/, and support a format argument for text, JSON, or HTML. Set `disable-model-invocation: true` so it only runs when I call it explicitly."

Notice `disable-model-invocation: true` -- this skill only runs when you explicitly type `/quality-report`. Claude will not trigger it automatically.

> **STOP -- What you just did:** You created three skills with different behaviors: `/analyze` runs in your main conversation, `/generate-tests` forks into a subagent, and `/quality-report` uses `disable-model-invocation: true` so it only runs when you explicitly call it. These three patterns cover most skill use cases you will encounter.

> **Engineering value:**
> - *Entry-level:* `disable-model-invocation` is your safety switch — it means this skill only runs when YOU ask for it, never automatically.
> - *Mid-level:* In production repos, you'll want destructive or expensive operations (database resets, deployment scripts, full test suites) as manual-only skills. This prevents accidental execution during normal conversation.

> **Quick check before continuing:**
> - [ ] `/analyze src/` runs and produces output
> - [ ] `/generate-tests` runs in a forked context (you should see subagent output)
> - [ ] `/quality-report` exists with disable-model-invocation: true

### Step 4: Use custom slash commands with arguments

Test argument substitution:

```
/analyze src/rules/
```

```
/generate-tests src/scanner.py
```

```
/quality-report --format json
```

The `$ARGUMENTS` placeholder captures everything after the skill name. You can also use positional arguments like `$0`, `$1` for more structured inputs.

### Step 5: Hot-reload skills

> **Why this step:** Hot-reload means you can iterate on skills without restarting Claude Code. This makes skill development fast -- edit, test, edit, test -- just like editing code with a live-reloading server.

Edit one of your SKILL.md files (add a new step or change the description). You do not need to restart Claude Code -- skills are reloaded when invoked. Test by modifying the analyze skill and running `/analyze src/` again.

### Step 6: Create a no-AI skill

Ask Claude to create a no-AI skill that just runs a shell command. This one should list all available analysis rules by executing `sentinel rules list` -- no AI processing needed.

> "Create a skill at .claude/skills/list-rules/SKILL.md that just runs `!sentinel rules list`. Set `disable-model-invocation: true` since it doesn't need AI."

This skill just executes a shell command. No AI processing needed. Test it:

```
/list-rules
```

> **STOP -- What you just did:** You built a no-AI skill -- a slash command that runs a shell command directly without invoking the model. This is useful for quick reference commands where you do not need Claude to interpret the output. Between `/analyze`, `/generate-tests`, `/quality-report`, and `/list-rules`, you now have a custom command palette tailored to Sentinel. In real projects, you will accumulate skills like these over time until your most common workflows are all one-command operations.

### Checkpoint

You just built your own commands. Running analysis and generating tests is now one slash command away.

- [ ] `/analyze` skill exists and works with path arguments
- [ ] `/generate-tests` skill exists, runs in a forked context, and produces tests
- [ ] `/quality-report` skill exists with disable-model-invocation: true
- [ ] You tested argument substitution ($ARGUMENTS) in at least one skill
- [ ] You edited a skill and saw hot-reload work without restarting
- [ ] `/list-rules` works as a no-AI skill
