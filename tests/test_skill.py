"""Tests for SKILL.md structural integrity and required content."""

import re
import pytest
from conftest import REPO_ROOT


def _read_skill():
    return (REPO_ROOT / ".claude" / "skills" / "start" / "SKILL.md").read_text(
        encoding="utf-8"
    )


class TestSkillFrontmatter:
    """SKILL.md must have valid frontmatter."""

    def test_starts_with_frontmatter(self):
        content = _read_skill()
        assert content.startswith("---"), "SKILL.md must start with --- frontmatter"

    def test_frontmatter_has_name(self):
        content = _read_skill()
        assert "name: start" in content, "Frontmatter must have name: start"

    def test_frontmatter_has_description(self):
        content = _read_skill()
        assert "description:" in content, "Frontmatter must have a description"

    def test_frontmatter_disables_model_invocation(self):
        content = _read_skill()
        assert "disable-model-invocation: true" in content, \
            "SKILL.md should have disable-model-invocation: true"


class TestSkillSteps:
    """SKILL.md must contain all required steps."""

    @pytest.mark.parametrize("step_header", [
        "## Step 1:",
        "## Step 1b:",
        "## Step 2:",
        "## Step 2b:",
        "## Step 3:",
        "## Step 3b:",
        "## Step 4:",
        "## Step 5:",
        "## Step 6:",
    ])
    def test_step_exists(self, step_header):
        content = _read_skill()
        assert step_header in content, f"SKILL.md missing step: {step_header}"

    @pytest.mark.parametrize("substep", [
        "### 6.1",
        "### 6.2",
        "### 6.3",
        "### 6.4",
        "### 6.5",
        "### 6.6",
        "### 6.7",
        "### 6.8",
        "### 6.9",
    ])
    def test_module1_substep_exists(self, substep):
        content = _read_skill()
        assert substep in content, f"SKILL.md missing substep: {substep}"


class TestSkillPacing:
    """SKILL.md must enforce the pacing rule."""

    def test_pacing_rule_exists(self):
        content = _read_skill()
        assert "PACING" in content, "SKILL.md must have a pacing rule"

    def test_stop_instructions_between_substeps(self):
        """Each substep 6.1-6.7 should have a STOP instruction."""
        content = _read_skill()
        for i in range(1, 9):  # 6.1 through 6.8
            section_marker = f"### 6.{i}"
            next_marker = f"### 6.{i + 1}"
            start = content.index(section_marker)
            end = content.index(next_marker)
            section = content[start:end]
            assert "STOP" in section.upper(), \
                f"Substep 6.{i} must have a STOP instruction"


class TestSkillContent:
    """SKILL.md must contain specific critical content."""

    def test_five_options_listed(self):
        content = _read_skill()
        for project in ["Canvas", "Forge", "Nexus", "Sentinel", "Your Own Project"]:
            assert project in content, f"SKILL.md must mention option: {project}"

    def test_canvas_recommended(self):
        content = _read_skill()
        assert "Recommended" in content, \
            "Canvas should be marked as recommended for first-timers"

    def test_os_detection(self):
        content = _read_skill()
        assert "uname" in content or "Detect" in content.lower() or "detect" in content, \
            "SKILL.md must include OS detection"

    def test_experience_levels(self):
        content = _read_skill()
        for level in ["beginner", "intermediate", "advanced"]:
            assert level in content, f"SKILL.md must mention experience level: {level}"

    def test_environment_options(self):
        content = _read_skill()
        for env in ["venv", "conda", "Docker"]:
            assert env in content, f"SKILL.md must mention environment: {env}"


class TestSkillGitConfig:
    """SKILL.md must check git config before first commit."""

    def test_git_config_check_exists(self):
        content = _read_skill()
        assert "git config user.name" in content, \
            "SKILL.md must check git config user.name"
        assert "git config user.email" in content, \
            "SKILL.md must check git config user.email"

    def test_git_config_before_commit(self):
        """Git config check must appear BEFORE the git commit command."""
        content = _read_skill()
        config_pos = content.index("git config user.name")
        commit_pos = content.index('git commit -m "Initial project setup')
        assert config_pos < commit_pos, \
            "Git config check must come before the initial commit"


class TestSkillResumeCapability:
    """SKILL.md must support resume via onboarding-state.json."""

    def test_onboarding_state_mentioned(self):
        content = _read_skill()
        assert "onboarding-state.json" in content, \
            "SKILL.md must reference onboarding-state.json"

    def test_step_3b_exists(self):
        content = _read_skill()
        assert "## Step 3b:" in content, \
            "SKILL.md must have Step 3b for resume check"

    def test_resume_message(self):
        content = _read_skill()
        assert "Welcome back" in content, \
            "SKILL.md must have a 'Welcome back' message for resume"

    def test_currentstep_tracking(self):
        content = _read_skill()
        assert "currentStep" in content, \
            "SKILL.md must track currentStep in onboarding state"

    def test_state_json_schema(self):
        """The onboarding state JSON must include all required fields."""
        content = _read_skill()
        for field in ["project", "language", "os", "environment",
                       "experienceLevel", "currentStep", "packageManager"]:
            assert f'"{field}"' in content, \
                f"Onboarding state JSON must include field: {field}"

    def test_step_3b_runs_before_step_1(self):
        """Step 3b instructions must say to run BEFORE Steps 1-3."""
        content = _read_skill()
        step3b_start = content.index("## Step 3b:")
        step3b_section = content[step3b_start:step3b_start + 500]
        assert "BEFORE" in step3b_section, \
            "Step 3b must specify it runs BEFORE Steps 1-3"


class TestSkillModuleCompletionPattern:
    """SKILL.md must instruct all modules to end with 'next module' prompt."""

    def test_module_completion_pattern_exists(self):
        content = _read_skill()
        assert "Module completion pattern" in content, \
            "SKILL.md must have a module completion pattern instruction"

    def test_next_module_prompt(self):
        content = _read_skill()
        assert '"next module"' in content or "**next module**" in content.lower() or \
               '**"next module"**' in content, \
            "SKILL.md must instruct delivery of 'next module' prompt"

    def test_module10_exception(self):
        content = _read_skill()
        assert "Module 10" in content and "completion" in content.lower(), \
            "SKILL.md must handle Module 10 differently (course completion)"

    def test_claude_local_md_update(self):
        """Must instruct updating CLAUDE.local.md after module completion."""
        content = _read_skill()
        # Find the module completion pattern section
        assert "Current Module" in content and "CLAUDE.local.md" in content, \
            "SKILL.md must instruct updating Current Module in CLAUDE.local.md"


class TestSkillInstallTable:
    """SKILL.md must have install commands for all platforms."""

    def test_install_table_exists(self):
        content = _read_skill()
        assert "brew" in content, "SKILL.md must mention brew (macOS)"
        assert "winget" in content, "SKILL.md must mention winget (Windows)"
        assert "apt" in content or "apt-get" in content, \
            "SKILL.md must mention apt (Linux)"

    @pytest.mark.parametrize("tool", ["git", "python", "node", "go", "rust", "sqlite3"])
    def test_install_command_for_tool(self, tool):
        content = _read_skill()
        assert tool in content.lower(), f"SKILL.md must have install info for: {tool}"

    def test_conda_auto_install(self):
        content = _read_skill()
        assert "miniconda" in content.lower() or "Miniconda" in content, \
            "SKILL.md must support conda/Miniconda auto-install"

    def test_docker_auto_install(self):
        content = _read_skill()
        assert "docker" in content.lower(), \
            "SKILL.md must support Docker auto-install"


class TestSkillScaffold:
    """SKILL.md must scaffold correctly for each project."""

    def test_canvas_scaffold(self):
        content = _read_skill()
        for filename in ["index.html", "main.css", "main.js"]:
            assert filename in content, \
                f"Canvas scaffold must create: {filename}"

    def test_canvas_no_package_json(self):
        """Canvas should NOT instruct creating a package.json."""
        content = _read_skill()
        # Find the Canvas scaffold section
        canvas_idx = content.index("chose Canvas**, scaffold")
        next_section = content.index("**For all other projects**")
        canvas_section = content[canvas_idx:next_section]
        # "No package.json" is fine — it's an explicit exclusion.
        # We only fail if the section tells Claude to CREATE one.
        mentions = [line for line in canvas_section.split("\n")
                    if "package.json" in line]
        for mention in mentions:
            assert "no package.json" in mention.lower(), \
                f"Canvas scaffold must NOT create package.json, but found: {mention.strip()}"

    def test_workspace_directory(self):
        content = _read_skill()
        assert "workspace/" in content, \
            "SKILL.md must scaffold inside workspace/"
