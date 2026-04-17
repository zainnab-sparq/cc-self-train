#!/usr/bin/env node
// Runs the module-boundary assessment algorithm from CLAUDE.md deterministically.
// Invoked by Claude when the learner says "next module", BEFORE the next module
// file is read.
//
// Algorithm (mirrors CLAUDE.md "Module Boundary Assessment" prose):
//   - Read moduleAverageQuality and moduleInteractions breakdown.
//   - If quality >= 3.8 AND productive ratio > 60%  → bump Effective Level UP
//   - If quality <= 2.0 AND unproductive ratio > 50% → bump Effective Level DOWN
//   - Otherwise                                     → keep current level
//   - Never cross the beginner / advanced bounds.
//   - Always reset moduleInteractions + moduleQualityScores and bump currentModule.
//   - If the level changed, queue a "module-boundary" banner in pendingBanners
//     so learner-context.js surfaces the shift on the next SessionStart.
//
// Emits a JSON summary on stdout describing what happened -- Claude reads this
// to know whether to mention the shift or proceed silently (banner handles the
// learner-facing message).
//
// Exits 0 on success; never blocks. If profile or CLAUDE.local.md are missing
// (e.g. mid-/start), emits {status: "skipped"} and returns.

const fs = require("fs");
const path = require("path");

const PROFILE_PATH = path.join(process.cwd(), "learner-profile.json");
const CLAUDE_LOCAL_PATH = path.join(process.cwd(), "CLAUDE.local.md");
const LEVELS = ["beginner", "intermediate", "advanced"];

function computeNewLevel(currentLevel, profile) {
  const quality = profile.moduleAverageQuality || 0;
  const ci = profile.moduleInteractions || {};
  const productive =
    (ci.concept_question || 0) +
    (ci.independent_exploration || 0) +
    (ci.debug_attempt || 0);
  const unproductive = (ci.answer_seeking || 0) + (ci.passive_acceptance || 0);
  const total = productive + unproductive;
  if (total === 0) return currentLevel; // no non-neutral data this module

  const productiveRatio = productive / total;
  const unproductiveRatio = unproductive / total;
  const idx = LEVELS.indexOf(currentLevel);
  if (idx === -1) return currentLevel;

  if (quality >= 3.8 && productiveRatio > 0.6 && idx < LEVELS.length - 1) {
    return LEVELS[idx + 1];
  }
  if (quality <= 2.0 && unproductiveRatio > 0.5 && idx > 0) {
    return LEVELS[idx - 1];
  }
  return currentLevel;
}

function readLevel(claudeLocal) {
  const effMatch = claudeLocal.match(/^Effective Level:\s*(\w+)/m);
  if (effMatch) return { level: effMatch[1].toLowerCase(), hasEffective: true };
  const expMatch = claudeLocal.match(/^Experience Level:\s*(\w+)/m);
  if (expMatch) return { level: expMatch[1].toLowerCase(), hasEffective: false };
  return null;
}

function updateEffectiveLevel(claudeLocal, newLevel) {
  if (/^Effective Level:/m.test(claudeLocal)) {
    return claudeLocal.replace(
      /^Effective Level:\s*\w+/m,
      `Effective Level: ${newLevel}`,
    );
  }
  // No Effective Level line -- leave the file alone. The caller decides whether
  // to add one; this script only overwrites what's already there to avoid
  // surprising edits in a file the student owns.
  return claudeLocal;
}

function main() {
  if (!fs.existsSync(PROFILE_PATH) || !fs.existsSync(CLAUDE_LOCAL_PATH)) {
    console.log(
      JSON.stringify({
        status: "skipped",
        reason: "profile or CLAUDE.local.md missing",
      }),
    );
    process.exit(0);
  }

  let profile;
  let claudeLocal;
  try {
    profile = JSON.parse(fs.readFileSync(PROFILE_PATH, "utf-8"));
    claudeLocal = fs.readFileSync(CLAUDE_LOCAL_PATH, "utf-8");
  } catch (err) {
    console.log(JSON.stringify({ status: "error", reason: String(err) }));
    process.exit(0);
  }

  const levelInfo = readLevel(claudeLocal);
  if (!levelInfo) {
    console.log(
      JSON.stringify({
        status: "skipped",
        reason: "no Effective/Experience Level in CLAUDE.local.md",
      }),
    );
    process.exit(0);
  }

  const oldLevel = levelInfo.level;
  const newLevel = computeNewLevel(oldLevel, profile);
  const module = profile.currentModule || 1;
  const levelChanged = newLevel !== oldLevel;

  // Preserve the quality score BEFORE reset -- we report it in the summary so
  // Claude knows what the boundary saw.
  const moduleQuality = profile.moduleAverageQuality || 0;

  // Reset per-module state regardless of whether level changed.
  profile.moduleInteractions = {
    concept_question: 0,
    independent_exploration: 0,
    debug_attempt: 0,
    answer_seeking: 0,
    passive_acceptance: 0,
    neutral: 0,
  };
  profile.moduleQualityScores = [];
  profile.moduleAverageQuality = 0;
  profile.currentModule = module + 1;

  if (levelChanged) {
    profile.pendingBanners = profile.pendingBanners || [];
    profile.pendingBanners.push({
      type: "module-boundary",
      payload: {
        module,
        score: Math.round(moduleQuality * 10) / 10,
        oldLevel,
        newLevel,
      },
      created: new Date().toISOString(),
      acknowledged: false,
    });
  }

  fs.writeFileSync(PROFILE_PATH, JSON.stringify(profile, null, 2));
  if (levelChanged && levelInfo.hasEffective) {
    fs.writeFileSync(CLAUDE_LOCAL_PATH, updateEffectiveLevel(claudeLocal, newLevel));
  }

  console.log(
    JSON.stringify({
      status: "ok",
      module,
      nextModule: module + 1,
      moduleQuality: Math.round(moduleQuality * 10) / 10,
      oldLevel,
      newLevel,
      levelChanged,
    }),
  );
}

main();
