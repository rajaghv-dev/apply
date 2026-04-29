#!/usr/bin/env python3
"""
tools/narrator.py — Claude API narrator for high-match job roles.

Reads a match output file from matcher.py and calls Claude API to generate:
  - Gap narrative   (honest gap assessment + fastest close path)
  - Why-me bullets  (role-specific strengths)
  - Recruiter message (cold outreach draft)

The system prompt is prompt-cached — subsequent calls on the same session
reuse the cached tokens (Haiku cost: ~$0.001 per role at 40% cache hit rate).

Usage:
    python tools/narrator.py                         # reads latest match file
    python tools/narrator.py --jd path/to/jd.txt    # runs matcher first, then narrates
    python tools/narrator.py --match-file path/to/match.md
    python tools/narrator.py --threshold 50          # only narrate ≥50% matches

Requires:
    pip install anthropic pyyaml
    export ANTHROPIC_API_KEY=your-key
"""

import os
import sys
import re
import yaml
import argparse
import subprocess
from pathlib import Path
from datetime import date

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic not installed. Run: pip install anthropic")
    sys.exit(1)

REPO_ROOT   = Path(__file__).parent.parent
PROFILE     = REPO_ROOT / "profile" / "my-profile.yaml"
JOBS_DIR    = REPO_ROOT / "gap-analysis" / "jobs"

MODEL = "claude-haiku-4-5-20251001"

# Cached system prompt — describes the assistant's role and output format.
# Marked ephemeral so Anthropic caches it for 5 minutes across calls.
SYSTEM_PROMPT = """\
You are a career intelligence assistant for a senior engineer with a rare multi-domain
background spanning chip design, embedded systems, AI/ML, legal tech, and fintech.
Your job is to generate concise, high-signal career narrative for specific job applications.

You receive:
  1. A JD match analysis table (skills scored STRONG / PARTIAL / GAP, with section weights)
  2. The applicant's current skill profile

Generate exactly three sections, each preceded by its exact header line:

## GAP NARRATIVE
2–3 sentences. What are the real gaps for this role, and what is the fastest credible path
to close them? Be honest — recruiters probe gaps in interviews. Flag [REQUIRED] gaps first.

## WHY ME
3–5 bullet points starting with "•". Concrete strengths relevant to THIS role.
Reference actual skills from the STRONG list. End with the cross-domain bridge
that makes this candidate rare (hardware×AI, AI×legal, etc.).

## RECRUITER MESSAGE
5–7 lines. Cold LinkedIn message or email to the recruiter or hiring manager.
First person, professional, specific to the role. End with a clear ask.
No sycophantic openers ("Hope this finds you well" etc.)."""


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def find_latest_match_file() -> Path | None:
    if not JOBS_DIR.exists():
        return None
    candidates = sorted(
        JOBS_DIR.glob("match-*pct-latest.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def parse_match_pct(path: Path) -> float:
    m = re.search(r"match-(\d+(?:\.\d+)?)pct", path.stem)
    return float(m.group(1)) if m else 0.0


def build_profile_summary(profile_path: Path) -> str:
    data   = load_yaml(profile_path)
    skills = data.get("skills") or {}
    lines  = ["Applicant skill summary:"]
    for sid, v in skills.items():
        if v and v.get("level"):
            lines.append(f"  {sid}: {v['level']} (last used {v.get('last_used', '?')})")
    if len(lines) == 1:
        lines.append("  [Profile not yet filled — using match table only]")
    return "\n".join(lines)


def call_claude(match_text: str, match_pct: float, profile_summary: str) -> tuple[str, dict]:
    client = anthropic.Anthropic()

    user_msg = (
        f"Match score: {match_pct}%\n\n"
        f"{match_text}\n\n"
        "---\n\n"
        f"{profile_summary}\n\n"
        "Generate the three sections as specified."
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=900,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_msg}],
    )

    usage = {
        "input_tokens":         response.usage.input_tokens,
        "output_tokens":        response.usage.output_tokens,
        "cache_creation_tokens": getattr(response.usage, "cache_creation_input_tokens", 0),
        "cache_read_tokens":     getattr(response.usage, "cache_read_input_tokens", 0),
    }

    return response.content[0].text, usage


def save_narration(source_file: Path, narration: str, match_pct: float) -> Path:
    today    = date.today()
    out_path = source_file.parent / f"narration-{match_pct:.0f}pct-{today}.md"
    out_path.write_text(
        f"# Role Narration — {match_pct:.0f}% match — {today}\n\n"
        f"Source: {source_file.name}\n\n"
        f"---\n\n{narration}\n"
    )
    return out_path


def print_usage(usage: dict):
    total_in  = usage["input_tokens"]
    cache_r   = usage["cache_read_tokens"]
    cache_w   = usage["cache_creation_tokens"]
    out_tok   = usage["output_tokens"]
    # Haiku pricing (approx): $0.80/1M input, $4.00/1M output, $0.08/1M cache-read
    cost = (
        (total_in - cache_r - cache_w) * 0.80 / 1_000_000
        + cache_r * 0.08 / 1_000_000
        + cache_w * 0.80 / 1_000_000
        + out_tok * 4.00 / 1_000_000
    )
    print(f"  Tokens: {total_in} in / {out_tok} out  |  cache read {cache_r} / created {cache_w}  |  ~${cost:.4f}")


def main():
    parser = argparse.ArgumentParser(
        description="Claude API narrator for high-match job roles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/narrator.py                          # latest match file, default threshold 40%
  python tools/narrator.py --jd gap-analysis/jobs/jd.txt
  python tools/narrator.py --match-file gap-analysis/jobs/match-72pct-latest.md
  python tools/narrator.py --threshold 60           # only roles worth applying to
        """,
    )
    parser.add_argument("--jd",         help="Run matcher on this JD file first, then narrate")
    parser.add_argument("--match-file", help="Path to a specific match .md file")
    parser.add_argument("--profile",    default=str(PROFILE), help="Profile YAML path")
    parser.add_argument("--threshold",  type=float, default=40.0,
                        help="Min match%% to narrate (default 40). Use 60 for apply-tier only.")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set.")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    # Optionally run matcher first
    if args.jd:
        print(f"Running matcher on {args.jd} ...")
        subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "matcher.py"),
             "--jd", args.jd, "--profile", args.profile],
            check=False,
        )

    # Resolve match file
    if args.match_file:
        match_file = Path(args.match_file)
    else:
        match_file = find_latest_match_file()

    if not match_file or not match_file.exists():
        print("No match file found. Run 'python tools/matcher.py --jd <file>' first.")
        sys.exit(1)

    match_pct  = parse_match_pct(match_file)
    match_text = match_file.read_text()

    print(f"Match file : {match_file.name}")
    print(f"Match score: {match_pct}%")

    if match_pct < args.threshold:
        print(f"Below threshold {args.threshold}% — skipping narration.")
        print(f"Use --threshold {int(match_pct)} or lower to force narration.")
        sys.exit(0)

    profile_summary = build_profile_summary(Path(args.profile))
    print(f"Calling {MODEL} ...")

    narration, usage = call_claude(match_text, match_pct, profile_summary)

    print("\n" + "─" * 60)
    print(narration)
    print("─" * 60)
    print_usage(usage)

    out_path = save_narration(match_file, narration, match_pct)
    print(f"Saved → {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
