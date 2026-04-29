#!/usr/bin/env python3
"""
tools/ssi-dashboard.py — LinkedIn analytics trend dashboard (matplotlib).

Reads linkedin/analytics-log.md → renders a 2×2 chart:
  SSI score · Profile views · Recruiter InMails · Search appearances

Usage:
    python tools/ssi-dashboard.py             # render + save PNG
    python tools/ssi-dashboard.py --no-show   # save PNG only (no window)

Output: linkedin/ssi-dashboard.png

Requires:
    pip install matplotlib
"""

import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

REPO_ROOT  = Path(__file__).parent.parent
LOG_FILE   = REPO_ROOT / "linkedin" / "analytics-log.md"
OUTPUT_PNG = REPO_ROOT / "linkedin" / "ssi-dashboard.png"

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
except ImportError:
    print("ERROR: matplotlib not installed. Run: pip install matplotlib")
    sys.exit(1)


def parse_log(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        if not line.startswith("| 20"):
            continue
        parts = [p.strip() for p in line.strip("| \n").split("|")]
        if len(parts) < 5:
            continue
        try:
            rows.append({
                "date":     datetime.strptime(parts[0], "%Y-%m-%d"),
                "ssi":      float(parts[1]),
                "views":    int(parts[2]),
                "inmails":  int(parts[3]),
                "searches": int(parts[4]),
                "notes":    parts[5] if len(parts) > 5 else "",
            })
        except (ValueError, IndexError):
            continue
    return sorted(rows, key=lambda r: r["date"])


def render(rows: list[dict], show: bool = True) -> None:
    dates    = [r["date"]    for r in rows]
    ssi      = [r["ssi"]     for r in rows]
    views    = [r["views"]   for r in rows]
    inmails  = [r["inmails"] for r in rows]
    searches = [r["searches"]for r in rows]

    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle("LinkedIn Analytics", fontsize=14, fontweight="bold")

    fmt = mdates.DateFormatter("%b %d")
    specs = [
        (axes[0, 0], ssi,      "SSI Score (0–100)",         "#2563eb", (0, 100)),
        (axes[0, 1], views,    "Profile Views (7 d)",       "#16a34a", None),
        (axes[1, 0], inmails,  "Recruiter InMails (30 d)",  "#dc2626", None),
        (axes[1, 1], searches, "Search Appearances (7 d)",  "#9333ea", None),
    ]
    for ax, data, title, color, ylim in specs:
        ax.plot(dates, data, marker="o", color=color, linewidth=2, markersize=5)
        ax.fill_between(dates, data, alpha=0.08, color=color)
        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.xaxis.set_major_formatter(fmt)
        ax.tick_params(axis="x", rotation=40)
        ax.grid(True, alpha=0.3)
        if ylim:
            ax.set_ylim(ylim)
        if len(rows) >= 2:
            delta = data[-1] - data[-2]
            sign  = "+" if delta >= 0 else ""
            ax.set_xlabel(
                f"Latest: {data[-1]}   ({sign}{delta:.0f} vs prev week)",
                fontsize=8.5,
            )

    plt.tight_layout()
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PNG, dpi=150, bbox_inches="tight")
    try:
        label = OUTPUT_PNG.relative_to(REPO_ROOT)
    except ValueError:
        label = OUTPUT_PNG
    print(f"Saved → {label}")

    if show:
        try:
            matplotlib.use("TkAgg")
            plt.show()
        except Exception:
            print("(Could not open display window — PNG saved above)")


def main():
    parser = argparse.ArgumentParser(description="LinkedIn analytics trend dashboard")
    parser.add_argument("--no-show", action="store_true", help="Save PNG only, no window")
    args = parser.parse_args()

    rows = parse_log(LOG_FILE)
    if not rows:
        print(f"No data in {LOG_FILE.relative_to(REPO_ROOT) if LOG_FILE.exists() else LOG_FILE}")
        print("Add entries first:")
        print("  python tools/log-linkedin.py --ssi 72 --views 45 --inmails 3 --searches 120")
        return

    print(f"Loaded {len(rows)} data points")
    render(rows, show=not args.no_show)


if __name__ == "__main__":
    main()
