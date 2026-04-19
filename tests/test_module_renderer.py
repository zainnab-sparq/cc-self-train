"""Integration tests for render-module.js preprocessor.

Exercises the renderer via `node` in a subprocess so we verify real behavior
(not a reimplemented Python mock). Each test writes a tiny fixture module
file + a CLAUDE.local.md with a specific Effective Level into a tmp dir,
runs the renderer with that dir as CLAUDE_PROJECT_DIR, and asserts on stdout.
"""

from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import textwrap

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
RENDERER = REPO_ROOT / ".claude" / "scripts" / "render-module.js"

NODE = shutil.which("node")

pytestmark = pytest.mark.skipif(
    NODE is None,
    reason="node runtime not found; renderer requires node to execute",
)


def _run(
    module_path: pathlib.Path, project_dir: pathlib.Path
) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["CLAUDE_PROJECT_DIR"] = str(project_dir)
    return subprocess.run(
        [NODE, str(RENDERER), str(module_path)],
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )


def _write_local(project_dir: pathlib.Path, body: str) -> None:
    (project_dir / "CLAUDE.local.md").write_text(body, encoding="utf-8")


def _write_module(project_dir: pathlib.Path, body: str) -> pathlib.Path:
    module = project_dir / "module.md"
    module.write_text(textwrap.dedent(body).lstrip("\n"), encoding="utf-8")
    return module


SAMPLE = """
    # Module 5

    Baseline paragraph shown to everyone.

    <!-- guide-only -->
    Here's the gentle beginner explanation: hooks are like event listeners.
    <!-- /guide-only -->

    Middle baseline paragraph.

    <!-- advanced-only -->
    See `context/hooks.txt` for the full event table.
    <!-- /advanced-only -->

    End paragraph.
    """


def test_beginner_sees_guide_strips_advanced(tmp_path):
    module = _write_module(tmp_path, SAMPLE)
    _write_local(tmp_path, "Effective Level: beginner\n")

    result = _run(module, tmp_path)

    assert result.returncode == 0, result.stderr
    assert "gentle beginner explanation" in result.stdout
    assert "full event table" not in result.stdout
    assert "Baseline paragraph" in result.stdout
    assert "End paragraph" in result.stdout


def test_intermediate_sees_guide_strips_advanced(tmp_path):
    module = _write_module(tmp_path, SAMPLE)
    _write_local(tmp_path, "Effective Level: intermediate\n")

    result = _run(module, tmp_path)

    assert result.returncode == 0, result.stderr
    assert "gentle beginner explanation" in result.stdout
    assert "full event table" not in result.stdout


def test_advanced_strips_guide_keeps_advanced(tmp_path):
    module = _write_module(tmp_path, SAMPLE)
    _write_local(tmp_path, "Effective Level: advanced\n")

    result = _run(module, tmp_path)

    assert result.returncode == 0, result.stderr
    assert "gentle beginner explanation" not in result.stdout
    assert "full event table" in result.stdout
    assert "Baseline paragraph" in result.stdout


def test_falls_back_to_experience_level_when_effective_absent(tmp_path):
    module = _write_module(tmp_path, SAMPLE)
    _write_local(tmp_path, "Experience Level: advanced\n")

    result = _run(module, tmp_path)

    assert result.returncode == 0, result.stderr
    assert "gentle beginner explanation" not in result.stdout
    assert "full event table" in result.stdout


def test_missing_claude_local_defaults_to_intermediate(tmp_path):
    module = _write_module(tmp_path, SAMPLE)
    # No CLAUDE.local.md written.

    result = _run(module, tmp_path)

    assert result.returncode == 0, result.stderr
    # Intermediate behavior: keep guide-only, strip advanced-only.
    assert "gentle beginner explanation" in result.stdout
    assert "full event table" not in result.stdout


def test_no_markers_passes_through_unchanged(tmp_path):
    content = "# Plain module\n\nJust some content.\n"
    module = tmp_path / "plain.md"
    module.write_text(content, encoding="utf-8")
    _write_local(tmp_path, "Effective Level: advanced\n")

    result = _run(module, tmp_path)

    assert result.returncode == 0, result.stderr
    assert result.stdout == content


def test_unbalanced_markers_exits_2(tmp_path):
    module = _write_module(
        tmp_path,
        """
        # Module

        <!-- guide-only -->
        Missing close tag.

        End.
        """,
    )
    _write_local(tmp_path, "Effective Level: advanced\n")

    result = _run(module, tmp_path)

    assert result.returncode == 2
    assert "Unbalanced" in result.stderr


def test_missing_file_exits_1(tmp_path):
    _write_local(tmp_path, "Effective Level: beginner\n")
    nonexistent = tmp_path / "nope.md"

    result = _run(nonexistent, tmp_path)

    assert result.returncode == 1
    assert "not found" in result.stderr.lower()


def test_multiple_guide_blocks_all_stripped_for_advanced(tmp_path):
    module = _write_module(
        tmp_path,
        """
        # Module

        <!-- guide-only -->
        First guide block.
        <!-- /guide-only -->

        Middle.

        <!-- guide-only -->
        Second guide block.
        <!-- /guide-only -->

        End.
        """,
    )
    _write_local(tmp_path, "Effective Level: advanced\n")

    result = _run(module, tmp_path)

    assert result.returncode == 0, result.stderr
    assert "First guide block" not in result.stdout
    assert "Second guide block" not in result.stdout
    assert "Middle." in result.stdout
    assert "End." in result.stdout


def test_unknown_level_value_defaults_to_intermediate(tmp_path):
    module = _write_module(tmp_path, SAMPLE)
    _write_local(tmp_path, "Effective Level: expert\n")  # not a valid value

    result = _run(module, tmp_path)

    assert result.returncode == 0, result.stderr
    # Falls through to intermediate default.
    assert "gentle beginner explanation" in result.stdout
    assert "full event table" not in result.stdout


def test_markers_never_leak_to_output(tmp_path):
    """Marker comments are implementation detail; they should never appear in
    any rendered output regardless of level."""
    module = _write_module(tmp_path, SAMPLE)
    for level in ("beginner", "intermediate", "advanced"):
        _write_local(tmp_path, f"Effective Level: {level}\n")
        result = _run(module, tmp_path)
        assert result.returncode == 0, result.stderr
        assert "<!-- guide-only -->" not in result.stdout, (
            f"guide-only open marker leaked at level={level}"
        )
        assert "<!-- /guide-only -->" not in result.stdout, (
            f"guide-only close marker leaked at level={level}"
        )
        assert "<!-- advanced-only -->" not in result.stdout, (
            f"advanced-only open marker leaked at level={level}"
        )
        assert "<!-- /advanced-only -->" not in result.stdout, (
            f"advanced-only close marker leaked at level={level}"
        )


def test_output_collapses_triple_blank_lines(tmp_path):
    module = _write_module(tmp_path, SAMPLE)
    _write_local(tmp_path, "Effective Level: advanced\n")

    result = _run(module, tmp_path)

    assert result.returncode == 0, result.stderr
    # After stripping the guide-only block, no run of 3+ consecutive newlines.
    assert "\n\n\n" not in result.stdout
