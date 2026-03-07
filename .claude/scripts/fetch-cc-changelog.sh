#!/usr/bin/env bash
# Fetch the Claude Code CHANGELOG.md from GitHub.
# Outputs raw markdown to stdout. Exits non-zero on failure.
set -euo pipefail
curl -sf https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
