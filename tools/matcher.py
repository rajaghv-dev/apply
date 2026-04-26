#!/usr/bin/env python3
"""
JD → Profile matcher using the skills ontology.

Usage:
    python tools/matcher.py --jd path/to/jd.txt --profile path/to/profile.yaml
    python tools/matcher.py --jd path/to/jd.txt          # uses profile/my-profile.yaml
    echo "paste JD text" | python tools/matcher.py

Output:
    - Match score (%)
    - STRONG / PARTIAL / GAP breakdown
    - Gap action list
    - Suggested role cluster
    - "Why me" bullet drafts
"""

import sys
import re
import yaml
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SKILLS_GRAPH = REPO_ROOT / "ontology" / "skills-graph.yaml"
ROLES_GRAPH  = REPO_ROOT / "ontology" / "roles-graph.yaml"
DOMAINS      = REPO_ROOT / "ontology" / "domains.yaml"
PROFILE      = REPO_ROOT / "profile" / "my-profile.yaml"

LEVEL_SCORE = {"EXPERT": 3, "PROFICIENT": 2, "FAMILIAR": 1, "": 0, None: 0}


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def extract_skills_from_jd(jd_text: str, skills_graph: dict) -> dict[str, float]:
    """
    Scan JD text for skill synonyms. Return {skill_id: confidence}.
    confidence = 1.0 if keyword found, scaled by position weight.
    """
    jd_lower = jd_text.lower()
    found = {}
    for skill_id, skill in skills_graph["skills"].items():
        synonyms = [skill["label"].lower()] + [s.lower() for s in skill.get("synonyms", [])]
        for syn in synonyms:
            if re.search(r'\b' + re.escape(syn) + r'\b', jd_lower):
                found[skill_id] = found.get(skill_id, 0) + 1
                break
    return found


def score_profile_against_jd(
    jd_skills: dict,
    profile_skills: dict,
    skills_graph: dict,
) -> dict:
    """
    For each JD skill, compute:
      direct_score  = profile level score (3/2/1/0)
      implied_score = best implied score from other skills you have
      final_score   = max(direct, implied)
      status        = STRONG / PARTIAL / GAP
    """
    results = {}
    all_skills = skills_graph["skills"]

    for jd_skill_id in jd_skills:
        if jd_skill_id not in all_skills:
            continue

        # Direct score
        my_level = profile_skills.get(jd_skill_id, {}).get("level", "")
        direct = LEVEL_SCORE.get(my_level, 0)

        # Implied score: check if any skill I have implies this one
        implied = 0.0
        for my_skill_id, my_skill_data in profile_skills.items():
            if my_skill_id not in all_skills:
                continue
            my_score = LEVEL_SCORE.get(my_skill_data.get("level", ""), 0)
            implies = all_skills[my_skill_id].get("implies", {})
            if isinstance(implies, list):
                # handle list-of-dicts or list-of-str formats
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
        max_possible = 3.0

        if final >= 2.5:
            status = "STRONG"
        elif final >= 1.2:
            status = "PARTIAL"
        else:
            status = "GAP"

        results[jd_skill_id] = {
            "label": all_skills[jd_skill_id]["label"],
            "direct_score": direct,
            "implied_score": round(implied, 2),
            "final_score": round(final, 2),
            "max_possible": max_possible,
            "status": status,
            "my_level": my_level or "none",
        }

    return results


def compute_match_percent(scored: dict) -> float:
    if not scored:
        return 0.0
    total_score = sum(v["final_score"] for v in scored.values())
    total_max   = sum(v["max_possible"] for v in scored.values())
    return round(total_score / total_max * 100, 1) if total_max else 0.0


def suggest_role_clusters(jd_skills: dict, roles_graph: dict, match_pct: float) -> list[str]:
    """Find role clusters whose required skills most overlap with the JD."""
    scores = {}
    for role_id, role in roles_graph.get("roles", {}).items():
        required = set(role.get("required", {}).keys())
        preferred = set(role.get("preferred", {}).keys())
        jd_set = set(jd_skills.keys())
        overlap = len(required & jd_set) + 0.5 * len(preferred & jd_set)
        if overlap > 0:
            scores[role_id] = overlap
    return sorted(scores, key=scores.get, reverse=True)[:3]


def print_report(jd_text: str, scored: dict, match_pct: float, role_clusters: list,
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

    strong  = [v for v in scored.values() if v["status"] == "STRONG"]
    partial = [v for v in scored.values() if v["status"] == "PARTIAL"]
    gaps    = [v for v in scored.values() if v["status"] == "GAP"]

    print(f"\n  STRONG ({len(strong)}): ", ", ".join(v["label"] for v in strong) or "none")
    print(f"  PARTIAL ({len(partial)}): ", ", ".join(v["label"] for v in partial) or "none")
    print(f"  GAP ({len(gaps)}): ", ", ".join(v["label"] for v in gaps) or "none")

    if gaps:
        print(f"\n{sep}")
        print(f"  GAP ACTIONS")
        print(f"{sep}")
        for g in gaps:
            skill_data = skills_graph["skills"].get(
                next((k for k, v in scored.items() if v["label"] == g["label"]), ""), {}
            )
            print(f"  • {g['label']}")
            if skill_data.get("implies"):
                print(f"    → Build via: {list(skill_data.get('implies', {}).keys())[:3]}")

    if partial:
        print(f"\n{sep}")
        print(f"  PARTIAL → STRONG UPGRADES")
        print(f"{sep}")
        for p in partial:
            print(f"  • {p['label']} (score {p['final_score']:.1f}/3) "
                  f"— {'direct knowledge, deepen it' if p['direct_score'] > 0 else 'implied only — get hands-on evidence'}")

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
        print(f"  2. Working knowledge of {partial[0]['label']} with evidence of "
              f"adjacent skills ({strong_labels[0] if strong_labels else 'see profile'})")
    print(f"  3. [Add your unique bridge / differentiator from profile/domains.md]")
    print()


def main():
    parser = argparse.ArgumentParser(description="Match a JD against your skills profile")
    parser.add_argument("--jd",      help="Path to JD text file")
    parser.add_argument("--profile", help="Path to profile YAML", default=str(PROFILE))
    args = parser.parse_args()

    # Load ontology
    if not SKILLS_GRAPH.exists():
        print(f"ERROR: skills-graph.yaml not found at {SKILLS_GRAPH}")
        sys.exit(1)
    skills_graph = load_yaml(SKILLS_GRAPH)
    roles_graph  = load_yaml(ROLES_GRAPH)

    # Load JD
    if args.jd:
        jd_text = Path(args.jd).read_text()
    elif not sys.stdin.isatty():
        jd_text = sys.stdin.read()
    else:
        print("Paste JD text below (Ctrl+D when done):\n")
        jd_text = sys.stdin.read()

    # Load profile
    profile_path = Path(args.profile)
    if not profile_path.exists():
        print(f"WARNING: Profile not found at {profile_path}")
        print("Create profile/my-profile.yaml from the template in profile/questionnaire.md")
        print("Running with empty profile — all results will show as GAP\n")
        profile_skills = {}
    else:
        profile_data = load_yaml(profile_path)
        profile_skills = profile_data.get("skills", {})

    # Run matching
    jd_skills    = extract_skills_from_jd(jd_text, skills_graph)
    scored       = score_profile_against_jd(jd_skills, profile_skills, skills_graph)
    match_pct    = compute_match_percent(scored)
    role_clusters = suggest_role_clusters(jd_skills, roles_graph, match_pct)

    print_report(jd_text, scored, match_pct, role_clusters, roles_graph, skills_graph)

    # Save to gap-analysis/jobs/
    output_dir = REPO_ROOT / "gap-analysis" / "jobs"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"match-{match_pct:.0f}pct-latest.md"
    with open(out_file, "w") as f:
        f.write(f"# JD Match — {match_pct}%\n\n")
        f.write("| Skill | Status | My level | Score |\n")
        f.write("|-------|--------|----------|-------|\n")
        for sid, sv in scored.items():
            f.write(f"| {sv['label']} | {sv['status']} | {sv['my_level']} | {sv['final_score']}/3 |\n")
    print(f"  Saved to: {out_file.relative_to(REPO_ROOT)}\n")


if __name__ == "__main__":
    main()
