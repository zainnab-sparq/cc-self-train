#!/usr/bin/env node
// Preprocessor for module files. Strips persona-level-gated content blocks
// before the student reads the module.
//
// Invoked by Claude when the student says "next module", AFTER module-boundary.js
// has run. Produces a level-appropriate rendering of the module file on stdout.
//
// Level markers (HTML comments so they're invisible in native markdown preview):
//
//   <!-- guide-only -->...<!-- /guide-only -->
//     Shown for beginner + intermediate. Stripped for advanced.
//     Use for extra explanation, analogies, encouragement.
//
//   <!-- advanced-only -->...<!-- /advanced-only -->
//     Shown only for advanced. Stripped for beginner + intermediate.
//     Use for terse alternatives or expert-only pointers.
//
// Unmarked content is baseline — shown to every level. Existing module files
// are written at the intermediate baseline; this preprocessor only strips
// gated blocks, it does not rewrite anything.
//
// Usage:   node render-module.js <path-to-module.md>
// Outputs: rendered markdown to stdout
// Exit:    0 success; 1 bad args / file not found; 2 unbalanced markers

const fs = require("fs");
const path = require("path");

const VALID_LEVELS = ["beginner", "intermediate", "advanced"];

function readLevel(cwd) {
  const localPath = path.join(cwd, "CLAUDE.local.md");
  if (!fs.existsSync(localPath)) return "intermediate";
  const content = fs.readFileSync(localPath, "utf8");
  const effMatch = content.match(/^Effective Level:\s*(\w+)/m);
  if (effMatch) {
    const level = effMatch[1].toLowerCase();
    if (VALID_LEVELS.includes(level)) return level;
  }
  const expMatch = content.match(/^Experience Level:\s*(\w+)/m);
  if (expMatch) {
    const level = expMatch[1].toLowerCase();
    if (VALID_LEVELS.includes(level)) return level;
  }
  return "intermediate";
}

function validateBalanced(content, tagName) {
  const openRe = new RegExp("<!--\\s*" + tagName + "\\s*-->", "g");
  const closeRe = new RegExp("<!--\\s*/" + tagName + "\\s*-->", "g");
  const opens = (content.match(openRe) || []).length;
  const closes = (content.match(closeRe) || []).length;
  return opens === closes;
}

function stripBlocks(content, tagName) {
  const pattern = new RegExp(
    "<!--\\s*" + tagName + "\\s*-->[\\s\\S]*?<!--\\s*/" + tagName + "\\s*-->",
    "g"
  );
  return content.replace(pattern, "");
}

function normalizeBlankLines(content) {
  // Match both LF and CRLF runs so Windows-authored files collapse the same
  // way as LF-normalized ones. Replaces with two LFs; if the file was CRLF,
  // the collapsed paragraph-break loses its \r but no tool/editor cares.
  return content.replace(/(\r?\n){3,}/g, "\n\n");
}

function render(raw, level) {
  let out = raw;
  if (level === "advanced") {
    out = stripBlocks(out, "guide-only");
  } else {
    out = stripBlocks(out, "advanced-only");
  }
  return normalizeBlankLines(out);
}

function main() {
  const modulePath = process.argv[2];
  if (!modulePath) {
    process.stderr.write("Usage: render-module.js <path-to-module.md>\n");
    process.exit(1);
  }
  if (!fs.existsSync(modulePath)) {
    process.stderr.write("File not found: " + modulePath + "\n");
    process.exit(1);
  }

  const raw = fs.readFileSync(modulePath, "utf8");

  if (!validateBalanced(raw, "guide-only") || !validateBalanced(raw, "advanced-only")) {
    process.stderr.write(
      "Unbalanced level markers in " + modulePath + ". Every <!-- guide-only --> " +
      "needs a closing <!-- /guide-only --> (same for advanced-only).\n"
    );
    process.exit(2);
  }

  const cwd = process.env.CLAUDE_PROJECT_DIR || process.cwd();
  const level = readLevel(cwd);
  process.stdout.write(render(raw, level));
}

main();
