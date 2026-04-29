"""Tests for tools/log-linkedin.py — file creation and row appending."""
import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

import importlib
import types


def _load_log_linkedin(tmp_path):
    """Load log-linkedin module with LOG_FILE patched to tmp_path."""
    spec   = importlib.util.spec_from_file_location(
        "log_linkedin",
        Path(__file__).parent.parent / "tools" / "log-linkedin.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.LOG_FILE = tmp_path / "analytics-log.md"
    return mod


def test_creates_file_if_missing(tmp_path):
    mod = _load_log_linkedin(tmp_path)
    log = tmp_path / "analytics-log.md"
    assert not log.exists()
    mod.ensure_log(log)
    assert log.exists()
    assert "SSI" in log.read_text()


def test_header_written_once(tmp_path):
    mod = _load_log_linkedin(tmp_path)
    log = tmp_path / "analytics-log.md"
    mod.ensure_log(log)
    mod.ensure_log(log)   # calling twice should not duplicate header
    content = log.read_text()
    assert content.count("| Date |") == 1


def test_append_row_format(tmp_path):
    mod = _load_log_linkedin(tmp_path)
    log = tmp_path / "analytics-log.md"
    mod.ensure_log(log)
    mod.append_row(log, 72.5, 45, 3, 120, "after headline change")
    content = log.read_text()
    today   = str(date.today())
    assert today in content
    assert "72.5" in content
    assert "45" in content
    assert "after headline change" in content


def test_multiple_rows_appended(tmp_path):
    mod = _load_log_linkedin(tmp_path)
    log = tmp_path / "analytics-log.md"
    mod.ensure_log(log)
    mod.append_row(log, 70.0, 30, 1, 80,  "week 1")
    mod.append_row(log, 72.0, 40, 2, 100, "week 2")
    mod.append_row(log, 75.0, 55, 4, 130, "week 3")
    rows = [l for l in log.read_text().splitlines() if l.startswith("| 20")]
    assert len(rows) == 3


def test_creates_parent_directory(tmp_path):
    mod = _load_log_linkedin(tmp_path)
    nested = tmp_path / "linkedin" / "analytics-log.md"
    mod.LOG_FILE = nested
    mod.ensure_log(nested)
    assert nested.exists()
