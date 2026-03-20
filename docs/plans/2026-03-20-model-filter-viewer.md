# Model Filter Viewer Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add model-name filtering with searchable suggestions to the Streamlit export viewer.

**Architecture:** Keep session loading and filtering logic in `dataclaw/viewer.py` so it is easy to test, then wire the Streamlit UI in `scripts/view_export.py` to browse only the filtered sessions. Use a searchable select box so users get model-name suggestions while typing.

**Tech Stack:** Python, Streamlit, pytest

---

### Task 1: Add failing helper tests

**Files:**
- Modify: `tests/test_viewer.py`
- Modify: `dataclaw/viewer.py`

**Step 1: Write the failing test**

Add tests for:
- extracting sorted model names from sessions
- filtering sessions by exact model name
- leaving sessions unchanged when no model filter is selected

**Step 2: Run test to verify it fails**

Run: `PYTHONPATH=. pytest tests/test_viewer.py -v`
Expected: FAIL because helper functions do not exist yet.

**Step 3: Write minimal implementation**

Implement helper functions in `dataclaw/viewer.py`.

**Step 4: Run test to verify it passes**

Run: `PYTHONPATH=. pytest tests/test_viewer.py -v`
Expected: PASS

### Task 2: Update the Streamlit viewer

**Files:**
- Modify: `scripts/view_export.py`

**Step 1: Connect the helpers**

Add a searchable model select box with `All models` as the default option.

**Step 2: Scope navigation to filtered results**

Make previous/next, index input, row count, and session-id lookup all operate on the filtered sessions list.

**Step 3: Run validation**

Run:
```bash
PYTHONPATH=. pytest tests/test_viewer.py -v
python3 -m py_compile dataclaw/viewer.py scripts/view_export.py
```

Expected: PASS
