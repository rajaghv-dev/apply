"""Tests for tools/ssi-dashboard.py — log parsing and chart rendering."""
import sys
import importlib.util
from pathlib import Path
from datetime import datetime

def _load():
    spec = importlib.util.spec_from_file_location(
        "ssi_dashboard",
        Path(__file__).parent.parent / "tools" / "ssi-dashboard.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules["ssi_dashboard"] = mod
    return mod

_mod      = _load()
parse_log = _mod.parse_log

LOG_CONTENT = """\
# LinkedIn Analytics Log

| Date | SSI | Profile Views (7d) | InMails (30d) | Search Appearances (7d) | Notes |
|------|-----|--------------------|---------------|------------------------|-------|
| 2026-04-01 | 65.0 | 30 | 1 | 80 | baseline |
| 2026-04-08 | 68.5 | 42 | 2 | 95 | after headline update |
| 2026-04-15 | 71.0 | 55 | 3 | 120 | |
"""


def test_parse_count(tmp_path):
    log = tmp_path / "analytics-log.md"
    log.write_text(LOG_CONTENT)
    assert len(parse_log(log)) == 3


def test_parse_values(tmp_path):
    log = tmp_path / "analytics-log.md"
    log.write_text(LOG_CONTENT)
    row = parse_log(log)[0]
    assert row["ssi"]      == 65.0
    assert row["views"]    == 30
    assert row["inmails"]  == 1
    assert row["searches"] == 80
    assert row["notes"]    == "baseline"


def test_parse_sorted(tmp_path):
    shuffled = """\
| Date | SSI | Profile Views (7d) | InMails (30d) | Search Appearances (7d) | Notes |
|------|-----|--------------------|---------------|------------------------|-------|
| 2026-04-15 | 71.0 | 55 | 3 | 120 | |
| 2026-04-01 | 65.0 | 30 | 1 | 80  | |
"""
    log = tmp_path / "log.md"
    log.write_text(shuffled)
    rows = parse_log(log)
    assert rows[0]["date"] < rows[1]["date"]


def test_parse_empty_file(tmp_path):
    log = tmp_path / "log.md"
    log.write_text("# Header only\n")
    assert parse_log(log) == []


def test_parse_missing_file(tmp_path):
    assert parse_log(tmp_path / "missing.md") == []


def test_parse_skips_bad_rows(tmp_path):
    bad = """\
| Date | SSI | Views | InMails | Searches | Notes |
|------|-----|-------|---------|----------|-------|
| 2026-04-01 | 65.0 | 30 | 1 | 80 | ok |
| not-a-date | bad  | xx | y  | z  | skip |
| 2026-04-08 | 68.0 | 40 | 2 | 90 | ok |
"""
    log = tmp_path / "log.md"
    log.write_text(bad)
    assert len(parse_log(log)) == 2


def test_render_saves_png(tmp_path):
    import matplotlib
    matplotlib.use("Agg")
    _mod.OUTPUT_PNG = tmp_path / "dashboard.png"
    rows = [
        {"date": datetime(2026, 4, 1),  "ssi": 65.0, "views": 30, "inmails": 1, "searches": 80,  "notes": ""},
        {"date": datetime(2026, 4, 8),  "ssi": 68.0, "views": 42, "inmails": 2, "searches": 95,  "notes": ""},
        {"date": datetime(2026, 4, 15), "ssi": 71.0, "views": 55, "inmails": 3, "searches": 120, "notes": ""},
    ]
    _mod.render(rows, show=False)
    assert (tmp_path / "dashboard.png").exists()
