"""Tests for context/ reference documentation completeness."""

import pathlib
import pytest
from conftest import REPO_ROOT, CONTEXT_FILES


class TestContextCompleteness:
    """All expected context files must exist."""

    @pytest.mark.parametrize("filename", CONTEXT_FILES)
    def test_context_file_exists(self, filename):
        path = REPO_ROOT / "context" / filename
        assert path.is_file(), f"Missing context file: context/{filename}"

    @pytest.mark.parametrize("filename", CONTEXT_FILES)
    def test_context_file_not_trivially_small(self, filename):
        """Context files should have substantive content."""
        path = REPO_ROOT / "context" / filename
        if path.is_file():
            size = path.stat().st_size
            assert size > 100, \
                f"context/{filename} is only {size} bytes — seems too small"

    def test_no_unexpected_context_files(self):
        """Flag any context files not in the expected list (warning, not fail)."""
        context_dir = REPO_ROOT / "context"
        actual = {f.name for f in context_dir.iterdir() if f.is_file()}
        expected = set(CONTEXT_FILES)
        extra = actual - expected
        # This is informational — extra files aren't necessarily wrong
        # but we want to know about them
        if extra:
            pytest.skip(f"Extra context files found (may be intentional): {extra}")


class TestContextForModuleTopics:
    """Each module topic should have a matching context file."""

    def test_hooks_context_exists(self):
        """Module 5 teaches hooks — context/hooks.txt must exist."""
        assert (REPO_ROOT / "context" / "hooks.txt").is_file()

    def test_mcp_context_exists(self):
        """Module 6 teaches MCP — context/mcp.txt must exist."""
        assert (REPO_ROOT / "context" / "mcp.txt").is_file()

    def test_subagents_context_exists(self):
        """Module 8 teaches subagents — context/subagents.txt must exist."""
        assert (REPO_ROOT / "context" / "subagents.txt").is_file()

    def test_tasks_context_exists(self):
        """Module 9 teaches tasks — context/tasks.txt must exist."""
        assert (REPO_ROOT / "context" / "tasks.txt").is_file()

    def test_skills_context_exists(self):
        """Module 4 teaches skills — context/skillsmd.txt must exist."""
        assert (REPO_ROOT / "context" / "skillsmd.txt").is_file()

    def test_plugins_context_exists(self):
        """Module 10 teaches plugins — context/plugins.txt must exist."""
        assert (REPO_ROOT / "context" / "plugins.txt").is_file()

    def test_interactive_mode_context_exists(self):
        """Module 1 teaches keyboard shortcuts — context/interactive-mode.txt must exist."""
        assert (REPO_ROOT / "context" / "interactive-mode.txt").is_file()
