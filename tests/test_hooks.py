"""Tests for hook scripts and settings configuration."""

import json
import re
import subprocess
import sys
import pytest
from conftest import REPO_ROOT


class TestSettingsJson:
    """Verify .claude/settings.json is valid and properly configured."""

    def test_settings_is_valid_json(self):
        path = REPO_ROOT / ".claude" / "settings.json"
        content = path.read_text(encoding="utf-8")
        data = json.loads(content)  # raises on invalid JSON
        assert isinstance(data, dict)

    def test_settings_has_hooks(self):
        path = REPO_ROOT / ".claude" / "settings.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "hooks" in data, "settings.json must have a 'hooks' key"

    def test_session_start_hooks_configured(self):
        path = REPO_ROOT / ".claude" / "settings.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "SessionStart" in data["hooks"], \
            "settings.json must have SessionStart hooks"

    def test_two_session_start_hooks(self):
        path = REPO_ROOT / ".claude" / "settings.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        hooks = data["hooks"]["SessionStart"]
        assert len(hooks) == 3, \
            f"Expected 3 SessionStart hooks, got {len(hooks)}"

    def test_hook_scripts_referenced_exist(self):
        """Every script referenced in settings.json must exist."""
        path = REPO_ROOT / ".claude" / "settings.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for event_hooks in data["hooks"].values():
            for matcher_block in event_hooks:
                for hook in matcher_block.get("hooks", []):
                    cmd = hook.get("command", "")
                    # Extract the script path from the command
                    # e.g., "node .claude/scripts/welcome.js" → ".claude/scripts/welcome.js"
                    parts = cmd.split()
                    if len(parts) >= 2:
                        script_path = parts[-1]  # last arg is the file
                        assert (REPO_ROOT / script_path).is_file(), \
                            f"Hook script not found: {script_path} (from command: {cmd})"


class TestWelcomeScript:
    """Verify welcome.js script works correctly."""

    def test_welcome_script_is_valid_js(self):
        """welcome.js should parse without errors."""
        script = REPO_ROOT / ".claude" / "scripts" / "welcome.js"
        result = subprocess.run(
            ["node", "--check", str(script)],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0, \
            f"welcome.js has syntax errors: {result.stderr}"

    def test_welcome_script_outputs_json(self):
        """welcome.js should output valid JSON with a systemMessage."""
        script = REPO_ROOT / ".claude" / "scripts" / "welcome.js"
        result = subprocess.run(
            ["node", str(script)],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0, f"welcome.js failed: {result.stderr}"
        data = json.loads(result.stdout)
        assert "systemMessage" in data, \
            "welcome.js must output a systemMessage"

    def test_welcome_mentions_start_command(self):
        """The welcome banner must tell users to type /start."""
        script = REPO_ROOT / ".claude" / "scripts" / "welcome.js"
        result = subprocess.run(
            ["node", str(script)],
            capture_output=True, text=True, timeout=10,
        )
        data = json.loads(result.stdout)
        assert "/start" in data["systemMessage"], \
            "Welcome banner must mention /start"


class TestCheckUpdatesScript:
    """Verify check-updates.js script is structurally valid."""

    def test_check_updates_is_valid_js(self):
        """check-updates.js should parse without errors."""
        script = REPO_ROOT / ".claude" / "scripts" / "check-updates.js"
        result = subprocess.run(
            ["node", "--check", str(script)],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0, \
            f"check-updates.js has syntax errors: {result.stderr}"

    def test_check_updates_contains_github_api(self):
        """check-updates.js must query GitHub for releases."""
        content = (REPO_ROOT / ".claude" / "scripts" / "check-updates.js").read_text(
            encoding="utf-8"
        )
        assert "api.github.com" in content, \
            "check-updates.js must query GitHub API"
        assert "anthropics/claude-code" in content, \
            "check-updates.js must check the anthropics/claude-code repo"

    def test_check_updates_has_timeout(self):
        """check-updates.js must have a timeout to not block offline users."""
        content = (REPO_ROOT / ".claude" / "scripts" / "check-updates.js").read_text(
            encoding="utf-8"
        )
        assert "timeout" in content.lower(), \
            "check-updates.js must have a timeout"

    def test_check_updates_fails_silently(self):
        """check-updates.js must catch errors and exit 0 on failure."""
        content = (REPO_ROOT / ".claude" / "scripts" / "check-updates.js").read_text(
            encoding="utf-8"
        )
        assert "process.exit(0)" in content, \
            "check-updates.js must exit(0) on failure (silent fail)"


class TestLearnerStreakCheckScript:
    """Verify learner-streak-check.js (UserPromptSubmit hook) is configured correctly."""

    SCRIPT = REPO_ROOT / ".claude" / "scripts" / "learner-streak-check.js"

    def test_script_is_valid_js(self):
        result = subprocess.run(
            ["node", "--check", str(self.SCRIPT)],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0, \
            f"learner-streak-check.js has syntax errors: {result.stderr}"

    def test_user_prompt_submit_hook_configured(self):
        """settings.json must wire the script into UserPromptSubmit."""
        path = REPO_ROOT / ".claude" / "settings.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "UserPromptSubmit" in data["hooks"], \
            "settings.json must have a UserPromptSubmit hook"
        commands = [
            h.get("command", "")
            for block in data["hooks"]["UserPromptSubmit"]
            for h in block.get("hooks", [])
        ]
        assert any("learner-streak-check.js" in c for c in commands), \
            "UserPromptSubmit must invoke learner-streak-check.js"

    def test_respects_observe_lock(self):
        """Must check for .observe-lock to avoid racing with observe-interaction.js."""
        content = self.SCRIPT.read_text(encoding="utf-8")
        assert ".observe-lock" in content, \
            "learner-streak-check.js must check for .observe-lock"

    def test_fires_only_on_transitions(self):
        """Must compare current streak against lastAnnouncedStreak to suppress repeats."""
        content = self.SCRIPT.read_text(encoding="utf-8")
        assert "lastAnnouncedStreak" in content, \
            "learner-streak-check.js must track lastAnnouncedStreak"


class TestGitHubApiIntegration:
    """Integration tests that verify GitHub API parsing works end-to-end.

    These tests hit the real GitHub API. They are skipped when offline or
    rate-limited so they don't break CI, but they catch parsing bugs like
    the grep pattern issue (v2.5.0) that static tests miss.
    """

    @pytest.fixture(autouse=True)
    def _skip_if_offline(self):
        """Skip all tests in this class if GitHub API is unreachable."""
        try:
            result = subprocess.run(
                ["curl", "-sf", "--max-time", "5",
                 "https://api.github.com/rate_limit"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode != 0:
                pytest.skip("GitHub API unreachable")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("curl not available or timed out")

    def test_skill_curl_fetches_version(self):
        """The curl command in SKILL.md Step 0 must return JSON with tag_name.

        SKILL.md uses plain `curl` to fetch the latest release; Claude parses
        the JSON response to extract the version.  This test verifies the API
        returns the expected structure.
        """
        skill_content = (
            REPO_ROOT / ".claude" / "skills" / "start" / "SKILL.md"
        ).read_text(encoding="utf-8")

        # Verify the curl command exists in SKILL.md (no grep pipeline)
        assert re.search(
            r"curl\s+-sf\s+https://api\.github\.com/repos/anthropics/claude-code/releases/latest",
            skill_content,
        ), "Could not find the curl command for GitHub releases in SKILL.md"

        # Verify the API returns valid JSON with a parseable tag_name
        result = subprocess.run(
            ["curl", "-sf", "--max-time", "10",
             "https://api.github.com/repos/anthropics/claude-code/releases/latest"],
            capture_output=True, timeout=15,
        )
        assert result.returncode == 0, \
            f"GitHub API curl failed (exit {result.returncode}): {result.stderr.decode('utf-8', errors='replace')}"

        data = json.loads(result.stdout.decode("utf-8"))
        tag = data.get("tag_name", "")
        assert re.match(r"^v?\d+\.\d+\.\d+", tag), \
            f"tag_name is not a valid version — got: '{tag}'"

    def test_check_updates_parses_github_response(self):
        """check-updates.js must successfully parse the GitHub API response.

        Fetches the same API endpoint and verifies the tag_name field can be
        extracted — the same logic check-updates.js performs at runtime.
        """
        result = subprocess.run(
            ["curl", "-sf", "--max-time", "10",
             "https://api.github.com/repos/anthropics/claude-code/releases?per_page=1"],
            capture_output=True, timeout=15,
        )
        assert result.returncode == 0, \
            f"GitHub API request failed: {result.stderr.decode('utf-8', errors='replace')}"

        data = json.loads(result.stdout.decode("utf-8"))
        assert isinstance(data, list) and len(data) > 0, \
            "GitHub releases API returned empty or non-array response"

        tag = data[0].get("tag_name", "")
        version = tag.lstrip("v")
        assert re.match(r"^\d+\.\d+\.\d+", version), \
            f"GitHub release tag_name is not a valid version — got: '{tag}'"
