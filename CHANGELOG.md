# Changelog

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
