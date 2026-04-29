#!/usr/bin/env python3
"""
tools/salary-pull.py — Salary benchmarks for target roles by geography.

Two modes:
  --builtin   Show curated 2025 benchmark table (offline, no scraping)
  --scrape    Open LinkedIn Salary in a visible browser (requires manual login)

Usage:
    python tools/salary-pull.py --builtin           # print table
    python tools/salary-pull.py --builtin --save    # append to profile/market-scan.md
    python tools/salary-pull.py --scrape --role "ML Engineer" --location Zurich

Data source: Levels.fyi, Glassdoor, LinkedIn Salary (2025 estimates).
Update BENCHMARKS when you have fresh data points.
"""

import sys
import argparse
from pathlib import Path
from datetime import date

REPO_ROOT   = Path(__file__).parent.parent
OUTPUT_FILE = REPO_ROOT / "profile" / "market-scan.md"

# {role: {geography: (base_min, base_max, currency, note)}}
BENCHMARKS: dict[str, dict[str, tuple]] = {
    "Silicon / ASIC Engineer (Staff/Principal)": {
        "USA":         (180_000, 280_000, "USD", "FAANG; equity on top"),
        "Switzerland": (140_000, 200_000, "CHF", "Zurich/Geneva — Qualcomm, Google"),
        "UK":          (90_000,  140_000, "GBP", "Cambridge/London — ARM, Intel"),
        "Germany":     (85_000,  130_000, "EUR", "Munich/Berlin"),
        "India":       (35_00_000, 70_00_000, "INR", "Bangalore — Qualcomm, Samsung"),
    },
    "AI Hardware / ML Accelerator Engineer": {
        "USA":         (190_000, 300_000, "USD", "NVIDIA, Google, Apple — top of market"),
        "Switzerland": (150_000, 220_000, "CHF", "Google Zurich, Cerebras"),
        "UK":          (95_000,  150_000, "GBP", "Graphcore, ARM, DeepMind"),
        "India":       (40_00_000, 80_00_000, "INR", "NVIDIA, AMD Hyderabad"),
    },
    "ML / AI Engineer (Staff/Principal)": {
        "USA":         (175_000, 300_000, "USD", "FAANG + hot AI startups"),
        "Switzerland": (140_000, 210_000, "CHF", "Google, Amazon, local AI cos"),
        "UK":          (90_000,  150_000, "GBP", "DeepMind, Waymo, Goldman AI"),
        "Germany":     (80_000,  120_000, "EUR", "Aleph Alpha, Bosch AI"),
        "Netherlands": (75_000,  110_000, "EUR", "Booking.com, ASML AI"),
        "India":       (30_00_000, 65_00_000, "INR", "Google, Microsoft, Flipkart"),
    },
    "Embedded / Firmware Engineer (Senior/Staff)": {
        "Switzerland": (110_000, 160_000, "CHF", "ABB, Bosch, Sensirion, u-blox"),
        "UK":          (75_000,  110_000, "GBP", "ARM, Imagination, Rolls Royce"),
        "Germany":     (70_000,  105_000, "EUR", "Siemens, Bosch, Infineon"),
        "India":       (20_00_000, 45_00_000, "INR", "TI, Qualcomm, NXP"),
    },
    "Legal AI / LegalTech Engineer": {
        "USA":         (150_000, 220_000, "USD", "Harvey AI, Casetext, Thomson Reuters"),
        "UK":          (80_000,  130_000, "GBP", "Allen & Overy, Luminance, RAVN"),
        "Switzerland": (120_000, 170_000, "CHF", "Axiom, LexisNexis"),
        "Germany":     (70_000,  100_000, "EUR", "Wolters Kluwer, LexisNexis"),
    },
    "FinTech / Finance AI Engineer": {
        "UK":          (90_000,  160_000, "GBP", "Jane Street, Man Group, Revolut"),
        "Switzerland": (130_000, 200_000, "CHF", "UBS, Julius Baer, Six Group"),
        "Germany":     (75_000,  115_000, "EUR", "Deutsche Bank, N26, Trade Republic"),
        "India":       (25_00_000, 55_00_000, "INR", "Goldman Sachs, Morgan Stanley"),
    },
}


def print_benchmarks() -> None:
    sep = "─" * 80
    print(f"\n{sep}")
    print("  SALARY BENCHMARKS (2025 estimates — base only; equity/bonus additional)")
    print("  Source: Levels.fyi · Glassdoor · LinkedIn Salary")
    print(f"{sep}\n")
    for role, geos in BENCHMARKS.items():
        print(f"  {role}")
        for geo, (lo, hi, curr, note) in geos.items():
            print(f"    {geo:<14} {curr} {lo:>14,} – {hi:>14,}   {note}")
        print()


def salary_section() -> str:
    lines = [
        f"\n## Salary Benchmarks\n\n",
        f"_Source: Levels.fyi, Glassdoor, LinkedIn Salary. "
        f"Base only. Last updated: {date.today()}._\n\n",
    ]
    for role, geos in BENCHMARKS.items():
        lines.append(f"\n### {role}\n\n")
        lines.append("| Geography | Min | Max | Currency | Notes |\n")
        lines.append("|-----------|-----|-----|----------|-------|\n")
        for geo, (lo, hi, curr, note) in geos.items():
            lines.append(f"| {geo} | {lo:,} | {hi:,} | {curr} | {note} |\n")
    return "".join(lines)


def append_to_market_scan(section: str) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT_FILE.exists():
        text = OUTPUT_FILE.read_text()
        marker = "## Salary Benchmarks"
        if marker in text:
            text = text[: text.index(marker)] + section.lstrip("\n")
        else:
            text += section
        OUTPUT_FILE.write_text(text)
    else:
        header = f"# Market Scan — {date.today()}\n\n_Run `tools/market-scan.py` to populate skill frequency._\n"
        OUTPUT_FILE.write_text(header + section)
    print(f"Saved → {OUTPUT_FILE.relative_to(REPO_ROOT)}")


def scrape_linkedin(role: str, location: str) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    url = (f"https://www.linkedin.com/salary/search"
           f"?keywords={role.replace(' ', '+')}&location={location.replace(' ', '+')}")
    print(f"Opening LinkedIn Salary: {url}")
    print("NOTE: You must be logged in. Browser opens visibly so you can interact.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page    = browser.new_page()
        page.goto(url, timeout=20000)
        page.wait_for_timeout(6000)
        try:
            print("\nPage title:", page.title())
            print("First 300 chars:\n", page.inner_text("body")[:300])
        except Exception as e:
            print(f"Could not extract data: {e}")
        input("\nPress Enter to close browser...")
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Salary benchmarks for target roles")
    parser.add_argument("--builtin", action="store_true", help="Show curated offline benchmarks")
    parser.add_argument("--save",    action="store_true", help="Append to profile/market-scan.md")
    parser.add_argument("--scrape",  action="store_true", help="Open LinkedIn Salary in browser")
    parser.add_argument("--role",    default="ML Engineer")
    parser.add_argument("--location",default="London")
    args = parser.parse_args()

    if args.scrape:
        scrape_linkedin(args.role, args.location)
        return

    print_benchmarks()
    if args.save:
        append_to_market_scan(salary_section())


if __name__ == "__main__":
    main()
