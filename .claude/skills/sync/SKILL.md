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

3. Triage each entry. **Skip**: bug fixes, IDE-specific changes, platform-specific tweaks, performance improvements, cosmetic changes. **Keep** and classify:
   - **Added** — new features, new tools, new commands, new hook events, new APIs
   - **Changed** — renamed commands, changed defaults, altered behavior, updated syntax
   - **Removed** — deprecated features, removed commands, deleted options

4. Map each relevant entry to the affected module and context file:

   | Feature Category | Module | Context File(s) |
   |---|---|---|
   | CLAUDE.md, /init, memory, keyboard shortcuts | 01 | `claudemd.txt`, `interactive-mode.txt` |
   | Plan mode, git integration | 02 | `common-workflows.txt` |
   | Rules, CLAUDE.local.md, @imports, /compact | 03 | `claudemd.txt` |
   | Skills, SKILL.md, frontmatter, commands | 04 | `skillsmd.txt` |
   | Hooks (PostToolUse, Stop, SessionStart) | 05 | `hooks.txt`, `configure-hooks.txt` |
   | MCP servers, .mcp.json | 06 | `mcp.txt`, `skills-plus-mcp.txt` |
   | Guard rails, PreToolUse, hook decisions | 07 | `hooks.txt` |
   | Subagents, .claude/agents/, agent teams | 08 | `subagents.txt`, `agent-teams.txt` |
   | Tasks, TDD, dependencies | 09 | `tasks.txt` |
   | Worktrees, plugins, eval, parallel dev | 10 | `plugins.txt` |

5. If zero entries are curriculum-relevant → report "No curriculum-relevant changes found between v{local} and v{latest}." and stop.

### Step 3: Research & Present Plan

For each significant change (not just minor tweaks):

#### 3a. Research

- Use WebFetch to pull the official docs page for each feature if a URL is available (e.g., `https://code.claude.com/docs/en/<feature>`).
- If WebFetch fails or the URL is unknown, use WebSearch for official docs or usage guides.
- If both fail, rely on the CHANGELOG entry text alone — note in the plan that research was limited for that item.
- Read the affected context files (`context/*.txt`) to understand current coverage depth and format.
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
