---
name: sync
description: "Maintainer tool: sync curriculum with latest Claude Code release. Updates context files and appends new module steps. Does NOT commit — review with `git diff` first."
disable-model-invocation: true
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, WebSearch, WebFetch
---

# Curriculum Sync

You are a maintainer tool that updates the cc-self-train curriculum to match the latest Claude Code release. You update context files and safely append new steps to module files — never modifying existing steps.

## Step 1: Detect Version Gap

1. Read the first `## vX.Y.Z` heading from `context/changelog-cc.txt`. This is the **local version** (what the curriculum currently covers).
2. Fetch the latest Claude Code version from GitHub:
   ```bash
   curl -sf https://api.github.com/repos/anthropics/claude-code/releases/latest | grep -o '"tag_name"[^"]*"[^"]*"' | head -1 | grep -o '[0-9][0-9.]*'
   ```
3. If the fetch fails → report "Could not fetch latest CC version. Check your network connection." and stop.
4. If the versions match → report "Curriculum is up to date with CC v{version}." and stop.
5. If the versions differ → continue to Step 2. Tell the maintainer: "Curriculum covers v{local}, latest is v{latest}. Syncing now..."

## Step 2: Fetch & Triage Changelog

1. Fetch the raw CHANGELOG from GitHub:
   ```bash
   curl -sf https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
   ```
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

## Step 3: Research & Update Files

For each significant change (not just minor tweaks):

### 3a. Research

Use WebSearch for official docs, blog posts, or usage guides. Read existing context files to understand current coverage depth.

### 3b. Update context files

1. **Update `context/changelog-cc.txt`** — prepend new entries in the same format (version header + bullet list).

2. **Update affected `context/*.txt` files** — read the file first, then apply the right action:
   - **Added**: Add documentation for the new feature alongside existing content. Match format and depth.
   - **Changed**: Find the existing documentation and update it to reflect the new behavior, syntax, or defaults. Remove outdated information.
   - **Removed**: Delete documentation for the removed feature.

### 3c. Append new steps to module files (safe insertion strategy)

For each new feature that maps to a module, update all 4 project variants (`projects/canvas/modules/`, `projects/forge/modules/`, `projects/nexus/modules/`, `projects/sentinel/modules/`). **Never modify or renumber existing steps.** For each file:

1. Read the file to understand its structure, existing steps, and the project's domain context.

2. Find the Checkpoint section at the bottom. The heading varies by project:
   - Canvas: `### Checkpoint`
   - Forge: `## Checkpoint`
   - Nexus: `### Checkpoint`
   - Sentinel: `### Checkpoint`

3. Determine the next sequential step number by reading the last step before Checkpoint.

4. Insert a new step **immediately before** the Checkpoint heading. Match the project's heading style:
   - Canvas uses `### X.N Title` (e.g., `### 5.8 Explore Hook Variables`)
   - Forge uses `## X.N Title` (e.g., `## 5.8 Explore Hook Variables`)
   - Nexus uses `### Step N: Title` or `### Step Nb: Title`
   - Sentinel uses `### Step N: Title` or `### Step Nb: Title`

5. Match the module's teaching persona depth:
   - Modules 1-3 (Guide): Explain the concept before the exercise. Define terms. Be encouraging.
   - Modules 4-6 (Collaborator): Brief context, then point the user to try it. Ask questions.
   - Modules 7-9 (Peer): Terse, direct. Point to docs, let them figure it out.
   - Module 10 (Launcher): State the goal, step back.

6. Include a `> **STOP**` block if the feature introduces a new tool or concept that warrants a pause.

7. Add a checkbox to the Checkpoint list for the new feature.

8. For **Changed** features: do NOT modify existing steps. Append a brief note step before Checkpoint mentioning the updated behavior.

9. For **Removed** features: append a note step before Checkpoint explaining the removal and the recommended alternative. Do NOT delete existing steps.

## Step 4: Self-Verification

After all file updates, verify every modified file.

### Context files

- Re-read each modified context file.
- Check: no duplicated section headers, no empty sections, no truncated content (file should not end mid-sentence).
- If malformed → revert with `git checkout -- context/<filename>` and note the revert.

### Module files

- Re-read each modified module file.
- Check ALL of the following:
  1. Step numbers are sequential with no gaps or duplicates
  2. The Checkpoint section still exists (the heading was not accidentally deleted or modified)
  3. No existing `> **STOP**` blocks were broken or removed
  4. No markdown syntax errors (unclosed code blocks, broken headings)
  5. The new step appears immediately before the Checkpoint heading, not after it or embedded inside another step
- If any check fails → revert with `git checkout -- projects/<project>/modules/<filename>` and note the revert.

Keep a list of all files that passed and all files that were reverted.

## Step 5: Write Sync Report

Write `.claude/sync-report.md` with the following sections:

```markdown
# Curriculum Sync Report
Synced from CC v{local} to v{latest} on {date}

## Context Files Updated
- `context/changelog-cc.txt` — added v{latest} entries
- `context/{file}.txt` — {one-line summary of change}

## Module Steps Appended
- Module {N} ({title}): appended step {X.N} "{step title}" across all 4 projects
  - Feature: {brief description}

## Reverted Files (failed verification)
- `projects/{project}/modules/{file}` — {reason for revert}

## Not Updated (no relevant changes)
- Module {N} — no changes needed
```

If no files were reverted, omit the "Reverted Files" section.

## Step 6: Summary (do NOT commit)

Print a summary:
- "Updated X context files and Y module files. See `.claude/sync-report.md` for details."
- "Review changes with `git diff`, then commit manually when satisfied."
- Do NOT run `git add` or `git commit`. The maintainer reviews and commits.
