from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import streamlit as st

from dataclaw.viewer import (
    clamp_index,
    filter_sessions_by_model,
    get_model_options,
    load_sessions,
)


DEFAULT_EXPORT = Path(__file__).resolve().parents[1] / "dataclaw_conversations.jsonl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="View DataClaw JSONL exports in Streamlit.")
    parser.add_argument(
        "--file",
        default=str(DEFAULT_EXPORT),
        help="Path to the DataClaw JSONL export file.",
    )
    parser.add_argument(
        "--index",
        type=int,
        default=0,
        help="Initial zero-based row index to open.",
    )
    return parser.parse_args()


def format_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def render_message(message: dict[str, Any], index: int) -> None:
    role = message.get("role", "unknown")
    title = f"Message {index + 1} · {role}"
    with st.container(border=True):
        st.markdown(f"### {title}")

        timestamp = message.get("timestamp")
        if timestamp:
            st.caption(timestamp)

        content = message.get("content")
        if content:
            st.markdown("**Content**")
            st.code(str(content), language="markdown")

        thinking = message.get("thinking")
        if thinking:
            st.markdown("**Thinking**")
            st.code(str(thinking), language="text")

        tool_uses = message.get("tool_uses")
        if tool_uses:
            st.markdown("**Tool Uses**")
            st.code(format_json(tool_uses), language="json")

        extra = {
            key: value
            for key, value in message.items()
            if key not in {"role", "timestamp", "content", "thinking", "tool_uses"}
        }
        if extra:
            st.markdown("**Other Fields**")
            st.code(format_json(extra), language="json")


def main() -> None:
    args = parse_args()
    export_path = Path(args.file).expanduser().resolve()

    st.set_page_config(page_title="DataClaw Viewer", layout="wide")
    st.title("DataClaw Export Viewer")
    st.caption(str(export_path))

    if not export_path.exists():
        st.error(f"Export file not found: {export_path}")
        st.stop()

    sessions = load_sessions(export_path)
    if not sessions:
        st.warning("No sessions found in this export file.")
        st.stop()

    model_options = ["All models", *get_model_options(sessions)]
    selected_model = st.selectbox(
        "Model",
        options=model_options,
        index=0,
        help="Type to search model names and filter the session list.",
    )
    model_filter = None if selected_model == "All models" else selected_model

    filtered_sessions = filter_sessions_by_model(sessions, model_filter)
    total = len(filtered_sessions)
    if total == 0:
        st.warning("No sessions match the selected model.")
        st.stop()

    if "session_index" not in st.session_state:
        st.session_state.session_index = clamp_index(args.index, total)
    else:
        st.session_state.session_index = clamp_index(int(st.session_state.session_index), total)

    current = clamp_index(int(st.session_state.session_index), total)

    controls = st.columns([1, 1, 2, 2])
    with controls[0]:
        if st.button("Previous", use_container_width=True, disabled=current == 0):
            st.session_state.session_index = clamp_index(current - 1, total)
            st.rerun()
    with controls[1]:
        if st.button("Next", use_container_width=True, disabled=current >= total - 1):
            st.session_state.session_index = clamp_index(current + 1, total)
            st.rerun()
    with controls[2]:
        selected = st.number_input(
            "Index",
            min_value=0,
            max_value=total - 1,
            value=current,
            step=1,
        )
    with controls[3]:
        session_id_query = st.text_input(
            "Session ID",
            value=str(filtered_sessions[current].get("session_id", "")),
            help="Jump to a session ID within the current filtered results.",
        )

    selected = clamp_index(int(selected), total)
    if selected != current:
        st.session_state.session_index = selected
        st.rerun()

    if session_id_query and session_id_query != str(filtered_sessions[current].get("session_id", "")):
        match_index = next(
            (
                idx
                for idx, item in enumerate(filtered_sessions)
                if str(item.get("session_id", "")) == session_id_query
            ),
            None,
        )
        if match_index is not None:
            st.session_state.session_index = match_index
            st.rerun()

    session = filtered_sessions[st.session_state.session_index]
    messages = session.get("messages", [])

    if model_filter:
        st.caption(f"Showing {total} sessions for model `{model_filter}`")

    st.subheader(f"Row {st.session_state.session_index + 1} of {total}")

    meta_col, stats_col = st.columns(2)
    with meta_col:
        st.markdown("### Session")
        st.json(
            {
                "session_id": session.get("session_id"),
                "project": session.get("project"),
                "source": session.get("source"),
                "model": session.get("model"),
                "git_branch": session.get("git_branch"),
                "start_time": session.get("start_time"),
                "end_time": session.get("end_time"),
                "message_count": len(messages),
            }
        )
    with stats_col:
        st.markdown("### Stats")
        st.json(session.get("stats", {}))

    if messages:
        st.markdown("### Messages")
        for idx, message in enumerate(messages):
            render_message(message, idx)
    else:
        st.info("This session has no messages.")


if __name__ == "__main__":
    main()
