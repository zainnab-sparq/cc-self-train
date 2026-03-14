"""Tests for cross-references between files — ensures nothing points to missing content."""

import re
import pytest
from conftest import REPO_ROOT, PROJECTS, CONTEXT_FILES


class TestClaudeMdReferences:
    """CLAUDE.md references must resolve to real files."""

    def test_context_files_listed_in_claudemd_exist(self):
        """Every context file mentioned in CLAUDE.md must exist."""
        for filename in CONTEXT_FILES:
            path = REPO_ROOT / "context" / filename
            assert path.is_file(), \
                f"CLAUDE.md references context/{filename} but it doesn't exist"

    def test_project_paths_in_claudemd(self):
        """CLAUDE.md must reference all 5 options."""
        content = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        for project in PROJECTS:
            assert f"projects/{project}" in content or project in content.lower(), \
                f"CLAUDE.md must reference project: {project}"


class TestSkillReferencesToContextFiles:
    """SKILL.md references to context/ must resolve."""

    def test_interactive_mode_reference(self):
        """SKILL.md references interactive-mode.txt (for keyboard shortcuts)."""
        path = REPO_ROOT / "context" / "interactive-mode.txt"
        assert path.is_file(), "context/interactive-mode.txt must exist"
        content = path.read_text(encoding="utf-8")
        assert len(content) > 100, "interactive-mode.txt seems too short"


class TestModuleCrossLinks:
    """Module files must reference the next module correctly."""

    @pytest.mark.parametrize("project", PROJECTS)
    def test_module1_links_to_module2(self, project):
        """Module 1 should mention Module 2 / 02-blueprint.md."""
        path = REPO_ROOT / "projects" / project / "modules" / "01-setup.md"
        content = path.read_text(encoding="utf-8")
        assert "02-blueprint" in content or "Module 2" in content, \
            f"{project}/01-setup.md must reference Module 2"


class TestContextFileIntegrity:
    """Context files must not be empty and should contain expected content."""

    @pytest.mark.parametrize("filename", CONTEXT_FILES)
    def test_context_file_not_empty(self, filename):
        path = REPO_ROOT / "context" / filename
        if path.is_file():
            size = path.stat().st_size
            if path.suffix in (".pdf", ".png", ".jpg"):
                assert size > 1000, \
                    f"context/{filename} is only {size} bytes — seems too small for a binary file"
            else:
                content = path.read_text(encoding="utf-8")
                assert len(content) > 50, \
                    f"context/{filename} seems too short ({len(content)} chars)"

    def test_hooks_txt_covers_all_events(self):
        """context/hooks.txt should mention key hook events."""
        path = REPO_ROOT / "context" / "hooks.txt"
        content = path.read_text(encoding="utf-8")
        for event in ["SessionStart", "PreToolUse", "PostToolUse", "Stop"]:
            assert event in content, \
                f"context/hooks.txt must mention hook event: {event}"

    def test_claudemd_txt_covers_hierarchy(self):
        """context/claudemd.txt should explain the memory hierarchy."""
        path = REPO_ROOT / "context" / "claudemd.txt"
        content = path.read_text(encoding="utf-8")
        assert "CLAUDE.md" in content, \
            "context/claudemd.txt must explain CLAUDE.md"

    def test_skillsmd_txt_covers_frontmatter(self):
        """context/skillsmd.txt should explain skill frontmatter."""
        path = REPO_ROOT / "context" / "skillsmd.txt"
        content = path.read_text(encoding="utf-8")
        assert "frontmatter" in content.lower() or "---" in content, \
            "context/skillsmd.txt must cover skill frontmatter"


class TestSkillToProjectMapping:
    """SKILL.md project names and directories must match actual project dirs."""

    @pytest.mark.parametrize("project,dirname", [
        ("Canvas", "canvas-site"),
        ("Forge", "forge-toolkit"),
        ("Nexus", "nexus-gateway"),
        ("Sentinel", "sentinel"),
    ])
    def test_skill_suggests_correct_directory(self, project, dirname):
        content = (REPO_ROOT / ".claude" / "skills" / "start" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert dirname in content, \
            f"SKILL.md must suggest workspace/{dirname} for {project}"
