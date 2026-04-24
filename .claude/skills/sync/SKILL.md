---
name: sync
description: "Maintainer tool: audit curriculum against latest CC release, present update plan for approval, then execute. Does NOT commit."
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, WebSearch, WebFetch, Agent
---

# Curriculum Sync

You are a maintainer tool that updates the cc-self-train curriculum to match the latest Claude Code release. This is a **two-phase** process: Phase 1 audits and presents a plan for approval, Phase 2 executes after the maintainer approves.

**Never modify existing steps in module files. Never commit changes — the maintainer reviews with `git diff` first.**

---

## Pipeline Overview

The paper (Section 9) describes this as a six-phase pipeline: **detect → fetch & triage → map → research → update → verify**. Those phases map to the numbered steps below as follows:

| Paper phase | Skill step(s) |
|---|---|
| Detect version gap | Step 1 |
| Fetch & triage changelog (with internal mapping) | Step 2 |
| Map to modules/context files | Step 2 (second half) + Step 2.5 verification + Step 2.6 health check |
| Research features | Step 3 |
| Update files | Step 4 (context) + Step 5 (module steps) |
| Verify integrity | Step 6 |

Step 7 is a post-run summary report, not part of the pipeline itself. Steps 2.5 and 2.6 are verification add-ons guarding the triage output; they refine phase 3 rather than introduce new phases.

---

## Phase 1: Audit & Plan (Steps 1-3)

Phase 1 researches changes and presents a structured update plan. It **stops for maintainer approval** before making any file changes.

### Step 1: Detect Version Gap

1. Read the first version number from `context/changelog-cc.txt` (the first line that is just a version number, e.g., `2.1.68`). This is the **local version** (what the curriculum currently covers).
2. Fetch the latest Claude Code version from GitHub:
   ```bash
   curl -sf https://api.github.com/repos/anthropics/claude-code/releases/latest | grep -o '"tag_name"[^"]*"[^"]*"' | head -1 | grep -o '[0-9][0-9.]*'
   ```
3. If the fetch fails → report "Could not fetch latest CC version. Check your network connection." and stop.
4. If the versions match → report "Curriculum is up to date with CC v{version}." and stop.
5. If the versions differ → continue to Step 2. Tell the maintainer: "Curriculum covers v{local}, latest is v{latest}. Analyzing changelog..."

### Step 2: Fetch & Triage Changelog

1. Fetch the changelog. Try sources in order:
   - **Primary**: WebFetch `https://code.claude.com/docs/en/changelog`
   - **Fallback 1**: WebFetch `https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md`
   - **Fallback 2**: Report "Could not fetch changelog from any source." and stop.

2. Extract all entries between v{latest} and v{local}.

3. Triage each entry. Classify into **skip** or **keep** using these criteria:

   **SKIP (do not include in plan):**
   - Pure bug fixes that don't change documented behavior (e.g., "Fixed crash when...")
   - Performance improvements with no user-visible behavior change (e.g., "Reduced memory by...")
   - Cosmetic/UI polish (e.g., "Improved color rendering in tmux")
   - Security patches that don't introduce new settings or features

   **KEEP (always include):**
   - New slash commands, CLI flags, or settings — even small ones like `/color` or `-n`
   - New or renamed frontmatter fields for skills, agents, or hooks
   - New hook events, hook fields, or hook behavior changes
   - New environment variables that users would set
   - Voice mode feature additions (language support, keybindings)
   - Remote Control / IDE integration features that affect workflows
   - Model changes (new defaults, effort level changes, output token limits)
   - Renamed or deprecated commands (e.g., `/fork` → `/branch`, `/output-style` deprecated)
   - New bundled skills that ship with CC
   - Sandbox/permission setting additions
   - Breaking changes (even if they seem minor)
   - Status line / statusline script changes

   **GRAY AREA — keep if it changes documented behavior:**
   - VS Code-specific features: SKIP pure VS Code UI fixes, KEEP features that also work in CLI or represent major workflow additions (e.g., Remote Control bridge)
   - Platform-specific: SKIP platform build fixes, KEEP feature additions available to that platform's users (e.g., voice mode on WSL)

   For items you keep, classify as:
   - **Added** — new features, new tools, new commands, new hook events, new APIs
   - **Changed** — renamed commands, changed defaults, altered behavior, updated syntax
   - **Removed** — deprecated features, removed commands, deleted options

4. Map each relevant entry to the affected module and context file:

   | Feature Category | Module | Context File(s) |
   |---|---|---|
   | CLAUDE.md, /init, /memory, memory timestamps | 01 | `claudemd.txt`, `auto-memory.txt` |
   | Keyboard shortcuts, input modes, /color, session naming | 01 | `interactive-mode.txt` |
   | Plan mode, git integration, /branch (was /fork) | 02 | `common-workflows.txt` |
   | Rules, CLAUDE.local.md, @imports, /compact | 03 | `claudemd.txt` |
   | Skills, SKILL.md, frontmatter fields, bundled skills | 04 | `skillsmd.txt` |
   | Hooks: PostToolUse, Stop, SessionStart, new events | 05 | `hooks.txt`, `configure-hooks.txt` |
   | MCP servers, .mcp.json, elicitation, channels | 06 | `mcp.txt`, `skills-plus-mcp.txt` |
   | Guard rails, PreToolUse, sandbox settings, permissions | 07 | `hooks.txt` |
   | Subagents, .claude/agents/, agent teams, SendMessage | 08 | `subagents.txt`, `agent-teams.txt` |
   | Tasks, TDD, /loop, cron scheduling | 09 | `tasks.txt` |
   | Worktrees, plugins, eval, parallel dev | 10 | `plugins.txt` |
   | IDE integration, Remote Control, VS Code features | 10 | `ide-integration.txt` |
   | Models, effort levels, /effort, modelOverrides | 01 | `models.txt` |
   | Voice mode, push-to-talk, language support | 01 | `interactive-mode.txt` |
   | Status line, statusline scripts, rate_limits field | 01 | `sl-guide.txt` |
   | System prompt, includeGitInstructions | 02/03 | `prompt.txt` |
   | Feature selection guidance | (all) | `when-to-use-features.txt` |

5. If zero entries are curriculum-relevant → report "No curriculum-relevant changes found between v{local} and v{latest}." and stop.

### Step 2.5: Second-Pass Verification

Re-read the full changelog one more time. For each entry you marked as "skip", ask: "Would a CC learner benefit from knowing this changed?" If yes, move it to "keep". Common second-pass catches:
- Items with "Added" that look minor but introduce new user-facing commands
- Items with "Changed" that rename or deprecate something already in the curriculum
- IDE features that represent genuinely new capabilities (not just fixes)
- Entries that mention new env vars, settings, or frontmatter fields

### Step 2.6: Module Health Check

Before presenting the plan, assess curriculum balance:

1. Count the number of steps in each module (across any one project variant, e.g., Canvas) by counting `### X.N` headings before the Checkpoint.
2. Flag any module where:
   - **Bloat risk**: The module has 2x+ the steps of the smallest module (e.g., Module 5 has 14 steps but Module 3 has 6)
   - **This sync would add 3+ steps to a single module** — consider whether the feature could reasonably split across two modules instead
3. If flagged, include a **Health Warning** in the Phase 1 plan output:
   ```
   ⚠️ Module Health Warning:
   - Module 5 (Hooks) has 14 steps — 2.3x the size of Module 3 (6 steps)
   - This sync would add 2 more steps to Module 5
   - Consider: Could any of these features live in Module 7 (Guard Rails) instead?
   ```
4. The maintainer decides — the sync skill flags but does not auto-rebalance.

### Step 3: Research & Present Plan

For each significant change (not just minor tweaks):

#### 3a. Research

- For each kept changelog entry, use the Agent tool with `subagent_type: "claude-code-guide"` to research the feature. Prompt the agent with the changelog entry text and ask it to explain the feature's purpose, syntax, configuration, and any gotchas. Example prompt: "Explain the Claude Code feature: [changelog entry]. Include syntax, configuration options, and common pitfalls."
- If the agent returns insufficient detail, fall back to WebSearch for official docs or usage guides.
- If both fail, rely on the CHANGELOG entry text alone — note in the plan that research was limited for that item.
- Read the affected context files (`context/*.txt`) to understand current coverage depth and format.
- **Cross-reference all context files**: Run `ls context/` and read the first 5-10 lines of every context file. For each changelog entry, check if ANY context file (not just the ones in the mapping table) already documents related functionality. If so, that context file needs updating too. This catches features that span multiple areas.
- Read the affected module files to understand existing step structure and numbering.

#### 3b. Build the update plan

Compile a structured plan with these sections:

**Context files to update:**

| File | Action | Summary |
|------|--------|---------|
| `context/changelog-cc.txt` | Prepend | Add v{X} through v{Y} entries |
| `context/{file}.txt` | Update/Create | {what to add/change/remove} |

**Module steps to append:**

| Module | Step # | Title | Persona | Content outline |
|--------|--------|-------|---------|-----------------|
| {NN} | {X.N} | {title} | {Guide/Collaborator/Peer/Launcher} | {1-2 sentence outline} |

**New context files to create** (if a wholly new feature area):

| File | Purpose |
|------|---------|
| `context/{name}.txt` | {what it covers} |

**Completeness check before presenting plan:**
- [ ] Every `context/*.txt` file was considered — not just the ones in the mapping table
- [ ] All new slash commands are accounted for
- [ ] All new CLI flags are accounted for
- [ ] All new/changed frontmatter fields are accounted for
- [ ] All new hook events are accounted for
- [ ] All new environment variables are accounted for
- [ ] All renamed/deprecated features are accounted for
- [ ] All new settings (user, project, managed) are accounted for
- [ ] Voice mode changes are accounted for
- [ ] Remote Control / IDE changes are accounted for
- [ ] Model/effort changes are accounted for
- [ ] Bundled skill additions are accounted for

#### 3c. Present plan and STOP

Present the plan tables above. Then print:

```
---
Phase 1 complete. Review the plan above.
- "proceed" — execute all changes
- "skip X" — remove item X from the plan
- "also add Y" — add something to the plan
- "abort" — cancel sync
---
```

**STOP HERE. Do not proceed to Phase 2 until the maintainer responds.**

---

## Phase 2: Execute (Steps 4-7)

Phase 2 runs only after the maintainer approves the plan from Phase 1. Apply changes exactly as planned (with any modifications the maintainer requested).

### Step 4: Update Context Files

1. **Update `context/changelog-cc.txt`** — prepend new entries in the same format (version header + bullet list). Keep existing entries intact.

2. **Update affected `context/*.txt` files** — read the file first, then apply the right action:
   - **Added**: Add documentation for the new feature alongside existing content. Match format and depth.
   - **Changed**: Find the existing documentation and update it to reflect the new behavior, syntax, or defaults. Remove outdated information.
   - **Removed**: Delete documentation for the removed feature.

3. **Create new context files** if the plan calls for them. Match the format of existing context files.

### Step 5: Append Module Steps (All 5 Projects)

For each new feature that maps to a module, update all 5 project variants (`projects/canvas/modules/`, `projects/forge/modules/`, `projects/nexus/modules/`, `projects/sentinel/modules/`, `projects/byop/modules/`). **Never modify or renumber existing steps.** For each file:

1. Read the file to understand its structure, existing steps, and the project's domain context.

2. Find the Checkpoint section at the bottom. The heading varies by project:
   - Canvas: `### Checkpoint`
   - Forge: `## Checkpoint`
   - Nexus: `### Checkpoint`
   - Sentinel: `### Checkpoint`
   - BYOP: `### Checkpoint`

3. Determine the next sequential step number by reading the last step before Checkpoint.

4. Insert a new step **immediately before** the Checkpoint heading. All projects use `### X.N Title` format (e.g., `### 5.8 Explore Hook Variables`).

5. Match the module's teaching persona. Module files use the **intermediate row** from CLAUDE.md's adaptive persona table:
   - **Modules 1-3 (Guide)**: Explain the concept before the exercise. Define terms. Be encouraging.
   - **Modules 4-6 (Collaborator)**: Brief context, then point the user to try it. Ask questions.
   - **Modules 7-9 (Peer)**: Terse, direct. Point to docs, let them figure it out.
   - **Module 10 (Launcher)**: State the goal, step back.

6. Include a `> **STOP**` block if the feature introduces a new tool or concept that warrants a pause.

7. Add a checkbox to the Checkpoint list for the new feature.

8. For **Changed** features: do NOT modify existing steps. Append a brief note step before Checkpoint mentioning the updated behavior.

9. For **Removed** features: append a note step before Checkpoint explaining the removal and the recommended alternative. Do NOT delete existing steps.

10. **Regenerate module header blocks.** After all per-project edits are complete, run the shared header generator once:

    ```bash
    node "$CLAUDE_PROJECT_DIR/.claude/scripts/render-module-headers.js"
    ```

    The generator rewrites the block between `<!-- progress:start -->` and `<!-- progress:end -->` markers in every module file from `config/curriculum.json`. If the sync added or split a module, update `config/curriculum.json` first (total_modules, estimated_time for the new entry) so the regenerated bars reflect the new count.

    Expected output on an already-correct run: `{"unchanged": 50}`. Any `"updated"` count is fine if you changed `config/curriculum.json`. An `"error"` or `"skipped"` count means a module file is missing the progress markers — investigate before continuing.

### Handling Foundational Features

Most new CC features fit cleanly into the existing 10-module structure. Occasionally, a feature is so foundational that appending it to an existing module would be misleading — it deserves more prominence than "Step 5.14" buried at the bottom of a module.

**Signs a feature might be foundational:**
- It changes how ALL modules work (e.g., a new permission model, a new project config format)
- It's a prerequisite for understanding features in later modules
- Students who skip it would be confused by content in 3+ other modules
- It's comparable in scope to an existing module topic (e.g., hooks, skills, MCP)

**When this happens, do NOT force it into an existing module.** Instead:
1. Flag it in the Phase 1 plan as a **"Foundational Feature Alert"**
2. Recommend one of these options to the maintainer:
   - **Option A: Promote to early module.** Add a substantial new section (not just a step) to Module 1, 2, or 3 where foundational concepts are taught. This is appropriate when the feature is simple but universal.
   - **Option B: Split an existing module.** If a module has grown to 12+ steps, propose splitting it into two modules (e.g., Module 5a and 5b). This requires renumbering all subsequent modules across all 5 projects — flag the scope clearly.
   - **Option C: Create Module 11.** As a last resort for a wholly new feature area that doesn't overlap with any existing module. Requires updating CLAUDE.md, README.md, the feature matrix, all 5 project READMEs, and tests.
3. The maintainer decides. The sync skill does NOT auto-create new modules.

### Step 6: Self-Verification

After all file updates, verify every modified file.

#### Context files

- Re-read each modified context file.
- Check: no duplicated section headers, no empty sections, no truncated content (file should not end mid-sentence).
- If malformed → revert with `git checkout -- context/<filename>` and note the revert.

#### Module files

- Re-read each modified module file.
- Check ALL of the following:
  1. Step numbers are sequential with no gaps or duplicates
  2. The Checkpoint section still exists (the heading was not accidentally deleted or modified)
  3. No existing `> **STOP**` blocks were broken or removed
  4. No markdown syntax errors (unclosed code blocks, broken headings)
  5. The new step appears immediately before the Checkpoint heading, not after it or embedded inside another step
- If any check fails → revert with `git checkout -- projects/<project>/modules/<filename>` and note the revert.

Keep a list of all files that passed and all files that were reverted.

### Step 7: Sync Report & Summary

Write `.claude/sync-report.md` with the following sections:

```markdown
# Curriculum Sync Report
Synced from CC v{local} to v{latest} on {date}

## Changes Approved
- {brief list of what the maintainer approved from the Phase 1 plan}

## Context Files Updated
- `context/changelog-cc.txt` — added v{latest} entries
- `context/{file}.txt` — {one-line summary of change}

## Module Steps Appended
- Module {N} ({title}): appended step {X.N} "{step title}" across all 5 projects
  - Feature: {brief description}

## Reverted Files (failed verification)
- `projects/{project}/modules/{file}` — {reason for revert}

## Not Updated (no relevant changes)
- Module {N} — no changes needed
```

If no files were reverted, omit the "Reverted Files" section.

Then print a summary:
- "Updated X context files and Y module files. See `.claude/sync-report.md` for details."
- "Review changes with `git diff`, then commit manually when satisfied."
- Do NOT run `git add` or `git commit`. The maintainer reviews and commits.
