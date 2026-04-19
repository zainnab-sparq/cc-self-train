# Module 2 -- Blueprint and Build

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

**Why this actually matters -- a story:**

Dev A asks Claude to "refactor the auth flow to use JWT." Claude touches 14 files, introduces a bug in the refresh logic, and Dev A spends 3 hours reverting half the changes and debugging the other half.

Dev B enters plan mode first and asks the same question. Claude produces a 6-step plan, flags that the refresh logic is subtle, and asks whether the existing session-based code needs to coexist. Dev B clarifies the scope, agrees to the plan, exits plan mode -- and the refactor lands clean in 20 minutes.

Same model, same task, same prompt. **The difference is plan mode.** You spend 2 minutes planning to save 3 hours untangling. Use it every time the answer might touch more than one file.

So far, you've been talking to Claude in normal mode -- you say something, Claude does it. Press `Shift+Tab` to switch to plan mode. You will see the mode indicator
change. In plan mode, Claude analyzes and plans without making changes. **Instead of writing code, Claude thinks *with* you -- it analyzes, suggests architecture, and asks clarifying questions, but doesn't touch any files.** This is where you design before you build.

Alternatively, type:

```
/plan
```

### 2.2 Design the Architecture

Now describe your portfolio site to Claude. Tell it what pages you want -- home, about, projects, blog, contact -- and what each page should include. Don't worry about getting the prompt perfect. Just describe your vision and let Claude ask clarifying questions.

Try a prompt like this:

```
I want to build a personal portfolio site with about five pages. Help me plan the architecture -- what pages should I have, what goes on each one, and how should the CSS and file structure work? Don't write any code yet, just the plan.
```

Claude will probably ask about your design preferences, layout style, and what kind of content you want to feature. Answer naturally -- these choices are yours. The back-and-forth is the point: you are designing *with* Claude, not dictating to it.

Once Claude produces a plan, read it carefully.

### 2.3 Review and Iterate

Still in plan mode, push back on the plan. Ask about the trade-offs Claude made. Challenge the decisions you are unsure about. For example:

```
Why did you choose that approach for the CSS? What are the trade-offs? And how should the navigation highlight the current page?
```

Claude does not get defensive about its plans -- ask hard questions and it will revise. If something does not feel right, say so. Refine the plan until you are satisfied with the architecture.

**STOP -- What you just did:** You used plan mode to design your entire site architecture before writing a single line of code. This is a pattern you will use constantly: plan first, then build. The back-and-forth questioning in step 2.3 is how you pressure-test a design. Claude does not get defensive about its plans -- ask hard questions and it will revise.

### 2.3b Models Work Automatically for Now

**Why this step:** Claude Code picks a model for you based on your subscription — for this training, the default just works. You will learn fine-grained model control later, once the basics are solid.

- **Pro / API users** default to Sonnet 4.6 — the balanced model that handles most coding tasks well.
- **Max / Team Premium users** default to Opus 4.6 — the most capable model for complex reasoning.

Either default is great for what we are doing. Module 8 (subagents) shows when and how to switch models with `/model`, tune reasoning depth with `/effort`, or speed up Opus with `/fast`.

**STOP -- What you just did:** You learned that Claude Code picks a model automatically. Trust the default for this training; you will learn when and how to switch it in Module 8. Full reference: `context/models.txt`.

### 2.4 Exit Plan Mode and Execute

Press `Shift+Tab` to return to normal mode. Now tell Claude to start building -- but scope it down. You do not want all five pages at once. Ask for just the foundation:

```
Let's start building from the plan. Create the shared navigation, footer, the home page with its hero section, and the CSS design system. Don't build the other pages yet -- just the home page and shared components.
```

Constraining scope is a key prompting skill -- it keeps Claude focused and prevents runaway file creation. Let Claude create the files, then open `index.html` in your browser to check it.

**Try it now -- show Claude your site.** Open `index.html` in the browser, take a screenshot of the home page, and paste it into the Claude Code chat. On Windows use `Alt+V` to paste from clipboard, on macOS/Linux use `Ctrl+V`. You can also drag and drop a screenshot file directly into the chat. Tell Claude something like: "Here's what the home page looks like -- what do you think?" Claude can see the image and give you feedback on layout, colors, spacing, or anything that looks off. This is one of the most useful tricks for visual work -- showing is faster than describing.

**STOP -- What you just did:** You went from plan mode to normal mode and gave Claude a focused, scoped instruction. Notice that you told Claude what to build *and* what NOT to build yet ("Do NOT build the other pages yet"). Constraining scope is a key prompting skill -- it keeps Claude focused and prevents runaway file creation. You also learned that you can share screenshots with Claude -- paste or drag them right into the chat so Claude can see what you see.

**Quick check before continuing:**
- [ ] Your site plan covers all 5 pages (home, about, projects, blog, contact)
- [ ] Claude created the shared nav, footer, home page, and CSS design system
- [ ] You opened `index.html` in your browser and it renders correctly
- [ ] You are back in normal mode (check the mode indicator)

### 2.5 Create a Feature Branch

**New to branches?** A Git branch is a parallel copy of your code where you can experiment safely. If the experiment works, you merge it back to main. If it fails, you delete the branch and main is untouched. The command below creates a new branch called `feature/core-pages` and switches you to it — you can see which branch you are on anytime with `! git branch`.

**Why this step:** Feature branches keep your experiments separate from working code. If something goes wrong, you can throw away the branch without affecting main. This is also how real teams work -- every feature gets its own branch.

```
! git checkout -b feature/core-pages
```

### 2.6 Build the About Page

Ask Claude to build your About page. Describe what sections you want -- a bio, your skills, your experience or education timeline. Tell Claude about yourself (or use placeholder content for now). Something like:

```
Create the about page with my bio, a skills section grouped by category, and a timeline of my experience. Use the shared nav and footer and the CSS design system we already have.
```

If the result does not match what you imagined, tell Claude what to change. This is a conversation, not a one-shot.

### 2.7 Build the Projects Page

Now ask Claude for the projects page. Describe the layout you want -- a card grid with your projects (or placeholders). Tell Claude how you want the cards to look and how many columns at different screen sizes:

```
Build a projects page with a responsive card grid. Each card should have a title, description, technology tags, and a link. Make it responsive -- one column on mobile, more on larger screens.
```

Open each page in your browser. Test the navigation links between pages.

**STOP -- What you just did:** You gave Claude two separate, focused prompts to build two pages. Notice the pattern: each prompt specified the page structure, the content sections, and the CSS approach. The more specific your prompt, the closer the result matches what you want. You also tested in the browser after each page -- always verify Claude's output visually.

### 2.8 Write and Run Tests

**Why this step:** Even static sites can have automated tests. Claude can write a validation script that checks for broken internal links, missing files, valid HTML structure, and consistent navigation -- catching issues that are easy to miss by eye. This is the same build-test-fix cycle you would use on any project.

Ask Claude to write a test script for your site. Try a prompt like this:

```
Write a test script that validates my site. Check that all internal links point to existing files, every page has a title tag and meta description, the navigation is consistent across all pages, and images have alt text. Then run it.
```

Watch Claude write the script, run it, and fix any failures. You do not need a fancy test framework -- a simple script that exits with an error if something is wrong is all you need.

**STOP -- What you just did:** You just experienced the build-test-fix loop that will be your primary workflow for the rest of this project. Claude wrote tests, ran them, saw failures, fixed the code, and re-ran until everything passed. This tight feedback loop is why Claude Code is so effective -- Claude gets concrete error messages and fixes them immediately, rather than guessing. And yes, even a static HTML site benefits from automated checks.

### 2.9 Manual Testing

Test your site by opening each page in the browser. Click through the navigation, resize the window to check responsiveness, and look for anything that seems off. If you find issues -- broken links, layout problems, pages that look wrong on mobile -- tell Claude what you see and ask it to fix them.

### 2.10 Commit and Merge

**Why this step:** Committing through Claude Code (using `!` prefix for shell commands) keeps everything in one place. You do not need to switch terminals. The merge back to main means your feature branch work is now part of your stable codebase.

**If something goes wrong:** The most common issue on a first merge is a *conflict* — when Git cannot figure out how to combine changes. For this module, `main` has not moved since you branched, so conflicts are not expected. If you do see a conflict message, do not panic — ask Claude: "I got a merge conflict. Can you help me resolve it?" and Claude will walk you through it.

```
! git status                # inspect what's about to be staged
! git add <files or dirs you want to commit>   # name them explicitly
! git commit -m "feat: home, about, and projects pages with CSS design system"
! git checkout main
! git merge feature/core-pages
```

**Heads up:** `git add -A` is tempting, but it will stage `.env` files, IDE configs, and build artifacts you may not have meant to commit. Run `git status` first, then `git add` the specific paths you actually want. The first time someone commits a `.env` is a very bad day.

### 2.11 Branching & Quick Plans

Two workflow tricks to try now:

**`/branch`** — makes a copy of your current conversation so you can explore a tangent without losing your main thread. Useful when you want to try something risky without burning your main session.

**`/plan <description>`** — enters plan mode and immediately starts planning on the topic you describe. Example: `/plan add a contact form to the homepage`. Faster than pressing `Shift+Tab` then typing a prompt.

<details>
<summary><strong>Advanced settings you can ignore for now</strong></summary>

- **Session naming from plans.** When you accept a plan, your session is automatically named from the plan content, making `/resume` more useful.
- **Git instruction control.** The `includeGitInstructions` setting (or `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` env var) lets you remove Claude's built-in commit workflow from the system prompt if your CLAUDE.md already has custom git rules.
- **Edit without Read.** The Edit tool now works on files you have viewed via Bash (`sed -n` or `cat`), without requiring a separate `Read` call first — fewer permission prompts when you are already looking at file content.

</details>

> **STOP** -- Try `/plan add a contact form to the homepage` to test the quick-plan workflow.

### Heads Up — What's Coming in Module 3

Module 3 introduces **rule files** — small Markdown files in `.claude/rules/` that tell Claude how to write code for different parts of your project. You will see files that start with `---` marks at the top, followed by lines like `name: react` or `paths: ["*.py"]`.

That opening block is called **frontmatter** — metadata about the file, written in a format called **YAML**. Think of it like a form at the top of the document telling Claude Code how to use the file. One-sentence version: frontmatter lines are the file's settings, the body is its content. You will see much more of this starting in Module 3 and throughout skills, hooks, and agents.

If either term is still fuzzy, the [glossary](../../../GLOSSARY.md) has plain-English definitions.

### Checkpoint

You just went from a blank page to a working website. Plan mode helped you think before building, and now you have real pages to show for it.

- [ ] Tried `/branch` and `/plan <description>` quick workflow
- [ ] You used plan mode to design the architecture before writing code
- [ ] CSS design system exists with custom properties for colors, fonts, spacing
- [ ] Home page has a hero section, intro, and navigation
- [ ] About page has bio, skills, and timeline sections
- [ ] Projects page has a responsive card grid
- [ ] Navigation works between all pages
- [ ] Layout is responsive (mobile, tablet, desktop)
- [ ] Automated test script passes (links, titles, nav consistency)
- [ ] Changes are committed and merged to main
