#!/usr/bin/env node
// Regenerates the progress bar + estimated-time block at the top of every
// module file from config/curriculum.json (single source of truth).
//
// For each projects/*/modules/NN-*.md file, finds the block between
// <!-- progress:start --> and <!-- progress:end --> markers and rewrites it.
// Idempotent: a second run with no config changes produces zero diff.
//
// Output: JSON summary of {updated, unchanged, skipped, error} counts.
// Exits 1 if any file errored (malformed markers). Skipped files (markers
// missing) are reported but do not fail the run — that lets this script be
// run before the initial marker inserts without blowing up.

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const CONFIG_PATH = path.join(ROOT, "config", "curriculum.json");
const PROJECTS_DIR = path.join(ROOT, "projects");
const START_MARKER = "<!-- progress:start -->";
const END_MARKER = "<!-- progress:end -->";

function renderBar(n, total) {
  const filled = "\u2588".repeat(n);
  const empty = "\u2591".repeat(total - n);
  return `[${filled}${empty}]`;
}

function renderBlock(module, total) {
  const pct = Math.round((module.n / total) * 100);
  const bar = renderBar(module.n, total);
  return [
    START_MARKER,
    `**Progress:** Module ${module.n} of ${total} \`${bar}\` ${pct}%`,
    "",
    `**Estimated time:** ${module.estimated_time}`,
    END_MARKER,
  ].join("\n");
}

function moduleForFile(filename, modules) {
  const match = filename.match(/^(\d{2})-/);
  if (!match) return null;
  const n = parseInt(match[1], 10);
  return modules.find((m) => m.n === n) || null;
}

function processFile(filePath, module, total) {
  const content = fs.readFileSync(filePath, "utf-8");
  const startIdx = content.indexOf(START_MARKER);
  const endIdx = content.indexOf(END_MARKER);
  if (startIdx === -1 || endIdx === -1) {
    return { file: filePath, status: "skipped", reason: "markers not found" };
  }
  if (endIdx < startIdx) {
    return { file: filePath, status: "error", reason: "end marker before start" };
  }
  // Preserve the file's dominant line ending so a CRLF file stays CRLF.
  // Without this, Node would write LF and the generator would appear to
  // "update" every file on every run even when content is logically identical.
  const eol = content.includes("\r\n") ? "\r\n" : "\n";
  const newBlock = renderBlock(module, total).replace(/\n/g, eol);
  const updated =
    content.slice(0, startIdx) +
    newBlock +
    content.slice(endIdx + END_MARKER.length);
  if (updated === content) {
    return { file: filePath, status: "unchanged" };
  }
  fs.writeFileSync(filePath, updated);
  return { file: filePath, status: "updated" };
}

function main() {
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, "utf-8"));
  const total = config.total_modules;
  const projects = fs
    .readdirSync(PROJECTS_DIR)
    .filter((d) => fs.statSync(path.join(PROJECTS_DIR, d)).isDirectory());

  const results = [];
  for (const project of projects) {
    const moduleDir = path.join(PROJECTS_DIR, project, "modules");
    if (!fs.existsSync(moduleDir)) continue;
    const files = fs.readdirSync(moduleDir).filter((f) => f.endsWith(".md"));
    for (const filename of files) {
      const module = moduleForFile(filename, config.modules);
      if (!module) continue;
      const result = processFile(path.join(moduleDir, filename), module, total);
      results.push(result);
    }
  }

  const summary = results.reduce((acc, r) => {
    acc[r.status] = (acc[r.status] || 0) + 1;
    return acc;
  }, {});
  console.log(JSON.stringify(summary, null, 2));

  const errors = results.filter((r) => r.status === "error");
  if (errors.length > 0) {
    console.error("Errors:", errors);
    process.exit(1);
  }
}

main();
