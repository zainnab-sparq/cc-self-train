# Adaptive Persona System — Audit

## Verdict (updated after PR #3)

**Partially works — streak-transition visibility is now closed; module-boundary enforcement still isn't.**

Update: PR #3 added a `pendingBanners` queue to `learner-profile.json` that `observe-interaction.js` writes to on streak transitions and `learner-context.js` drains on SessionStart. The banner emits a learner-facing one-liner (`SHOW TO LEARNER`) distinct from the existing Claude-facing narrative, and is marked acknowledged once shown so it only fires once. This closes the "no learner-visible signal" gap for streak events. Plus new skills `/stuck` and `/experience` let learners act on what they see. Module-boundary enforcement (the 3.8/2.0 threshold algorithm in CLAUDE.md) is still prose-only and deferred.

## Verdict (original)

**Partially works — the core loop is real, the last mile isn't enforced.**

The three hook scripts (`observe-interaction.js`, `learner-streak-check.js`, `learner-context.js`) fire on the documented events, correctly classify interactions, maintain `learner-profile.json`, and emit streak alerts and engagement narratives. This was verified empirically by `tests/test_adaptive_system.py` (12 tests, all passing — see [Verification](#verification) below).

What *isn't* enforced by code is the step that converts observation into adaptation. CLAUDE.md lines 100-118 describe an algorithm — read `moduleAverageQuality` and the ratio of productive-to-unproductive interactions at each module boundary, then adjust `Effective Level` in CLAUDE.local.md up or down — but no script implements this. Claude is trusted to consult the persona table and the adjustment rules manually, and the learner has no visible signal when the persona is supposed to shift. Jordan's and Alex's reports both evaluated the system from source for exactly this reason: there is nothing observable to evaluate from outside.

Three gaps matter most:

1. **No profile initialization.** New learners have no `learner-profile.json` for the first ~5 responses. SessionStart context injection is silent until enough interactions accumulate, so the first module runs with no adaptive signal at all.
2. **No code enforces the module-boundary algorithm.** The thresholds in CLAUDE.md (lines 109-116) are documented but depend entirely on Claude noticing, reading, calculating, and updating. There is no regression test against the algorithm.
3. **`currentModule` drifts.** The profile is seeded with `currentModule: 1` and no script updates it as modules progress, so the "this module vs. all-time" distinction is structurally suspect.

## Component inventory

| File | Lines | Event | What it's supposed to do (from comments) | What it actually does | Divergence |
|---|---|---|---|---|---|
| `.claude/scripts/observe-interaction.js` | 211 | Stop hook | Classify last user message into 6 categories, track quality scores and streaks in `learner-profile.json`. Silent. Never blocks. | Reads `transcript_path` from stdin JSON, parses JSONL, runs keyword-based classifier, accumulates last 100 scores, detects streaks over last 3 non-neutral turns, writes profile. Uses `.observe-lock` for re-entrancy. | None — matches spec. |
| `.claude/scripts/learner-streak-check.js` | 69 | UserPromptSubmit | Surface streak transitions mid-session without nagging. Silent when state unchanged. | Reads profile, compares current streak to `lastAnnouncedStreak`, emits alert on transition, persists new `lastAnnouncedStreak`. Exits silently if profile missing or lock present. | None. |
| `.claude/scripts/learner-context.js` | 76 | SessionStart | Inject engagement narrative at session boot. Silent for new students. | Reads profile, computes productive/unproductive ratio, selects pattern + teaching note, appends streak alert if present, writes to stdout. Silent if total non-neutral interactions < 5. | None. |
| `.claude/settings.json` | 57 | — | Wire the three scripts to their hooks. | All three wired on matcher-less triggers. `welcome.js` and `check-updates.js` also on SessionStart with `matcher: "startup"`. | None. |
| `CLAUDE.md` §"Adaptive Learning" | 100-118 | — | Describe Effective Level, struggle/engagement streak signals, and the module-boundary adjustment algorithm (thresholds: >=3.8 quality + >60% productive → UP; <=2.0 quality + >50% unproductive → DOWN). | **Prose only.** No script executes this. Claude is expected to read, compute, and update `CLAUDE.local.md` manually on "next module." | Algorithm documented but not enforced. |
| `.claude/skills/start/SKILL.md` Step 2b | 376-389 | — | Collect experience level (First timer / Some experience / CC veteran) and store in onboarding-state + CLAUDE.local.md. | Works. Stores `experienceLevel` field. | Collected value feeds the persona table lookup, but no code forces the table lookup; that's also Claude's responsibility to consult. |

## End-to-end flow trace

### Scenario 1 — New learner runs `/start`

1. SessionStart fires all three SessionStart hooks: `welcome.js` → prints banner, `check-updates.js` → CC version + repo freshness check, `learner-context.js` → exits silently (no profile yet).
2. `/start` Step 2b writes `experienceLevel` to `.claude/onboarding-state.json` and later to `CLAUDE.local.md`.
3. **No learner-profile.json is created.** The adaptive scripts observe nothing until the first Stop hook fires.

**Verification:** `test_context_silent_when_history_too_small` (passes).

### Scenario 2 — Learner completes Module 1

1. Every response in the session triggers Stop → `observe-interaction.js` fires. First call creates `learner-profile.json` via `loadProfile()` default; subsequent calls accumulate.
2. After 5+ non-neutral interactions, the next SessionStart's `learner-context.js` emits the `LEARNER PROFILE` narrative.
3. **No module-boundary logic fires.** Claude is trusted to say "next module" and consult CLAUDE.md's persona table.

**Verification:** `test_observe_classifies_concept_question`, `test_context_injects_narrative_with_engagement_history` (both pass).

### Scenario 3 — 3 consecutive answer-seeking questions mid-module

1. Third Stop hook writes `struggleStreak: true` to the profile (`observe-interaction.js` lines 186-196).
2. Next UserPromptSubmit fires `learner-streak-check.js`, which compares against `lastAnnouncedStreak: "none"` → transition detected → stdout emits `⚠ STRUGGLE STREAK just triggered …`.
3. Claude receives the alert and is expected (per CLAUDE.md lines 117-118) to "offer more scaffolding immediately without waiting for the module boundary."

**Verification:** `test_observe_accumulates_across_runs_and_detects_struggle_streak`, `test_streak_check_emits_alert_on_struggle_transition`, `test_end_to_end_observe_then_streak_then_context` (all pass). The classification-to-alert path is verified; the "Claude actually scaffolds more" step is unverifiable without a conversation-level test.

### Scenario 4 — Learner completes Module 2 (module boundary)

1. Learner says "next module."
2. Claude is expected (per CLAUDE.md lines 103-109) to:
   - Read `learner-profile.json`.
   - Compute `moduleAverageQuality` and productive-ratio for the module.
   - Compare against thresholds: `>=3.8 and >60% productive → +1 level`, `<=2.0 and >50% unproductive → -1 level`.
   - Update `Effective Level` and `Engagement Trend` in CLAUDE.local.md.
   - Reset `moduleInteractions` and `moduleQualityScores` in the profile.
3. **No code does any of this.** There is no module-boundary hook. Claude's manual compliance with the algorithm is the enforcement mechanism.

**Verification:** None. This is the single largest gap — the cited algorithm has no runtime guarantor.

### Scenario 5 — Learner only copy-pastes, never asks concept questions

1. `observe-interaction.js` repeatedly classifies as `answer_seeking` or `passive_acceptance`, eventually sets `struggleStreak: true`.
2. `learner-streak-check.js` emits the struggle alert; `learner-context.js` on next SessionStart reports "Tends to seek direct answers. Needs more scaffolding."
3. **What actually changes for the learner?** The PERSONA TONE that Claude uses (if Claude consults the table and the alert). **Module content is unchanged** — the same STOP callouts, same checkpoints, same section depth. Jordan specifically reported this: he could not tell whether the adaptive system was doing anything, because the content he read looked identical.

**Verification:** `test_context_injects_scaffolding_note_for_struggle` (passes). The teaching note reaches Claude; the content reaching the learner remains static.

## Gap list

### Implemented and verifiable

- Interaction classification into 6 categories by keyword heuristics.
- Quality score accumulation (last 100 all-time, last 50 per module).
- Trend computation over the last 5 vs. prior 5 scores.
- Struggle/engagement streak detection over last 3 non-neutral.
- Streak-transition alerts via UserPromptSubmit hook.
- Engagement narrative injection via SessionStart hook, gated at ≥5 non-neutral interactions.
- **[PR #3]** Banner event queued in `pendingBanners` on streak transition.
- **[PR #3]** Learner-facing banner emitted from SessionStart, marked acknowledged once shown.
- **[PR #3]** Stale banners (>24h) silently acknowledged, not surfaced.
- **[PR #3]** `/stuck` skill re-explains the current step at a different tier.
- **[PR #3]** `/experience` skill updates `Experience Level` + `Effective Level` mid-course.

### Implemented but unverifiable

- **Claude actually scaffolds more after a struggle alert.** The alert reaches Claude via stdout; nothing confirms Claude changed approach.
- **Claude consults the persona table at module boundaries.** No test, no log.
- **Claude updates `Effective Level` in CLAUDE.local.md on module completion.** No commit record, no log entry, no diff to observe.

### Documented but not implemented

- **Module-boundary adjustment algorithm** (CLAUDE.md lines 103-116). No script runs it; the thresholds sit in prose.
- **Profile reset on module boundary.** `moduleInteractions` and `moduleQualityScores` are supposed to reset; nothing resets them.

### Implemented but disconnected

- `profile.currentModule` is seeded at 1 and never updated as the learner progresses. The "per-module" metrics are effectively aggregates-with-a-stale-label.
- `experienceLevel` collected in `/start` Step 2b ends up in `CLAUDE.local.md` and `onboarding-state.json`, but the adaptive scripts read `learner-profile.json` instead. The two state files don't cross-reference.

## Recommended observability additions (Stage 3 follow-ups)

These are not shipping in this PR. Listed for follow-up work gated on this audit's findings.

1. **Seed `learner-profile.json` at `/start` completion** with experience-level-derived defaults. Eliminates the silent-first-5-interactions gap.
2. **Emit a structured event to `.claude/adaptive-events.log`** every time a streak fires, the persona table is consulted, or `Effective Level` changes. Makes invisible transitions visible.
3. **Add a `module-boundary.js` script** that runs the CLAUDE.md algorithm deterministically. Wire it to a hook the `/start` skill invokes on "next module." Closes the largest gap.
4. **Update `profile.currentModule`** from CLAUDE.local.md's `Current Module` field at SessionStart. Keeps per-module metrics meaningful.
5. **Add a conversation-level test** that verifies Claude adjusts tone after a struggle alert. Exercises the "trust the model" assumption.

## Verification

This audit's empirical claims are backed by `tests/test_adaptive_system.py` (12 tests, all passing as of this commit):

```
pytest tests/test_adaptive_system.py -v
```

Every "Implemented and verifiable" item above has one or more tests. Every "Implemented but unverifiable" item is flagged as untested in the gap list above.
