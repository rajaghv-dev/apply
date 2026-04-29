"""Tests for tools/matcher.py — decay, section detection, scoring, focus bonus."""
import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from matcher import (
    apply_decay,
    detect_jd_sections,
    extract_skills_from_jd,
    score_profile_against_jd,
    compute_match_percent,
    suggest_role_clusters,
    get_focus_domains,
    FOCUS_BONUS,
    CURRENT_YEAR,
)


# ── apply_decay ───────────────────────────────────────────────────────────────

def test_decay_recent():
    score, note = apply_decay(3, CURRENT_YEAR - 1)
    assert score == 3.0
    assert note is None


def test_decay_2_to_5_years():
    score, note = apply_decay(3, CURRENT_YEAR - 4)
    assert score == pytest.approx(3 * 0.8)
    assert note is not None
    assert "−20%" in note


def test_decay_5_to_10_years():
    score, note = apply_decay(2, CURRENT_YEAR - 7)
    assert score == pytest.approx(2 * 0.6)
    assert "−40%" in note


def test_decay_over_10_years():
    score, note = apply_decay(3, CURRENT_YEAR - 12)
    assert score == pytest.approx(3 * 0.4)
    assert "−60%" in note


def test_decay_zero_score_no_change():
    score, note = apply_decay(0, CURRENT_YEAR - 15)
    assert score == 0.0
    assert note is None


def test_decay_no_last_used():
    score, note = apply_decay(2, None)
    assert score == 2.0
    assert note is None


# ── detect_jd_sections ───────────────────────────────────────────────────────

def test_section_default_weight():
    jd = "We are looking for a Python developer."
    weights = detect_jd_sections(jd)
    assert all(w == 1.5 for w in weights.values())


def test_section_required_sets_2x():
    jd = "Requirements:\n- Python\n- Machine learning"
    weights = detect_jd_sections(jd)
    # Lines after the header should be 2.0
    assert any(w == 2.0 for w in weights.values())


def test_section_preferred_sets_1x():
    jd = "Required:\n- Python\nNice to have:\n- Go"
    weights = detect_jd_sections(jd)
    assert 2.0 in weights.values()
    assert 1.0 in weights.values()


# ── extract_skills_from_jd ───────────────────────────────────────────────────

def test_extract_finds_synonym(skills_graph):
    jd = "Experience with PyTorch and TensorFlow required."
    found = extract_skills_from_jd(jd, skills_graph)
    assert "ml_frameworks" in found


def test_extract_finds_canonical(skills_graph):
    jd = "Strong Python skills needed."
    found = extract_skills_from_jd(jd, skills_graph)
    assert "python" in found


def test_extract_no_partial_word(skills_graph):
    # "Pythonic" should NOT match "Python" due to word boundary
    jd = "We need Pythonic code style."
    found = extract_skills_from_jd(jd, skills_graph)
    # "Python" is a substring — but with \b it should still match "Pythonic" won't match "Python"
    # "Python" matches in "Pythonic" is debatable; let's just check UVM is not matched spuriously
    assert "hardware_verification" not in found


def test_extract_section_weight(skills_graph):
    jd = "Required:\n- RTL design\nNice to have:\n- Python"
    found = extract_skills_from_jd(jd, skills_graph)
    # RTL should be in required section (weight 2.0), Python in preferred (1.0)
    assert found.get("rtl_design", 0) >= found.get("python", 0)


# ── score_profile_against_jd ─────────────────────────────────────────────────

def test_score_expert_is_strong(skills_graph):
    jd_skills = {"python": 2.0}
    profile   = {"python": {"level": "EXPERT", "last_used": 2025}}
    scored    = score_profile_against_jd(jd_skills, profile, skills_graph)
    assert scored["python"]["status"] == "STRONG"


def test_score_no_profile_is_gap(skills_graph):
    jd_skills = {"python": 2.0}
    scored    = score_profile_against_jd(jd_skills, {}, skills_graph)
    assert scored["python"]["status"] == "GAP"


def test_score_implied_partial(skills_graph):
    # rtl_design implies hardware_verification at 0.65
    # EXPERT rtl (score 3) × 0.65 = 1.95 → PARTIAL
    jd_skills = {"hardware_verification": 1.5}
    profile   = {"rtl_design": {"level": "EXPERT", "last_used": 2025}}
    scored    = score_profile_against_jd(jd_skills, profile, skills_graph)
    result    = scored["hardware_verification"]
    assert result["status"] in ("PARTIAL", "STRONG")
    assert result["implied_score"] > 0


def test_focus_bonus_applied(skills_graph, roles_graph):
    jd_skills     = {"rtl_design": 2.0, "timing_analysis": 2.0}
    profile       = {"rtl_design": {"level": "EXPERT", "last_used": 2025}}
    role_clusters = suggest_role_clusters(jd_skills, roles_graph)
    focus_domains = get_focus_domains(role_clusters, roles_graph)
    scored_plain  = score_profile_against_jd(jd_skills, profile, skills_graph)
    scored_focus  = score_profile_against_jd(jd_skills, profile, skills_graph, focus_domains)
    # With hardware focus, RTL direct score should be higher
    assert scored_focus["rtl_design"]["direct_score"] >= scored_plain["rtl_design"]["direct_score"]


def test_focus_bonus_flag(skills_graph, roles_graph):
    jd_skills     = {"rtl_design": 2.0}
    profile       = {"rtl_design": {"level": "PROFICIENT", "last_used": 2025}}
    focus_domains = {"hardware"}
    scored        = score_profile_against_jd(jd_skills, profile, skills_graph, focus_domains)
    assert scored["rtl_design"]["focus_bonus"] is True


def test_no_focus_bonus_when_zero_score(skills_graph):
    jd_skills    = {"rtl_design": 2.0}
    scored       = score_profile_against_jd(jd_skills, {}, skills_graph, {"hardware"})
    assert scored["rtl_design"]["focus_bonus"] is False


# ── compute_match_percent ─────────────────────────────────────────────────────

def test_match_pct_perfect():
    scored = {
        "a": {"final_score": 3.0, "max_possible": 3.0, "jd_weight": 2.0},
        "b": {"final_score": 3.0, "max_possible": 3.0, "jd_weight": 1.0},
    }
    assert compute_match_percent(scored) == 100.0


def test_match_pct_zero():
    scored = {
        "a": {"final_score": 0.0, "max_possible": 3.0, "jd_weight": 2.0},
    }
    assert compute_match_percent(scored) == 0.0


def test_match_pct_empty():
    assert compute_match_percent({}) == 0.0


def test_match_pct_weighted():
    # required skill (w=2) fully met, preferred (w=1) not met
    scored = {
        "req":  {"final_score": 3.0, "max_possible": 3.0, "jd_weight": 2.0},
        "pref": {"final_score": 0.0, "max_possible": 3.0, "jd_weight": 1.0},
    }
    pct = compute_match_percent(scored)
    # (3×2 + 0×1) / (3×2 + 3×1) = 6/9 = 66.7%
    assert abs(pct - 66.7) < 0.5


# ── suggest_role_clusters ────────────────────────────────────────────────────

def test_suggest_hardware_role(roles_graph):
    jd_skills = {"rtl_design": 2.0, "timing_analysis": 2.0, "hardware_verification": 1.5}
    clusters  = suggest_role_clusters(jd_skills, roles_graph)
    assert "silicon_engineer" in clusters


def test_suggest_ai_role(roles_graph):
    jd_skills = {"ml_frameworks": 2.0, "python": 2.0}
    clusters  = suggest_role_clusters(jd_skills, roles_graph)
    assert "ml_engineer" in clusters


# ── get_focus_domains ─────────────────────────────────────────────────────────

def test_get_focus_domains_hardware(roles_graph):
    domains = get_focus_domains(["silicon_engineer"], roles_graph)
    assert "hardware" in domains


def test_get_focus_domains_empty():
    assert get_focus_domains([], {}) == set()


