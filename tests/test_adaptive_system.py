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
MODULE_BOUNDARY = SCRIPTS / "module-boundary.js"

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


def _run_module_boundary(cwd: pathlib.Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [NODE, str(MODULE_BOUNDARY)],
        cwd=cwd,
        input="",
        capture_output=True,
        text=True,
        timeout=5,
    )


def _seed_claude_local(cwd: pathlib.Path, experience: str = "beginner", effective: str = None) -> None:
    effective = effective if effective is not None else experience
    content = (
        "# Active Project\n"
        "Project: Canvas | Language: HTML/CSS/JS | OS: Windows | Directory: workspace/x | Current Module: 2\n"
        f"Experience Level: {experience}\n"
        f"Effective Level: {effective}\n"
        "Engagement Trend: not yet measured\n"
    )
    (cwd / "CLAUDE.local.md").write_text(content, encoding="utf-8")


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


# --- classifier honesty improvements (consolidated-signals T3.2) ----------


def _write_transcript_with_long_assistant(path: pathlib.Path, user_msg: str) -> None:
    """Variant that puts a long assistant message first so the 'short reply
    to long assistant' heuristic (passive_acceptance) is live. Used to prove
    the ack allowlist bypasses passive_acceptance for real acks."""
    long_assistant = "Here's the plan. " * 60  # ~1000 chars, well over the 500 threshold
    lines = [
        json.dumps({"type": "assistant", "message": long_assistant}),
        json.dumps({"type": "human", "message": user_msg}),
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_observe_ack_allowlist_bypasses_passive_acceptance(tmp_path):
    """Short ack ('ship it') after a long assistant message should classify
    as neutral, not passive_acceptance. Reeves v2 quantified this as a
    major misclassification source for senior engineers."""
    transcript = tmp_path / "transcript.jsonl"
    _write_transcript_with_long_assistant(transcript, "ship it")

    result = _run_observe(tmp_path, transcript)

    assert result.returncode == 0, result.stderr
    profile = _profile(tmp_path)
    assert profile["interactions"]["neutral"] == 1
    assert profile["interactions"]["passive_acceptance"] == 0


def test_observe_ack_allowlist_handles_common_variants(tmp_path):
    """Multiple common ack forms all route to neutral."""
    transcript = tmp_path / "transcript.jsonl"
    for ack in ["lgtm", "ok", "next", "thanks.", "sgtm", "sounds good"]:
        _write_transcript_with_long_assistant(transcript, ack)
        assert _run_observe(tmp_path, transcript).returncode == 0

    profile = _profile(tmp_path)
    assert profile["interactions"]["neutral"] == 6
    assert profile["interactions"]["passive_acceptance"] == 0


def test_observe_long_conceptual_question_without_keywords(tmp_path):
    """A long well-phrased conceptual question that doesn't hit any of
    the short keyword patterns should still classify as concept_question,
    not fall through to neutral. Must avoid debugPatterns words like 'bug'
    and 'issue' which would short-circuit to debug_attempt."""
    transcript = tmp_path / "transcript.jsonl"
    long_msg = (
        "Walk me through the failure mode when a PreToolUse hook returns "
        "a permissionDecision of 'allow' but the underlying script had a "
        "subtle implementation flaw that prevented its deny branch from "
        "ever being reachable. I want to understand what Claude Code sees "
        "and why this looks identical to a correctly-written allow path "
        "from the outside."
    )
    _write_transcript(transcript, long_msg)

    result = _run_observe(tmp_path, transcript)

    assert result.returncode == 0
    profile = _profile(tmp_path)
    assert profile["interactions"]["concept_question"] == 1


def test_observe_long_first_person_exploration_without_keywords(tmp_path):
    """A long first-person exploration message that doesn't hit the short
    'i tried' / 'i noticed' patterns should still classify as exploration.
    Must avoid longConceptMarkers (why/how/what/walk me) which would
    match first."""
    transcript = tmp_path / "transcript.jsonl"
    long_msg = (
        "I'm thinking about the data flow between the stop hook and the "
        "streak-check hook. My hypothesis is that the race is prevented "
        "by the lock file but only if both hooks agree on its location. "
        "I'm wondering whether the lock path should be per-project or "
        "global, and whether the lastAnnouncedStreak field interacts with "
        "the first run after the file is created."
    )
    _write_transcript(transcript, long_msg)

    result = _run_observe(tmp_path, transcript)

    assert result.returncode == 0
    profile = _profile(tmp_path)
    assert profile["interactions"]["independent_exploration"] == 1


def test_observe_short_non_ack_still_passive_acceptance(tmp_path):
    """Regression guard: the ack allowlist must not over-match. A short
    reply that isn't in the allowlist after a long assistant message
    should still classify as passive_acceptance."""
    transcript = tmp_path / "transcript.jsonl"
    _write_transcript_with_long_assistant(transcript, "hmm")

    result = _run_observe(tmp_path, transcript)

    assert result.returncode == 0
    profile = _profile(tmp_path)
    assert profile["interactions"]["passive_acceptance"] == 1


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


# --- module-boundary.js (PR #5) -------------------------------------------


def test_module_boundary_bumps_level_up_on_high_engagement(tmp_path):
    _seed_claude_local(tmp_path, experience="beginner", effective="beginner")
    _seed_profile(
        tmp_path,
        currentModule=2,
        moduleAverageQuality=4.5,
        moduleInteractions={
            "concept_question": 4,
            "independent_exploration": 3,
            "debug_attempt": 1,
            "answer_seeking": 1,
            "passive_acceptance": 0,
            "neutral": 0,
        },
    )

    result = _run_module_boundary(tmp_path)

    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["levelChanged"] is True
    assert summary["oldLevel"] == "beginner"
    assert summary["newLevel"] == "intermediate"
    claude_local = (tmp_path / "CLAUDE.local.md").read_text(encoding="utf-8")
    assert "Effective Level: intermediate" in claude_local


def test_module_boundary_bumps_level_down_on_low_engagement(tmp_path):
    _seed_claude_local(tmp_path, experience="intermediate", effective="intermediate")
    _seed_profile(
        tmp_path,
        currentModule=3,
        moduleAverageQuality=1.5,
        moduleInteractions={
            "concept_question": 0,
            "independent_exploration": 0,
            "debug_attempt": 1,
            "answer_seeking": 4,
            "passive_acceptance": 2,
            "neutral": 0,
        },
    )

    result = _run_module_boundary(tmp_path)

    summary = json.loads(result.stdout)
    assert summary["levelChanged"] is True
    assert summary["newLevel"] == "beginner"
    assert "Effective Level: beginner" in (tmp_path / "CLAUDE.local.md").read_text(encoding="utf-8")


def test_module_boundary_no_change_in_middle_range(tmp_path):
    _seed_claude_local(tmp_path, experience="beginner", effective="beginner")
    _seed_profile(
        tmp_path,
        currentModule=2,
        moduleAverageQuality=3.0,
        moduleInteractions={
            "concept_question": 2,
            "independent_exploration": 1,
            "debug_attempt": 1,
            "answer_seeking": 2,
            "passive_acceptance": 1,
            "neutral": 0,
        },
    )

    result = _run_module_boundary(tmp_path)

    summary = json.loads(result.stdout)
    assert summary["levelChanged"] is False
    assert summary["newLevel"] == "beginner"
    profile = _profile(tmp_path)
    assert profile.get("pendingBanners", []) == []


def test_module_boundary_stays_at_bounds(tmp_path):
    _seed_claude_local(tmp_path, experience="beginner", effective="beginner")
    _seed_profile(
        tmp_path,
        currentModule=2,
        moduleAverageQuality=1.0,
        moduleInteractions={
            "concept_question": 0,
            "independent_exploration": 0,
            "debug_attempt": 0,
            "answer_seeking": 5,
            "passive_acceptance": 0,
            "neutral": 0,
        },
    )

    result = _run_module_boundary(tmp_path)

    summary = json.loads(result.stdout)
    assert summary["levelChanged"] is False  # can't go below beginner
    assert summary["newLevel"] == "beginner"


def test_module_boundary_resets_per_module_counters_and_bumps_currentModule(tmp_path):
    _seed_claude_local(tmp_path, experience="beginner", effective="beginner")
    _seed_profile(
        tmp_path,
        currentModule=2,
        moduleAverageQuality=3.0,
        moduleInteractions={
            "concept_question": 2,
            "independent_exploration": 1,
            "debug_attempt": 0,
            "answer_seeking": 1,
            "passive_acceptance": 0,
            "neutral": 0,
        },
        moduleQualityScores=[5, 4, 5, 1],
    )

    _run_module_boundary(tmp_path)

    profile = _profile(tmp_path)
    assert profile["currentModule"] == 3
    assert profile["moduleInteractions"]["concept_question"] == 0
    assert profile["moduleInteractions"]["answer_seeking"] == 0
    assert profile["moduleQualityScores"] == []
    assert profile["moduleAverageQuality"] == 0


def test_module_boundary_queues_banner_on_level_change(tmp_path):
    _seed_claude_local(tmp_path, experience="beginner", effective="beginner")
    _seed_profile(
        tmp_path,
        currentModule=2,
        moduleAverageQuality=4.5,
        moduleInteractions={
            "concept_question": 5,
            "independent_exploration": 2,
            "debug_attempt": 0,
            "answer_seeking": 1,
            "passive_acceptance": 0,
            "neutral": 0,
        },
    )

    _run_module_boundary(tmp_path)

    profile = _profile(tmp_path)
    banners = profile["pendingBanners"]
    assert len(banners) == 1
    b = banners[0]
    assert b["type"] == "module-boundary"
    assert b["payload"]["module"] == 2
    assert b["payload"]["oldLevel"] == "beginner"
    assert b["payload"]["newLevel"] == "intermediate"
    assert b["acknowledged"] is False


def test_module_boundary_skips_when_no_profile(tmp_path):
    _seed_claude_local(tmp_path)

    result = _run_module_boundary(tmp_path)

    summary = json.loads(result.stdout)
    assert summary["status"] == "skipped"


def test_context_dedups_contradictory_struggle_and_engagement_banners(tmp_path):
    """Reeves v2 finding (consolidated-signals T3.3). If both struggle and
    engagement banners are pending in the same session, emitting both would
    produce contradictory lines. Dedup rule: keep the later-created one,
    silently acknowledge the other."""
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc)
    older_struggle_iso = (now - datetime.timedelta(minutes=30)).isoformat()
    newer_engagement_iso = now.isoformat()
    _seed_profile(
        tmp_path,
        pendingBanners=[
            {"type": "struggle", "created": older_struggle_iso, "acknowledged": False},
            {"type": "engagement", "created": newer_engagement_iso, "acknowledged": False},
        ],
    )

    result = _run_context(tmp_path)

    assert result.returncode == 0
    # Newer engagement wins; older struggle is silently acknowledged.
    assert "engagement" in result.stdout.lower()
    assert "struggle" not in result.stdout.lower()
    profile = _profile(tmp_path)
    # Both end up acknowledged — engagement because it emitted, struggle
    # because the dedup pass silenced it.
    assert all(b["acknowledged"] for b in profile["pendingBanners"])


def test_context_dedup_prefers_struggle_when_newer(tmp_path):
    """Symmetric case: if struggle is the later-created banner, it wins."""
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc)
    older_engagement_iso = (now - datetime.timedelta(minutes=30)).isoformat()
    newer_struggle_iso = now.isoformat()
    _seed_profile(
        tmp_path,
        pendingBanners=[
            {"type": "engagement", "created": older_engagement_iso, "acknowledged": False},
            {"type": "struggle", "created": newer_struggle_iso, "acknowledged": False},
        ],
    )

    result = _run_context(tmp_path)

    assert result.returncode == 0
    assert "struggle" in result.stdout.lower()
    # Older engagement should not surface even as text fragment.
    assert "matching your energy" not in result.stdout.lower()


def test_context_emits_module_boundary_banner(tmp_path):
    import datetime
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    _seed_profile(
        tmp_path,
        pendingBanners=[
            {
                "type": "module-boundary",
                "payload": {"module": 2, "score": 4.2, "oldLevel": "beginner", "newLevel": "intermediate"},
                "created": now_iso,
                "acknowledged": False,
            }
        ],
    )

    result = _run_context(tmp_path)

    assert result.returncode == 0
    assert "SHOW TO LEARNER" in result.stdout
    assert "Module 2" in result.stdout
    assert "intermediate" in result.stdout
    assert "4.2/5" in result.stdout


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
