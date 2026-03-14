"""Tests that all expected files and directories exist in the repo."""

import pathlib
import pytest
from conftest import REPO_ROOT, PROJECTS


class TestTopLevelFiles:
    """Verify top-level repo files exist."""

    @pytest.mark.parametrize("filename", [
        "README.md",
        "CLAUDE.md",
        ".gitignore",
        ".gitattributes",
        "CHANGELOG.md",
    ])
    def test_top_level_file_exists(self, filename):
        assert (REPO_ROOT / filename).is_file(), f"Missing top-level file: {filename}"

    def test_claudemd_not_empty(self):
        content = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        assert len(content) > 100, "CLAUDE.md seems too short"


class TestDirectoryStructure:
    """Verify expected directories exist."""

    @pytest.mark.parametrize("dirname", [
        ".claude",
        ".claude/skills",
        ".claude/skills/start",
        ".claude/scripts",
        "context",
        "projects",
    ])
    def test_directory_exists(self, dirname):
        assert (REPO_ROOT / dirname).is_dir(), f"Missing directory: {dirname}"

    @pytest.mark.parametrize("project", PROJECTS)
    def test_project_directory_exists(self, project):
        assert (REPO_ROOT / "projects" / project).is_dir(), \
            f"Missing project directory: projects/{project}"

    @pytest.mark.parametrize("project", PROJECTS)
    def test_project_modules_directory_exists(self, project):
        assert (REPO_ROOT / "projects" / project / "modules").is_dir(), \
            f"Missing modules directory: projects/{project}/modules"

    @pytest.mark.parametrize("project", PROJECTS)
    def test_project_readme_exists(self, project):
        assert (REPO_ROOT / "projects" / project / "README.md").is_file(), \
            f"Missing README: projects/{project}/README.md"


class TestClaudeDirectory:
    """Verify .claude directory structure."""

    @pytest.mark.parametrize("filename", [
        ".claude/settings.json",
        ".claude/skills/start/SKILL.md",
        ".claude/skills/doctor/SKILL.md",
        ".claude/skills/recap/SKILL.md",
        ".claude/scripts/welcome.js",
        ".claude/scripts/check-updates.js",
    ])
    def test_claude_file_exists(self, filename):
        assert (REPO_ROOT / filename).is_file(), f"Missing file: {filename}"


class TestGitignore:
    """Verify .gitignore has required entries."""

    def test_workspace_gitignored(self):
        content = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        assert "workspace/" in content, ".gitignore must exclude workspace/"

    def test_claude_local_md_gitignored(self):
        content = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        assert "CLAUDE.local.md" in content, ".gitignore must exclude CLAUDE.local.md"

    def test_onboarding_state_gitignored(self):
        content = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        assert "onboarding-state.json" in content, \
            ".gitignore must exclude onboarding-state.json"

    def test_settings_local_gitignored(self):
        content = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        assert "settings.local.json" in content, \
            ".gitignore must exclude settings.local.json"

    def test_tests_gitignored(self):
        content = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        assert "tests/" in content, ".gitignore must exclude tests/"
