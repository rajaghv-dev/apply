"""Tests for tools/market-scan.py — skill extraction and frequency counting."""
import sys
import importlib.util
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))  # conftest

def _load():
    spec = importlib.util.spec_from_file_location(
        "market_scan",
        Path(__file__).parent.parent / "tools" / "market-scan.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules["market_scan"] = mod
    return mod

_mod           = _load()
extract_skills = _mod.extract_skills
scan_directory = _mod.scan_directory
write_output   = _mod.write_output

from conftest import SKILLS_GRAPH


def test_extract_synonym():
    found = extract_skills("We need PyTorch and TensorFlow experience.", SKILLS_GRAPH)
    assert "ml_frameworks" in found


def test_extract_canonical():
    found = extract_skills("Strong Python skills required.", SKILLS_GRAPH)
    assert "python" in found


def test_extract_multiple():
    found = extract_skills("Python, RTL design, and machine learning.", SKILLS_GRAPH)
    assert "python" in found
    assert "rtl_design" in found
    assert "ml_frameworks" in found


def test_extract_case_insensitive():
    found = extract_skills("PYTHON AND VERILOG.", SKILLS_GRAPH)
    assert "python" in found
    assert "rtl_design" in found


def test_extract_empty():
    assert extract_skills("", SKILLS_GRAPH) == set()


def test_extract_no_match():
    assert extract_skills("The quick brown fox.", SKILLS_GRAPH) == set()


def test_scan_counts(tmp_path):
    (tmp_path / "jd1.txt").write_text("Python and RTL design required.")
    (tmp_path / "jd2.txt").write_text("Python and machine learning.")
    (tmp_path / "jd3.txt").write_text("Just Python.")
    freq, count = scan_directory(tmp_path, SKILLS_GRAPH)
    assert count == 3
    assert freq.get("python", 0) == 3
    assert freq.get("rtl_design", 0) == 1
    assert freq.get("ml_frameworks", 0) == 1


def test_scan_empty_dir(tmp_path):
    freq, count = scan_directory(tmp_path, SKILLS_GRAPH)
    assert count == 0
    assert freq == {}


def test_write_output(tmp_path):
    _mod.OUTPUT_FILE = tmp_path / "market-scan.md"
    freq = {"python": 5, "ml_frameworks": 3, "rtl_design": 1}
    write_output(freq, SKILLS_GRAPH, jd_count=5, top=10)
    content = (tmp_path / "market-scan.md").read_text()
    assert "Python" in content
    assert "100%" in content   # 5/5


def test_write_output_top_n(tmp_path):
    _mod.OUTPUT_FILE = tmp_path / "market-scan.md"
    freq = {sid: i for i, sid in enumerate(SKILLS_GRAPH["skills"], 1)}
    write_output(freq, SKILLS_GRAPH, jd_count=10, top=2)
    content = (tmp_path / "market-scan.md").read_text()
    # Only top 2 rows should be in the table
    data_rows = [l for l in content.splitlines() if l.startswith("| ") and "Rank" not in l and "---" not in l and l.strip() != "|"]
    assert len(data_rows) <= 2
