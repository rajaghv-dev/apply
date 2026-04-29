#!/usr/bin/env python3
"""
tools/offer-compare.py — Compare job offers by total compensation.

Usage (CLI):
    python tools/offer-compare.py \
      --offer "Google Zurich,CHF,180000,50000,20,Zurich" \
      --offer "ARM Cambridge,GBP,120000,20000,15,Cambridge"

Usage (interactive):
    python tools/offer-compare.py

Format per --offer: "company,currency,base,equity_annual,bonus_pct,city"

Output:
    Ranked table — nominal total and purchasing-power-adjusted USD equivalent.
    Saved to job-tracker/offers.md
"""

import argparse
import sys
from pathlib import Path
from datetime import date

REPO_ROOT   = Path(__file__).parent.parent
OUTPUT_FILE = REPO_ROOT / "job-tracker" / "offers.md"

# Approximate FX to USD (2025 mid-market rates)
FX: dict[str, float] = {
    "USD": 1.00, "CHF": 1.10, "GBP": 1.27,
    "EUR": 1.08, "INR": 0.012, "SGD": 0.74, "AED": 0.27,
}

# Cost-of-living index relative to NYC = 100 (higher = more expensive = less purchasing power)
COL: dict[str, int] = {
    "Zurich": 130, "Geneva": 128, "London": 110, "Cambridge": 100,
    "Berlin": 85, "Amsterdam": 95, "Munich": 90, "Frankfurt": 92,
    "Bangalore": 35, "Hyderabad": 32, "Pune": 30, "Mumbai": 45,
    "Singapore": 110, "Dubai": 85, "Abu Dhabi": 80,
    "New York": 100, "San Francisco": 120, "Seattle": 105, "Austin": 88,
    "Remote": 80,
}


def parse_offer_str(s: str) -> dict:
    parts = [p.strip() for p in s.split(",")]
    if len(parts) != 6:
        raise ValueError(
            f"Expected 'company,currency,base,equity_annual,bonus_pct,city'\n  Got: {s!r}"
        )
    return {
        "company":   parts[0],
        "currency":  parts[1].upper(),
        "base":      float(parts[2]),
        "equity":    float(parts[3]),
        "bonus_pct": float(parts[4]),
        "city":      parts[5],
    }


def prompt_offers() -> list[dict]:
    print("Enter offers interactively. Press Enter with empty company name to finish.\n")
    offers = []
    while True:
        company = input("Company name (blank to finish): ").strip()
        if not company:
            break
        currency  = input("  Currency (USD/CHF/GBP/EUR/INR): ").strip().upper()
        base      = float(input("  Base salary (annual): ").strip())
        equity    = float(input("  Annual equity value (0 if none): ").strip())
        bonus_pct = float(input("  Bonus % of base (0 if none): ").strip())
        city      = input("  City: ").strip()
        offers.append(dict(company=company, currency=currency, base=base,
                           equity=equity, bonus_pct=bonus_pct, city=city))
        print()
    return offers


def enrich(offer: dict) -> dict:
    base     = offer["base"]
    equity   = offer["equity"]
    bonus    = base * offer["bonus_pct"] / 100
    total    = base + equity + bonus
    fx       = FX.get(offer["currency"], 1.0)
    col      = COL.get(offer["city"], 100)
    adj_usd  = total * fx * (100 / col)
    return {**offer, "bonus": bonus, "total": total, "adj_usd": adj_usd}


def print_table(rows: list[dict]) -> None:
    sep = "─" * 72
    print(f"\n{sep}")
    print("  OFFER COMPARISON  (sorted by nominal total)")
    print(f"{sep}")
    print(f"  {'Company':<24} {'City':<14} {'Curr':<5} {'Base':>11} {'Total':>12} {'CoL-adj $':>11}")
    print(f"  {'-'*24} {'-'*14} {'-'*5} {'-'*11} {'-'*12} {'-'*11}")
    for r in rows:
        print(f"  {r['company']:<24} {r['city']:<14} {r['currency']:<5} "
              f"{r['base']:>11,.0f} {r['total']:>12,.0f} {r['adj_usd']:>11,.0f}")

    best_nominal = rows[0]
    best_adj     = max(rows, key=lambda x: x["adj_usd"])
    print(f"\n  Best nominal total : {best_nominal['company']} ({best_nominal['currency']} {best_nominal['total']:,.0f})")
    print(f"  Best CoL-adjusted  : {best_adj['company']} (~USD {best_adj['adj_usd']:,.0f} equivalent)\n")


def save_output(rows: list[dict]) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Offer Comparison — {date.today()}\n\n",
        "| Company | City | Currency | Base | Equity | Bonus | Total | CoL-adj USD |\n",
        "|---------|------|----------|------|--------|-------|-------|-------------|\n",
    ]
    for r in rows:
        lines.append(
            f"| {r['company']} | {r['city']} | {r['currency']} "
            f"| {r['base']:,.0f} | {r['equity']:,.0f} | {r['bonus']:,.0f} "
            f"| {r['total']:,.0f} | {r['adj_usd']:,.0f} |\n"
        )
    OUTPUT_FILE.write_text("".join(lines))
    print(f"Saved → {OUTPUT_FILE.relative_to(REPO_ROOT)}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare job offers by total compensation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Example:\n  python tools/offer-compare.py --offer "Google Zurich,CHF,180000,50000,20,Zurich"',
    )
    parser.add_argument("--offer",   action="append", dest="offers", metavar="STR",
                        help="'company,currency,base,equity,bonus_pct,city'  (repeat per offer)")
    parser.add_argument("--no-save", action="store_true", help="Don't write job-tracker/offers.md")
    args = parser.parse_args()

    raw = [parse_offer_str(s) for s in args.offers] if args.offers else prompt_offers()
    if not raw:
        print("No offers entered.")
        sys.exit(0)

    rows = sorted([enrich(o) for o in raw], key=lambda x: x["total"], reverse=True)
    print_table(rows)
    if not args.no_save:
        save_output(rows)


if __name__ == "__main__":
    main()
