"""Integration tests for the adaptive persona system.

These tests exercise the three hook scripts end-to-end (no mocking) to verify
the adaptive system actually fires and produces the documented state:

  observe-interaction.js   Stop hook               -> learner-profile.json writes
  learner-streak-check.js  UserPromptSubmit hook  -> struggle/engagement alerts
  learner-context.js       SessionStart hook      -> engagement narrative

Tests run each script via `node` in a subprocess with cwd set to a temporary
directory so the real repo's learner-profile.json is never touched.
"""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / ".claude" / "scripts"
OBSERVE = SCRIPTS / "observe-interaction.js"
STREAK_CHECK = SCRIPTS / "learner-streak-check.js"
CONTEXT = SCRIPTS / "learner-context.js"

NODE = shutil.which("node")

pytestmark = pytest.mark.skipif(
    NODE is None,
    reason="node runtime not found; adaptive hooks require node to execute",
)


def _write_transcript(path: pathlib.Path, user_msg: str, assistant_msg: str = "ok") -> None:
    """Write a two-line JSONL transcript: one user message, one assistant reply.

    Format mirrors what Claude Code writes to `transcript_path` — each line a
    JSON object with `type` ('human' or 'assistant') and a `message` field.
    """
    lines = [
        json.dumps({"type": "human", "message": user_msg}),
        json.dumps({"type": "assistant", "message": assistant_msg}),
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _run_observe(cwd: pathlib.Path, transcript_path: pathlib.Path) -> subprocess.CompletedProcess:
    payload = json.dumps({"transcript_path": str(transcript_path)})
    return subprocess.run(
        [NODE, str(OBSERVE)],
        cwd=cwd,
        input=payload,
        capture_output=True,
        text=True,
        timeout=10,
    )


def _run_streak_check(cwd: pathlib.Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [NODE, str(STREAK_CHECK)],
        cwd=cwd,
        input="",
        capture_output=True,
        text=True,
        timeout=5,
    )


def _run_context(cwd: pathlib.Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [NODE, str(CONTEXT)],
        cwd=cwd,
        input="",
        capture_output=True,
        text=True,
        timeout=5,
    )


def _profile(cwd: pathlib.Path) -> dict:
    return json.loads((cwd / "learner-profile.json").read_text(encoding="utf-8"))


# --- observe-interaction.js -------------------------------------------------


def test_observe_classifies_concept_question(tmp_path):
    transcript = tmp_path / "transcript.jsonl"
    _write_transcript(transcript, "Why does plan mode prevent writes?")

    result = _run_observe(tmp_path, transcript)

    assert result.returncode == 0, result.stderr
    profile = _profile(tmp_path)
    assert profile["interactions"]["concept_question"] == 1
    assert profile["qualityScores"] == [5]


def test_observe_classifies_answer_seeking(tmp_path):
    transcript = tmp_path / "transcript.jsonl"
    _write_transcript(transcript, "just do it for me")

    result = _run_observe(tmp_path, transcript)

    assert result.returncode == 0, result.stderr
    profile = _profile(tmp_path)
    assert profile["interactions"]["answer_seeking"] == 1
    assert profile["qualityScores"] == [1]


def test_observe_accumulates_across_runs_and_detects_struggle_streak(tmp_path):
    transcript = tmp_path / "transcript.jsonl"

    for msg in ["just do it", "just write it", "just fix it"]:
        _write_transcript(transcript, msg)
        result = _run_observe(tmp_path, transcript)
        assert result.returncode == 0, result.stderr

    profile = _profile(tmp_path)
    assert profile["interactions"]["answer_seeking"] == 3
    assert profile["struggleStreak"] is True
    assert profile["engagementStreak"] is False


def test_observe_detects_engagement_streak(tmp_path):
    transcript = tmp_path / "transcript.jsonl"

    for msg in [
        "Why does this pattern work?",
        "I tried running the tests and they pass.",
        "Can you explain the difference between skills and commands?",
    ]:
        _write_transcript(transcript, msg)
        result = _run_observe(tmp_path, transcript)
        assert result.returncode == 0, result.stderr

    profile = _profile(tmp_path)
    assert profile["engagementStreak"] is True
    assert profile["struggleStreak"] is False


# --- learner-streak-check.js ------------------------------------------------


def _seed_profile(cwd: pathlib.Path, **overrides) -> None:
    profile = {
        "currentModule": 1,
        "interactions": {
            "concept_question": 0,
            "independent_exploration": 0,
            "debug_attempt": 0,
            "answer_seeking": 0,
            "passive_acceptance": 0,
            "neutral": 0,
        },
        "moduleInteractions": {
            "concept_question": 0,
            "independent_exploration": 0,
            "debug_attempt": 0,
            "answer_seeking": 0,
            "passive_acceptance": 0,
            "neutral": 0,
        },
        "qualityScores": [],
        "moduleQualityScores": [],
        "recentCategories": [],
        "struggleStreak": False,
        "engagementStreak": False,
        "averageQuality": 0,
        "moduleAverageQuality": 0,
        "recentTrend": "not yet measured",
        "lastUpdated": "2026-04-16T00:00:00.000Z",
    }
    profile.update(overrides)
    (cwd / "learner-profile.json").write_text(json.dumps(profile), encoding="utf-8")


def test_streak_check_emits_alert_on_struggle_transition(tmp_path):
    _seed_profile(tmp_path, struggleStreak=True)

    result = _run_streak_check(tmp_path)

    assert result.returncode == 0, result.stderr
    assert "STRUGGLE STREAK" in result.stdout
    profile = _profile(tmp_path)
    assert profile["lastAnnouncedStreak"] == "struggle"


def test_streak_check_silent_when_no_profile(tmp_path):
    result = _run_streak_check(tmp_path)

    assert result.returncode == 0
    assert result.stdout == ""


def test_streak_check_silent_when_state_unchanged(tmp_path):
    _seed_profile(tmp_path, struggleStreak=True, lastAnnouncedStreak="struggle")

    result = _run_streak_check(tmp_path)

    assert result.returncode == 0
    assert result.stdout == ""


def test_streak_check_emits_engagement_alert(tmp_path):
    _seed_profile(tmp_path, engagementStreak=True)

    result = _run_streak_check(tmp_path)

    assert result.returncode == 0
    assert "ENGAGEMENT STREAK" in result.stdout


# --- learner-context.js -----------------------------------------------------


def test_context_silent_when_history_too_small(tmp_path):
    _seed_profile(tmp_path)

    result = _run_context(tmp_path)

    assert result.returncode == 0
    assert result.stdout == ""


def test_context_injects_narrative_with_engagement_history(tmp_path):
    interactions = {
        "concept_question": 5,
        "independent_exploration": 3,
        "debug_attempt": 1,
        "answer_seeking": 0,
        "passive_acceptance": 0,
        "neutral": 0,
    }
    _seed_profile(
        tmp_path,
        interactions=interactions,
        moduleAverageQuality=4.5,
        recentTrend="improving",
    )

    result = _run_context(tmp_path)

    assert result.returncode == 0
    assert "LEARNER PROFILE" in result.stdout
    assert "strong engagement" in result.stdout.lower()
    assert "improving" in result.stdout


def test_context_injects_scaffolding_note_for_struggle(tmp_path):
    interactions = {
        "concept_question": 0,
        "independent_exploration": 0,
        "debug_attempt": 0,
        "answer_seeking": 6,
        "passive_acceptance": 0,
        "neutral": 0,
    }
    _seed_profile(
        tmp_path,
        interactions=interactions,
        moduleAverageQuality=1.0,
        recentTrend="declining",
    )

    result = _run_context(tmp_path)

    assert result.returncode == 0
    assert "LEARNER PROFILE" in result.stdout
    assert "scaffolding" in result.stdout.lower() or "guiding questions" in result.stdout.lower()


# --- End-to-end flow --------------------------------------------------------


# --- Banner queueing (observe-interaction.js PR #3 addition) ---------------


def test_observe_queues_banner_on_struggle_streak_transition(tmp_path):
    transcript = tmp_path / "transcript.jsonl"
    for msg in ["just do it", "just write it", "just fix it"]:
        _write_transcript(transcript, msg)
        assert _run_observe(tmp_path, transcript).returncode == 0

    profile = _profile(tmp_path)
    assert profile["struggleStreak"] is True
    assert len(profile["pendingBanners"]) == 1
    banner = profile["pendingBanners"][0]
    assert banner["type"] == "struggle"
    assert banner["acknowledged"] is False
    assert "created" in banner


def test_observe_queues_banner_on_engagement_streak_transition(tmp_path):
    transcript = tmp_path / "transcript.jsonl"
    for msg in [
        "Why does this work?",
        "I tried running it and noticed something.",
        "Can you explain the difference?",
    ]:
        _write_transcript(transcript, msg)
        assert _run_observe(tmp_path, transcript).returncode == 0

    profile = _profile(tmp_path)
    assert profile["engagementStreak"] is True
    assert len(profile["pendingBanners"]) == 1
    assert profile["pendingBanners"][0]["type"] == "engagement"


def test_observe_does_not_requeue_banner_while_streak_continues(tmp_path):
    transcript = tmp_path / "transcript.jsonl"
    # Trigger the streak.
    for msg in ["just do it", "just write it", "just fix it"]:
        _write_transcript(transcript, msg)
        assert _run_observe(tmp_path, transcript).returncode == 0
    # One more answer_seeking -- streak is still active but no NEW transition.
    _write_transcript(transcript, "just create it")
    assert _run_observe(tmp_path, transcript).returncode == 0

    profile = _profile(tmp_path)
    assert profile["struggleStreak"] is True
    assert len(profile["pendingBanners"]) == 1, "banner should fire once per entry, not per turn"


# --- Banner emission (learner-context.js PR #3 addition) -------------------


def _banner_profile(created_iso: str, *, acknowledged: bool = False, banner_type: str = "struggle") -> dict:
    return {
        "pendingBanners": [
            {"type": banner_type, "created": created_iso, "acknowledged": acknowledged},
        ],
    }


def test_context_emits_pending_banner_and_marks_acknowledged(tmp_path):
    import datetime
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    _seed_profile(tmp_path, **_banner_profile(now_iso, banner_type="struggle"))

    result = _run_context(tmp_path)

    assert result.returncode == 0
    assert "SHOW TO LEARNER" in result.stdout
    assert "struggle" in result.stdout.lower()
    profile = _profile(tmp_path)
    assert profile["pendingBanners"][0]["acknowledged"] is True


def test_context_skips_already_acknowledged_banner(tmp_path):
    import datetime
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    _seed_profile(tmp_path, **_banner_profile(now_iso, acknowledged=True))

    result = _run_context(tmp_path)

    assert result.returncode == 0
    assert "SHOW TO LEARNER" not in result.stdout


def test_context_marks_stale_banner_acknowledged_without_emitting(tmp_path):
    import datetime
    two_days_ago = (
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)
    ).isoformat()
    _seed_profile(tmp_path, **_banner_profile(two_days_ago))

    result = _run_context(tmp_path)

    assert result.returncode == 0
    assert "SHOW TO LEARNER" not in result.stdout
    profile = _profile(tmp_path)
    assert profile["pendingBanners"][0]["acknowledged"] is True


def test_context_emits_banner_before_narrative_threshold(tmp_path):
    import datetime
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # Only 3 non-neutral interactions -- below the 5 threshold for the
    # narrative, but banner should still fire.
    interactions = {
        "concept_question": 0,
        "independent_exploration": 0,
        "debug_attempt": 0,
        "answer_seeking": 3,
        "passive_acceptance": 0,
        "neutral": 0,
    }
    _seed_profile(
        tmp_path,
        interactions=interactions,
        **_banner_profile(now_iso, banner_type="struggle"),
    )

    result = _run_context(tmp_path)

    assert result.returncode == 0
    assert "SHOW TO LEARNER" in result.stdout
    assert "LEARNER PROFILE" not in result.stdout  # narrative still gated


def test_end_to_end_observe_then_streak_then_context(tmp_path):
    """Simulate a full session: observe fires 3 times (struggle), streak-check
    emits an alert, then SessionStart context injects the narrative."""
    transcript = tmp_path / "transcript.jsonl"

    for msg in ["just do it", "just write it", "just fix it"]:
        _write_transcript(transcript, msg)
        assert _run_observe(tmp_path, transcript).returncode == 0

    # Need >= 5 non-neutral interactions for context to emit; add two more.
    for msg in ["just create it", "just make it"]:
        _write_transcript(transcript, msg)
        assert _run_observe(tmp_path, transcript).returncode == 0

    profile = _profile(tmp_path)
    assert profile["struggleStreak"] is True
    assert profile["interactions"]["answer_seeking"] == 5

    streak_result = _run_streak_check(tmp_path)
    assert "STRUGGLE STREAK" in streak_result.stdout

    context_result = _run_context(tmp_path)
    assert "LEARNER PROFILE" in context_result.stdout
    assert "STRUGGLE STREAK" in context_result.stdout
