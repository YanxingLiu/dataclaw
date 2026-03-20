"""Tests for dataclaw.viewer helpers used by the Streamlit export viewer."""

import json

import pytest

from dataclaw.viewer import clamp_index, load_sessions


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
