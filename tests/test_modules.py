"""Tests for module completeness and consistency across all 5 projects."""

import pathlib
import re
import pytest
from conftest import REPO_ROOT, PROJECTS, MODULE_FILES, MODULE_TITLES


class TestModuleCompleteness:
    """Every project must have all 10 modules."""

    @pytest.mark.parametrize("project", PROJECTS)
    @pytest.mark.parametrize("module_file", MODULE_FILES)
    def test_module_exists(self, project, module_file):
        path = REPO_ROOT / "projects" / project / "modules" / module_file
        assert path.is_file(), f"Missing module: projects/{project}/modules/{module_file}"

    @pytest.mark.parametrize("project", PROJECTS)
    def test_no_extra_modules(self, project):
        """No unexpected files in the modules directory."""
        modules_dir = REPO_ROOT / "projects" / project / "modules"
        actual = {f.name for f in modules_dir.iterdir() if f.is_file()}
        expected = set(MODULE_FILES)
        extra = actual - expected
        assert not extra, f"Unexpected files in {project}/modules/: {extra}"


class TestModuleStructure:
    """Every module file must follow the expected structure."""

    @pytest.mark.parametrize("project", PROJECTS)
    @pytest.mark.parametrize("module_file", MODULE_FILES)
    def test_module_has_h1_title(self, project, module_file):
        path = REPO_ROOT / "projects" / project / "modules" / module_file
        content = path.read_text(encoding="utf-8")
        assert content.startswith("# Module "), \
            f"{project}/{module_file} must start with '# Module '"

    @pytest.mark.parametrize("project", PROJECTS)
    @pytest.mark.parametrize("module_file", MODULE_FILES)
    def test_module_has_cc_features_line(self, project, module_file):
        path = REPO_ROOT / "projects" / project / "modules" / module_file
        content = path.read_text(encoding="utf-8")
        assert "**CC features:**" in content, \
            f"{project}/{module_file} must list CC features"

    @pytest.mark.parametrize("project", PROJECTS)
    @pytest.mark.parametrize("module_file", MODULE_FILES)
    def test_module_has_persona_line(self, project, module_file):
        path = REPO_ROOT / "projects" / project / "modules" / module_file
        content = path.read_text(encoding="utf-8")
        assert "**Persona" in content, \
            f"{project}/{module_file} must specify a persona"

    @pytest.mark.parametrize("project", PROJECTS)
    @pytest.mark.parametrize("module_file", MODULE_FILES)
    def test_module_not_empty(self, project, module_file):
        path = REPO_ROOT / "projects" / project / "modules" / module_file
        content = path.read_text(encoding="utf-8")
        assert len(content) > 200, \
            f"{project}/{module_file} seems too short ({len(content)} chars)"


class TestModuleNumbering:
    """Module numbering must be consistent."""

    @pytest.mark.parametrize("project", PROJECTS)
    @pytest.mark.parametrize("module_file", MODULE_FILES)
    def test_module_number_matches_filename(self, project, module_file):
        """The H1 title module number must match the filename number."""
        num = module_file.split("-")[0]  # "01", "02", etc.
        path = REPO_ROOT / "projects" / project / "modules" / module_file
        first_line = path.read_text(encoding="utf-8").split("\n")[0]
        assert f"Module {int(num)}" in first_line or f"Module {num}" in first_line, \
            f"{project}/{module_file}: H1 says '{first_line}' but filename says Module {num}"


class TestPersonaProgression:
    """Module files must have the default (intermediate) persona tag."""

    PERSONA_MAP = {
        "01": "Guide",
        "02": "Guide",
        "03": "Guide",
        "04": "Collaborator",
        "05": "Collaborator",
        "06": "Collaborator",
        "07": "Peer",
        "08": "Peer",
        "09": "Peer",
        "10": "Launcher",
    }

    @pytest.mark.parametrize("project", PROJECTS)
    @pytest.mark.parametrize("module_file", MODULE_FILES)
    def test_persona_matches_module(self, project, module_file):
        num = module_file.split("-")[0]
        expected_persona = self.PERSONA_MAP[num]
        path = REPO_ROOT / "projects" / project / "modules" / module_file
        content = path.read_text(encoding="utf-8")
        assert f"Persona -- {expected_persona}" in content or \
               f"Persona — {expected_persona}" in content, \
            f"{project}/{module_file}: expected persona '{expected_persona}'"


class TestAdaptivePersonaTable:
    """Adaptive persona boundaries must be consistent and well-ordered."""

    ADAPTIVE_MAP = {
        "beginner":     {"Guide": range(1, 5),  "Collaborator": range(5, 8),  "Peer": range(8, 10),  "Launcher": range(10, 11)},
        "intermediate": {"Guide": range(1, 4),  "Collaborator": range(4, 7),  "Peer": range(7, 10),  "Launcher": range(10, 11)},
        "advanced":     {"Guide": range(1, 2),  "Collaborator": range(2, 5),  "Peer": range(5, 10),  "Launcher": range(10, 11)},
    }

    PERSONA_ORDER = ["Guide", "Collaborator", "Peer", "Launcher"]

    @pytest.mark.parametrize("level", ["beginner", "intermediate", "advanced"])
    def test_all_levels_cover_all_modules(self, level):
        covered = set()
        for r in self.ADAPTIVE_MAP[level].values():
            covered.update(r)
        assert covered == set(range(1, 11)), \
            f"{level} doesn't cover all modules 1-10: missing {set(range(1, 11)) - covered}"

    @pytest.mark.parametrize("level", ["beginner", "intermediate", "advanced"])
    def test_module_10_always_launcher(self, level):
        assert 10 in self.ADAPTIVE_MAP[level]["Launcher"], \
            f"{level}: Module 10 should always be Launcher"

    def test_intermediate_matches_module_file_defaults(self):
        intermediate = self.ADAPTIVE_MAP["intermediate"]
        for num_str, expected in TestPersonaProgression.PERSONA_MAP.items():
            num = int(num_str)
            assert num in intermediate[expected], \
                f"Module {num}: intermediate map says {expected} but file default disagrees"

    @pytest.mark.parametrize("level", ["beginner", "intermediate", "advanced"])
    def test_persona_never_goes_backward(self, level):
        mapping = self.ADAPTIVE_MAP[level]
        for mod in range(1, 11):
            persona = next(p for p, r in mapping.items() if mod in r)
            idx = self.PERSONA_ORDER.index(persona)
            if mod < 10:
                next_persona = next(p for p, r in mapping.items() if (mod + 1) in r)
                next_idx = self.PERSONA_ORDER.index(next_persona)
                assert next_idx >= idx, \
                    f"{level}: persona goes backward from {persona} (mod {mod}) to {next_persona} (mod {mod+1})"

    def test_advanced_reaches_peer_earlier(self):
        adv_peer_start = min(self.ADAPTIVE_MAP["advanced"]["Peer"])
        int_peer_start = min(self.ADAPTIVE_MAP["intermediate"]["Peer"])
        assert adv_peer_start < int_peer_start, \
            "Advanced should reach Peer before intermediate"

    def test_beginner_stays_guide_longer(self):
        beg_guide_end = max(self.ADAPTIVE_MAP["beginner"]["Guide"])
        int_guide_end = max(self.ADAPTIVE_MAP["intermediate"]["Guide"])
        assert beg_guide_end > int_guide_end, \
            "Beginner should stay in Guide longer than intermediate"


class TestModuleConsistencyAcrossProjects:
    """All 5 projects should have matching CC features for each module."""

    @staticmethod
    def _extract_features(content: str) -> set[str]:
        """Extract CC features as a normalized set.

        Handles: backtick wrapping, line continuation, abbreviations.
        """
        lines = content.split("\n")
        raw = ""
        collecting = False
        for line in lines:
            if "**CC features:**" in line:
                raw = line.split("**CC features:**")[1]
                collecting = True
                continue
            if collecting:
                stripped = line.strip()
                # continuation line: doesn't start with **, #, or blank
                if stripped and not stripped.startswith("**") and not stripped.startswith("#"):
                    raw += " " + stripped
                else:
                    break
        # Normalize: strip backticks, lowercase, split by comma
        raw = raw.replace("`", "").strip()
        items = {f.strip().lower() for f in raw.split(",") if f.strip()}
        # Normalize common abbreviations
        normalized = set()
        for item in items:
            item = item.replace("git worktrees", "worktrees")
            item = item.replace("evaluation", "eval")
            normalized.add(item)
        return normalized

    @pytest.mark.parametrize("module_file", MODULE_FILES)
    def test_cc_features_match_across_projects(self, module_file):
        """The CC features should cover the same topics across all 5 projects."""
        features = {}
        for project in PROJECTS:
            path = REPO_ROOT / "projects" / project / "modules" / module_file
            content = path.read_text(encoding="utf-8")
            features[project] = self._extract_features(content)

        # Use the first project as reference
        reference = features[PROJECTS[0]]
        for project in PROJECTS[1:]:
            diff = reference.symmetric_difference(features[project])
            assert not diff, \
                f"{module_file}: CC features differ between {PROJECTS[0]} and {project}: {diff}"
