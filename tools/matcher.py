#!/usr/bin/env python3
"""
JD → Profile matcher using the skills ontology.

Usage:
    python tools/matcher.py --jd path/to/jd.txt --profile path/to/profile.yaml
    python tools/matcher.py --jd path/to/jd.txt          # uses profile/my-profile.yaml
    echo "paste JD text" | python tools/matcher.py

Output:
    - Match score (%) — weighted by JD section (required 2×, preferred 1×)
    - STRONG / PARTIAL / GAP breakdown with decay notes
    - Gap action list (required gaps flagged)
    - Suggested role cluster
    - "Why me" bullet drafts
    - Saved to gap-analysis/jobs/match-<N>pct-latest.md
"""

import sys
import re
import yaml
import argparse
from datetime import date
from pathlib import Path

REPO_ROOT    = Path(__file__).parent.parent
SKILLS_GRAPH = REPO_ROOT / "ontology" / "skills-graph.yaml"
ROLES_GRAPH  = REPO_ROOT / "ontology" / "roles-graph.yaml"
PROFILE      = REPO_ROOT / "profile" / "my-profile.yaml"

CURRENT_YEAR = date.today().year
LEVEL_SCORE  = {"EXPERT": 3, "PROFICIENT": 2, "FAMILIAR": 1, "": 0, None: 0}

REQUIRED_PATTERNS = [
    r'required[:\s]', r'must have[:\s]', r'you must', r'essential[:\s]',
    r'minimum qualifications', r'basic qualifications', r'requirements[:\s]',
    r"what you.ll need", r'what we require',
]
PREFERRED_PATTERNS = [
    r'preferred[:\s]', r'nice to have[:\s]', r'desired[:\s]', r'bonus[:\s]',
    r'\bplus[:\s]', r'ideally[:\s]', r'additional qualifications',
    r"what.s a plus", r'good to have',
]


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def apply_decay(level_score: int, last_used: int | None) -> tuple[float, str | None]:
    """Tiered recency decay. Returns (decayed_score, note_or_None)."""
    if not last_used or level_score == 0:
        return float(level_score), None
    years_ago = CURRENT_YEAR - int(last_used)
    if years_ago <= 2:
        return float(level_score), None
    elif years_ago <= 5:
        return level_score * 0.8, f"last used {last_used} (−20%)"
    elif years_ago <= 10:
        return level_score * 0.6, f"last used {last_used} (−40%)"
    else:
        return level_score * 0.4, f"last used {last_used} (−60%)"


def detect_jd_sections(jd_text: str) -> dict[int, float]:
    """
    Walk JD line by line; detect required / preferred section headers.
    Returns {line_index: weight} — 2.0 = required, 1.0 = preferred.
    Default weight before any header is 1.5 (unknown = slightly above preferred).
    """
    lines = jd_text.split("\n")
    line_weight: dict[int, float] = {}
    current_weight = 1.5

    for i, line in enumerate(lines):
        ll = line.lower().strip()
        new_weight = None
        for pat in REQUIRED_PATTERNS:
            if re.search(pat, ll):
                new_weight = 2.0
                break
        if new_weight is None:
            for pat in PREFERRED_PATTERNS:
                if re.search(pat, ll):
                    new_weight = 1.0
                    break
        if new_weight is not None:
            current_weight = new_weight
        line_weight[i] = current_weight

    return line_weight


def extract_skills_from_jd(jd_text: str, skills_graph: dict) -> dict[str, float]:
    """
    Scan JD for skill synonyms. Returns {skill_id: jd_weight}.
    jd_weight = max weight of any line in which the skill appears.
    """
    lines = jd_text.split("\n")
    line_weights = detect_jd_sections(jd_text)
    found: dict[str, float] = {}

    for skill_id, skill in skills_graph["skills"].items():
        synonyms = [skill["label"].lower()] + [s.lower() for s in skill.get("synonyms", [])]
        for i, line in enumerate(lines):
            ll = line.lower()
            w = line_weights.get(i, 1.5)
            for syn in synonyms:
                if re.search(r"\b" + re.escape(syn) + r"\b", ll):
                    found[skill_id] = max(found.get(skill_id, 0), w)
                    break

    return found


def score_profile_against_jd(
    jd_skills: dict[str, float],
    profile_skills: dict,
    skills_graph: dict,
) -> dict:
    """
    Score each JD skill against profile.
    direct_score uses decay; implied_score propagates decayed scores through implies edges.
    """
    results = {}
    all_skills = skills_graph["skills"]

    for jd_skill_id, jd_weight in jd_skills.items():
        if jd_skill_id not in all_skills:
            continue

        my_data  = profile_skills.get(jd_skill_id, {})
        my_level = my_data.get("level", "")
        last_used = my_data.get("last_used")
        raw_direct = LEVEL_SCORE.get(my_level, 0)
        direct, decay_note = apply_decay(raw_direct, last_used)

        implied = 0.0
        for my_skill_id, my_sd in profile_skills.items():
            if my_skill_id not in all_skills:
                continue
            raw = LEVEL_SCORE.get(my_sd.get("level", ""), 0)
            my_score, _ = apply_decay(raw, my_sd.get("last_used"))
            implies = all_skills[my_skill_id].get("implies", {})
            if isinstance(implies, list):
                for item in implies:
                    if isinstance(item, dict):
                        for implied_skill, weight in item.items():
                            if implied_skill == jd_skill_id:
                                implied = max(implied, my_score * weight)
                    elif isinstance(item, str) and item == jd_skill_id:
                        implied = max(implied, my_score * 0.5)
            elif isinstance(implies, dict):
                weight = implies.get(jd_skill_id, 0)
                if weight:
                    implied = max(implied, my_score * weight)

        final = max(direct, implied)

        if final >= 2.5:
            status = "STRONG"
        elif final >= 1.2:
            status = "PARTIAL"
        else:
            status = "GAP"

        results[jd_skill_id] = {
            "label":        all_skills[jd_skill_id]["label"],
            "direct_score": round(direct, 2),
            "implied_score": round(implied, 2),
            "final_score":  round(final, 2),
            "max_possible": 3.0,
            "status":       status,
            "my_level":     my_level or "none",
            "decay_note":   decay_note,
            "jd_weight":    jd_weight,
        }

    return results


def compute_match_percent(scored: dict) -> float:
    if not scored:
        return 0.0
    total_score = sum(v["final_score"] * v["jd_weight"] for v in scored.values())
    total_max   = sum(v["max_possible"] * v["jd_weight"] for v in scored.values())
    return round(total_score / total_max * 100, 1) if total_max else 0.0


def suggest_role_clusters(jd_skills: dict, roles_graph: dict) -> list[str]:
    scores = {}
    for role_id, role in roles_graph.get("roles", {}).items():
        required  = set(role.get("required", {}).keys())
        preferred = set(role.get("preferred", {}).keys())
        jd_set    = set(jd_skills.keys())
        overlap   = len(required & jd_set) + 0.5 * len(preferred & jd_set)
        if overlap > 0:
            scores[role_id] = overlap
    return sorted(scores, key=scores.get, reverse=True)[:3]


def print_report(scored: dict, match_pct: float, role_clusters: list,
                 roles_graph: dict, skills_graph: dict):
    sep = "─" * 60

    print(f"\n{sep}")
    print(f"  JD MATCH REPORT")
    print(f"{sep}")
    print(f"  Match score: {match_pct}%", end="  ")
    if match_pct >= 60:
        print("→ APPLY ✓")
    elif match_pct >= 40:
        print("→ STRETCH (close gaps in parallel)")
    else:
        print("→ SKIP or major gap-close needed")

    n_req  = sum(1 for v in scored.values() if v["jd_weight"] >= 2.0)
    n_pref = sum(1 for v in scored.values() if v["jd_weight"] < 2.0)
    if n_req or n_pref:
        print(f"  Sections detected: {n_req} required (2×), {n_pref} preferred (1×)")

    strong  = [v for v in scored.values() if v["status"] == "STRONG"]
    partial = [v for v in scored.values() if v["status"] == "PARTIAL"]
    gaps    = [v for v in scored.values() if v["status"] == "GAP"]

    print(f"\n  STRONG  ({len(strong)}):  {', '.join(v['label'] for v in strong) or 'none'}")
    print(f"  PARTIAL ({len(partial)}): {', '.join(v['label'] for v in partial) or 'none'}")
    print(f"  GAP     ({len(gaps)}):  {', '.join(v['label'] for v in gaps) or 'none'}")

    decayed = [v for v in scored.values() if v.get("decay_note")]
    if decayed:
        print(f"\n  DECAY APPLIED:")
        for v in decayed:
            print(f"  • {v['label']}: {v['decay_note']}")

    if gaps:
        print(f"\n{sep}")
        print(f"  GAP ACTIONS")
        print(f"{sep}")
        for g in gaps:
            skill_data = skills_graph["skills"].get(
                next((k for k, v in scored.items() if v["label"] == g["label"]), ""), {}
            )
            req_tag = " [REQUIRED]" if g["jd_weight"] >= 2.0 else " [preferred]"
            print(f"  • {g['label']}{req_tag}")
            if skill_data.get("implies"):
                print(f"    → Build via: {list(skill_data.get('implies', {}).keys())[:3]}")

    if partial:
        print(f"\n{sep}")
        print(f"  PARTIAL → STRONG UPGRADES")
        print(f"{sep}")
        for p in partial:
            req_tag = " [REQUIRED]" if p["jd_weight"] >= 2.0 else " [preferred]"
            note = "direct — deepen it" if p["direct_score"] > 0 else "implied only — get hands-on evidence"
            print(f"  • {p['label']}{req_tag} ({p['final_score']:.1f}/3) — {note}")

    print(f"\n{sep}")
    print(f"  SUGGESTED ROLE CLUSTERS")
    print(f"{sep}")
    for rc in role_clusters:
        role = roles_graph["roles"].get(rc, {})
        print(f"  • {role.get('label', rc)}")
        print(f"    Titles: {', '.join(role.get('title_synonyms', [])[:3])}")

    print(f"\n{sep}")
    print(f"  WHY ME — DRAFT BULLETS (edit before use)")
    print(f"{sep}")
    strong_labels = [v["label"] for v in strong[:3]]
    if strong_labels:
        print(f"  1. Direct expertise in {', '.join(strong_labels)} — proven in production")
    if partial:
        adj = strong_labels[0] if strong_labels else "adjacent skills"
        print(f"  2. Working knowledge of {partial[0]['label']} — supported by {adj}")
    print(f"  3. [Add your unique bridge / differentiator from profile/domains.md]")
    print()


def main():
    parser = argparse.ArgumentParser(description="Match a JD against your skills profile")
    parser.add_argument("--jd",      help="Path to JD text file")
    parser.add_argument("--profile", help="Path to profile YAML", default=str(PROFILE))
    args = parser.parse_args()

    if not SKILLS_GRAPH.exists():
        print(f"ERROR: skills-graph.yaml not found at {SKILLS_GRAPH}")
        sys.exit(1)
    skills_graph = load_yaml(SKILLS_GRAPH)
    roles_graph  = load_yaml(ROLES_GRAPH)

    if args.jd:
        jd_text = Path(args.jd).read_text()
    elif not sys.stdin.isatty():
        jd_text = sys.stdin.read()
    else:
        print("Paste JD text below (Ctrl+D when done):\n")
        jd_text = sys.stdin.read()

    profile_path = Path(args.profile)
    if not profile_path.exists():
        print(f"WARNING: Profile not found at {profile_path}")
        print("Running with empty profile — all results will show as GAP\n")
        profile_skills = {}
    else:
        profile_data   = load_yaml(profile_path)
        profile_skills = profile_data.get("skills", {})

    jd_skills     = extract_skills_from_jd(jd_text, skills_graph)
    scored        = score_profile_against_jd(jd_skills, profile_skills, skills_graph)
    match_pct     = compute_match_percent(scored)
    role_clusters = suggest_role_clusters(jd_skills, roles_graph)

    print_report(scored, match_pct, role_clusters, roles_graph, skills_graph)

    output_dir = REPO_ROOT / "gap-analysis" / "jobs"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"match-{match_pct:.0f}pct-latest.md"
    with open(out_file, "w") as f:
        f.write(f"# JD Match — {match_pct}%\n\n")
        f.write("| Skill | Section | Status | My level | Score | Decay |\n")
        f.write("|-------|---------|--------|----------|-------|-------|\n")
        for sv in scored.values():
            section = "required" if sv["jd_weight"] >= 2.0 else "preferred"
            decay   = sv.get("decay_note") or "—"
            f.write(f"| {sv['label']} | {section} | {sv['status']} | {sv['my_level']} | {sv['final_score']}/3 | {decay} |\n")
    print(f"  Saved to: {out_file.relative_to(REPO_ROOT)}\n")


if __name__ == "__main__":
    main()
