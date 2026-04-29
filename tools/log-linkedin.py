#!/usr/bin/env python3
"""
tools/log-linkedin.py — Append a weekly LinkedIn analytics snapshot.

Usage:
    python tools/log-linkedin.py --ssi 72 --views 45 --inmails 3 --searches 120
    python tools/log-linkedin.py --ssi 72 --views 45 --inmails 3 --searches 120 --notes "after headline change"

Creates linkedin/analytics-log.md if it doesn't exist, then appends one row.
Run weekly after checking:
  SSI        → linkedin.com/sales/ssi
  Views      → LinkedIn Analytics → Profile views (7 days)
  InMails    → LinkedIn Notifications → filter InMail (30 days)
  Searches   → LinkedIn Analytics → Search appearances (7 days)
"""

import argparse
from pathlib import Path
from datetime import date

REPO_ROOT = Path(__file__).parent.parent
LOG_FILE  = REPO_ROOT / "linkedin" / "analytics-log.md"

HEADER = """\
# LinkedIn Analytics Log

Weekly snapshots. Run: `python tools/log-linkedin.py --ssi N --views N --inmails N --searches N`
Use `python tools/ssi-dashboard.py` to visualise trends.

| Date | SSI | Profile Views (7d) | InMails (30d) | Search Appearances (7d) | Notes |
|------|-----|--------------------|---------------|------------------------|-------|
"""


def ensure_log(path: Path) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(HEADER)


def append_row(path: Path, ssi: float, views: int, inmails: int,
               searches: int, notes: str) -> None:
    row = f"| {date.today()} | {ssi} | {views} | {inmails} | {searches} | {notes} |\n"
    with open(path, "a") as f:
        f.write(row)


def main():
    parser = argparse.ArgumentParser(description="Log weekly LinkedIn analytics snapshot")
    parser.add_argument("--ssi",      type=float, required=True, help="SSI score (0–100)")
    parser.add_argument("--views",    type=int,   required=True, help="Profile views last 7 days")
    parser.add_argument("--inmails",  type=int,   required=True, help="Recruiter InMails last 30 days")
    parser.add_argument("--searches", type=int,   required=True, help="Search appearances last 7 days")
    parser.add_argument("--notes",    default="",               help="Optional notes (e.g. 'after headline change')")
    args = parser.parse_args()

    ensure_log(LOG_FILE)
    append_row(LOG_FILE, args.ssi, args.views, args.inmails, args.searches, args.notes)
    print(f"Logged: SSI={args.ssi}  views={args.views}  inmails={args.inmails}  searches={args.searches}")
    print(f"File  : {LOG_FILE.relative_to(REPO_ROOT)}")
    print(f"Tip   : python tools/ssi-dashboard.py  to visualise trends")


if __name__ == "__main__":
    main()
