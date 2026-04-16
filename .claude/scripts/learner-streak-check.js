#!/usr/bin/env node
// UserPromptSubmit hook: Surfaces streak transitions mid-session.
//
// The Stop hook (observe-interaction.js) updates struggleStreak/engagementStreak
// in learner-profile.json after every response, but the SessionStart hook
// (learner-context.js) only injects the alert at session start. Without this
// hook, a streak that develops within a session wouldn't reach Claude until
// the next session boot. This closes that gap.
//
// Fires only on transitions (none → struggle, none → engagement, or
// struggle ↔ engagement) — stays silent when the streak state is unchanged
// since the last alert, so Claude isn't nagged every turn.

const fs = require("fs");
const path = require("path");

const PROFILE_PATH = path.join(process.cwd(), "learner-profile.json");
const LOCK_PATH = path.join(process.cwd(), ".observe-lock");

function currentStreak(profile) {
  if (profile.struggleStreak) return "struggle";
  if (profile.engagementStreak) return "engagement";
  return "none";
}

function alertFor(kind) {
  if (kind === "struggle") {
    return "LEARNER SIGNAL (do not mention to student): ⚠ STRUGGLE STREAK just triggered — 3+ consecutive passive/answer-seeking turns. Offer more scaffolding NOW.";
  }
  if (kind === "engagement") {
    return "LEARNER SIGNAL (do not mention to student): ENGAGEMENT STREAK just triggered — student is in flow. Match with deeper content.";
  }
  return "";
}

function main() {
  if (!fs.existsSync(PROFILE_PATH)) process.exit(0);

  // observe-interaction.js may be mid-write; skip this turn to avoid racing.
  // The transition will be picked up on the next prompt.
  if (fs.existsSync(LOCK_PATH)) process.exit(0);

  let profile;
  try {
    profile = JSON.parse(fs.readFileSync(PROFILE_PATH, "utf-8"));
  } catch {
    process.exit(0);
  }

  const current = currentStreak(profile);
  const lastAnnounced = profile.lastAnnouncedStreak || "none";

  if (current === lastAnnounced) process.exit(0);

  // Update the tracker either way, so a later re-triggering fires again
  profile.lastAnnouncedStreak = current;
  try {
    fs.writeFileSync(PROFILE_PATH, JSON.stringify(profile, null, 2));
  } catch {
    process.exit(0);
  }

  if (current === "none") process.exit(0);

  process.stdout.write(alertFor(current));
  process.exit(0);
}

main();
