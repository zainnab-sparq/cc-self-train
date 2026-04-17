#!/usr/bin/env node
// SessionStart hook: Reads learner-profile.json and injects engagement context.
// If no profile exists (new student), exits silently.
//
// Two output channels:
//   1. Pending banners (student-visible)  -- drained from profile.pendingBanners.
//      Explicitly labeled "SHOW TO LEARNER" so Claude surfaces them verbatim.
//      Marked acknowledged once emitted so they only fire once.
//   2. Narrative (Claude-facing, internal) -- current behavior, unchanged:
//      labeled "do not mention this to the student", used to shape teaching.

const fs = require("fs");
const path = require("path");

const PROFILE_PATH = path.join(process.cwd(), "learner-profile.json");
const BANNER_TTL_MS = 24 * 60 * 60 * 1000;

function drainBanners(profile) {
  const banners = Array.isArray(profile.pendingBanners) ? profile.pendingBanners : [];
  if (banners.length === 0) return { lines: [], changed: false };

  const now = Date.now();
  const lines = [];
  let changed = false;
  for (const banner of banners) {
    if (banner.acknowledged) continue;
    const createdAt = Date.parse(banner.created || "");
    if (isNaN(createdAt) || now - createdAt > BANNER_TTL_MS) {
      // Too old to be relevant to this session -- mark acknowledged silently.
      banner.acknowledged = true;
      changed = true;
      continue;
    }
    if (banner.type === "struggle") {
      lines.push("\u{1F440} Noticed a run of struggle \u2014 shifting teaching style for a bit.");
    } else if (banner.type === "engagement") {
      lines.push("\u{1F4C8} Noticed a run of engagement \u2014 matching your energy with deeper content.");
    } else {
      // Unknown banner type -- skip but acknowledge so it doesn't re-fire.
      banner.acknowledged = true;
      changed = true;
      continue;
    }
    banner.acknowledged = true;
    changed = true;
  }
  return { lines, changed };
}

function main() {
  if (!fs.existsSync(PROFILE_PATH)) process.exit(0);

  let profile;
  try {
    profile = JSON.parse(fs.readFileSync(PROFILE_PATH, "utf-8"));
  } catch {
    process.exit(0);
  }

  // Drain pending banners first -- they fire even for new learners who haven't
  // yet accumulated the 5 non-neutral interactions needed for the narrative.
  const { lines: bannerLines, changed: bannersChanged } = drainBanners(profile);
  if (bannersChanged) {
    try {
      fs.writeFileSync(PROFILE_PATH, JSON.stringify(profile, null, 2));
    } catch { /* silent */ }
  }

  const totalNonNeutral =
    (profile.interactions?.concept_question || 0) +
    (profile.interactions?.independent_exploration || 0) +
    (profile.interactions?.debug_attempt || 0) +
    (profile.interactions?.answer_seeking || 0) +
    (profile.interactions?.passive_acceptance || 0);

  if (totalNonNeutral < 5) {
    if (bannerLines.length > 0) {
      process.stdout.write(
        "SHOW TO LEARNER (display verbatim):\n" + bannerLines.join("\n"),
      );
    }
    process.exit(0);
  }

  // Build the dominant pattern description
  const cats = profile.interactions || {};
  const productive = (cats.concept_question || 0) + (cats.independent_exploration || 0) + (cats.debug_attempt || 0);
  const unproductive = (cats.answer_seeking || 0) + (cats.passive_acceptance || 0);
  const ratio = productive / Math.max(productive + unproductive, 1);

  let pattern = "";
  if (ratio >= 0.7) {
    pattern = "Asks conceptual questions and explores independently (strong engagement).";
  } else if (ratio >= 0.4) {
    pattern = "Mixed — sometimes explores concepts, sometimes seeks direct answers.";
  } else {
    pattern = "Tends to seek direct answers rather than exploring. Needs more scaffolding.";
  }

  let teachingNote = "";
  if (ratio >= 0.7) {
    teachingNote = "Encourage their curiosity. Match their energy with deeper explanations.";
  } else if (ratio >= 0.4) {
    teachingNote = "When they ask for direct answers, redirect: 'What have you tried so far?'";
  } else {
    teachingNote = "Provide more structure and worked examples. Ask guiding questions before giving answers.";
  }

  const quality = profile.moduleAverageQuality || profile.averageQuality || 0;
  const trend = profile.recentTrend || "not yet measured";

  // Streak alerts (Hooshyar et al., 2026)
  let streakNote = "";
  if (profile.struggleStreak) {
    streakNote = "\n- ⚠ STRUGGLE STREAK: 3+ consecutive passive/answer-seeking interactions. Offer more scaffolding NOW.";
  } else if (profile.engagementStreak) {
    streakNote = "\n- ENGAGEMENT STREAK: Student is in flow. Match with deeper content.";
  }

  const msg = [
    "LEARNER PROFILE (auto-generated — do not mention this to the student):",
    `- Engagement quality: ${quality}/5 this module (${trend} trend)`,
    `- Pattern: ${pattern}`,
    `- Teaching note: ${teachingNote}`,
  ].join("\n") + streakNote;

  const out = [];
  if (bannerLines.length > 0) {
    out.push("SHOW TO LEARNER (display verbatim):");
    out.push(...bannerLines);
    out.push("");
  }
  out.push(msg);

  process.stdout.write(out.join("\n"));
  process.exit(0);
}

main();
