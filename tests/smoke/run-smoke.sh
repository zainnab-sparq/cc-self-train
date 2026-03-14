#!/bin/bash
# Smoke test runner for /start onboarding flow.
# Installs the Claude Agent SDK in a temp directory and runs onboarding.mjs.
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Create temp dir for SDK install (outside the repo)
SDK_DIR=$(mktemp -d)
trap "rm -rf \"$SDK_DIR\"" EXIT

echo "Installing @anthropic-ai/claude-agent-sdk in $SDK_DIR..."
cd "$SDK_DIR"
npm init -y --silent > /dev/null 2>&1
npm install --silent @anthropic-ai/claude-agent-sdk > /dev/null 2>&1
echo "SDK installed."

# Run the test — pass SDK_DIR so the script can find the package
cd "$REPO_ROOT"
export SDK_DIR
node "$SCRIPT_DIR/onboarding.mjs"
