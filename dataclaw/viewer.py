"""Helpers for viewing exported DataClaw JSONL sessions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_sessions(path: str | Path) -> list[dict[str, Any]]:
    """Load a JSONL export file into a list of session dictionaries."""
    export_path = Path(path)
    sessions: list[dict[str, Any]] = []

    with export_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            raw = line.strip()
            if not raw:
                continue
            item = json.loads(raw)
            if isinstance(item, dict):
                sessions.append(item)

    return sessions


def clamp_index(index: int, total: int) -> int:
    """Clamp an index into the valid range for a collection size."""
    if total <= 0:
        return 0
    return max(0, min(index, total - 1))


def get_model_options(sessions: list[dict[str, Any]]) -> list[str]:
    """Return sorted unique model names present in the export."""
    models = {
        str(session.get("model"))
        for session in sessions
        if session.get("model")
    }
    return sorted(models)


def filter_sessions_by_model(
    sessions: list[dict[str, Any]], model_name: str | None
) -> list[dict[str, Any]]:
    """Filter sessions by exact model name, or return all sessions when unset."""
    if not model_name:
        return sessions
    return [session for session in sessions if session.get("model") == model_name]
