#!/usr/bin/env bash
# Fetch the latest Claude Code version from GitHub releases API.
# Outputs just the version number (e.g. "2.15.0") to stdout.
# Exits non-zero on failure (network error, rate limit, parse error).
set -euo pipefail
curl -sf https://api.github.com/repos/anthropics/claude-code/releases/latest \
  | grep -o '"tag_name"[^"]*"[^"]*"' \
  | head -1 \
  | grep -o '[0-9][0-9.]*'
