"""Tests for the /doctor and /recap skills."""

import pytest
from conftest import REPO_ROOT


class TestDoctorSkill:
    """Verify /doctor skill structure."""

    def test_doctor_has_frontmatter(self):
        content = (REPO_ROOT / ".claude" / "skills" / "doctor" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert content.startswith("---"), "/doctor SKILL.md must start with frontmatter"
        assert "name: doctor" in content

    def test_doctor_checks_claudelocal(self):
        content = (REPO_ROOT / ".claude" / "skills" / "doctor" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert "CLAUDE.local.md" in content, \
            "/doctor must check for CLAUDE.local.md"

    def test_doctor_checks_workspace(self):
        content = (REPO_ROOT / ".claude" / "skills" / "doctor" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert "workspace" in content.lower(), \
            "/doctor must check workspace directory"

    def test_doctor_checks_git(self):
        content = (REPO_ROOT / ".claude" / "skills" / "doctor" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert "git" in content.lower(), "/doctor must check git status"


class TestRecapSkill:
    """Verify /recap skill structure."""

    def test_recap_has_frontmatter(self):
        content = (REPO_ROOT / ".claude" / "skills" / "recap" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert content.startswith("---"), "/recap SKILL.md must start with frontmatter"
        assert "name: recap" in content

    def test_recap_reads_modules(self):
        content = (REPO_ROOT / ".claude" / "skills" / "recap" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert "modules" in content.lower(), \
            "/recap must read completed module files"

    def test_recap_reads_claudelocal(self):
        content = (REPO_ROOT / ".claude" / "skills" / "recap" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert "CLAUDE.local.md" in content, \
            "/recap must read CLAUDE.local.md for progress"
