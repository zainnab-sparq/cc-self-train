# Module 2 -- Blueprint and Build

**CC features:** Plan mode, model selection, git integration, basic prompting

**Persona -- Guide:** Explain everything, define terms, celebrate small wins. "Let's try...", "Here's what that does..."

### 2.1 Enter Plan Mode

**Why this step:** Plan mode is one of Claude Code's most important features. It lets you think through architecture *with* Claude before any code gets written. This prevents the "just start coding" trap that leads to messy rewrites later.

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

### 2.3b Choose Your Model

**Why this step:** Claude Code is not one model -- it is three. Picking the right one for the task at hand saves time and money, and gets you better results.

Type `/model` to open the model picker. You will see three tiers:

- **Haiku** -- fastest and cheapest. Great for quick lookups, simple edits, and repetitive tasks.
- **Sonnet** -- the balanced default. Handles ~90% of everyday coding: building features, fixing bugs, writing tests.
- **Opus** -- deepest reasoning. Use it for architecture decisions, complex refactors, and security reviews.

You will also see an **effort level** bar at the bottom of the picker (low / medium / high) when Opus or Sonnet is selected. Use the `<-` `->` arrow keys to adjust it. Higher effort means deeper reasoning but slower responses. Medium is the default and works for most tasks. Try low for simple edits, high for complex design decisions.

You just spent time in plan mode designing your site architecture. That kind of open-ended design thinking is where Opus shines -- deeper reasoning means better tradeoff analysis. Now that you are about to switch to execution mode and build pages, Sonnet is the right choice -- the instructions are clear and scoped.

**Other useful commands:**

- `Alt+P` (or `Option+P` on Mac) -- switch models without clearing your prompt
- `/fast` -- toggle fast mode for quicker responses (same model, optimized output)

**STOP -- What you just did:** You learned that Claude Code is not one-size-fits-all. Planning benefits from Opus's deeper reasoning. Mechanical code generation can use Sonnet. Quick lookups can use Haiku. Matching the model to the task is a habit that saves time and money. Use Opus for design system architecture, Sonnet for building pages. See `context/models.txt` for the full reference.

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

```
! git add -A
! git commit -m "feat: home, about, and projects pages with CSS design system"
! git checkout main
! git merge feature/core-pages
```

### 2.11 Branching & Quick Plans

Two workflow commands have been updated recently:

**`/branch` (was `/fork`).** The command to branch your conversation into a new session has been renamed from `/fork` to `/branch` (v2.1.77). The old name still works as an alias, but `/branch` is now the canonical command.

**`/plan` with a description.** You can now pass a description directly: `/plan fix the auth bug`. This enters plan mode and immediately starts planning -- no extra prompt needed (v2.1.72).

**Session naming from plans.** When you accept a plan, your session is automatically named based on the plan content (v2.1.77). This makes `/resume` more useful since sessions have meaningful names.

**Git instruction control.** The `includeGitInstructions` setting (or `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` env var) lets you remove Claude's built-in commit and PR workflow instructions from the system prompt. Useful if your CLAUDE.md already has custom git rules (v2.1.69).

**Edit without Read.** The Edit tool now works on files you've viewed via Bash (using `sed -n` or `cat`), without requiring a separate `Read` call first. This means fewer permission prompts when you're already looking at file content (v2.1.89).

> **STOP** -- Try `/plan add a contact form to the homepage` to test the quick-plan workflow.

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
