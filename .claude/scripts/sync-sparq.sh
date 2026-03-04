#!/usr/bin/env bash
# Sync master branch and tags to the sparq remote (zainnab-sparq/cc-self-train)
# Usage: bash .claude/scripts/sync-sparq.sh

set -e

echo "Pushing master to sparq..."
git push sparq master

echo "Pushing tags to sparq..."
git push sparq --tags

echo "Done. sparq remote is in sync."
