#!/usr/bin/env node
// Stop hook: Observes student interaction quality and writes signals to learner-profile.json.
// Inspired by Chung et al. (2025) — engagement quality predicts learning outcomes.
// Streak detection inspired by Hooshyar et al. (2026) — sequential patterns
// (e.g., 3 consecutive struggles) are more informative than isolated events,
// and non-mastery signals should be weighted more heavily than mastery signals.
// Silent (no stdout) — exits 0 always. Never blocks.

const fs = require("fs");
const path = require("path");

const PROFILE_PATH = path.join(process.cwd(), "learner-profile.json");
const LOCK_PATH = path.join(process.cwd(), ".observe-lock");

// Prevent re-entrancy
if (fs.existsSync(LOCK_PATH)) process.exit(0);

// Quality scores per category
const QUALITY = {
  concept_question: 5,
  independent_exploration: 4,
  debug_attempt: 3,
  answer_seeking: 1,
  passive_acceptance: 1,
  neutral: 3,
};

function classify(userMsg, assistantMsgLength) {
  if (!userMsg || userMsg.trim().length === 0) return "neutral";
  const msg = userMsg.toLowerCase();

  // Answer-seeking patterns
  const answerPatterns = [
    "just do it", "write it for me", "give me the code", "can you just",
    "just fix", "just make", "do it for me", "just create", "just write",
  ];
  if (answerPatterns.some((p) => msg.includes(p))) return "answer_seeking";

  // Concept question patterns
  const conceptPatterns = [
    "why does", "why do", "why is", "how does", "how do", "how is",
    "explain", "what happens if", "what's the difference", "what is the difference",
    "what does", "what is a ", "what are ", "can you explain", "help me understand",
    "i don't understand", "i'm confused", "what's the purpose",
  ];
  if (conceptPatterns.some((p) => msg.includes(p))) return "concept_question";

  // Independent exploration patterns
  const explorePatterns = [
    "i tried", "i tested", "i noticed", "i changed", "i modified",
    "i added", "i created", "i wrote", "i built", "i experimented",
    "i figured out", "i found that", "i realized", "i see that",
    "when i run", "when i try", "i got it working",
  ];
  if (explorePatterns.some((p) => msg.includes(p))) return "independent_exploration";

  // Debug attempt patterns
  const debugPatterns = [
    "error", "failed", "not working", "broke", "doesn't work",
    "getting an error", "it says", "the output is wrong", "unexpected",
    "stack trace", "exception", "bug", "issue",
  ];
  if (debugPatterns.some((p) => msg.includes(p))) return "debug_attempt";

  // Passive acceptance (short reply to long assistant message)
  if (msg.trim().length < 15 && assistantMsgLength > 500) return "passive_acceptance";

  return "neutral";
}

function getLastUserMessage(transcriptPath) {
  try {
    const content = fs.readFileSync(transcriptPath, "utf-8");
    const lines = content.trim().split("\n");
    // Read last 20 lines to find the most recent user message
    const recent = lines.slice(-20);
    let lastUserMsg = "";
    let lastAssistantLength = 0;

    for (const line of recent) {
      try {
        const entry = JSON.parse(line);
        if (entry.type === "human" || entry.role === "user") {
          // Extract text content
          if (typeof entry.message === "string") lastUserMsg = entry.message;
          else if (entry.message?.content) {
            if (typeof entry.message.content === "string") lastUserMsg = entry.message.content;
            else if (Array.isArray(entry.message.content)) {
              const textParts = entry.message.content
                .filter((c) => c.type === "text")
                .map((c) => c.text);
              lastUserMsg = textParts.join(" ");
            }
          }
        }
        if (entry.type === "assistant" || entry.role === "assistant") {
          if (typeof entry.message === "string") lastAssistantLength = entry.message.length;
          else if (entry.message?.content) {
            if (typeof entry.message.content === "string") lastAssistantLength = entry.message.content.length;
            else if (Array.isArray(entry.message.content)) {
              lastAssistantLength = entry.message.content
                .filter((c) => c.type === "text")
                .map((c) => c.text || "")
                .join("").length;
            }
          }
        }
      } catch { /* skip malformed lines */ }
    }
    return { lastUserMsg, lastAssistantLength };
  } catch {
    return { lastUserMsg: "", lastAssistantLength: 0 };
  }
}

function loadProfile() {
  try {
    return JSON.parse(fs.readFileSync(PROFILE_PATH, "utf-8"));
  } catch {
    return {
      currentModule: 1,
      interactions: { concept_question: 0, independent_exploration: 0, debug_attempt: 0, answer_seeking: 0, passive_acceptance: 0, neutral: 0 },
      moduleInteractions: { concept_question: 0, independent_exploration: 0, debug_attempt: 0, answer_seeking: 0, passive_acceptance: 0, neutral: 0 },
      qualityScores: [],
      moduleQualityScores: [],
      recentCategories: [],
      struggleStreak: false,
      engagementStreak: false,
      // Queue of {type, created, acknowledged} events written on streak
      // transitions. learner-context.js drains this queue on SessionStart,
      // emits one-line banners, and marks entries acknowledged.
      pendingBanners: [],
      averageQuality: 0,
      moduleAverageQuality: 0,
      recentTrend: "not yet measured",
      lastUpdated: new Date().toISOString(),
    };
  }
}

function computeTrend(scores) {
  if (scores.length < 6) return "not yet measured";
  const recent = scores.slice(-5);
  const earlier = scores.slice(-10, -5);
  if (earlier.length === 0) return "stable";
  const recentAvg = recent.reduce((a, b) => a + b, 0) / recent.length;
  const earlierAvg = earlier.reduce((a, b) => a + b, 0) / earlier.length;
  const diff = recentAvg - earlierAvg;
  if (diff > 0.5) return "improving";
  if (diff < -0.5) return "declining";
  return "stable";
}

async function main() {
  let input = "";
  for await (const chunk of process.stdin) input += chunk;

  let data;
  try { data = JSON.parse(input); } catch { process.exit(0); }

  const transcriptPath = data.transcript_path;
  if (!transcriptPath) process.exit(0);

  // Create lock
  try { fs.writeFileSync(LOCK_PATH, ""); } catch { /* ok */ }

  try {
    const { lastUserMsg, lastAssistantLength } = getLastUserMessage(transcriptPath);
    if (!lastUserMsg) { cleanup(); process.exit(0); }

    const category = classify(lastUserMsg, lastAssistantLength);
    const quality = QUALITY[category];

    const profile = loadProfile();
    profile.interactions[category] = (profile.interactions[category] || 0) + 1;
    profile.moduleInteractions[category] = (profile.moduleInteractions[category] || 0) + 1;

    // Keep last 100 quality scores for trend computation
    profile.qualityScores = (profile.qualityScores || []).concat(quality).slice(-100);
    profile.moduleQualityScores = (profile.moduleQualityScores || []).concat(quality).slice(-50);

    const allScores = profile.qualityScores;
    profile.averageQuality = Math.round((allScores.reduce((a, b) => a + b, 0) / allScores.length) * 10) / 10;

    const modScores = profile.moduleQualityScores;
    profile.moduleAverageQuality = Math.round((modScores.reduce((a, b) => a + b, 0) / modScores.length) * 10) / 10;

    profile.recentTrend = computeTrend(allScores);

    // Streak detection (Hooshyar et al., 2026): sequential patterns are more
    // informative than isolated events. Track last 5 non-neutral categories.
    if (category !== "neutral") {
      profile.recentCategories = (profile.recentCategories || []).concat(category).slice(-5);
    }
    const rc = profile.recentCategories || [];
    const last3 = rc.slice(-3);
    const struggle = ["answer_seeking", "passive_acceptance"];
    const engaged = ["concept_question", "independent_exploration"];
    const prevStruggleStreak = profile.struggleStreak === true;
    const prevEngagementStreak = profile.engagementStreak === true;
    profile.struggleStreak = last3.length >= 3 && last3.every((c) => struggle.includes(c));
    profile.engagementStreak = last3.length >= 3 && last3.every((c) => engaged.includes(c));

    // Queue a learner-visible banner on transitions INTO a streak.
    // Transitions out (streak ending) stay silent — the banner message only
    // makes sense while the run is active.
    profile.pendingBanners = profile.pendingBanners || [];
    if (!prevStruggleStreak && profile.struggleStreak) {
      profile.pendingBanners.push({
        type: "struggle",
        created: new Date().toISOString(),
        acknowledged: false,
      });
    }
    if (!prevEngagementStreak && profile.engagementStreak) {
      profile.pendingBanners.push({
        type: "engagement",
        created: new Date().toISOString(),
        acknowledged: false,
      });
    }

    profile.lastUpdated = new Date().toISOString();

    fs.writeFileSync(PROFILE_PATH, JSON.stringify(profile, null, 2));
  } catch { /* silent failure */ }

  cleanup();
  process.exit(0);
}

function cleanup() {
  try { fs.unlinkSync(LOCK_PATH); } catch { /* ok */ }
}

main();
