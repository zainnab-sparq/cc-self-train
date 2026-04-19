"""Shared fixtures for cc-self-train repo tests."""

import pathlib
import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

PROJECTS = ["canvas", "forge", "nexus", "sentinel", "byop"]

MODULE_FILES = [
    "01-setup.md",
    "02-blueprint.md",
    "03-rules-memory-context.md",
    "04-skills-commands.md",
    "05-hooks.md",
    "06-mcp-servers.md",
    "07-guard-rails.md",
    "08-subagents.md",
    "09-tasks-tdd.md",
    "10-parallel-plugins-eval.md",
]

MODULE_TITLES = {
    "01": "Setup",
    "02": "Blueprint",
    "03": "Rules",
    "04": "Skills",
    "05": "Hooks",
    "06": "MCP",
    "07": "Guard",
    "08": "Subagents",
    "09": "Tasks",
    "10": "Parallel",
}

# All context files that should exist (single source of truth)
CONTEXT_FILES = [
    "anthropic-basics.txt",
    "changelog-cc.txt",
    "claudemd.txt",
    "skillsmd.txt",
    "hooks.txt",
    "configure-hooks.txt",
    "subagents.txt",
    "agent-teams.txt",
    "plugins.txt",
    "tasks.txt",
    "mcp.txt",
    "skills-plus-mcp.txt",
    "interactive-mode.txt",
    "common-workflows.txt",
    "when-to-use-features.txt",
    "boris-workflow.txt",
    "sl-guide.txt",
    "auto-memory.txt",
    "ide-integration.txt",
    "models.txt",
    "prompt.txt",
    "security.txt",
    "The-Complete-Guide-to-Building-Skill-for-Claude.pdf",
]


@pytest.fixture
def repo_root():
    return REPO_ROOT


@pytest.fixture(params=PROJECTS)
def project(request):
    return request.param


@pytest.fixture(params=MODULE_FILES)
def module_file(request):
    return request.param
