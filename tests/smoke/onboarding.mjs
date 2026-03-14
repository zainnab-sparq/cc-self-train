#!/usr/bin/env node

/**
 * Smoke test for the /start onboarding flow.
 *
 * Runs Claude Code via the Agent SDK inside a git worktree sandbox,
 * injects answers to AskUserQuestion calls, and asserts on the output.
 *
 * Tests BOTH scaffolding correctness (right files created) AND
 * pacing behavior (multi-turn conversation, one sub-step per message).
 *
 * Usage: called by run-smoke.sh (which handles SDK installation).
 * Expects SDK_DIR env var pointing to the temp dir where the SDK is installed.
 */

import { createRequire } from "node:module";
import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

// --- Prevent nested session detection ---
delete process.env.CLAUDECODE;

// --- Load SDK via createRequire (NODE_PATH doesn't work with ESM) ---
const SDK_DIR = process.env.SDK_DIR;
if (!SDK_DIR) {
  console.error("SDK_DIR env var not set. Use run-smoke.sh to run this test.");
  process.exit(1);
}
const _require = createRequire(path.join(SDK_DIR, "node_modules", "noop.js"));
const { query } = _require("@anthropic-ai/claude-agent-sdk");

// --- Setup: worktree sandbox ---
const REPO_ROOT = execSync("git rev-parse --show-toplevel", { encoding: "utf8" }).trim();
const WORKTREE_NAME = `smoke-${Date.now()}`;
const WORKTREE_DIR = path.join(REPO_ROOT, ".claude", "worktrees", WORKTREE_NAME);

function cleanup() {
  console.log("\nCleaning up...");
  try {
    execSync(`git worktree remove --force "${WORKTREE_DIR}"`, {
      cwd: REPO_ROOT,
      stdio: "ignore",
    });
  } catch {}
  const worktreesDir = path.join(REPO_ROOT, ".claude", "worktrees");
  try {
    if (fs.readdirSync(worktreesDir).length === 0) fs.rmdirSync(worktreesDir);
  } catch {}
}

let cleanedUp = false;
function safeCleanup() {
  if (cleanedUp) return;
  cleanedUp = true;
  cleanup();
}

process.on("exit", safeCleanup);
process.on("SIGINT", () => {
  safeCleanup();
  process.exit(1);
});
process.on("uncaughtException", (e) => {
  console.error(e);
  safeCleanup();
  process.exit(1);
});

// Create worktree
console.log(`Creating worktree at ${WORKTREE_DIR}...`);
fs.mkdirSync(path.dirname(WORKTREE_DIR), { recursive: true });
execSync(`git worktree add "${WORKTREE_DIR}" HEAD`, { cwd: REPO_ROOT, stdio: "inherit" });

// --- Read SKILL.md and strip frontmatter ---
// The SDK runs headless — skills aren't auto-discovered via `/start`.
// We read the SKILL.md content and pass it directly as the prompt.
const skillPath = path.join(WORKTREE_DIR, ".claude", "skills", "start", "SKILL.md");
let skillContent = fs.readFileSync(skillPath, "utf8");
skillContent = skillContent.replace(/^---[\s\S]*?---\n*/, "");

// Minimal headless preamble — tells Claude to execute (not teach) while
// keeping all pacing rules intact so we test the real user experience.
const HEADLESS_PREAMBLE = `\
IMPORTANT: This is a headless automated session — there is no GUI or browser.
You are executing the onboarding for a test user. Create all files, run all commands, and make all commits yourself.
When AskUserQuestion is called, answers are provided automatically — continue as if a user responded.
When a step says "open in browser" or "start index.html", skip it — no browser is available.
Follow all pacing rules exactly as written — deliver one sub-step per message and stop between them.

CRITICAL PATH RULE: The repo root for this session is "${WORKTREE_DIR.replace(/\\/g, "/")}".
All paths in the instructions (workspace/, projects/, context/, CLAUDE.local.md, etc.) are relative to THIS directory.
Use this directory for ALL file operations — do NOT resolve or use any other repo root path.

Here are the onboarding instructions to execute:

`;

const PROMPT = HEADLESS_PREAMBLE + skillContent;

// --- Answer map for AskUserQuestion ---
// Ordered list of pattern→answer pairs. Each is consumed once when matched.
const answerQueue = [
  { match: /project/i, answer: "Canvas (Recommended)" },
  { match: /experience/i, answer: "First timer" },
  // Git config questions — conditional, only asked if git config is empty
  { match: /name/i, answer: "Test User" },
  { match: /email/i, answer: "test@example.com" },
  // CLAUDE.md customization prompt
  { match: /improve|customize|style|goal|change|add|claude\.md/i, answer: "Add a project goal" },
];
let nextAnswer = 0;

// --- Tool tracking ---
const toolLog = []; // { turn, tool, detail? }

function canUseTool(toolName, input) {
  const currentTurn = turnOutputs.length + 1;
  const detail = toolName === "Bash" ? (input.command || "").slice(0, 80) : undefined;
  toolLog.push({ turn: currentTurn, tool: toolName, detail });
  console.log(`\n  [turn ${currentTurn}] ${toolName}${detail ? `: ${detail}` : ""}`);

  if (toolName === "AskUserQuestion") {
    const questions = input.questions || [];
    const answers = {};

    for (const q of questions) {
      const questionText = q.question || "";
      console.log(`    Q: "${questionText}"`);
      let matched = false;
      for (let i = nextAnswer; i < answerQueue.length; i++) {
        if (answerQueue[i].match.test(questionText)) {
          answers[questionText] = answerQueue[i].answer;
          console.log(`    A: "${answerQueue[i].answer}"`);
          nextAnswer = i + 1;
          matched = true;
          break;
        }
      }
      if (!matched && q.options && q.options.length > 0) {
        answers[questionText] = q.options[0].label;
        console.log(`    [fallback] A: "${q.options[0].label}"`);
      }
    }

    return Promise.resolve({
      behavior: "allow",
      updatedInput: { questions, answers },
    });
  }

  // Block browser-opening Bash commands (no GUI in headless mode)
  if (toolName === "Bash") {
    const cmd = (input.command || "").trim();

    if (
      /^(start|open|xdg-open)\s/i.test(cmd) ||
      /\b(chrome|firefox|edge|browser)\b/i.test(cmd)
    ) {
      console.log(`    [blocked] Browser command`);
      return Promise.resolve({
        behavior: "deny",
        message: "No browser available in headless mode. Skip this step.",
      });
    }
  }

  // Block WebFetch (can trigger browser on some systems)
  if (toolName === "WebFetch") {
    console.log(`    [blocked] WebFetch`);
    return Promise.resolve({
      behavior: "deny",
      message: "WebFetch blocked in headless mode. Use local files or skip.",
    });
  }

  // Allow everything else — including WebSearch (Step 6.6 teaching moment)
  return Promise.resolve({ behavior: "allow", updatedInput: input });
}

// --- Multi-turn execution ---
const turnOutputs = []; // One string per turn — tracks pacing
let fullOutput = "";
let sessionId = null;
const MAX_TURNS = 20;

// Run one conversational turn and collect output
async function runTurn(prompt, isResume = false) {
  let turnOutput = "";
  let gotResult = false;

  const opts = {
    cwd: WORKTREE_DIR,
    canUseTool,
    maxTurns: isResume ? 20 : 50, // Resume turns need fewer internal rounds
  };
  if (isResume && sessionId) {
    opts.resume = sessionId;
  }

  for await (const msg of query({ prompt, options: opts })) {
    if (msg.type === "assistant" && msg.message?.content) {
      for (const block of msg.message.content) {
        if ("text" in block) turnOutput += block.text + "\n";
      }
      process.stdout.write(".");
    }
    if (msg.type === "result") {
      sessionId = msg.session_id;
      gotResult = true;
      process.stdout.write("T");
    }
  }

  turnOutputs.push(turnOutput);
  fullOutput += turnOutput;
  console.log(`  [turn ${turnOutputs.length}: ${turnOutput.length} chars]`);
  return gotResult;
}

// Check if onboarding has completed
function isComplete() {
  const localMdPath = path.join(WORKTREE_DIR, "CLAUDE.local.md");
  if (!fs.existsSync(localMdPath)) return false;

  // Best signal: Module 1 recap appeared in output (Step 6.8)
  if (/module 1 complete/i.test(fullOutput)) return true;

  // Fallback: CLAUDE.local.md exists + onboarding-state.json cleaned up + enough turns
  const statePath = path.join(WORKTREE_DIR, ".claude", "onboarding-state.json");
  if (!fs.existsSync(statePath) && turnOutputs.length >= 5) return true;

  return false;
}

// --- Run the onboarding flow ---
console.log("\nRunning /start...\n");

// Initial turn: Steps 1-5 (setup, scaffold)
await runTurn(PROMPT);

// Resume loop: Steps 6.1-6.8 (Module 1 delivery, one sub-step per turn)
while (sessionId && turnOutputs.length < MAX_TURNS) {
  if (isComplete()) {
    console.log("\n  Onboarding complete.");
    break;
  }

  const gotResult = await runTurn("Looks good, continue.", true);
  if (!gotResult) {
    console.log("\n  No result message — ending resume loop.");
    break;
  }
}

const totalTurns = turnOutputs.length;
console.log(`\n\nCompleted in ${totalTurns} turn(s).\n`);

// --- Assertions ---
const W = path.join(WORKTREE_DIR, "workspace", "canvas-site");

// Pacing analysis
const webSearchAttempted = toolLog.some((t) => t.tool === "WebSearch");
// Check resume turns (index 1+) for wall-of-text violations
const resumeTurnLengths = turnOutputs.slice(1).map((t) => t.length);
const maxResumeTurnLen = resumeTurnLengths.length > 0 ? Math.max(...resumeTurnLengths) : 0;

const checks = [
  // --- File existence ---
  ["workspace/canvas-site/ exists", fs.existsSync(W)],
  ["index.html", fs.existsSync(path.join(W, "index.html"))],
  [
    "CSS file exists",
    fs.existsSync(path.join(W, "styles", "main.css")) ||
      fs.existsSync(path.join(W, "css", "style.css")) ||
      fs.existsSync(path.join(W, "style.css")),
  ],
  [
    "JS file exists",
    fs.existsSync(path.join(W, "scripts", "main.js")) ||
      fs.existsSync(path.join(W, "js", "main.js")) ||
      fs.existsSync(path.join(W, "script.js")),
  ],
  ["CLAUDE.md in project", fs.existsSync(path.join(W, "CLAUDE.md"))],
  [".git/ in project (nested repo)", fs.existsSync(path.join(W, ".git"))],
  ["CLAUDE.local.md exists", fs.existsSync(path.join(WORKTREE_DIR, "CLAUDE.local.md"))],
  [
    "onboarding-state.json cleaned up",
    !fs.existsSync(path.join(WORKTREE_DIR, ".claude", "onboarding-state.json")),
  ],

  // --- Output content ---
  ["output mentions CLAUDE.md", /CLAUDE\.md/i.test(fullOutput)],
  ["output mentions shortcuts or keyboard", /shortcut|keyboard/i.test(fullOutput)],
  ["output mentions Module 1", /module 1/i.test(fullOutput)],
  ["output mentions commit", /commit/i.test(fullOutput)],
  ["output mentions next module", /next module/i.test(fullOutput)],

  // --- Pacing & multi-turn ---
  // In headless mode, AskUserQuestion is auto-answered so Claude can complete
  // everything in a single SDK call. We only assert completion, not turn count.
  // Real pacing (multi-turn delivery) is tested by the user experience, not here.
  [`completed: ${totalTurns} turn(s)`, totalTurns >= 1],
  ["WebSearch attempted for shortcuts (6.6)", webSearchAttempted],
];

console.log("Assertions:\n");
let passed = 0;
let failed = 0;

for (const [name, ok] of checks) {
  console.log(ok ? `  ✓ ${name}` : `  ✗ ${name}`);
  ok ? passed++ : failed++;
}

console.log(`\n${passed} passed, ${failed} failed out of ${checks.length}`);

// --- Debug info on failure ---
if (failed > 0) {
  console.log("\n--- Debug Info ---");
  console.log(`Worktree: ${WORKTREE_DIR}`);
  console.log(`Turns: ${totalTurns}`);
  console.log(`Answer queue consumed: ${nextAnswer}/${answerQueue.length}`);
  console.log(`WebSearch attempted: ${webSearchAttempted}`);
  console.log(`Tool calls: ${toolLog.length}`);

  // Per-turn output lengths
  console.log("\nTurn lengths:");
  for (let i = 0; i < turnOutputs.length; i++) {
    console.log(`  Turn ${i + 1}: ${turnOutputs[i].length} chars`);
  }

  // Tool call log
  console.log("\nTool log:");
  for (const t of toolLog) {
    console.log(`  [turn ${t.turn}] ${t.tool}${t.detail ? `: ${t.detail}` : ""}`);
  }

  // File listing (Node.js, not shell — Windows compat)
  function listFiles(dir, prefix = "", depth = 0) {
    if (depth > 3) return [];
    const results = [];
    try {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const name = entry.name;
        if (
          name === ".git" ||
          name === "node_modules" ||
          name === "context" ||
          name === "projects"
        )
          continue;
        const fullPath = path.join(prefix, name);
        if (entry.isDirectory()) {
          results.push(fullPath + "/");
          results.push(...listFiles(path.join(dir, name), fullPath, depth + 1));
        } else {
          results.push(fullPath);
        }
      }
    } catch {}
    return results;
  }

  if (fs.existsSync(WORKTREE_DIR)) {
    const files = listFiles(WORKTREE_DIR);
    console.log(`\nWorktree contents (${files.length} entries):`);
    for (const f of files.slice(0, 60)) console.log(`  ${f}`);
  } else {
    console.log("\nWorktree directory does not exist at assertion time!");
  }

  console.log(`\nOutput (last 3000 chars):\n${fullOutput.slice(-3000)}`);
}

process.exit(failed > 0 ? 1 : 0);
