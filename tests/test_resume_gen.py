"""Tests for tools/resume-gen.py — cluster resume generation."""
import sys
import importlib.util
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))  # conftest

def _load():
    spec = importlib.util.spec_from_file_location(
        "resume_gen",
        Path(__file__).parent.parent / "tools" / "resume-gen.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules["resume_gen"] = mod
    return mod

_mod        = _load()
build_resume = _mod.build_resume

from conftest import SKILLS_GRAPH, ROLES_GRAPH


def test_generates_markdown_header():
    role    = ROLES_GRAPH["roles"]["ml_engineer"]
    content = build_resume("ml_engineer", role, {}, SKILLS_GRAPH)
    assert "# Resume" in content
    assert "ML Engineer" in content


def test_empty_profile_shows_warning():
    role    = ROLES_GRAPH["roles"]["ml_engineer"]
    content = build_resume("ml_engineer", role, {}, SKILLS_GRAPH)
    assert "Profile not filled" in content or "my-profile.yaml" in content


def test_filled_profile_shows_skills():
    role    = ROLES_GRAPH["roles"]["ml_engineer"]
    profile = {
        "python":        {"level": "EXPERT",    "last_used": 2025, "evidence": ""},
        "ml_frameworks": {"level": "PROFICIENT", "last_used": 2024, "evidence": "github.com/x"},
    }
    content = build_resume("ml_engineer", role, profile, SKILLS_GRAPH)
    assert "Python" in content
    assert "ML Frameworks" in content
    assert "Expert" in content or "Proficient" in content


def test_missing_skills_section_shown():
    role    = ROLES_GRAPH["roles"]["silicon_engineer"]
    content = build_resume("silicon_engineer", role, {}, SKILLS_GRAPH)
    assert "Gaps" in content or "pathfinder" in content


def test_target_titles_listed():
    role    = ROLES_GRAPH["roles"]["silicon_engineer"]
    content = build_resume("silicon_engineer", role, {}, SKILLS_GRAPH)
    assert "ASIC Engineer" in content or "RTL Engineer" in content


def test_req_tag_present():
    role    = ROLES_GRAPH["roles"]["ml_engineer"]
    profile = {"python": {"level": "EXPERT", "last_used": 2025, "evidence": ""}}
    content = build_resume("ml_engineer", role, profile, SKILLS_GRAPH)
    assert "[req]" in content


def test_output_writable(tmp_path):
    role    = ROLES_GRAPH["roles"]["ml_engineer"]
    content = build_resume("ml_engineer", role, {}, SKILLS_GRAPH)
    out     = tmp_path / "test.md"
    out.write_text(content)
    assert out.read_text() == content


def test_familiar_in_supporting():
    role    = ROLES_GRAPH["roles"]["ml_engineer"]
    profile = {"backend_apis": {"level": "FAMILIAR", "last_used": 2024, "evidence": ""}}
    content = build_resume("ml_engineer", role, profile, SKILLS_GRAPH)
    assert "Supporting" in content or "Familiar" in content
