#!/usr/bin/env python3
"""
tools/market-scan.py — Batch skill frequency analysis across multiple JDs.

Scans a directory of JD text files, counts how many mention each skill,
and writes a ranked frequency table to profile/market-scan.md.

Usage:
    # 1. Save JD text files to gap-analysis/jobs/jds/
    mkdir -p gap-analysis/jobs/jds
    # Paste each JD as jd1.txt, jd2.txt, etc.

    # 2. Run the scan
    python tools/market-scan.py
    python tools/market-scan.py --jd-dir gap-analysis/jobs/jds --top 25

Output: profile/market-scan.md — ranked skill frequency table
"""

import re
import yaml
import argparse
from pathlib import Path
from datetime import date
from collections import defaultdict

REPO_ROOT    = Path(__file__).parent.parent
SKILLS_GRAPH = REPO_ROOT / "ontology" / "skills-graph.yaml"
DEFAULT_DIR  = REPO_ROOT / "gap-analysis" / "jobs" / "jds"
OUTPUT_FILE  = REPO_ROOT / "profile" / "market-scan.md"


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def extract_skills(jd_text: str, skills_graph: dict) -> set[str]:
    jd_lower = jd_text.lower()
    found: set[str] = set()
    for skill_id, skill in skills_graph["skills"].items():
        synonyms = [skill["label"].lower()] + [s.lower() for s in skill.get("synonyms", [])]
        for syn in synonyms:
            if re.search(r"\b" + re.escape(syn) + r"\b", jd_lower):
                found.add(skill_id)
                break
    return found


def scan_directory(jd_dir: Path, skills_graph: dict) -> tuple[dict[str, int], int]:
    files = sorted(list(jd_dir.glob("*.txt")) + list(jd_dir.glob("*.md")))
    freq: dict[str, int] = defaultdict(int)
    for f in files:
        found = extract_skills(f.read_text(), skills_graph)
        for sid in found:
            freq[sid] += 1
        print(f"  {f.name}: {len(found)} skills")
    return dict(freq), len(files)


def write_output(freq: dict[str, int], skills_graph: dict, jd_count: int, top: int) -> None:
    all_skills    = skills_graph["skills"]
    sorted_skills = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top]

    lines = [
        f"# Market Scan — {date.today()}\n\n",
        f"Analyzed **{jd_count} JDs**. "
        f"Frequency = number of JDs that mention each skill.\n\n---\n\n",
        "## Skill Frequency\n\n",
        "| Rank | Skill | Domain | JDs | % |\n",
        "|------|-------|--------|-----|---|\n",
    ]
    for rank, (sid, count) in enumerate(sorted_skills, 1):
        skill  = all_skills.get(sid, {})
        label  = skill.get("label", sid)
        domain = skill.get("domain", "")
        pct    = round(count / jd_count * 100) if jd_count else 0
        lines.append(f"| {rank} | {label} | {domain} | {count} | {pct}% |\n")

    lines += [
        "\n---\n\n## Interpretation\n\n",
        "- **>50% of JDs** → must-have; ensure PROFICIENT or higher in profile\n",
        "- **20–50%** → differentiator; mention explicitly in resume/LinkedIn\n",
        "- **<20%** → niche; only relevant for specialist roles\n",
        "\n---\n\n## Salary Benchmarks\n\n",
        "_Run `python tools/salary-pull.py --builtin --save` to populate this section._\n",
    ]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Batch skill frequency analysis across JDs")
    parser.add_argument("--jd-dir", default=str(DEFAULT_DIR))
    parser.add_argument("--top",    type=int, default=30, help="Top N skills to include")
    args = parser.parse_args()

    jd_dir = Path(args.jd_dir)
    if not jd_dir.exists():
        print(f"JD directory not found: {jd_dir}")
        print(f"Create it and add .txt JD files:")
        print(f"  mkdir -p {jd_dir.relative_to(REPO_ROOT)}")
        return

    skills_graph = load_yaml(SKILLS_GRAPH)
    print(f"Scanning {jd_dir.relative_to(REPO_ROOT)} ...")
    freq, jd_count = scan_directory(jd_dir, skills_graph)

    if not freq:
        print("No skills matched. Check that .txt files contain recognisable skill keywords.")
        return

    write_output(freq, skills_graph, jd_count, args.top)
    top5 = [all_skills.get("label", sid) for sid, _ in
            sorted(freq.items(), key=lambda x: -x[1])[:5]
            for all_skills in [skills_graph["skills"].get(sid, {})]]
    print(f"\nWrote → {OUTPUT_FILE.relative_to(REPO_ROOT)}")
    print(f"Top 5 : {[skills_graph['skills'].get(sid, {}).get('label', sid) for sid, _ in sorted(freq.items(), key=lambda x: -x[1])[:5]]}")


if __name__ == "__main__":
    main()
