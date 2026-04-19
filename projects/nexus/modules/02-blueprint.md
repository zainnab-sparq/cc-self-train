# Module 2 -- Blueprint & Build

<!-- progress:start -->
**Progress:** Module 2 of 10 `[██░░░░░░░░]` 20%

**Estimated time:** ~60-90 min
<!-- progress:end -->

<details>
<summary>What you’ll use in this module</summary>

**CC features:** Plan mode, model selection, git integration, basic prompting

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try...", "Here's what that does..."

</details>

### 2.1 Enter Plan Mode

So far, you've been talking to Claude in normal mode -- you say something, Claude does it. Press `Shift+Tab` to switch to plan mode. The indicator in your prompt area changes to show you are in planning mode. **Instead of writing code, Claude thinks *with* you -- it analyzes, suggests architecture, and asks clarifying questions, but doesn't touch any files.**

**Why this actually matters -- a story:**

Dev A asks Claude to "refactor the auth flow to use JWT." Claude touches 14 files, introduces a bug in the refresh logic, and Dev A spends 3 hours reverting half the changes and debugging the other half.

Dev B enters plan mode first and asks the same question. Claude produces a 6-step plan, flags that the refresh logic is subtle, and asks whether the existing session-based code needs to coexist. Dev B clarifies the scope, agrees to the plan, exits plan mode -- and the refactor lands clean in 20 minutes.

Same model, same task, same prompt. **The difference is plan mode.** You spend 2 minutes planning to save 3 hours untangling. Use it every time the answer might touch more than one file.

### 2.2 Design the Architecture

Now describe your gateway to Claude. Tell it about the core pieces you want -- an HTTP server, a route registry, request forwarding, a config file, a health endpoint, and a CLI. Don't worry about getting the prompt perfect; just describe your vision and let Claude ask clarifying questions.

Try something like:

```
I want to build a local API gateway called nexus-gateway. It should listen for HTTP requests, match them against configured routes, and forward them to upstream services. I also want a CLI, a health check endpoint, and a config file for route definitions. Help me design the architecture -- ask me questions about anything that's unclear.
```

Claude will probably ask about your config format preference (YAML, JSON, TOML), how you want to handle path parameters, and what the CLI commands should look like. Answer naturally -- these are your design decisions.

Once Claude produces a plan with a directory structure and module breakdown, read it carefully. Push back on anything you would do differently. Remember, you are still in Plan mode, so nothing is being written to disk yet.

### 2.3 Review and Iterate

Read Claude's plan carefully. While still in Plan mode, push on the details. Ask about edge cases:

```
What happens when no route matches? How will path parameters like /users/:id work? Where does the config file live?
```

If something in the design feels off, say so. Claude will revise. Iterate until you are satisfied -- this is a conversation, not a one-shot prompt.

**STOP -- What you just did:** You used plan mode to design your gateway's architecture before writing any code. This is one of Claude Code's most powerful patterns: think through complex decisions *with* Claude before committing to an approach. Plan mode prevents the "just start coding" trap that leads to rewrites. You will use this plan-first pattern at the start of every major feature.

### 2.3b Models Work Automatically for Now

**Why this step:** Claude Code picks a model for you based on your subscription -- for this training, the default just works. You will learn fine-grained model control later, once the basics are solid.

- **Pro / API users** default to Sonnet 4.6 -- the balanced model that handles most coding tasks well.
- **Max / Team Premium users** default to Opus 4.6 -- the most capable model for complex reasoning.

Either default is great for what we are doing. Module 8 (subagents) shows when and how to switch models with `/model`, tune reasoning depth with `/effort`, or speed up Opus with `/fast`.

**STOP -- What you just did:** You learned that Claude Code picks a model automatically. Trust the default for this training; you will learn when and how to switch it in Module 8. Full reference: `context/models.txt`.

### 2.4 Exit Plan Mode and Execute

Press `Shift+Tab` to switch back to Act mode. Now ask Claude to create the project structure you just designed together. Tell it to set up the directory layout, create placeholder files for each module, and write a config file with a couple of example routes.

Try something like:

```
Let's build out the project structure from our plan. Create the directories, placeholder files, and a config file with two example routes -- one for /api/users and one for /api/products.
```

**Why this step:** Feature branches keep your experiments separate from working code. If something goes wrong, you can throw away the branch without affecting main. This is standard practice in professional development and Claude Code's git integration makes it seamless.

### 2.5 Create a Feature Branch

**New to branches?** A Git branch is a parallel copy of your code where you can experiment safely. If the experiment works, you merge it back to main. If it fails, you delete the branch and main is untouched. The command below creates a new branch called `feature/core` and switches you to it -- you can see which branch you are on anytime with `! git branch`.

```
! git status                # inspect what's about to be staged
! git add <files or dirs you want to commit>   # name them explicitly
! git commit -m "Initial project structure"
! git checkout -b feature/core
```

**Heads up:** `git add -A` is tempting, but it will stage `.env` files, IDE configs, and build artifacts you may not have meant to commit. Run `git status` first, then `git add` the specific paths you actually want. The first time someone commits a `.env` is a very bad day.

Or ask Claude to handle the git workflow for you:

```
Create a feature branch called feature/core and commit the current project structure.
```

**Screenshot trick:** If you hit an error you can't figure out, take a screenshot and drag it directly into the Claude Code chat. Claude can see images -- so instead of copy-pasting a messy stack trace, just screenshot your terminal and drop it in. You can also paste images from clipboard with `Ctrl+V` (macOS/Linux) or `Alt+V` (Windows).

**STOP -- What you just did:** You went from an empty directory to a planned, structured project on its own feature branch -- all without leaving Claude Code. The `!` prefix for shell commands and Claude's ability to run git operations mean your entire workflow lives in one place. Notice how each prompt was focused on one concern (structure, then commit, then branch) rather than asking for everything at once.

Ready to start building the core gateway?

### 2.6 Implement the Core Gateway

**Why this step:** Breaking implementation into separate, focused prompts (server, routing, forwarding) gives Claude better results than one giant "build everything" prompt. Each prompt is specific enough that Claude can implement it completely before moving on.

Work with Claude to build the core components one at a time. Start by asking for the HTTP server -- tell Claude it should read the port from config, listen for requests, pass them to the route matcher, and return 404 when nothing matches.

Try something like:

```
Let's start with the HTTP server module. It needs to read the port from config, listen for requests, hand them off to the route matcher, and return a 404 JSON response when no route matches.
```

Once that is working, move to route matching. Describe what you need -- loading routes from config, matching by method and path pattern, supporting exact and prefix matches.

```
Now let's build the route matching module. It should load routes from our config file and match incoming requests by method and path. I want exact path matches and simple prefix matching.
```

Then ask for request forwarding -- taking the matched upstream target, forwarding the original request, and handling connection errors with 502.

```
Next, the request forwarding module. It takes the matched upstream target, forwards the original request with its method, headers, and body, and returns the upstream response. If the upstream is unreachable, return 502 Bad Gateway.
```

Notice the pattern: each prompt focuses on one component. Claude will ask you clarifying questions along the way -- answer them based on your design from Step 2.

### 2.7 Write and Run Tests

Ask Claude to write tests for the route matching module. Describe the scenarios you care about -- exact matches, prefix matches, method filtering, no-match behavior, and priority when multiple routes could match. Let Claude decide on the test structure.

```
Write tests for the route matcher. I want to cover exact path matching, prefix matching, method filtering, what happens when nothing matches, and which route wins when multiple routes could match. Then run them.
```

After tests pass, ask Claude to commit the work with a descriptive message.

```
Commit the route matching implementation and its tests.
```

**STOP -- What you just did:** You built the core gateway and validated it with tests -- the build-test-commit cycle that you will repeat for every feature going forward. Notice the pattern: implement a focused piece, write tests to prove it works, commit when tests pass. This tight loop catches bugs early and gives you safe rollback points.

**Quick check before continuing:**
- [ ] The gateway starts and listens on a port
- [ ] Route matching works for at least 2 routes
- [ ] Tests pass for the route matching module
- [ ] You are on the feature/core branch (not main)

### 2.8 Implement the CLI

Tell Claude about the CLI you want. Describe the subcommands -- starting the server, listing routes, adding a route, and checking health. Let Claude suggest the argument structure and help text.

```
I want a CLI for the gateway. I need commands to start the server, list all configured routes, add a new route with a path, method, and upstream, and check if the gateway is healthy. What's the best way to structure this?
```

Claude will implement the CLI and may ask about argument parsing libraries for your language. Pick what you are comfortable with.

### 2.9 Manual Testing

Start a simple upstream service (or ask Claude to create a tiny echo server), then test the gateway end-to-end. Ask Claude to help you set up the test and walk you through the curl commands.

```
Help me test the gateway manually. I need a simple echo server on port 4001 as an upstream, then show me how to test each route and the /health endpoint with curl.
```

Claude will create the echo server, start the gateway, and give you the curl commands. Run them and verify the responses look right.

### 2.10 Merge to Main

**If something goes wrong:** The most common issue on a first merge is a *conflict* -- when Git cannot figure out how to combine changes. For this module, `main` has not moved since you branched, so conflicts are not expected. If you do see a conflict message, do not panic -- ask Claude: "I got a merge conflict. Can you help me resolve it?" and Claude will walk you through it.

Ask Claude to commit any remaining changes and merge the feature branch back to main.

```
Commit everything and merge feature/core into main.
```

**STOP -- What you just did:** You completed a full feature development cycle: plan in plan mode, branch, implement incrementally, test, and merge. This plan-branch-build-test-merge workflow is how professional teams ship software, and you just did it entirely through Claude Code. Every future module builds on this same cycle.

### 2.11 Branching & Quick Plans

Two workflow tricks to try now:

**`/branch`** -- makes a copy of your current conversation so you can explore a tangent without losing your main thread. Useful when you want to try something risky without burning your main session.

**`/plan <description>`** -- enters plan mode and immediately starts planning on the topic you describe. Example: `/plan add a contact form to the homepage`. Faster than pressing `Shift+Tab` then typing a prompt.

<details>
<summary><strong>Advanced settings you can ignore for now</strong></summary>

- **Session naming from plans.** When you accept a plan, your session is automatically named from the plan content, making `/resume` more useful.
- **Git instruction control.** The `includeGitInstructions` setting (or `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` env var) lets you remove Claude's built-in commit workflow from the system prompt if your CLAUDE.md already has custom git rules.
- **Edit without Read.** The Edit tool now works on files you have viewed via Bash (`sed -n` or `cat`), without requiring a separate `Read` call first -- fewer permission prompts when you are already looking at file content.

</details>

> **STOP** -- Try `/plan add a contact form to the homepage` to test the quick-plan workflow.

### Heads Up -- What's Coming in Module 3

Module 3 introduces **rule files** -- small Markdown files in `.claude/rules/` that tell Claude how to write code for different parts of your project. You will see files that start with `---` marks at the top, followed by lines like `name: react` or `paths: ["*.py"]`.

That opening block is called **frontmatter** -- metadata about the file, written in a format called **YAML**. Think of it like a form at the top of the document telling Claude Code how to use the file. One-sentence version: frontmatter lines are the file's settings, the body is its content. You will see much more of this starting in Module 3 and throughout skills, hooks, and agents.

If either term is still fuzzy, the [glossary](../../../GLOSSARY.md) has plain-English definitions.

### Checkpoint

You just went from an empty directory to a working gateway. Plan mode kept you focused on architecture, and now requests actually route through your server.

- [ ] Tried `/branch` and `/plan <description>` quick workflow
- [ ] You used Plan mode to design before building
- [ ] The gateway starts and listens on the configured port
- [ ] Route matching works for at least 2 routes
- [ ] /health returns `{"status": "ok"}`
- [ ] Tests pass for the route matching module
- [ ] CLI commands work: start, routes list, health
- [ ] Feature branch merged to main
- [ ] At least 3 meaningful git commits
