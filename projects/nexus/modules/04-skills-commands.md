# Module 4 -- Skills & Commands

**CC features:** SKILL.md, frontmatter, custom slash commands, hot-reload, argument substitution, disable-model-invocation

**Persona -- Collaborator:** Ask before telling, give pointers not answers. "What do you think...", "Try this and tell me..."

**Why this step:** Skills turn multi-step workflows into one-command shortcuts. Instead of explaining "read the config, validate the route, add it, show the result" every time, you encode that workflow once and invoke it with `/add-route`. Skills are how you teach Claude repeatable processes.

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

### 4.1 Create the "add-route" Skill

**Where do skills go?** Create all skills in the cc-self-train root `.claude/skills/` directory — NOT inside `workspace/nexus-gateway/.claude/skills/`. Since Claude runs from the cc-self-train root, it only sees skills at that level.

Skills live in `.claude/skills/<skill-name>/SKILL.md`. Describe the workflow you want to Claude and ask it to create the skill file with the right frontmatter.

Try something like:

```
Create a skill called add-route that walks me through adding a new route to the gateway config. It should read the existing config, ask me for the path, method, and upstream target, validate there are no conflicts, add the route, show the updated list, and remind me to restart if the gateway is running. Make it user-triggered only -- I don't want Claude running this automatically.
```

Claude will create `.claude/skills/add-route/SKILL.md` with `disable-model-invocation: true` in the frontmatter. Test it by typing:

```
/add-route
```

Claude will walk through the guided route creation process.

### 4.2 Create the "test-endpoint" Skill

Now ask Claude to create a skill for testing endpoints. Describe what it should do -- fire a test request, report the result, and diagnose failures. Tell Claude it should accept arguments for the path and method.

```
Create a test-endpoint skill that fires a request at the running gateway and reports the result. It should take a path and an optional HTTP method as arguments, show me the status code, response time, headers, and body, and if it fails, diagnose whether the gateway is running, the route exists, and the upstream is reachable. User-triggered only.
```

Claude will create the skill with `$ARGUMENTS` for argument capture and `argument-hint` in the frontmatter. Test it:

```
/test-endpoint /api/users GET
```

**STOP -- What you just did:** You created two skills with `disable-model-invocation: true`, which means they only run when you explicitly type the slash command. This is important for skills that take action (adding routes, firing test requests) -- you want to control when they execute. The `argument-hint` frontmatter in test-endpoint tells users what arguments the skill expects, and `$ARGUMENTS` captures everything they type after the command name.

**Engineering value:**
- *Entry-level:* Skills turn multi-step prompts into one-word commands. Instead of explaining 'create a new page with the nav and footer and...' every time, you type `/new-page faq`.
- *Mid-level:* Skills are how you enforce team consistency. A `/new-component` skill ensures every component follows the same structure, naming, and testing pattern -- no matter who creates it.
- *Senior+:* Skills are essentially codified workflows -- the same concept as project templates, Yeoman generators, or `rails generate`, but defined in natural language and version-controlled with your project.

How about we create a status-report skill next?

### 4.3 Create the "status-report" Skill

Ask Claude to create a status report skill that gives you a full overview of the gateway -- whether it is running, all routes with their upstreams and health, rate limit configs, and the /health endpoint response.

```
Create a status-report skill that checks if the gateway is running, reads the route config, pings each upstream to see if it's reachable, shows rate limit settings, hits /health, and formats everything as a clean table. This one does NOT need disable-model-invocation -- I want Claude to be able to run status checks proactively.
```

Notice the difference: this skill omits `disable-model-invocation: true`, so Claude can invoke it automatically when it thinks a status check is relevant.

**Quick check before continuing:**
- [ ] `/add-route` walks you through adding a route to the config
- [ ] `/test-endpoint /health GET` fires a request and reports the result
- [ ] `/status-report` generates a gateway overview
- [ ] You understand that `disable-model-invocation: true` means "user-triggered only"

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

Claude picks up right where you left off -- your conversation history, CLAUDE.md, and rules are all still loaded. Type `/` and you should see your new skills (`add-route`, `test-endpoint`, `status-report`) in the autocomplete list.

**STOP -- What you just did:** You learned how to exit and resume a Claude Code session. The `--resume` flag restores your full conversation context, so you never lose progress. This is essential whenever you need to restart -- whether for new skills to appear, to free up memory, or just to take a break.

### 4.4 Argument Substitution

**Why this step:** Positional arguments (`$0`, `$1`, `$ARGUMENTS`) make skills flexible. Instead of creating separate skills for each route, one skill with `$0` can look up any route you specify. This is the difference between a rigid script and a reusable tool.

Skills support positional arguments. In the test-endpoint skill above, `$ARGUMENTS` captures everything after the skill name. You can also use:

- `$0` -- first argument
- `$1` -- second argument
- `$ARGUMENTS[0]` -- same as `$0`

Ask Claude to create a route-info skill that uses positional arguments to look up a specific route. Describe what details you want to see about the route.

```
Create a route-info skill that takes a path pattern as its first argument and looks it up in the config. Show me the full route definition, rate limit settings, whether the upstream is reachable, and how common request patterns would match against it. User-triggered only.
```

Claude will use `$0` (the first positional argument) in the skill body. Test it: `/route-info /api/users`

### 4.5 Hot-Reload Demonstration

With Claude Code running, open `.claude/skills/status-report/SKILL.md` in a separate editor and change the description text. Go back to Claude Code and type `/status-report`. Claude picks up the updated skill content without restarting.

Skills are re-read each time they are invoked, so edits take effect immediately.

**STOP -- What you just did:** You saw that skills are re-read every time they are invoked -- no restart needed. This hot-reload behavior means you can iterate on skill prompts in real time: edit the SKILL.md, invoke the command, see the result, refine. This tight feedback loop is how you dial in the exact workflow you want.

**Engineering value:**
- *Entry-level:* `disable-model-invocation` is your safety switch -- it means this skill only runs when YOU ask for it, never automatically.
- *Mid-level:* In production repos, you'll want destructive or expensive operations (database resets, deployment scripts, full test suites) as manual-only skills. This prevents accidental execution during normal conversation.

Shall we review how disable-model-invocation controls your skills?

### 4.6 Create a disable-model-invocation Skill

The `disable-model-invocation: true` frontmatter prevents Claude from using a skill automatically. It will only run when you explicitly type the slash command.

Review your skills and confirm:
- `add-route`: has `disable-model-invocation: true` (you control when routes are added)
- `test-endpoint`: has `disable-model-invocation: true` (you control when tests fire)
- `status-report`: does NOT have it (Claude can run status checks proactively)
- `route-info`: has `disable-model-invocation: true` (lookup on demand)

Ask Claude to explain which of your skills it can invoke automatically and which require you to type the slash command.

```
Which of my skills can you invoke on your own, and which ones do I have to trigger manually? What's the difference?
```

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

**`paths:` frontmatter for skills.** Just like rules (Module 3), skills can now accept `paths:` as a YAML list of globs. Try adding it to one of your existing skills -- for example, scope the add-route skill so it only activates when you're working in the config directory.

**`disableSkillShellExecution` setting.** Set `"disableSkillShellExecution": true` in settings.json to prevent skills from executing shell commands. This is a safety feature for shared environments where you want skills to generate and edit files but not run arbitrary commands.

Try both: add `paths:` to an existing skill, then toggle `disableSkillShellExecution` and invoke a skill that uses Bash to see what happens.

> **STOP** -- Test `paths:` scoping on a skill and observe what `disableSkillShellExecution` does.

### Choose Your Battles

You've just learned how to build skills. Resist the urge to make one for every workflow you have. A new skill has a maintenance cost -- you will forget what arguments it takes, how it fails, and what state it assumes.

**Rule of thumb:** Start with **2-3 skills** for workflows you do at least weekly. Add more only when a real, repeated friction appears. Delete skills you haven't invoked in a month.

For Nexus, plausible candidates include:

- `/add-route` -- walk through adding a new gateway route with validation
- `/health-check` -- probe upstreams and show a status summary
- `/reload-routes` -- hot-reload the routing config after edits

Pick two or three (or substitute your own). Everything else can wait.

### Checkpoint

You just built your own commands. Adding routes and testing endpoints is now one slash command away.

- [ ] Tested `paths:` on a skill and `disableSkillShellExecution`
- [ ] `.claude/skills/add-route/SKILL.md` exists and `/add-route` works
- [ ] `.claude/skills/test-endpoint/SKILL.md` exists and `/test-endpoint /health GET` works
- [ ] `.claude/skills/status-report/SKILL.md` exists and `/status-report` works
- [ ] `.claude/skills/route-info/SKILL.md` exists with `$0` substitution
- [ ] You modified a skill file and saw the change take effect without restart
- [ ] You understand the difference between `disable-model-invocation: true` and default
- [ ] All skills committed to git
- [ ] Tested `effort` frontmatter and `${CLAUDE_SKILL_DIR}` in a skill
