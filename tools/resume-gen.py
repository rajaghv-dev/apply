#!/usr/bin/env python3
"""
tools/resume-gen.py — Generate cluster-specific resume sections from profile YAML.

Reads my-profile.yaml + roles-graph.yaml → for each role cluster, generates a
tailored markdown skills section listing what you have vs. what the role needs.

Usage:
    python tools/resume-gen.py                     # generate all clusters
    python tools/resume-gen.py --cluster silicon_engineer
    python tools/resume-gen.py --list-clusters

Output: resume/cluster-{id}.md per cluster
"""

import sys
import yaml
import argparse
from pathlib import Path
from datetime import date

REPO_ROOT    = Path(__file__).parent.parent
PROFILE      = REPO_ROOT / "profile" / "my-profile.yaml"
ROLES_GRAPH  = REPO_ROOT / "ontology" / "roles-graph.yaml"
SKILLS_GRAPH = REPO_ROOT / "ontology" / "skills-graph.yaml"
RESUME_DIR   = REPO_ROOT / "resume"

LEVEL_SCORE = {"EXPERT": 3, "PROFICIENT": 2, "FAMILIAR": 1, "": 0, None: 0}
LEVEL_LABEL = {"EXPERT": "Expert", "PROFICIENT": "Proficient", "FAMILIAR": "Familiar"}


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def build_resume(role_id: str, role: dict, profile_skills: dict,
                 skills_graph: dict) -> str:
    role_label   = role.get("label", role_id)
    required     = role.get("required", {})
    preferred    = role.get("preferred", {})
    all_skills   = skills_graph.get("skills", {})
    all_role_ids = list(required) + [k for k in preferred if k not in required]

    strong, familiar, missing = [], [], []

    for skill_id in all_role_ids:
        sl   = all_skills.get(skill_id, {})
        lbl  = sl.get("label", skill_id)
        my   = (profile_skills.get(skill_id) or {})
        lvl  = my.get("level", "")
        score = LEVEL_SCORE.get(lvl, 0)
        ev    = my.get("evidence", "") or ""
        tag   = "[req]" if skill_id in required else "[pref]"

        if score >= 2:
            strong.append((lbl, lvl, ev, tag))
        elif score == 1:
            familiar.append((lbl, tag))
        else:
            missing.append((lbl, tag))

    lines = [
        f"# Resume — {role_label}\n\n",
        f"_Generated {date.today()} from `profile/my-profile.yaml`. Edit before use._\n\n---\n\n",
        "## Summary\n\n",
        "_Add a 2–3 sentence summary tailored to this role here._\n\n",
        "## Core Skills\n\n",
    ]

    if strong:
        for lbl, lvl, ev, tag in strong:
            ev_str = f" — {ev}" if ev else ""
            lines.append(f"- **{lbl}** ({LEVEL_LABEL.get(lvl, lvl)}) {tag}{ev_str}\n")
    else:
        lines.append("_Profile not filled — complete `profile/my-profile.yaml` first._\n")

    if familiar:
        lines.append("\n## Supporting / Familiar Skills\n\n")
        lines.append(", ".join(f"{lbl} {tag}" for lbl, tag in familiar) + "\n")

    if missing:
        lines.append("\n## Gaps (not in profile)\n\n")
        lines.append(", ".join(f"{lbl} {tag}" for lbl, tag in missing) + "\n")
        lines.append("\n_Close gaps with `python tools/pathfinder.py --role "
                     + role_id + "`_\n")

    lines += [
        "\n## Target Titles\n\n",
        "".join(f"- {t}\n" for t in role.get("title_synonyms", [])[:5]),
        "\n## Target Companies\n\n",
        ", ".join(role.get("target_companies", [])) + "\n",
        "\n## Geographies\n\n",
        ", ".join(role.get("geographies", [])) + "\n",
        "\n## Experience Bullets\n\n",
        "_Add STAR-format bullets here. Use `interview/prep.md` as input._\n",
    ]
    return "".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate cluster-specific resume sections")
    parser.add_argument("--cluster",       help="Specific role cluster ID")
    parser.add_argument("--list-clusters", action="store_true", help="List all cluster IDs")
    parser.add_argument("--profile",       default=str(PROFILE))
    args = parser.parse_args()

    roles_graph  = load_yaml(ROLES_GRAPH)
    skills_graph = load_yaml(SKILLS_GRAPH)
    roles        = roles_graph.get("roles", {})

    if args.list_clusters:
        print("\nAvailable clusters:")
        for rid, r in roles.items():
            print(f"  {rid:<40} {r.get('label', '')}")
        return

    profile_path   = Path(args.profile)
    profile_skills = load_yaml(profile_path).get("skills", {}) if profile_path.exists() else {}
    if not profile_path.exists():
        print(f"WARNING: {profile_path} not found — generating stubs with empty skills")

    if args.cluster:
        if args.cluster not in roles:
            print(f"Cluster '{args.cluster}' not found. Use --list-clusters.")
            sys.exit(1)
        targets = {args.cluster: roles[args.cluster]}
    else:
        targets = roles

    RESUME_DIR.mkdir(exist_ok=True)
    for role_id, role in targets.items():
        content  = build_resume(role_id, role, profile_skills, skills_graph)
        out_path = RESUME_DIR / f"cluster-{role_id}.md"
        out_path.write_text(content)
        print(f"  {out_path.relative_to(REPO_ROOT)}")

    print(f"\nGenerated {len(targets)} file(s) in resume/")


if __name__ == "__main__":
    main()
