#!/usr/bin/env python3
"""
tools/pathfinder.py — Shortest learning path using NetworkX graph traversal.

Given a target role or list of gap skills, finds the optimal order to
learn missing skills by traversing the implies graph in skills-graph.yaml.

Insight: if RTL implies FPGA (0.55), then knowing RTL is a stepping-stone
to FPGA. Dijkstra over the implies graph reveals which skills to learn first
so each one builds on what you already know.

Usage:
    python tools/pathfinder.py --role silicon_engineer
    python tools/pathfinder.py --role ai_engineer
    python tools/pathfinder.py --skill rag timing_analysis
    python tools/pathfinder.py --list-roles

Output:
    Ordered learning plan (build on existing skills first, from-scratch last)
    Path: RTL Design → FPGA Design  (1-hop, cost 0.45)

Requires:
    pip install networkx pyyaml
"""

import sys
import yaml
import argparse
from pathlib import Path
from typing import Optional

try:
    import networkx as nx
except ImportError:
    print("ERROR: networkx not installed. Run: pip install networkx")
    sys.exit(1)

REPO_ROOT    = Path(__file__).parent.parent
SKILLS_GRAPH = REPO_ROOT / "ontology" / "skills-graph.yaml"
ROLES_GRAPH  = REPO_ROOT / "ontology" / "roles-graph.yaml"
PROFILE      = REPO_ROOT / "profile" / "my-profile.yaml"

LEVEL_SCORE = {"EXPERT": 3, "PROFICIENT": 2, "FAMILIAR": 1, "": 0, None: 0}


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def build_skill_graph(skills_graph: dict) -> nx.DiGraph:
    """
    Build a directed weighted graph from implies edges.
    Edge A→B with weight w: knowing A transfers w of score to B.
    Dijkstra cost = 1 − weight so high-transfer edges are cheap hops.
    """
    G = nx.DiGraph()
    for skill_id, skill in skills_graph["skills"].items():
        G.add_node(skill_id, label=skill.get("label", skill_id), domain=skill.get("domain", ""))
        implies = skill.get("implies", {})
        if isinstance(implies, dict):
            for target, weight in implies.items():
                w = float(weight)
                G.add_edge(skill_id, target, weight=w, cost=round(1.0 - w, 3))
        elif isinstance(implies, list):
            for item in implies:
                if isinstance(item, dict):
                    for target, weight in item.items():
                        w = float(weight)
                        G.add_edge(skill_id, target, weight=w, cost=round(1.0 - w, 3))
                elif isinstance(item, str):
                    G.add_edge(skill_id, item, weight=0.5, cost=0.5)
    return G


def get_known_skills(profile_path: Path) -> set[str]:
    """Return skill IDs where the profile has any level set."""
    if not profile_path.exists():
        return set()
    data = load_yaml(profile_path)
    return {
        sid for sid, v in (data.get("skills") or {}).items()
        if v and LEVEL_SCORE.get(v.get("level", ""), 0) > 0
    }


def shortest_path_to(
    G: nx.DiGraph,
    sources: set[str],
    target: str,
) -> tuple[Optional[list[str]], float]:
    """
    Find the lowest-cost path from any source to target.
    Returns (path_list, cost) or (None, inf).
    """
    if target in sources:
        return ([target], 0.0)

    best_path: Optional[list[str]] = None
    best_cost = float("inf")

    for src in sources:
        if not G.has_node(src) or not G.has_node(target):
            continue
        try:
            path = nx.dijkstra_path(G, src, target, weight="cost")
            cost = nx.dijkstra_path_length(G, src, target, weight="cost")
            if cost < best_cost:
                best_cost = cost
                best_path = path
        except nx.NetworkXNoPath:
            continue

    return best_path, best_cost


def build_learning_plan(
    gap_skill_ids: list[str],
    known_skills: set[str],
    G: nx.DiGraph,
    skills_graph: dict,
) -> list[dict]:
    all_skills = skills_graph["skills"]
    plan = []

    for skill_id in gap_skill_ids:
        if skill_id not in all_skills:
            continue
        label  = all_skills[skill_id].get("label", skill_id)
        domain = all_skills[skill_id].get("domain", "")
        path, cost = shortest_path_to(G, known_skills, skill_id)

        if path and len(path) > 1:
            path_labels = [all_skills.get(n, {}).get("label", n) for n in path]
            hops = len(path) - 1
        else:
            path_labels = None
            hops        = None
            cost        = float("inf")

        plan.append({
            "skill_id":   skill_id,
            "label":      label,
            "domain":     domain,
            "path_labels": path_labels,
            "hops":       hops,
            "cost":       cost,
        })

    plan.sort(key=lambda x: x["cost"] if x["cost"] != float("inf") else 999)
    return plan


def get_role_gaps(role_id: str, known_skills: set[str], roles_graph: dict) -> tuple[str, list[str]]:
    """Return (role_label, [gap_skill_ids]) for a role ID or partial label."""
    roles = roles_graph.get("roles", {})
    matched_id = None

    if role_id in roles:
        matched_id = role_id
    else:
        for rid, r in roles.items():
            if role_id.lower() in r.get("label", "").lower() or role_id.lower() in rid.lower():
                matched_id = rid
                break

    if not matched_id:
        return ("", [])

    role  = roles[matched_id]
    label = role.get("label", matched_id)
    gaps  = [
        sid for sid in list(role.get("required", {}).keys()) + list(role.get("preferred", {}).keys())
        if sid not in known_skills
    ]
    return label, gaps


def print_plan(plan: list[dict], title: str = ""):
    sep = "─" * 60
    print(f"\n{sep}")
    if title:
        print(f"  LEARNING PATH → {title}")
    else:
        print(f"  LEARNING PATH")
    print(f"{sep}")

    reachable    = [s for s in plan if s["cost"] != float("inf")]
    from_scratch = [s for s in plan if s["cost"] == float("inf")]

    if not plan:
        print("\n  No gaps found — you already meet all requirements!")
        return

    if reachable:
        print(f"\n  BUILD ON EXISTING SKILLS ({len(reachable)}) — recommended learning order:\n")
        for i, s in enumerate(reachable, 1):
            hops_str = f"{s['hops']} hop" if s["hops"] == 1 else f"{s['hops']} hops"
            path_str = " → ".join(s["path_labels"]) if s["path_labels"] else s["label"]
            print(f"  {i:>2}. {s['label']}  [{s['domain']}]")
            print(f"      {path_str}  ({hops_str}, cost {s['cost']:.2f})")

    if from_scratch:
        print(f"\n  START FROM SCRATCH ({len(from_scratch)}) — no bridge from current skills:\n")
        for s in from_scratch:
            print(f"  •  {s['label']}  [{s['domain']}]")

    if reachable:
        print(f"\n  TIP: Start with item 1 — lowest cost, closest to what you know.")
        print(f"  Each item you complete expands your bridge for the next one.")
    print()


def list_roles(roles_graph: dict):
    print("\nAvailable role IDs (use with --role):\n")
    for role_id, role in roles_graph.get("roles", {}).items():
        print(f"  {role_id:<40} {role.get('label', '')}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Shortest learning path from your skills to a target role",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/pathfinder.py --role silicon_engineer
  python tools/pathfinder.py --role ai_engineer
  python tools/pathfinder.py --skill rag timing_analysis
  python tools/pathfinder.py --list-roles
        """,
    )
    parser.add_argument("--role",       help="Role ID or partial label")
    parser.add_argument("--skill",      nargs="+", help="One or more specific skill IDs")
    parser.add_argument("--profile",    default=str(PROFILE), help="Profile YAML path")
    parser.add_argument("--list-roles", action="store_true", help="Print all available role IDs")
    args = parser.parse_args()

    if not SKILLS_GRAPH.exists():
        print(f"ERROR: {SKILLS_GRAPH} not found")
        sys.exit(1)

    skills_graph = load_yaml(SKILLS_GRAPH)
    roles_graph  = load_yaml(ROLES_GRAPH)
    G            = build_skill_graph(skills_graph)

    if args.list_roles:
        list_roles(roles_graph)
        return

    if not args.role and not args.skill:
        parser.print_help()
        sys.exit(0)

    known = get_known_skills(Path(args.profile))

    if known:
        print(f"  Profile: {len(known)} skills — {', '.join(sorted(known)[:6])}{'...' if len(known) > 6 else ''}")
    else:
        print("  WARNING: Profile empty or not found — all skills will show as 'from scratch'")
        print(f"  Fill {PROFILE} to see personalized paths.")

    if args.role:
        role_label, gap_skills = get_role_gaps(args.role, known, roles_graph)
        if not gap_skills:
            if not role_label:
                print(f"\nRole '{args.role}' not found. Try --list-roles.")
            else:
                print(f"\nNo gaps for '{role_label}' — you already meet all requirements.")
            sys.exit(0)
        plan = build_learning_plan(gap_skills, known, G, skills_graph)
        print_plan(plan, role_label)

    elif args.skill:
        valid = [s for s in args.skill if s in skills_graph["skills"]]
        invalid = [s for s in args.skill if s not in skills_graph["skills"]]
        if invalid:
            print(f"  Unknown skill IDs: {invalid}")
        if valid:
            plan = build_learning_plan(valid, known, G, skills_graph)
            print_plan(plan)


if __name__ == "__main__":
    main()
