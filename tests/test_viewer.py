"""Tests for dataclaw.viewer helpers used by the Streamlit export viewer."""

import json

import pytest

from dataclaw.viewer import (
    clamp_index,
    filter_sessions_by_model,
    get_model_options,
    load_sessions,
)


def test_load_sessions_reads_jsonl_rows(tmp_path):
    export_file = tmp_path / "export.jsonl"
    rows = [
        {"session_id": "s1", "project": "alpha", "messages": []},
        {"session_id": "s2", "project": "beta", "messages": [{"role": "user", "content": "hi"}]},
    ]
    export_file.write_text("".join(json.dumps(row) + "\n" for row in rows))

    sessions = load_sessions(export_file)

    assert sessions == rows


@pytest.mark.parametrize(
    ("index", "total", "expected"),
    [
        (-5, 3, 0),
        (0, 3, 0),
        (1, 3, 1),
        (2, 3, 2),
        (99, 3, 2),
    ],
)
def test_clamp_index_handles_out_of_bounds_values(index, total, expected):
    assert clamp_index(index, total) == expected


def test_clamp_index_returns_zero_when_list_is_empty():
    assert clamp_index(5, 0) == 0


def test_get_model_options_returns_sorted_unique_models():
    sessions = [
        {"model": "gpt-5.4"},
        {"model": "kimi-k2"},
        {"model": "gpt-5.4"},
        {"model": None},
        {},
    ]

    assert get_model_options(sessions) == ["gpt-5.4", "kimi-k2"]


def test_filter_sessions_by_model_returns_matching_sessions():
    sessions = [
        {"session_id": "a", "model": "gpt-5.4"},
        {"session_id": "b", "model": "kimi-k2"},
        {"session_id": "c", "model": "gpt-5.4"},
    ]

    filtered = filter_sessions_by_model(sessions, "gpt-5.4")

    assert [session["session_id"] for session in filtered] == ["a", "c"]


def test_filter_sessions_by_model_returns_all_when_filter_not_set():
    sessions = [
        {"session_id": "a", "model": "gpt-5.4"},
        {"session_id": "b", "model": "kimi-k2"},
    ]

    assert filter_sessions_by_model(sessions, None) == sessions
    assert filter_sessions_by_model(sessions, "") == sessions
