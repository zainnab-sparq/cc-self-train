# Changelog

## v2.7.16 (2026-03-05)

- Add account-aware usage tracking step to Module 3 (all 4 projects) — teaches `/stats` for subscribers, `/cost` for API key users
- Update STOP blocks in Nexus/Sentinel Module 3 to reference three context management tools
- Add `/cost` to `context/interactive-mode.txt` command reference
- Update Module 10 final checklists and tips to include `/stats` or `/cost`
- Update all 4 READMEs with `/stats, /cost` in Module 3 feature lists

## v2.7.15 (2026-03-05)

- Expand /compact teaching with auto-compact explanation (~95% trigger, what gets preserved vs lost, CLAUDE.md survival insight)
- Add "When Claude Forgets" troubleshooting section to all 4 projects' Module 3
- Add context consumption tips to /context sections (what costs context, line-range reading tip)
- Fix Sentinel Module 3 memory hierarchy order (was incorrectly listing user memory before project memory)

## v2.7.14 (2026-03-05)

- Add automated test step (2.8) to Canvas Module 2 — validation script checks broken links, titles, nav consistency, alt text
- Update effort level documentation across all 4 Module 2 files — available for Opus and Sonnet, medium default, arrow key controls
- Rewrite effort levels section in context/models.txt
- Add formatting rule to CLAUDE.md — no blockquote formatting for student-facing content
- Add CC version mismatch warning to Step 6.8 in SKILL.md
- Remove outdated git pull tip from Module 1 recap
- Split Step 6.7 paragraph for readability

## v2.7.13 (2026-03-05)

- Fix blockquote formatting in verbatim messages — `>` prefix renders as dim italics in the CLI, replaced with plain text output

## v2.7.12 (2026-03-05)

- Convert all key teaching messages in SKILL.md to verbatim output — prevents Claude from truncating or rewording carefully crafted content
- Add "this is your space" welcome message — encourages students to ask questions, experiment, and go off-script anytime

## v2.7.11 (2026-03-05)

- Add screenshot lesson to Module 2 — students paste their homepage into Claude Code for visual feedback
- Add correct OS-specific image paste shortcuts (Alt+V on Windows, Ctrl+V on macOS/Linux)
- Add "normal mode vs plan mode" framing to all 4 Module 2 variants with bolded key behavior
- Add universal pacing rule to CLAUDE.md — one step per message, stop and wait for all modules
- Explain ~ path in Step 6.3 with OS-specific examples so beginners understand the location
- Introduce edit-check-commit loop in Step 6.5 when students first complete the cycle
- Add context to Step 6.7 explaining why CLAUDE.md preferences shape Claude's behavior
- List tracked files after first commit so beginners see exactly what's in their save point

## v2.7.10 (2026-03-05)

- Fix Windows file-open command — replace `start` (CMD built-in) with `powershell.exe -Command "Start-Process"` which works from bash

## v2.7.9 (2026-03-05)

- Remove blocking checkpoint (Step 0.6) from onboarding — curriculum sync runs fully in the background and finishes well before Module 2
- Add non-blocking status check at Module 1 completion (Step 6.8) for an informational update on sync progress
- Tell users at spawn time that the agent will finish on its own — no need to wait or watch

## v2.7.8 (2026-03-05)

- Fix checkpoint timing — ensure curriculum sync agent finishes before Module 1 starts by using blocking TaskOutput
- Add checkpoint reminder at end of Step 4 so Claude doesn't skip Step 0.6
- Fix "in another tab" wording to "in the background"

## v2.7.7 (2026-03-05)

- Fix agent viewing guidance timing — defer ↓/Esc/Ctrl+F instructions from spawn (Step 0.1) to checkpoint (Step 0.6), only shown when the agent is still running and there's something to watch

## v2.7.6 (2026-03-05)

- Add agent viewing guidance to background curriculum sync — teach users to press ↓ to watch the background agent work in real time, Esc to return, and Ctrl+F twice to kill it
- Make checkpoint wait (Step 0.6) interactive — encourage users to explore the agent manager instead of passively waiting

## v2.7.5 (2026-03-05)

- Run curriculum sync as a background agent — Steps 0.2–0.5 now execute in a background agent instead of blocking onboarding, so users start making choices immediately while the update runs
- Add checkpoint (Step 0.6) before project scaffolding to guarantee sync completion before Module 1 delivery
- Early teaching moment: users see a real background agent in action before Module 8 covers them formally

## v2.7.4 (2026-03-05)

- Add suggested next actions to onboarding step endings — each pause point in `/start` now ends with a bold suggested response (e.g., "let's go", "looks good", "ready") so beginners aren't left at a blank prompt

## v2.7.3 (2026-03-05)

- Add environment variable troubleshooting entry to `context/ide-integration.txt` — covers VS Code/Cursor not inheriting shell env vars (model config, Bedrock/Vertex provider setup)

## v2.7.2 (2026-03-05)

- Add model selection guidance to Module 2 curriculum (new Step 2.3b in all 4 projects)
- New `context/models.txt` reference doc covering model tiers, `/model`, `/fast`, effort levels, and prompting strategies
- Domain-specific model examples: Canvas (design system), Forge (storage format), Nexus (API gateway), Sentinel (analysis algorithm)

## v2.7.1 (2026-03-05)

- Improve `/release` skill — auto-commits pending changes and runs end-to-end without confirmations
- Add sparq GitHub Release step to release checklist (MEMORY.md + skill)

## v2.7.0 (2026-03-05)

- Add `/release` skill — interactive guided release checklist (version bump, tag, GitHub Release, sparq sync)
- Add release checklist to MEMORY.md for persistent cross-session reference
- Update README badge from v2.5.0 to v2.7.0

## v2.0.0

- Major content update: sync curriculum to Claude Code v2.1.43–v2.1.68 (26 releases)
- New context file: `context/auto-memory.txt` covering the auto-memory system
- Updated 8 context reference docs with new hook events (WorktreeCreate, WorktreeRemove, ConfigChange), HTTP hooks, auto-memory, new commands (/simplify, /batch, /copy, /memory), agent frontmatter (isolation: worktree, background: true), plugin settings.json, and model changes
- Updated 16 module files across all 4 projects (Modules 1, 5, 8, 10) with new CC features matched to teaching personas
- Added community cross-reference (affaan-m/everything-claude-code) to CLAUDE.md

## v1.2.0

- Add self-updating curriculum sync (Step 0 in `/start`) — detects when Claude Code has shipped new features since the curriculum was last synced, researches them, and updates context files + module guides across all 4 projects before onboarding begins
- Graceful offline fallback — curriculum sync skips silently if GitHub is unreachable
- Block GitHub fetch URLs in smoke test so curriculum sync doesn't interfere with headless testing

## v1.1.0

- Auto-detect package manager and batch-install missing tools in `/start` Step 4 (supports pip, npm, brew, apt, conda, Docker)
- Add git config check before first commit to prevent cryptic errors for new git users
- Add `/start` resume capability via `.claude/onboarding-state.json` for interrupted sessions
- Add "next module" prompt to all module deliveries, not just Module 1
- Replace full context file listing in CLAUDE.md with dynamic `ls context/` discovery
- Normalize CC features lines across all 4 projects for consistency
- Add gitignored test suite (479 tests) for repo validation

## v1.0.1

- Fixed `/start` skill error on macOS caused by backticks in SKILL.md triggering bash permission hook failures
- Added `.gitattributes` to enforce LF line endings on scripts for cross-platform compatibility
- Added MIT license, disclaimers, and legal notices

## v1.0.0

- Product launch
